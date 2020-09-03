ELK - Failed to start Elasticsearch. elasticsearch.service start operation timed out. Terminating. Can't move to started state when closed
====
升级到最新版后发现Elasticsearch启动不了，总是time out。

```
journalctl -u elasticsearch
```
```
systemd[1]: Starting Elasticsearch...
systemd[1]: elasticsearch.service start operation timed out. Terminating.
systemd-entrypoint[24309]: uncaught exception in thread [main]
systemd-entrypoint[24309]: java.lang.IllegalStateException: Can't move to started state when closed
systemd-entrypoint[24309]: at org.elasticsearch.common.component.Lifecycle.canMoveToStarted(Lifecycle.java:120)
systemd-entrypoint[24309]: at org.elasticsearch.common.component.AbstractLifecycleComponent.start(AbstractLifecycleComponent.java:53)
systemd-entrypoint[24309]: at org.elasticsearch.node.Node.start(Node.java:814)
systemd-entrypoint[24309]: at org.elasticsearch.bootstrap.Bootstrap.start(Bootstrap.java:317)
systemd-entrypoint[24309]: at org.elasticsearch.bootstrap.Bootstrap.init(Bootstrap.java:402)
systemd-entrypoint[24309]: at org.elasticsearch.bootstrap.Elasticsearch.init(Elasticsearch.java:170)
systemd-entrypoint[24309]: at org.elasticsearch.bootstrap.Elasticsearch.execute(Elasticsearch.java:161)
systemd-entrypoint[24309]: at org.elasticsearch.cli.EnvironmentAwareCommand.execute(EnvironmentAwareCommand.java:86)
systemd-entrypoint[24309]: at org.elasticsearch.cli.Command.mainWithoutErrorHandling(Command.java:127)
systemd-entrypoint[24309]: at org.elasticsearch.cli.Command.main(Command.java:90)
systemd-entrypoint[24309]: at org.elasticsearch.bootstrap.Elasticsearch.main(Elasticsearch.java:126)
systemd-entrypoint[24309]: at org.elasticsearch.bootstrap.Elasticsearch.main(Elasticsearch.java:92)
systemd-entrypoint[24309]: For complete error details, refer to the log at /var/log/elasticsearch/elasticsearch.log
systemd[1]: Failed to start Elasticsearch.
systemd[1]: Unit elasticsearch.service entered failed state.
systemd[1]: elasticsearch.service failed.
```
解决办法是增加服务启动时间。

缺省值是90s。
```
$ systemctl show elasticsearch | grep ^Timeout
TimeoutStartUSec=1min 30s
TimeoutStopUSec=0
```

修改为180。
```
$ systemctl edit elasticsearch.service

[Service]
TimeoutStartSec=180
```

文件实际被保存到以下路径，会覆盖服务原本的缺省值。
```
cat /etc/systemd/system/elasticsearch.service.d/override.conf
```
修改之后，TimeoutStartUSec变为3min。
```
$ systemctl daemon-reload
$ systemctl show elasticsearch | grep ^Timeout
TimeoutStartUSec=3min
TimeoutStopUSec=0
```

这里有个Linux的小坑。`TimeoutStartUSec`配置在文件里应该为`TimeoutStartSec`，不知道为什么这么无聊显示的时候要加多个`U`。
