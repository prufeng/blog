Nginx - Basic Authentication
===
使用Nginx Basic Authentication为Kibana增加登录验证功能。

# Install Nginx
Download package from https://nginx.org/download/nginx-1.16.1.tar.gz
```
tar zxvf nginx-1.16.1.tar.gz
cd nginx-1.16.1/

sudo ./configure --with-http_stub_status_module --with-http_ssl_module
sudo make
sudo make install
```

Install dependencies if need. (e.g. pcre pcre-devel, zlib zlib-develo, penssl, openssl-devel)
```
Configuration summary
  + using system PCRE library
  + OpenSSL library is not used
  + using system zlib library
```

Install done.
```
$ sudo nginx -V
nginx version: nginx/1.16.1
built by gcc 4.8.5 20150623 (Red Hat 4.8.5-36) (GCC)
built with OpenSSL 1.0.2k-fips  26 Jan 2017
TLS SNI support enabled
configure arguments: --with-http_stub_status_module --with-http_ssl_module
```

# Startup Nginx
```
ln -s /usr/local/nginx/sbin/nginx /usr/bin/nginx
sudo nginx

$ ps aux|grep nginx
root     14112  0.0  0.0  20556   612 ?        Ss   10:24   0:00 nginx: master process /usr/local/nginx/sbin/ngin
nobody   14113  0.0  0.0  23092  1388 ?        S    10:24   0:00 nginx: worker process
admin    14127  0.0  0.0 112716   976 pts/2    S+   10:24   0:00 grep --color=auto nginx
$ curl localhost
<html>
<head><title>403 Forbidden</title></head>
<body>
<center><h1>403 Forbidden</h1></center>
<hr><center>nginx/1.16.1</center>
</body>
</html>
```

# Install httpd-tools
To generate the `auth_basic_user_file`.

```
yum install httpd-tools

sudo htpasswd -b /usr/local/nginx/conf/passwd <username> <password>
```
The password file looks as below.
```
$ cat test.pwd
test:$apr1$y0scTAxi$EHurcBgQzTak3nwFAHfyC/
test1:$apr1$4ddNEKao$jqKyZAnqvjYKlceeBQiQN.

```

# Reload Nginx Configure
```
sudo vi /usr/local/nginx/conf/nginx.conf
sudo nginx -s reload
```
1. Change nobody to root for test (or grant right to nobody on passwd)

2. Add auth_basic configure

```conf
#user  nobody;
user   root;


    server {
        listen       80;
        server_name  192.168.1.88;

        auth_basic "Basic Auth";
        auth_basic_user_file /usr/local/nginx/conf/passwd;

        #charset koi8-r;

        #access_log  logs/host.access.log  main;

        location / {
            proxy_pass http://localhost:5601;
            proxy_http_version 1.1;
            proxy_set_header Upgrade $http_upgrade;
            proxy_set_header Connection 'upgrade';
            proxy_set_header Host $host;
            proxy_cache_bypass $http_upgrade;
            #root   html;
            #index  index.html index.htm;
        }
```

# Change Kibana Configure
```
sudo vi config/kibana.yml
```
Change from `0.0.0.0` to `localhost`.

```yml
#server.host: "0.0.0.0"
server.host: "localhost"
```
修改后重启。

想保留原来5601端口的链接不禁用，这里可以用具体IP，相应的`proxy_pass`也要改。

# Verification
需要登录才能进入Kibana。

http://192.168.1.88

![](assets/ELK_K_Auth.PNG)

# Reference

http://nginx.org/en/docs/http/ngx_http_auth_basic_module.html
https://httpd.apache.org/docs/2.4/programs/htpasswd.html
