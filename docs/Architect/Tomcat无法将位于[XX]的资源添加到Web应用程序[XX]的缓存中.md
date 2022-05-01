26-Jan-2022 09:52:13.920 警告 [main] org.apache.catalina.webresources.Cache.getResource 无法将位于[/WEB-INF/classes/***]的资源添加到Web应用程序[/helloworld]的缓存中，因为在清除过期缓存条目后可用空间仍不足 - 请考虑增加缓存的最大空间。

vi tomcat\conf\context.xml
```
<Resources cachingAllowed="true" cacheMaxSize="102400" />
```

# cacheMaxSize	
The maximum size of the static resource cache in kilobytes. If not specified, the default value is 10240 (10 megabytes). This value may be changed while the web application is running (e.g. via JMX). If the cache is using more memory than the new limit the cache will attempt to reduce in size over time to meet the new limit. If necessary, cacheObjectMaxSize will be reduced to ensure that it is no larger than cacheMaxSize/20.

# cacheObjectMaxSize	
Maximum size of the static resource that will be placed in the cache. If not specified, the default value is 512 (512 kilobytes). If this value is greater than cacheMaxSize/20 it will be reduced to cacheMaxSize/20. This value may be changed while the web application is running (e.g. via JMX).
