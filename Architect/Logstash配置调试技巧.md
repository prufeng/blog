Logstash配置调试技巧：Filter Grok日志模式Pattern匹配之类的确实很麻烦
====
之前我也很不耐烦，不过掌握了以下一些小技巧之后，感觉好多了。

# Logstash Config Test and Exit
```
/usr/share/logstash/bin/logstash --config.test_and_exit --path.settings /etc/logstash -f test.conf
```

# Logstash Config Automatic Reload
```
/usr/share/logstash/bin/logstash --path.settings /etc/logstash --config.reload.automatic -f test.conf
```

# Logstash Grok Debugger

一般用网页，因为不用登陆。

* Kibana -> Dev Tools -> Grok Debugger
* http://grokdebug.herokuapp.com/

# Logstash Input
接受命令行输入。
```
input {
  stdin {}
}
```

不过用了`stdin`之后不支持`--config.reload.automatic`，所以实际上我还是用Filebeat多。
```
input {
  beats {
    port => 5044
  }
}
```
只要简单append文本到目标文件即可。

## Force Filebeat to Send Data Again
也可以让Filebeat重新再发送一次所有文件。
```
rm -rf /var/lib/filebeat/registry/filebeat
systemctl restart filebeat
```

# Logstash Output

输出到控制台，输出不匹配的到文件。
```conf
output {
  stdout { codec => rubydebug }
  if "_grokparsefailure" in [tags] {
    file { "path" => "/tmp/grok_failures.log" }
  }
}
```

# P.S.
一开始感觉挺复杂，后来发现其实很多日志都不规范，而且一般也不需要全匹配，简单使用就足够了。

常用DATESTAMP，DATA，GREEDYDATA，SPACE等。   
特别是SPACE，一开始没想到要用，后来发现总是匹配不好，加上就正常了。

`/usr/share/logstash/vendor/bundle/jruby/2.5.0/gems/logstash-patterns-core-4.1.2/patterns/`
https://github.com/logstash-plugins/logstash-patterns-core/tree/master/patterns
