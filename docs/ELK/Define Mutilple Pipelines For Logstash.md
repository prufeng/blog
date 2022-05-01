Define Mutilple Pipelines For Logstash
====
Logstash有一个对初学者来说很大的坑，就是安装之后直接运行，它将默认只使用一个pipeline，把conf.d下面的配置文件一次全加载了。

如果不同配置文件的输入输出有冲突，比如缺少必要的条件判断，就会发生意想不到的结果。

使用多管道，势在必行。

# Default Pipeline
## pipeline.yml
默认的pipeline配置是这样子的。
```
# This file is where you define your pipelines. You can define multiple.
# For more information on multiple pipelines, see the documentation:
#   https://www.elastic.co/guide/en/logstash/current/multiple-pipelines.html

- pipeline.id: main
  path.config: "/etc/logstash/conf.d/*.conf"
```
## conf.d/app.conf
然后配置里需要一大堆ifelse，来区分来自不用的应用。

比如单说处理Filebeat的log，就需要在filter里根据不同的关键字分别进行处理。
```
input {
  beats {
    port => 5044
  }
}

filter {
  if [fields][type] == "aaaa" {
    grok {
        ...
    }
    date {
        ...
    }
  } else if [fields][type] == "bbbb" {
    grok {
        ...
    }
    date {
        ...
    }
  } else if [fields][type] == "cccc" {
    grok {
        ...
    }
    if "_grokparsefailure" in [tags] {
      drop{}
    }
    date {
        ...
    }
  }
}

output {
  if [fields][type] in ["aaaa", "bbbb", "cccc"] {
    elasticsearch {
      hosts => ["http://192.168.0.888:9200"]
      index => "%{[@metadata][beat]}-%{[fields][type]}-%{+YYYY.MM}"
    }
  }
}
```
输出其实也一样，不过这里用了些适配的技巧。

增加其他类型，一样要增加ifelse的判断。

# Multiple Pipelines
## pipeline.yml
在pipeline里按App分流。

每个App分别定义一个pipeline，再放到独立的配置文件里。
```
- pipeline.id: beats
  config.string: |
    input { beats { port => 5044 } }
    output {
      if [fields][type] == "aaaa" { pipeline { send_to => aaaa_addr }
      } else if [fields][type] == "bbbb" { pipeline { send_to => bbbb_addr }
      } else if [fields][type] == "cccc" { pipeline { send_to => cccc_addr }}
    }

- pipeline.id: aaaa
  path.config: "/etc/logstash/conf.d/{aaaa,beats_out}.conf"

- pipeline.id: bbbb
  path.config: "/etc/logstash/conf.d/{bbbb,beats_out}.conf"

- pipeline.id: cccc
  path.config: "/etc/logstash/conf.d/{cccc,beats_out}.conf"
```
配置文件路径支持适配的写法。每个App分别加载两个文件。

这里这样处理主要是因为他们的output配置刚好可以是一样的。

## beats_out.conf
虽然共享同一个配置，但是因为在不同管道，所以不需要加ifelse也不会混乱。
```
output {
  elasticsearch {
    hosts => ["http://192.168.0.888:9200"]
    index => "%{[@metadata][beat]}-%{[fields][type]}-%{+YYYY.MM}"
  }
}
```
## aaaa.conf
从上游管道地址接收输入。

直接处理log不需要再判断。
```
input { pipeline { address => aaaa_addr } }

filter {
  grok {
      ...
  }
  if "_grokparsefailure" in [tags] {
    drop{}
  }
  date {
      ...
  }
}

```

# 调试
可以先用最简单的例子来调试，一个一个添加。

```
- pipeline.id: upstream
  config.string: input {file { path => "/etc/logstash/iiii.log" }} output { pipeline { send_to => [myVirtualAddress] } }
- pipeline.id: downstream
  config.string: input { pipeline { address => myVirtualAddress } } output {file { path => "/etc/logstash/oooo.log" }}
```

我就是太心急了，直接刷刷一大堆，结果总是有错。

半天才发现，原来只是删除ifelse的时候，有些文件没有删掉多余的缩进，空格有些混乱，肉眼又很难看出来。
