Elasticsearch: Validation Failed: 1: this action would add [2] total shards, but this cluster currently has [1000]/[1000] maximum shards open
====
Elasticsearch突然就写不进去了，看日志，shards有1000的限制。

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
      "max_shards_per_node":2000
    }
  }
}
```

碰巧一起重启时，Kibana可能会因为这个错启动不了。
```
[Failed to create internal index mappings[org.elasticsearch.common.ValidationException: Validation Failed: 1: this action would add [2] shards, but this cluster currently has [1000]/[1000] maximum normal shards open;]]
```
但其实Elasticsearch还是可以访问的，用命令行即可。
```
curl localhost:9200/_cluster/health?pretty -uelasticuser:changeme

curl -X PUT "localhost:9200/_cluster/settings?pretty" -uelasticuser:changeme -H 'Content-Type: application/json' -d'
{
  "transient": {
    "cluster": {
      "max_shards_per_node":2000
    }
  }
}
'
```

以上命令只是临时更改配置，下次重启之后还是会失败，要持久化，可将transient改为persistent，不过注意这并没有从根本上解决shards太多的问题。


