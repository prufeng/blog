Nginx - LPAD Authentication
===

# Install http_auth_request_module
```
sudo ./configure --with-http_stub_status_module --with-http_ssl_module --with-http_auth_request_module
sudo make
sudo make install

$ sudo nginx -V
nginx version: nginx/1.16.1
built by gcc 4.8.5 20150623 (Red Hat 4.8.5-36) (GCC)
built with OpenSSL 1.0.2k-fips  26 Jan 2017
TLS SNI support enabled
configure arguments: --with-http_stub_status_module --with-http_ssl_module --with-http_auth_request_module
```
# Install python-ldap
I download and install offline.
```
# sudo yum install python-ldap
sudo rpm -hvi python-ldap-2.4.15-2.el7.x86_64.rpm

# sudo yum install openldap-devel
# cyrus-sasl-devel is dependency package
sudo rpm -hvi cyrus-sasl-devel-2.1.26-23.el7.x86_64.rpm
sudo rpm -hvi openldap-devel-2.4.44-21.el7_6.x86_64.rpm

```

# Nginx Configure
Download package from https://github.com/nginxinc/nginx-ldap-auth

Use sample configure.
```
cp /usr/local/nginx/conf/nginx.conf /usr/local/nginx/conf/nginx.conf_bak
cp nginx-ldap-auth.conf /usr/local/nginx/conf/nginx.conf
sudo nginx -t
sudo nginx -s reload
```
The listen port is 8081 in the sample configure.
We need to change/open the port and use correct LDAP configure for test.

# Startup LDAP Daemon
Run python below to start the daemon and sample app.

* nginx-ldap-auth-daemon.py
* backend-sample-app.py

Can use the following bash to start the daemon.
```
nginx-ldap-auth-daemon-ctl-rh.sh start
nginx-ldap-auth-daemon-ctl-rh.sh stop
```