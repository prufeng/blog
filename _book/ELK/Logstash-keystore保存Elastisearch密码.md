Logstash-keystore保存Elasticsearch或其他密码
====
方法好简单，文档好齐全，但还是有坑。

```
set +o history

# Have to setup keystore password to encrypt keystore, before running logstash-keystore
export LOGSTASH_KEYSTORE_PASS=changeme

# Have to save the password for service to kick start (installed by RPM), otherwise service will fail.
echo "LOGSTASH_KEYSTORE_PASS=changeme" > /etc/sysconfig/logstash

set -o history

# Have to add `--path.settings` paramemter, then logstash.keystore will be generated under this path
/usr/share/logstash/bin/logstash-keystore --path.settings /etc/logstash create
/usr/share/logstash/bin/logstash-keystore --path.settings /etc/logstash add ES_PWD
/usr/share/logstash/bin/logstash-keystore --path.settings /etc/logstash remove ES_PWD
```

Bug: Don't run the command under /etc/logstash, otherwise will see error below.
```
2020-11-16 16:10:37,143 main ERROR Unable to locate appender "${sys:ls.log.format}_console" for logger config "root"
2020-11-16 16:10:37,144 main ERROR Unable to locate appender "${sys:ls.log.format}_rolling" for logger config "root"
2020-11-16 16:10:37,144 main ERROR Unable to locate appender "${sys:ls.log.format}_rolling_slowlog" for logger config "slowlog"
2020-11-16 16:10:37,145 main ERROR Unable to locate appender "${sys:ls.log.format}_console_slowlog" for logger config "slowlog"
```


