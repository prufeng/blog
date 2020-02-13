HTTPS证书准备过程
===

使用`keytool`和`openssl`生成HTTPS证书的过程总结。

# 1. Generate Keystore
```sh
keytool -genkey -alias appssl -keyalg RSA -keysize 2048 -validity 731 -keystore appssl.keystore -keypass password -storepass password -dname "CN=appserver01.dummy.com, OU=MyOrg China, O=MyOrg, L=Guangzhou, ST=Guangdong, C=CN" -ext "SAN=dns:appserver01.dummy.com,dns:appserver02.dummy.com,dns:appserver03.dummy.com,dns:appserver04.dummy.com,dns:appserver05.dummy.com,dns:appserver06.dummy.com"  
```

# 2. Generate Sign Request File
```sh
keytool -certreq -keyalg RSA -alias appssl -file appssl.csr -keystore appssl.keystore -keypass password -storepass password -ext "SAN=dns:appserver01.dummy.com,dns:appserver02.dummy.com,dns:appserver03.dummy.com,dns:appserver04.dummy.com,dns:appserver05.dummy.com,dns:appserver06.dummy.com"
```

# 3. Send Sign Request to Certificate Management Group

发给CA机构（Certificate Authority），拿回认证后的`root cert`， `chain cert`和`server cert`。


# 4. Import Root Cert, Chain Cert and Server Cert.

```sh
keytool -list -keystore appssl.keystore -storepass password

keytool -import -alias rootcertificate -keystore appssl.keystore -trustcacerts -file Root.crt -storepass password

keytool -import -alias Intermediate -keystore appssl.keystore -trustcacerts -file Intermediate.crt -storepass password

keytool -import -alias appssl -keystore appssl.keystore -trustcacerts -file ServerCertificate.crt -storepass password
```

# 5. Extract Cert and Key from JKS Keystore

```sh
keytool -importkeystore -srckeystore appssl.keystore -srcalias appssl -destkeystore appssl.jks.p12 -deststoretype PKCS12 -storepass password

keytool -deststoretype PKCS12 -keystore appssl.jks.p12 -list -storepass password

openssl pkcs12 -in appssl.jks.p12 -nokeys -clcerts -out server_ssl.crt
openssl pkcs12 -in appssl.jks.p12 -nokeys -cacerts -out gs_intermediate_ca.crt
cat server_ssl.crt gs_intermediate_ca.crt >server.crt

openssl pkcs12 -nocerts -nodes -in appssl.jks.p12 -out server.key
```

# 6. Setup App with Cert and Key

e.g. for Kibana

```sh
sudo vi /etc/kibana/kibana.yml
```
```yml
server.ssl.enabled: true

server.ssl.certificate: /etc/kibana/server.crt
server.ssl.key: /etc/kibana/server.key
```

# 相关文章

[Nginx - 使用OpenSSL自签名证书配置HTTPS](https://blog.csdn.net/prufeng/article/details/102291147)