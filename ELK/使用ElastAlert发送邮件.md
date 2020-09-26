ELK - 使用ElastAlert发送邮件
===

简单记录下之前的研究。

https://buildmedia.readthedocs.org/media/pdf/elastalert/latest/elastalert.pdf

# Install Python

之前在[ElastAlert最大的坑](https://blog.csdn.net/prufeng/article/details/100847575)里说过，要用Python3！

# Install Pip
如果没有pip，则需要安装。
```
sudo easy_install pip 
```
或
Download get-pip.py: https://bootstrap.pypa.io/get-pip.py
```
sudo python get-pip.py
```

# Install Elastalert
```
sudo pip install elastalert
```
需要其他包按提示装好。

安装完后有这些命令可以用。
```
ll /usr/local/bin/ela*
/usr/local/bin/elastalert
/usr/local/bin/elastalert-create-index
/usr/local/bin/elastalert-rule-from-kibana
/usr/local/bin/elastalert-test-rule
```
可以这样运行。
```
sudo python3 /usr/local/bin/elastalert-test-rule --config config.yaml down_frequence_rule.yaml
sudo python3 /usr/local/bin/elastalert --verbose --config config.yaml --rule down_frequence_rule.yaml
sudo python3 /usr/local/bin/elastalert --verbose --rule down_frequence_rule.yaml
```
或者这样。
```
sudo python3 -m elastalert.elastalert --verbose --config config.yaml --rule down_frequence_rule.yaml
```
`elastalert-test-rule`的效果与`elastalert --debug`相似，验证规则但不真的发送邮件。

# 结果
先说结果。

使用`elastalert-test-rule`或`elastalert --debug`，可以看到自己定义的邮件内容。
```sh
INFO:elastalert:Queried rule Down frequency rule from 2019-11-18 11:32 CST to 2019-11-18 11:36 CST: 54 / 54 hits
INFO:elastalert:Skipping writing to ES: {'exponent': 0, 'rule_name': 'Down frequency rule', '@timestamp': '2019-11-18T03:36:20.578458Z', 'until': '2019-11-18T03:37:20.578442Z'}
INFO:elastalert:Alert for Down frequency rule at 2019-11-18T03:35:10.755Z:
INFO:elastalert:Dear Team, mq dev is down @ 2019-11-18T03:35:10.755Z, please take action!
### Number hits: 54
> Check time: 2019-11-18T03:35:10.755Z
> IP: 192.168.1.88
> Env: mq dev
> Status: down
>>> Error: dial tcp 192.168.1.88:8888: connect: connection refused
```

正常运行时，提示如下。
```sh
INFO:elastalert:Sleeping for 59.999735 seconds
INFO:elastalert:Sent email to ['my.dummy@email.com']
INFO:elastalert:Ignoring match for silenced rule Down frequency rule
INFO:elastalert:Ran Down frequency rule from 2019-11-18 10:10 CST to 2019-11-18 10:25 CST: 225 query hits (212 already seen), 2 matches, 1 alerts sent

```

# Create Index in Elasticsearch
ElastAlert的状态保存，需要在Elasticsearch里create index。

可以直接用示例配置来试。
```
cp config.yaml.example config.yaml
sudo python3 /usr/local/bin/elastalert-create-index --config config.yaml
```

# Create Rule
创建Alert规则，主要是怎样query，怎么trigger，定义SMTP和信息内容等。

初次测试，要确保query的条件满足，可以触发邮件发送。

Email那里，遇到一个坑：提示alerts sent，然而邮件并没有收到，乱改一通最后加上`from_addr`就正常了。

```yml
# Alert when the rate of events exceeds a threshold

# (Optional)
# Elasticsearch host
es_host: localhost

# (Optional)
# Elasticsearch port
es_port: 9200

# (OptionaL) Connect with SSL to Elasticsearch
#use_ssl: True

# (Optional) basic-auth username and password for Elasticsearch
#es_username: someusername
#es_password: somepassword

# (Required)
# Rule name, must be unique
name: Down frequency rule

# (Required)
# Type of alert.
# the frequency rule type alerts when num_events events occur with timeframe time
type: frequency

# (Required)
# Index to search, wildcard supported
index: heartbeat-*

# (Required, frequency specific)
# Alert when this many documents matching the query occur within a timeframe
num_events: 50

# (Required, frequency specific)
# num_events must occur within this amount of time to trigger an alert
timeframe:
  hours: 4

# (Required)
# A list of Elasticsearch filters used for find events
# These filters are joined with AND and nested in a filtered query
# For more info: http://www.elasticsearch.org/guide/en/elasticsearch/reference/current/query-dsl.html
filter:
- term:
    monitor.status: "down"

# (Required)
# The alert is use when a match is found
alert:
- "email"

# (required, email specific)
# a list of email addresses to send alerts to
email:
- "my.dummy@email.com"

from_addr: "rufeng.pan@email.com"
smtp_host: "dummy.smtp.host"
smtp_port: 25

alert_subject: "ELK Alert - {0} Down @ {1}"
alert_subject_args:
- monitor.name
- "@timestamp"

alert_text_type: alert_text_only
alert_text: |
  Dear Team, {} is down @ {}, please take action!
  ### Number hits: {}
  > Check time: {}
  > IP: {}
  > Env: {}
  > Status: {}
  >>> Error: {}

alert_text_args:
- monitor.name
- "@timestamp"
- num_hits
- "@timestamp"
- monitor.ip
- monitor.name
- monitor.status
- error.message
```

