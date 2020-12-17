Elasticsearch JVM OutofMemory, Kibana: [circuit_breaking_exception] [parent] Data too large
====		
Kibana打开就报错，其实也算是Kibana的bug，看到已经有人起了Issue，就算Elasticsearch出现Out of memory，但也不至于整个网页都死了嘛。

测试版本：7.9.0

>{"statusCode":500,"error":"Internal Server Error","message":"[parent] Data too large, data for [<http_request>] would be [1044896078/996.4mb], which is larger than the limit of [1020054732/972.7mb], real usage: [1044895496/996.4mb], new bytes reserved: [582/582b], usages [request=136/136b, fielddata=8487/8.2kb, in_flight_requests=582/582b, model_inference=0/0b, accounting=56798692/54.1mb]: [circuit_breaking_exception] [parent] Data too large, data for [<http_request>] would be [1044896078/996.4mb], which is larger than the limit of [1020054732/972.7mb], real usage: [1044895496/996.4mb], new bytes reserved: [582/582b], usages [request=136/136b, fielddata=8487/8.2kb, in_flight_requests=582/582b, model_inference=0/0b, accounting=56798692/54.1mb], with { bytes_wanted=1044896078 & bytes_limit=1020054732 & durability=\"PERMANENT\" }"}


**解决办法：**

Elasticsearch JVM内存加大试试？默认的太小了！
```
vi /etc/elasticsearch/jvm.options
```

```
-Xms1g
-Xmx1g
```




