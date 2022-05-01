SSL证书PEM文件里有什么和要有什么
===

Privacy-Enhanced Mail (PEM) 本来是研究来给邮件加密的，现在主要成为一种约定俗成的文件格式，用于存储和发送加密密钥，证书或其他数据。

简单理解就是格式如下这种文件。

```
-----BEGIN XXX-----
BASE64
-----END XXX-----
```

# JKS Keystore 转化为 PEM 的过程

在[HTTPS SSL证书准备过程](https://blog.csdn.net/prufeng/article/details/104297731)里介绍过，我们生成了证书请求发给 CA 后，会收到一个 JKS Keystore 。

JKS Keystore　转化为 PEM 文件过程如下。

``` 
keytool -importkeystore -srckeystore appssl.jks -destkeystore appssl.jks.p12 -deststoretype pkcs12

keytool -deststoretype PKCS12 -keystore appssl.jks.p12 -list -storepass password

openssl pkcs12 -in appssl.jks.p12 -nokeys -clcerts -out client.crt
openssl pkcs12 -in appssl.jks.p12 -nokeys -cacerts -out ca.crt
cat client.crt ca.crt >server.crt

openssl pkcs12 -nocerts -nodes -in appssl.jks.p12 -out server.key
```
`nokeys` 表示不包含 Private Key， `clcerts` 输出 Client Cert，`cacerts` 输出 Root Cert 和 Intermediate Cert。

`-nocerts -nodes` 即不包含 Cert 和不加密。

实际上`clcerts`和`cacerts`两个文件合起来和下面这句输出一致。
```
openssl pkcs12 -in appssl.jks.p12 -nokeys -out server.crt
```

使用`keytool`也可以直接从jks导出PEM，不过需要按alias逐个导出。
```
keytool -list -exportcert -keystore appssl.jks  -alias 'appssl' -file server.crt -rfc
```

使用 `openssl`导出的时候，还会添加如下Attributes。
```
Bag Attributes
    friendlyName: app
    localKeyID: 54 69 6D 65 20 41 45 48 49 45 44 42 44 40 42 49 41 47 
subject=...app.dummy.com
issuer=...Entrust Certification Authority - L1M
```

而且 Root Cert 和 Intermediate Cert 会出现重复，因为它们在 JKS Keystore 里本来就是重复的。


# JKS Keystore 里有什么

查看 JKS Keystore ， 可以发现里面包含3个实体，一个 PrivateKeyEntry 和两个 trustedCertEntry。

但 PrivateKeyEntry 里 `Certificate chain length: 3`， 即包含了另外两个 Cert，于是使用 Openssl转化以后 Root Cert 和 Intermediate Cert 就出现了重复。

```
$ keytool -list -keystore appssl.jks -rfc

Keystore type: jks
Keystore provider: SUN

Your keystore contains 3 entries

Alias name: appssl
Creation date: Apr 18, 2020
Entry type: PrivateKeyEntry
Certificate chain length: 3
Certificate[1]:
-----BEGIN CERTIFICATE-----
BASE64
-----END CERTIFICATE-----
Certificate[2]:
-----BEGIN CERTIFICATE-----BASE64
-----END CERTIFICATE-----
Certificate[3]:
-----BEGIN CERTIFICATE-----BASE64
-----END CERTIFICATE-----


*******************************************
*******************************************


Alias name: cn=entrust certification authority - intermediate
Creation date: Apr 18, 2020
Entry type: trustedCertEntry

-----BEGIN CERTIFICATE-----
BASE64
-----END CERTIFICATE-----


*******************************************
*******************************************


Alias name: cn=entrust root certification authority
Creation date: Apr 18, 2020
Entry type: trustedCertEntry

-----BEGIN CERTIFICATE-----
BASE64
-----END CERTIFICATE-----


*******************************************
*******************************************
```

# SSL 证书 PEM 文件里要有什么

特地做了下试验。

使用 Openssl 导出的 PEM 当然是可以了，里面包含了5个 PEM 。

删掉重复的 Root Cert 和 Intermediate Cert 之后，表现也正常。

最后，只留下 Client Cert，浏览器里表现正常，应用程序里测试会出错。

```
javax.net.ssl.SSLHandshakeException: PKIX path building failed: sun.security.provider.certpath.SunCertPathBuilderException: unable to find valid certification path to requested target
```

我的简单理解是，浏览器可以联网查找认证链，应用程序不行。

# 相关规范
https://tools.ietf.org/html/rfc1421   
https://tools.ietf.org/html/rfc7292   
https://tools.ietf.org/html/rfc7468
