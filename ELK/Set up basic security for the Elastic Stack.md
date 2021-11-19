Set up basic security for the Elastic Stack
====

1. Genrate CA: elastic-stack-ca.p12

cd /usr/share/elasticsearch
./bin/elasticsearch-certutil ca

Input password

2. Generate Cert: elastic-certificates.p12

./bin/elasticsearch-certutil cert --ca elastic-stack-ca.p12

Input password

Complete the following steps for each node in your cluster.

3. cp elastic-certificates.p12 /etc/elasticsearch/

chmod 644 elastic-certificates.p12

4. vi /etc/elasticsearch/elasticsearch.yml

//#cluster.name: my-cluster
//#node.name: node-1

xpack.security.transport.ssl.enabled: true
xpack.security.transport.ssl.verification_mode: certificate 
xpack.security.transport.ssl.client_authentication: required
xpack.security.transport.ssl.keystore.path: elastic-certificates.p12
xpack.security.transport.ssl.truststore.path: elastic-certificates.p12

5. Store the password in the Elasticsearch keystore

./bin/elasticsearch-keystore add xpack.security.transport.ssl.keystore.secure_password
./bin/elasticsearch-keystore add xpack.security.transport.ssl.truststore.secure_password

6. Restart elasticsearch


