ELK - Logstash收集多种Filebeat数据，如何区分不同来源
====
比如Filebeat。

# Logstash Filer Grok

Logstash配置可以使用`if [fields][type]`来区分来源。

test.conf
```conf
input {
  beats {
    port => 5044
  }
}

filter {
  if [fields][type] == "test" {
    grok {
      match => { "message" => "%{DATESTAMP:logTime}%-%{GREEDYDATA:message}" }
      overwrite => [ "message" ]
    }
  }
}

output {
  if [fields][type] == "test" {
    stdout { codec => rubydebug }
  }
  if "_grokparsefailure" in [tags] {
    file { "path" => "/tmp/grok_failures.log" }
  }
}
```

# Filebeat
Filebeat配置相应的加上`fields.type`定义。

```
vi /etc/filebeat/filebeat.yml
```
```yml
- type: log

  # Change to true to enable this input configuration.
  enabled: true

  # Paths that should be crawled and fetched. Glob based paths.
  paths:
    - /var/log/*.log
  fields:
    type: test

#output.elasticsearch:
  # Array of hosts to connect to.
  #hosts: ["localhost:9200"]

output.logstash:
  # The Logstash hosts
  hosts: ["remotehost:5044"]
```
