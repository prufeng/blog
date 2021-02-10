Elasticsearch: Validation Failed: 1: this action would add [2] total shards, but this cluster currently has [1000]/[1000] maximum shards open
====
突然就写不进去了，看日志，shards有1000的限制。

Dev Tool
```
{
  "error" : {
    "root_cause" : [
      {
        "type" : "runtime_exception",
        "reason" : "Failed to persist transform configuration"
      }
    ],
    "type" : "runtime_exception",
    "reason" : "Failed to persist transform configuration",
    "caused_by" : {
      "type" : "validation_exception",
      "reason" : "Validation Failed: 1: this action would add [2] total shards, but this cluster currently has [1000]/[1000] maximum shards open;"
    }
  },
  "status" : 500
}
```

elasticsearch.log
```
Caused by: org.elasticsearch.common.ValidationException: Validation Failed: 1: this action would add [2] total shards, but this cluster currently has [1000]/[1000] maximum shards open;
        at org.elasticsearch.indices.ShardLimitValidator.validateShardLimit(ShardLimitValidator.java:80) ~[elasticsearch-7.9.0.jar:7.9.0]
        at org.elasticsearch.cluster.metadata.MetadataCreateIndexService.aggregateIndexSettings(MetadataCreateIndexService.java:694) ~[elasticsearch-7.9.0.jar:7.9.0]
        at org.elasticsearch.cluster.metadata.MetadataCreateIndexService.applyCreateIndexRequestWithV1Templates(MetadataCreateIndexService.java:477) ~[elasticsearch-7.9.0.jar:7.9.0]
        at org.elasticsearch.cluster.metadata.MetadataCreateIndexService.applyCreateIndexRequest(MetadataCreateIndexService.java:360) ~[elasticsearch-7.9.0.jar:7.9.0]
        at org.elasticsearch.cluster.metadata.MetadataCreateIndexService.applyCreateIndexRequest(MetadataCreateIndexService.java:367) ~[elasticsearch-7.9.0.jar:7.9.0]
        at org.elasticsearch.action.admin.indices.create.AutoCreateAction$TransportAction$1.execute(AutoCreateAction.java:137) ~[elasticsearch-7.9.0.jar:7.9.0]
        at org.elasticsearch.cluster.ClusterStateUpdateTask.execute(ClusterStateUpdateTask.java:47) ~[elasticsearch-7.9.0.jar:7.9.0]
        at org.elasticsearch.cluster.service.MasterService.executeTasks(MasterService.java:702) ~[elasticsearch-7.9.0.jar:7.9.0]
        at org.elasticsearch.cluster.service.MasterService.calculateTaskOutputs(MasterService.java:324) ~[elasticsearch-7.9.0.jar:7.9.0]
        at org.elasticsearch.cluster.service.MasterService.runTasks(MasterService.java:219) ~[elasticsearch-7.9.0.jar:7.9.0]
        ... 10 more
```

权宜之计，当然是改大了。

```json
PUT /_cluster/settings
{
  "transient": {
    "cluster": {
      "max_shards_per_node":10000
    }
  }
}
```
