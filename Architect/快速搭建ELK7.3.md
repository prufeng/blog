快速搭建ELK7.3
===
A quick start guild of ELK 7.3.2, including package installation and simple test.

好吧，其实是发现之前的[快速搭建ELK7.2](https://blog.csdn.net/prufeng/article/details/95733467)有些坑，决定还是再来一次。

安装版相比直接解压版还是有些好处的，最起码安装完就是Service，省却打命令行的许多麻烦。
# Download and install
* elasticsearch-7.3.2-x86_64.rpm
* kibana-7.3.2-x86_64.rpm
* logstash-7.3.2.rpm
* filebeat-7.3.2-x86_64.rpm
* heartbeat-7.3.2-x86_64.rpm

https://www.elastic.co/guide/en/elastic-stack-get-started/current/get-started-elastic-stack.html

# Elasticsearch

## Install
```sh
$ sudo rpm -ivh elasticsearch-7.3.2-x86_64.rpm
warning: elasticsearch-7.3.2-x86_64.rpm: Header V4 RSA/SHA512 Signature, key ID d88e42b4: NOKEY
Preparing...                          ################################# [100%]
Creating elasticsearch group... OK
Creating elasticsearch user... OK
Updating / installing...
   1:elasticsearch-0:7.3.2-1          ################################# [100%]
### NOT starting on installation, please execute the following statements to configure elasticsearch service to start automatically using systemd
 sudo systemctl daemon-reload
 sudo systemctl enable elasticsearch.service
### You can start elasticsearch service by executing
 sudo systemctl start elasticsearch.service
Created elasticsearch keystore in /etc/elasticsearch
```
## Startup
```sh
sudo systemctl daemon-reload
sudo systemctl enable elasticsearch.service

sudo systemctl status elasticsearch.service
sudo systemctl start elasticsearch.service
### Check process
# ps -ef|grep ela
### Check installed files location
# sudo rpm -ql elasticsearch
```
## Test
```sh
$ curl localhost:9200
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

# Startup Commands
All other installations are similar, you can find the services list as below.
```
sudo systemctl start elasticsearch.service
sudo systemctl start kibana.service
sudo systemctl start logstash.service
sudo systemctl start filebeat.service
sudo systemctl start heartbeat-elastic.service
```
# Remote Access to Elasticsearch
```
sudo vi /etc/elasticsearch/elasticsearch.yml
```
```yml
#network.host: 192.168.0.1
network.host: 0.0.0.0

cluster.initial_master_nodes: node-1
```
The last configure change is for bootstrap error below.
```
sudo tail  /var/log/elasticsearch/elasticsearch.log
```
```
[2019-10-10T10:06:24,340][ERROR][o.e.b.Bootstrap          ] [appserver01] node validation exception
[1] bootstrap checks failed
[1]: the default discovery settings are unsuitable for production use; at least one of [discovery.seed_hosts, discovery.seed_providers, cluster.initial_master_nodes] must be configured
```
没有遇到[7.2解压版](https://blog.csdn.net/prufeng/article/details/95733467)里的`vm.max_map_count is too low`的问题。

粗略看一下，它是放到启动的script里了。
```
sudo view /etc/init.d/elasticsearch

MAX_OPEN_FILES=65535
MAX_MAP_COUNT=262144

sysctl -q -w vm.max_map_count=$MAX_MAP_COUNT
```

# Remote Access to Kibana
```sh
# curl localhost:5601
# curl localhost:5601/app/kibana
sudo vi /etc/kibana/kibana.yml
```
```yml
#server.host: "localhost"
server.host: "0.0.0.0"
```
```
sudo systemctl restart kibana.service
```
Now Kibana can be accessed from another host browser
http://192.168.1.88:5601/


# 安装路径问题
开始也尝试装到指定目录，但发现装完后Service里的路径并没有改过来，说明还需要些手动工作，还是不折腾了。
```
$ sudo rpm -ivh --prefix=/opt/elk elasticsearch-7.3.2-x86_64.rpm
warning: elasticsearch-7.3.2-x86_64.rpm: Header V4 RSA/SHA512 Signature, key ID d88e42b4: NOKEY
Preparing...                          ################################# [100%]
Creating elasticsearch group... OK
Creating elasticsearch user... OK
Updating / installing...
   1:elasticsearch-0:7.3.2-1          ################################# [100%]
### NOT starting on installation, please execute the following statements to configure elasticsearch service to start automatically using systemd
 sudo systemctl daemon-reload
 sudo systemctl enable elasticsearch.service
### You can start elasticsearch service by executing
 sudo systemctl start elasticsearch.service
/var/tmp/rpm-tmp.JyvHeM: line 8: /usr/share/elasticsearch/bin/elasticsearch-keystore: No such file or directory
chown: cannot access ‘/etc/elasticsearch/elasticsearch.keystore’: No such file or directory
chmod: cannot access ‘/etc/elasticsearch/elasticsearch.keystore’: No such file or directory
md5sum: /etc/elasticsearch/elasticsearch.keystore: No such file or directory
warning: %posttrans(elasticsearch-0:7.3.2-1.x86_64) scriptlet failed, exit status 1

```

# 重新安装问题
因为机器里原本有旧版本的ELK，重新安装Elasticsearch后发现启动不了。

网上说已经有一个在运行，但我这里并没有发现。

最后再一次重装解决了，重装之前把相关路径下的所有文件都删了一遍。

## failed to obtain node locks
Failed to startup Elasticsearch with below error.
```
[2019-09-23T16:41:39,751][ERROR][o.e.b.Bootstrap          ] [appserver01] Exception
java.lang.IllegalStateException: failed to obtain node locks, tried [[/var/lib/elasticsearch]] with lock id [0]; maybe these locations are not writable or multiple nodes were started without increasing [node.max_local_storage_nodes] (was [1])?

```
Not work even after nodes configure is updated as below.
```
node.max_local_storage_nodes: 2
```

The issue was solved after removing all related folders, and we also added CPU and memory (reboot) during the period.

Maybe the files were not cleaned up in the related folders when uninstalled old version.
```
$ sudo rpm -ql elasticsearch>elasticsearch_pkg.log
$ sudo rpm -ev elasticsearch
Preparing packages...
Stopping elasticsearch service... OK
elasticsearch-0:5.4.0-1.noarch
Deleting log directory... OK
$ sudo rpm -ql elasticsearch
package elasticsearch is not installed
```
```
find / -iname "elasticsearch"
```
Remove all old version files found.
```
sudo rm -rf /usr/share/elasticsearch
sudo rm -rf /etc/elasticsearch
sudo rm -rf /var/log/elasticsearch
sudo rm -rf /var/lib/elasticsearch
```
