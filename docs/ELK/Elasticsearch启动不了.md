ELK - Elasticsearch启动不了: Could not create the Java Virtual Machine
===
提供一个思路。

# Elasticsearch启动不了
```sh
Nov 04 15:45:10 appserver01 elasticsearch[25283]: Invalid -Xlog option '-Xlog:gc*,gc+age=trace,safepoint:file=/var/log/elasticsearch/gc.log:utctime,pid,tags:filecount=32,filesize=64m', see error log for details.
Nov 04 15:45:10 appserver01 elasticsearch[25283]: Error: Could not create the Java Virtual Machine.
Nov 04 15:45:10 appserver01 elasticsearch[25283]: Error: A fatal exception has occurred. Program will exit.
```

去看log发现整个folder都不见了（被人删了？）。

重建，grant right to elasticsearch就OK了。
```
/var/log/elasticsearch
```
