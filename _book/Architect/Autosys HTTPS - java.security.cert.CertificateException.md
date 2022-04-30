Autosys HTTPS - java.security.cert.CertificateException: subject/issuer verification failed
===
使用 Autosys HTTP Job 去监控服务是否正常的时候，遇到 Certificate 验证错误。

`java.security.cert.CertificateException: subject/issuer verification failed`

最后发现原因竟然是 Nginx 所使用的证书文件里有重复的元素，删掉重复的 Cert 即可。

那么，为什么 HTTP SSL 证书里会出现重复的元素？ SSL 证书里到底有些什么？

可以参考这一篇：[SSL 证书 PEM 文件里有什么和要有什么](https://github.com/prufeng/blog/blob/master/Architect/SSL%E8%AF%81%E4%B9%A6PEM%E6%96%87%E4%BB%B6%E9%87%8C%E6%9C%89%E4%BB%80%E4%B9%88%E5%92%8C%E8%A6%81%E6%9C%89%E4%BB%80%E4%B9%88.md)
