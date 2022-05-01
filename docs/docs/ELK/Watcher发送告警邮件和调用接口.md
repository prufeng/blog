ELK - Watcher发送告警邮件和调用接口
===

相比[使用ElastAlert发送告警邮件](https://blog.csdn.net/prufeng/article/details/103933769)，ELK提供的Wathcer要简单得多，也可以在发生警报的时候调用Web Service接口。

# Configure SMTP

https://www.elastic.co/guide/en/elasticsearch/reference/current/actions-email.html

以上文档提供了多种Email系统的配置方法(elasticsearch.yml)，包括Gmail, Outlook, Microsoft Exchange, Amazon SES。

比如Gmail：

```yml
xpack.notification.email.account:
    gmail_account:
        profile: gmail
        smtp:
            auth: true
            starttls.enable: true
            host: smtp.gmail.com
            port: 587
            user: <username>
```
当然还要在`elasticsearch-keystore`里配置相应的`password`
```
bin/elasticsearch-keystore add xpack.notification.email.account.gmail_account.smtp.secure_password
```

实际上公司一般有内部SMTP，只需授权，而无需用户名和密码。
```yml
xpack.notification.email.account:
  work:
    profile: standard
    email_defaults:
      from: my@dummy.email
    smtp:
      auth: false
      starttls.enable: false
      host: my.dummy.smtp.host
      port: 25
```

# Create Watcher

## Create Threshold Alert

`Management` -> `Elasticsearch` -> `Watcher` -> `Create threshold alert`.

填入`Name`，`Indices`，`Time field`， 则会出现`Add action`按钮。

![](assets/ELK_Watcher_Threshold.PNG)

>Watcher supports the following types of actions: email, webhook, index, logging, slack, and pagerduty.

Threshold Alert的主要作用，是它提供了界面，可以简单测试下配置有没有起效果。

比如Email， 填入邮件地址和内容，点击`Send test email`。

如果SMTP配置没问题的话，应该可以成功收到邮件。

![](assets/ELK_Watcher_Email.PNG)


调用接口则选`Webhook`，一样可以直接`Send request`进行测试。

![](assets/ELK_Watcher_Webhook.PNG)

注意到7.3还不支持HTTPS，7.6以后才有此选项。
`Advance Watch`则没有这个问题。

## Create Advance Watch
以下是缺省的模板，30分钟执行一次，查询所有indices，因而一般都能执行。

把时间调小，很快就可以在`elasticsearch.log`里看到输出的`text`。

```json
{
  "trigger": {
    "schedule": {
      "interval": "30m"
    }
  },
  "input": {
    "search": {
      "request": {
        "body": {
          "size": 0,
          "query": {
            "match_all": {}
          }
        },
        "indices": [
          "*"
        ]
      }
    }
  },
  "condition": {
    "compare": {
      "ctx.payload.hits.total": {
        "gte": 10
      }
    }
  },
  "actions": {
    "my-logging-action": {
      "logging": {
        "text": "There are {{ctx.payload.hits.total}} documents in your index. Threshold is 10."
      }
    }
  }
}
```

# Email Action
发送告警邮件的配置一般长这样。

```json
  "actions": {
    "send_email": {
      "email": {
        "profile": "standard",
        "to": [
          "my.support@dummy.email"
        ],
        "subject": "ELK Alert - XXX is Down",
        "body": {
          "html": "{{ctx.payload.hits.total}} XXX is over limit, please take action.<p>Note: Automatic email from ELK, please do not reply."
        }
      }
    }
  }
```

# Webhook Action
告警时调用接口配置一般长这样。

可以同时支持多个Action。

```json
  "actions": {
    "my-logging-action": {
      "logging": {
        "level": "info",
        "text": "There are {{ctx.payload.hits.total}} documents in your index. Threshold is 10."
      }
    },
    "my-webhook-action": {
      "webhook": {
        "scheme": "https",
        "host": "my.api.dummy.host",
        "port": 8443,
        "method": "put",
        "path": "api/alert",
        "params": {},
        "headers": {
          "Content-type": "application/json"
        },
        "body": "{status: 1}"
      }
    }
  }
```
