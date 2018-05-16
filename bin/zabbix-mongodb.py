#!/usr/bin/env python

# Date: 03/01/2017
# Author: Long Chen
# Description: A script to get MongoDB metrics
# Requires: MongoClient in python

import pymongo
from pymongo import MongoClient
from calendar import timegm
from time import gmtime
import socket
import json

class MongoDB(object):
    def __init__(self):
        self.mongo_host = "127.0.0.1"
        self.mongo_port = 27017
        self.mongo_db = ["admin", ]
        self.mongo_user = ""
        self.mongo_password = ""
        self.__conn = None
        self.__dbnames = None
        self.__metrics = []

    # Connect to MongoDB
    def connect(self):
        if self.__conn is None:
            try:
                self.__conn = MongoClient(host=self.mongo_host, port=self.mongo_port)
            except Exception as e:
                print 'Error in MongoDB connection: %s' % str(e)

    # Add each mectrics to the metrics list
    def addMetrics(self, k, v):
        dict = {}
        dict['key'] = k
        dict['value'] = v
        self.__metrics.append(dict)

    # Print out all metrics
    def printMetrics(self):
        metrics = self.__metrics
        for m in metrics:
            zabbix_item_key = str(m['key'])
            zabbix_item_value = str(m['value']).replace("\'","\"")
            print '- ' + zabbix_item_key + ' ' + zabbix_item_value.replace(" ", "")

    # Get a list of DB names
    def getDBNames(self):
        if self.__conn is None:
            self.connect()
        db = self.__conn[self.mongo_db[0]]
        if self.mongo_user and self.mongo_password:
            db.authenticate(self.mongo_user, self.mongo_password)
        master = db.command('isMaster')['ismaster']
        dict = {}
        dict['key'] = 'mongodb.ismaster'
        DBList = []
        if master:
            dict['value'] = 1
            DBNames = self.__conn.database_names()
            self.__dbnames = DBNames
        else:
            dict['value'] = 0
        self.__metrics.append(dict)

    # Print DB list in json format, to be used for mongo db discovery in zabbix
    def getMongoDBLLD(self):
        if self.__dbnames is None:
            DBNames = self.getDBNames()
        else:
            DBNames = self.__dbnames
        dictLLD = {}
        DBList = []
        dictLLD['key'] = 'mongodb.discovery'
        dictLLD['value'] = {"data": DBList}
        if DBNames is not None:
            for db in DBNames:
                dict = {}
                dict['{#MONGODBNAME}'] = str(db)
                DBList.append(dict)
            dictLLD['value'] = {"data": DBList}
        self.__metrics.insert(0, dictLLD)

    # Print slaves list, to used for mongo discovery lag replication
    def getMongoDBslaves(self):
        db = MongoClient(self.mongo_host, self.mongo_port)

        if self.mongo_user and self.mongo_password:
            db.admin.authenticate(self.mongo_user, self.mongo_password)
        
        master = db.admin.command('isMaster')['ismaster']
        if master:
 
            try:
                rscheck = db.admin.command( { "replSetGetStatus" : 1 } )
                rscheck = rscheck['ok']
            except pymongo.errors.OperationFailure: 
                rscheck = 0
        
            if int(rscheck) == 1:
                db_stats = db.admin.command({'replSetGetStatus'  :1})
        
                slaves = {}
                slaves_list = []
                slaves['key'] = 'mongodb.lag.discovery'
                slaves['value'] = {"data": slaves_list}

                for key in db_stats['members']:
                    if key['stateStr'] == 'SECONDARY':
                        dict = {}
                        dict['{#MONGODBSLAVE}'] = str(key['name'])
                        slaves_list.append(dict)
                    slaves['value'] = {"data": slaves_list}
                self.__metrics.insert(0, slaves)

    
    def getOplog(self):
        db = MongoClient(self.mongo_host, self.mongo_port)

        if self.mongo_user and self.mongo_password:
            db.admin.authenticate(self.mongo_user, self.mongo_password)

        try:
            rscheck = db.admin.command( { "replSetGetStatus" : 1 } )
            rscheck = rscheck['ok']
        except pymongo.errors.OperationFailure: 
            rscheck = 0
        
        if int(rscheck) == 1:
            dbl = db.local
            coll = dbl['oplog.rs']

            op_first = (coll.find().sort('$natural', 1).limit(1))

            while op_first.alive:
                op_fst = (op_first.next())['ts'].time

            op_last = (coll.find().sort('$natural', -1).limit(1))
            
            while op_last.alive:
                op_last_st = op_last[0]['ts']
                op_lst = (op_last.next())['ts'].time

            status = round(float(op_lst - op_fst), 1)
            self.addMetrics('mongodb.oplog', status)

            currentTime = timegm(gmtime())
            oplog = int(((str(op_last_st).split('('))[1].split(','))[0])
            self.addMetrics('mongodb.oplog-sync', (currentTime - oplog))

            #count lag for all SLAVES
            master = db.admin.command('isMaster')['ismaster']
            if master:
                db_stats = db.admin.command({'replSetGetStatus'  :1})

                primary_optime = 0
                secondary_optime = 0
                slaves = {}

                for key in db_stats['members']:
                    if key['stateStr'] == 'SECONDARY':
                        slaves[key['name']] = key['optimeDate']
                    if key['stateStr'] == 'PRIMARY':
                        primary_optime = key['optimeDate']
            
                for key in slaves:
                    secondary_optime = slaves[key]
                    seconds_lag = (primary_optime - secondary_optime ).total_seconds()
                    self.addMetrics('mongodb.replication.lag.[%s]' % key, (int(seconds_lag)))


    def getMaintenance(self):
        db = MongoClient(self.mongo_host, self.mongo_port)

        if self.mongo_user and self.mongo_password:
            db.admin.authenticate(self.mongo_user, self.mongo_password)

        host_name = socket.gethostname()
        host_ip = socket.gethostbyname(socket.gethostname())

        fsync_locked = int(db.is_locked)
        
        try:
            rscheck = db.admin.command( { "replSetGetStatus" : 1 } )
            rscheck = rscheck['ok']
        except pymongo.errors.OperationFailure:
            rscheck = 0
        
        if int(rscheck) == 1:
            config = db.admin.command("replSetGetConfig", 1)
            for i in range(0, len(config['config']['members'])):
                if host_name in config['config']['members'][i]['host'] or host_ip in config['config']['members'][i]['host']:
                    priority = config['config']['members'][i]['priority']
                    hidden = int(config['config']['members'][i]['hidden'])

            self.addMetrics('mongodb.fsync-locked', fsync_locked)
            self.addMetrics('mongodb.priority', priority)
            self.addMetrics('mongodb.hidden', hidden)


    # Get Server Status
    def getServerStatusMetrics(self):
        if self.__conn is None:
            self.connect()
        db = self.__conn[self.mongo_db[0]]
        if self.mongo_user and self.mongo_password:
            db.authenticate(self.mongo_user, self.mongo_password)
        ss = db.command('serverStatus')


        # db info
        self.addMetrics('mongodb.version', ss['version'])
        self.addMetrics('mongodb.storageEngine', ss['storageEngine']['name'])
        self.addMetrics('mongodb.uptime', int(ss['uptime']))
        self.addMetrics('mongodb.okstatus', int(ss['ok']))

        # asserts
        for k, v in ss['asserts'].items():
            self.addMetrics('mongodb.asserts.' + k, v)

        # operations
        for k, v in ss['opcounters'].items():
            self.addMetrics('mongodb.operation.' + k, v)

        # memory
        for k in ['resident', 'virtual', 'mapped', 'mappedWithJournal']:
            self.addMetrics('mongodb.memory.' + k, ss['mem'][k])

        # connections
        for k, v in ss['connections'].items():
            self.addMetrics('mongodb.connection.' + k, v)

        # network
        for k, v in ss['network'].items():
            self.addMetrics('mongodb.network.' + k, v)


        # extra info
        self.addMetrics('mongodb.page.faults', ss['extra_info']['page_faults'])

        ## wired tiger
 
        # block-manager
        self.addMetrics('mongodb.block-manager.blocks-pre-loaded', int(ss['wiredTiger']['block-manager']["blocks pre-loaded"]))
        self.addMetrics('mongodb.block-manager.blocks-read', int(ss['wiredTiger']['block-manager']["blocks read"]))
        self.addMetrics('mongodb.block-manager.blocks-written', int(ss['wiredTiger']['block-manager']["blocks written"]))
        self.addMetrics('mongodb.block-manager.bytes-read', int(ss['wiredTiger']['block-manager']["bytes read"]))
        self.addMetrics('mongodb.block-manager.bytes-written', int(ss['wiredTiger']['block-manager']["bytes written"]))
        self.addMetrics('mongodb.block-manager.bytes-written-for-checkpoint', int(ss['wiredTiger']['block-manager']["bytes written for checkpoint"]))

        # cache
        for k, v in ss['wiredTiger']['cache'].items():
            self.addMetrics('mongodb.cache.' + k.replace(" ", "-"), int(v))

        # connections
        for k, v in ss['wiredTiger']['connection'].items():
            self.addMetrics('mongodb.connection.' + k.replace(" ", "-"),int(v))

        # cursor 
        for k, v in ss['wiredTiger']['cursor'].items():
            self.addMetrics('mongodb.cursor.' + k.replace(" ", "-"),int(v))

        # data-handle
        for k, v in ss['wiredTiger']['data-handle'].items():
            self.addMetrics('mongodb.data-handle.' + k.replace(" ", "-"),int(v))

        # lock
        for k, v in ss['wiredTiger']['lock'].items():
            self.addMetrics('mongodb.lock.' + k.replace(" ", "-"),int(v))

        # log
        for k, v in ss['wiredTiger']['log'].items():
            self.addMetrics('mongodb.log.' + k.replace(" ", "-"),int(v))

        # reconciliation
        for k, v in ss['wiredTiger']['reconciliation'].items():
            self.addMetrics('mongodb.reconciliation.' + k.replace(" ", "-"),int(v))

        # session
        self.addMetrics('mongodb.session.open-cursor-count', int(ss['wiredTiger']['session']["open cursor count"]))
        self.addMetrics('mongodb.session.open-session-count', int(ss['wiredTiger']['session']["open session count"]))

        # transaction
        for k, v in ss['wiredTiger']['transaction'].items():
            self.addMetrics('mongodb.transaction.' + k.replace(" ", "-").replace("-(msecs)",""),int(v))

        ## wt end

        # global lock
        lockTotalTime = ss['globalLock']['totalTime']
        self.addMetrics('mongodb.globalLock.totalTime', lockTotalTime)
        for k, v in ss['globalLock']['currentQueue'].items():
            self.addMetrics('mongodb.globalLock.currentQueue.' + k, v)
        for k, v in ss['globalLock']['activeClients'].items():
            self.addMetrics('mongodb.globalLock.activeClients.' + k, v)

        ## metrics
        
        # queryExecutor
        self.addMetrics('mongodb.metrics.queryExecutor.scanned', int(ss['metrics']['queryExecutor']["scanned"]))
        self.addMetrics('mongodb.metrics.queryExecutor.scannedObjects', int(ss['metrics']['queryExecutor']["scannedObjects"]))

        # record
        self.addMetrics('mongodb.metrics.record.moves', int(ss['metrics']['record']["moves"]))

    # Get DB stats for each DB
    def getDBStatsMetrics(self):
        if self.__conn is None:
            self.connect()
        if self.__dbnames is None:
            self.getDBNames()
        if self.__dbnames is not None:
            for mongo_db in self.__dbnames:
                db = self.__conn[mongo_db]
                if self.mongo_user and self.mongo_password:
                    self.__conn[self.mongo_db[0]].authenticate(self.mongo_user, self.mongo_password)
                dbs = db.command('dbstats')
                for k, v in dbs.items():
                    if k in ['storageSize','ok','avgObjSize','indexes','objects','collections','fileSize','numExtents','dataSize','indexSize','nsSizeMB']:
                        self.addMetrics('mongodb.stats.' + k + '[' + mongo_db + ']', int(v))
    # Close connection
    def close(self):
        if self.__conn is not None:
            self.__conn.close()

if __name__ == '__main__':
    MongoDB = MongoDB()
    MongoDB.getDBNames()
    MongoDB.getMongoDBslaves()
    MongoDB.getMongoDBLLD()
    MongoDB.getOplog()
    MongoDB.getMaintenance()
    MongoDB.getServerStatusMetrics()
    MongoDB.getDBStatsMetrics()
    MongoDB.printMetrics()
    MongoDB.close()
