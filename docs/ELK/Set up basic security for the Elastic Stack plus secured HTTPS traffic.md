
Set up basic security for the Elastic Stack plus secured HTTPS traffic
====
Test version: 7.15

# 1. Generate HTTP cert with the same CA for transport SSL
```
cd /usr/share/elasticsearch
./bin/elasticsearch-certutil http
```
```
Generate a CSR? [y/N]n
Use an existing CA? [y/N]y
CA Path: /usr/share/elasticsearch/elastic-stack-ca.p12
For how long should your certificate be valid? [5y]
Generate a certificate per node? [y/N]y
node #1 name: appserver01

hostnames:
appserver01

IPs:
192.168.0.111
```
# 2. unzip elasticsearch-ssl-http.zip -d ssl
```
cp ssl/elasticsearch/appserver01/http.p12 /etc/elasticsearch/
chmod 644 /etc/elasticsearch/http.p12
```
# 3. vi /etc/elasticsearch/elasticsearch.yml
```
xpack.security.http.ssl.enabled: true
xpack.security.http.ssl.keystore.path: http.p12
```
# 4. Store the password in the Elasticsearch keystore
```
./bin/elasticsearch-keystore add xpack.security.http.ssl.keystore.secure_password
```
# 5. systemctl restart elasticsearch.service
# 6. Encrypt traffic between Kibana and Elasticsearch 
```
cp ssl/kibana/elasticsearch-ca.pem /etc/kibana/

vi /etc/kibana/kibana.yml
```
```
elasticsearch.hosts: ["https://appserver01:9200"]
elasticsearch.ssl.certificateAuthorities: /etc/kibana/elasticsearch-ca.pem
```
```
systemctl restart kibana
```
# 7. Beats to Elasticsearch 
e.g. Heartbeat
```
cp ssl/kibana/elasticsearch-ca.pem /etc/heartbeat/

vi /etc/heartbeat/heartbeat.yml

output.elasticsearch:
  # Array of hosts to connect to.
  hosts: ["https://appserver01:9200"]
  ssl.certificate_authorities: ["/etc/heartbeat/elasticsearch-ca.pem"]

systemctl restart heartbeat-elastic.service
```
# 8. Logstash to Elasticsearch
```
cp ssl/kibana/elasticsearch-ca.pem /etc/logstash/
chmod 644 /etc/logstash/elasticsearch-ca.pem

vi /etc/logstash/conf.d/app01.conf
```
```
output {
  elasticsearch {
    hosts => ["https://appserver01:9200"]
    ssl => true
    ssl_certificate_verification => true
    cacert => ["/etc/logstash/elasticsearch-ca.pem"]
    index => "%{[@metadata][beat]}-%{+YYYY.MM.dd}"
    user => "elastic"
    password => "${ES_PWD}"
  }
}
```
