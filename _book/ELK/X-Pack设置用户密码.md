
ELK - X-Pack设置用户密码
===
之前记录过[怎样使用Nginx代理为Kibana添加登录验证功能](https://blog.csdn.net/prufeng/article/details/102528147)，但其实Elastic本身也提供了基本的访问控制功能。   
虽然相关功能在X-Pack里，但还是可以免费使用的。   
参考[官网subscriptions](https://www.elastic.co/subscriptions)，可以看到在`Basic License`下的`Security`项目中包含了`Role-based access control`。

# Enable X-Pack Security
Elasticsearch设置密码命令如下。
```
$ sudo /usr/share/elasticsearch/bin/elasticsearch-setup-passwords interactive

Unexpected response code [500] from calling GET http://192.168.1.88:9200/_security/_authenticate?pretty
It doesn't look like the X-Pack security feature is enabled on this Elasticsearch node.
Please check if you have enabled X-Pack security in your elasticsearch.yml configuration file.

ERROR: X-Pack Security is disabled by configuration.
```
设置前，需要先enable X-Pack security。
```sh
sudo vi /etc/elasticsearch/elasticsearch.yml
```
```yml
xpack.security.enabled: true
xpack.security.transport.ssl.enabled: true
```
SSL也要同时enable，否则报错。
```
[2019-10-10T15:11:09,630][ERROR][o.e.b.Bootstrap          ] [appserver01] node validation exception
[1] bootstrap checks failed
[1]: Transport SSL must be enabled if security is enabled on a [basic] license. Please set [xpack.security.transport.ssl.enabled] to [true] or disable security by setting [xpack.security.enabled] to [false]

```
现在可以开始设置密码。   
可以看到Elasticsearch预置了许多角色和用户。
```
$ sudo /usr/share/elasticsearch/bin/elasticsearch-setup-passwords interactive
Initiating the setup of passwords for reserved users elastic,apm_system,kibana,logstash_system,beats_system,remote_monitoring_user.
You will be prompted to enter passwords as the process progresses.
Please confirm that you would like to continue [y/N]y


Enter password for [elastic]:
Reenter password for [elastic]:
Enter password for [apm_system]:
Reenter password for [apm_system]:
Enter password for [kibana]:
Reenter password for [kibana]:
Enter password for [logstash_system]:
Reenter password for [logstash_system]:
Enter password for [beats_system]:
Reenter password for [beats_system]:
Enter password for [remote_monitoring_user]:
Reenter password for [remote_monitoring_user]:
Changed password for user [apm_system]
Changed password for user [kibana]
Changed password for user [logstash_system]
Changed password for user [beats_system]
Changed password for user [remote_monitoring_user]
Changed password for user [elastic]

```
重启
```
sudo systemctl restart elasticsearch.service
```
需要加密码才能访问。
```sh
$ curl localhost:9200
{"error":{"root_cause":[{"type":"security_exception","reason":"missing authentication credentials for REST request [/]","header":{"WWW-Authenticate":"Basic realm=\"security\" charset=\"UTF-8\""}}],"type":"security_exception","reason":"missing authentication credentials for REST request [/]","header":{"WWW-Authenticate":"Basic realm=\"security\" charset=\"UTF-8\""}},"status":401}(base) 

$ curl localhost:9200 -uelastic:<password>
{
  "name" : "appserver01",
  "cluster_name" : "elasticsearch",
  "cluster_uuid" : "wCDlDy6UTriUSuZuDrqWrw",
  "version" : {
    "number" : "7.3.2",
    "build_flavor" : "default",
    "build_type" : "rpm",
    "build_hash" : "1c1faf1",
    "build_date" : "2019-09-06T14:40:30.409026Z",
    "build_snapshot" : false,
    "lucene_version" : "8.1.0",
    "minimum_wire_compatibility_version" : "6.8.0",
    "minimum_index_compatibility_version" : "6.0.0-beta1"
  },
  "tagline" : "You Know, for Search"
}
```

# Update Kibana Configure
After password setup in Elasticsearch, have to update configure for Kibana, Logstash and Beats.
e.g. Kibana
```
sudo vi /etc/kibana/kibana.yml
# sudo vi /etc/heartbeat/heartbeat.yml
```
```yml
elasticsearch.username: "elastic"
elasticsearch.password: "<password>"
```
```
sudo systemctl restart kibana.service
```

After restart, refresh Kibana and you will be asked for username and password now.
![](assets/ELK_K_Login.PNG)

To change the password, can go to Kibana Management -> Security -> Users.

![](assets/ELK_K_Pwd.PNG)

Or change data in Elasticsearch directly.
```
POST /_security/user/elastic/_password
{
  "password": "123456"
}
```
