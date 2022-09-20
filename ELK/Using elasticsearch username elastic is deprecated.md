
新建一个elastic/kibana token: mytoken
```
POST /_security/service/elastic/kibana/credential/token/mytoken
```
运行以上命令之后，记得把token记录下来，否则根本就找不回来（`GET /_security/service`），至少7.17如此。

试一下用token登陆。
```
curl -H "Authorization: Bearer <token>" http://localhost:9200/_security/_authenticate
```

测试没问题之后把Kibana里的ES用户名密码替换为serviceAccountToken重启就好。
```
vi /etc/kibana/kibana.yml
#elasticsearch.username: "elastic"
#elasticsearch.password: "******"
elasticsearch.serviceAccountToken: "<token>"

systemctl restart kibana
```

记录一下，主要还是因为踩了坑。

不要用`elasticsearch-service-tokens CLI tool`！
