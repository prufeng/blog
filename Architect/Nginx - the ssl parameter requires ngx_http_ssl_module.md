nginx: [emerg] the "ssl" parameter requires ngx_http_ssl_module
===
Nginx加ssl_certificate配置后报这个错。

将相应模块安装回来即可。
```
$ sudo nginx -s reload
nginx: [emerg] the "ssl" parameter requires ngx_http_ssl_module in /usr/local/nginx/conf/nginx.conf:38
```

修改前

```
$ sudo nginx -V
nginx version: nginx/1.16.1
built by gcc 4.8.5 20150623 (Red Hat 4.8.5-36) (GCC)
configure arguments:
```

重新编译
```
sudo ./configure --with-http_stub_status_module --with-http_ssl_module
sudo make
```

Copy ./objs/nginx
```
sudo cp /usr/local/nginx/sbin/nginx /usr/local/nginx/sbin/nginx.bak
sudo ls -l /usr/local/nginx/sbin/
sudo cp ./objs/nginx /usr/local/nginx/sbin/
```

重启
```
ps -aux|grep ngi
sudo kill -9 <PID>
/usr/local/nginx/sbin/nginx
```

安装成功
```
$ sudo nginx -V
nginx version: nginx/1.16.1
built by gcc 4.8.5 20150623 (Red Hat 4.8.5-36) (GCC)
built with OpenSSL 1.0.2k-fips  26 Jan 2017
TLS SNI support enabled
configure arguments: --with-http_stub_status_module --with-http_ssl_module
```

