# Zabbix-MongoDB

MongoDB 3.6, 4.0, 4.2 

**Installation**

1. Import the mongodb template to zabbix and link it to the zabbix mongodb host.
2. Copy the scripts to mongodb host in /usr/local/bin .
3. Copy mongodb zabbix agent configuration to /etc/zabbix-agent/zabbix_agentd.d and restart zabbix agent.

Note:
- Zabbix sender uses zabbix agent configuration to send the metrics, please check the hostname is set in the zabbix agent config /etc/zabbix/zabbix_agentd.conf, by default the hostname may be commented out.

The following metrics are collected on mongodb by using python mongodb client, and then sent by zabbix sender.

**Server Stats**
- mongodb.version
- mongodb.storageEngine
- mongodb.uptime
- mongodb.okstatus
- mongodb.asserts.msg
- mongodb.asserts.rollovers
- mongodb.asserts.regular
- mongodb.asserts.warning
- mongodb.asserts.user
- mongodb.operation.getmore
- mongodb.operation.insert
- mongodb.operation.update
- mongodb.operation.command
- mongodb.operation.query
- mongodb.operation.delete
- mongodb.memory.resident
- mongodb.memory.virtual
- mongodb.memory.mapped
- mongodb.memory.mappedWithJournal
- mongodb.connection.current
- mongodb.connection.available
- mongodb.connection.totalCreated
- mongodb.network.physicalBytesOut
- mongodb.network.numRequests
- mongodb.network.bytesOut
- mongodb.network.physicalBytesIn
- mongodb.network.bytesIn
- mongodb.page.faults
- mongodb.block-manager.blocks-pre-loaded
- mongodb.block-manager.blocks-read
- mongodb.block-manager.blocks-written
- mongodb.block-manager.bytes-read
- mongodb.block-manager.bytes-written
- mongodb.block-manager.bytes-written-for-checkpoint
- mongodb.cache.unmodified-pages-evicted
- mongodb.cache.eviction-server-evicting-pages
- mongodb.cache.tracked-dirty-pages-in-the-cache
- mongodb.cache.overflow-values-cached-in-memory
- mongodb.cache.eviction-calls-to-get-a-page-found-queue-empty-after-locking
- mongodb.cache.internal-pages-split-during-eviction
- mongodb.cache.application-threads-page-write-from-cache-to-disk-time-(usecs)
- mongodb.cache.page-split-during-eviction-deepened-the-tree
- mongodb.cache.leaf-pages-split-during-eviction
- mongodb.cache.pages-walked-for-eviction
- mongodb.cache.percentage-overhead
- mongodb.cache.pages-evicted-by-application-threads
- mongodb.cache.tracked-dirty-bytes-in-the-cache
- mongodb.cache.maximum-page-size-at-eviction
- mongodb.cache.failed-eviction-of-pages-that-exceeded-the-in-memory-maximum
- mongodb.cache.application-threads-page-write-from-cache-to-disk-count
- mongodb.cache.eviction-worker-thread-stable-number
- mongodb.cache.pages-evicted-because-they-exceeded-the-in-memory-maximum
- mongodb.cache.tracked-bytes-belonging-to-leaf-pages-in-the-cache
- mongodb.cache.eviction-server-candidate-queue-empty-when-topping-up
- mongodb.cache.bytes-written-from-cache
- mongodb.cache.force-re-tuning-of-eviction-workers-once-in-a-while
- mongodb.cache.eviction-empty-score
- mongodb.cache.eviction-server-slept,-because-we-did-not-make-progress-with-eviction
- mongodb.cache.pages-queued-for-urgent-eviction
- mongodb.cache.eviction-walks-abandoned
- mongodb.cache.eviction-currently-operating-in-aggressive-mode
- mongodb.cache.application-threads-page-read-from-disk-to-cache-count
- mongodb.cache.tracked-bytes-belonging-to-internal-pages-in-the-cache
- mongodb.cache.bytes-currently-in-the-cache
- mongodb.cache.pages-selected-for-eviction-unable-to-be-evicted
- mongodb.cache.hazard-pointer-maximum-array-length
- mongodb.cache.lookaside-table-remove-calls
- mongodb.cache.in-memory-page-passed-criteria-to-be-split
- mongodb.cache.eviction-state
- mongodb.cache.checkpoint-blocked-page-eviction
- mongodb.cache.pages-queued-for-urgent-eviction-during-walk
- mongodb.cache.eviction-calls-to-get-a-page-found-queue-empty
- mongodb.cache.application-threads-page-read-from-disk-to-cache-time-(usecs)
- mongodb.cache.pages-written-from-cache
- mongodb.cache.eviction-calls-to-get-a-page
- mongodb.cache.modified-pages-evicted-by-application-threads
- mongodb.cache.pages-seen-by-eviction-walk
- mongodb.cache.eviction-worker-thread-evicting-pages
- mongodb.cache.bytes-read-into-cache
- mongodb.cache.page-written-requiring-lookaside-records
- mongodb.cache.hazard-pointer-blocked-page-eviction
- mongodb.cache.lookaside-table-insert-calls
- mongodb.cache.bytes-not-belonging-to-page-images-in-the-cache
- mongodb.cache.pages-read-into-cache
- mongodb.cache.pages-written-requiring-in-memory-restoration
- mongodb.cache.pages-evicted-because-they-had-chains-of-deleted-items
- mongodb.cache.files-with-new-eviction-walks-started
- mongodb.cache.pages-queued-for-eviction
- mongodb.cache.eviction-worker-thread-removed
- mongodb.cache.eviction-worker-thread-active
- mongodb.cache.pages-requested-from-the-cache
- mongodb.cache.pages-read-into-cache-requiring-lookaside-entries
- mongodb.cache.eviction-server-candidate-queue-not-empty-when-topping-up
- mongodb.cache.files-with-active-eviction-walks
- mongodb.cache.hazard-pointer-check-entries-walked
- mongodb.cache.in-memory-page-splits
- mongodb.cache.internal-pages-evicted
- mongodb.cache.eviction-worker-thread-created
- mongodb.cache.overflow-pages-read-into-cache
- mongodb.cache.maximum-bytes-configured
- mongodb.cache.pages-currently-held-in-the-cache
- mongodb.cache.modified-pages-evicted
- mongodb.cache.eviction-server-unable-to-reach-eviction-goal
- mongodb.cache.bytes-belonging-to-page-images-in-the-cache
- mongodb.cache.hazard-pointer-check-calls
- mongodb.connection.total-read-I/Os
- mongodb.connection.memory-re-allocations
- mongodb.connection.pthread-mutex-shared-lock-write-lock-calls
- mongodb.connection.auto-adjusting-condition-resets
- mongodb.connection.detected-system-time-went-backwards
- mongodb.connection.pthread-mutex-condition-wait-calls
- mongodb.connection.memory-frees
- mongodb.connection.pthread-mutex-shared-lock-read-lock-calls
- mongodb.connection.total-fsync-I/Os
- mongodb.connection.files-currently-open
- mongodb.connection.memory-allocations
- mongodb.connection.auto-adjusting-condition-wait-calls
- mongodb.connection.total-write-I/Os
- mongodb.cursor.cursor-restarted-searches
- mongodb.cursor.cursor-prev-calls
- mongodb.cursor.cursor-insert-calls
- mongodb.cursor.cursor-reset-calls
- mongodb.cursor.cursor-update-calls
- mongodb.cursor.cursor-search-near-calls
- mongodb.cursor.cursor-search-calls
- mongodb.cursor.cursor-next-calls
- mongodb.cursor.cursor-create-calls
- mongodb.cursor.truncate-calls
- mongodb.cursor.cursor-remove-calls
- mongodb.data-handle.session-dhandles-swept
- mongodb.data-handle.connection-sweeps
- mongodb.data-handle.connection-sweep-dhandles-removed-from-hash-list
- mongodb.data-handle.connection-data-handles-currently-active
- mongodb.data-handle.connection-sweep-dhandles-closed
- mongodb.data-handle.session-sweep-attempts
- mongodb.data-handle.connection-sweep-candidate-became-referenced
- mongodb.data-handle.connection-sweep-time-of-death-sets
- mongodb.lock.schema-lock-application-thread-wait-time-(usecs) 
- mongodb.lock.table-lock-application-thread-time-waiting-for-the-table-lock-(usecs)
- mongodb.lock.checkpoint-lock-internal-thread-wait-time-(usecs)
- mongodb.lock.schema-lock-acquisitions
- mongodb.lock.handle-list-lock-eviction-thread-wait-time-(usecs)
- mongodb.lock.checkpoint-lock-acquisitions
- mongodb.lock.table-lock-internal-thread-time-waiting-for-the-table-lock-(usecs)
- mongodb.lock.checkpoint-lock-application-thread-wait-time-(usecs)
- mongodb.lock.table-lock-acquisitions
- mongodb.lock.metadata-lock-application-thread-wait-time-(usecs)
- mongodb.lock.schema-lock-internal-thread-wait-time-(usecs)
- mongodb.lock.metadata-lock-internal-thread-wait-time-(usecs)
- mongodb.lock.metadata-lock-acquisitions
- mongodb.log.log-sync_dir-operations
- mongodb.log.log-sync_dir-time-duration-(usecs)
- mongodb.log.log-write-operations
- mongodb.log.log-server-thread-advances-write-LSN
- mongodb.log.consolidated-slot-join-races
- mongodb.log.maximum-log-file-size
- mongodb.log.records-processed-by-log-scan
- mongodb.log.total-log-buffer-size
- mongodb.log.log-records-too-small-to-compress
- mongodb.log.log-force-write-operations-skipped
- mongodb.log.log-scan-operations
- mongodb.log.pre-allocated-log-files-used
- mongodb.log.pre-allocated-log-files-not-ready-and-missed
- mongodb.log.total-size-of-compressed-records
- mongodb.log.pre-allocated-log-files-prepared
- mongodb.log.log-sync-time-duration-(usecs)
- mongodb.log.total-in-memory-size-of-compressed-records
- mongodb.log.yields-waiting-for-previous-log-file-close
- mongodb.log.log-records-not-compressed
- mongodb.log.log-force-write-operations
- mongodb.log.consolidated-slot-unbuffered-writes
- mongodb.log.written-slots-coalesced 
- mongodb.log.consolidated-slot-join-active-slot-closed
- mongodb.log.log-records-compressed
- mongodb.log.number-of-pre-allocated-log-files-to-create
- mongodb.log.log-bytes-written
- mongodb.log.busy-returns-attempting-to-switch-slots
- mongodb.log.consolidated-slot-transitions-unable-to-find-free-slot
- mongodb.log.consolidated-slot-joins
- mongodb.log.log-files-manually-zero-filled
- mongodb.log.log-bytes-of-payload-data
- mongodb.log.log-flush-operations
- mongodb.log.log-sync-operations
- mongodb.log.log-scan-records-requiring-two-reads
- mongodb.log.logging-bytes-consolidated
- mongodb.log.log-server-thread-write-LSN-walk-skipped
- mongodb.log.consolidated-slot-join-transitions
- mongodb.log.log-release-advances-write-LSN
- mongodb.log.consolidated-slot-closures
- mongodb.reconciliation.fast-path-pages-deleted
- mongodb.reconciliation.split-objects-currently-awaiting-free
- mongodb.reconciliation.split-bytes-currently-awaiting-free
- mongodb.reconciliation.pages-deleted
- mongodb.reconciliation.page-reconciliation-calls-for-eviction
- mongodb.reconciliation.page-reconciliation-calls
- mongodb.session.open-cursor-count
- mongodb.session.open-session-count
- mongodb.transaction.number-of-named-snapshots-dropped
- mongodb.transaction.transaction-checkpoint-currently-running
- mongodb.transaction.transaction-begins
- mongodb.transaction.transaction-fsync-calls-for-checkpoint-after-allocating-the-transaction-ID
- mongodb.transaction.transactions-committed
- mongodb.transaction.transaction-checkpoint-most-recent-time
- mongodb.transaction.transaction-checkpoints
- mongodb.transaction.transaction-range-of-IDs-currently-pinned-by-a-checkpoint
- mongodb.transaction.transaction-sync-calls
- mongodb.transaction.transaction-checkpoint-scrub-dirty-target
- mongodb.transaction.transaction-fsync-duration-for-checkpoint-after-allocating-the-transaction-ID-(usecs)
- mongodb.transaction.transaction-checkpoints-skipped-because-database-was-clean
- mongodb.transaction.transaction-checkpoint-scrub-time
- mongodb.transaction.transaction-checkpoint-max-time
- mongodb.transaction.number-of-named-snapshots-created
- mongodb.transaction.transaction-checkpoint-min-time
- mongodb.transaction.transaction-checkpoint-total-time
- mongodb.transaction.transaction-checkpoint-generation
- mongodb.transaction.transaction-failures-due-to-cache-overflow
- mongodb.transaction.transaction-range-of-IDs-currently-pinned-by-named-snapshots
- mongodb.transaction.transactions-rolled-back
- mongodb.transaction.transaction-range-of-IDs-currently-pinned
- mongodb.globalLock.totalTime
- mongodb.globalLock.currentQueue.total
- mongodb.globalLock.currentQueue.writers
- mongodb.globalLock.currentQueue.readers
- mongodb.globalLock.activeClients.total
- mongodb.globalLock.activeClients.writers
- mongodb.globalLock.activeClients.readers
- mongodb.metrics.queryExecutor.scanned
- mongodb.metrics.queryExecutor.scannedObjects
- mongodb.metrics.record.moves

**Replication Stats**
- mongodb.ismaster
- mongodb.oplog
- mongodb.oplog-sync
- mongodb.replication.lag.[name]
- mongodb.fsync-locked
- mongodb.priority
- mongodb.hidden

**DB Stats**
- mongodb.stats.storageSize[db]
- mongodb.stats.ok[db]
- mongodb.stats.avgObjSize[db]
- mongodb.stats.indexes[db]
- mongodb.stats.objects[db]
- mongodb.stats.collections[db]
- mongodb.stats.fileSize[db]
- mongodb.stats.numExtents[db]
- mongodb.stats.dataSize[db]
- mongodb.stats.indexSize[db]
- mongodb.stats.nsSizeMB[db]
