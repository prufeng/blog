Nginx - cannot load certificate SSL: error:0200100D:system library:fopen:Permission denied:fopen
===

换了SSL Cert之后，Nginx无法启动，发生如下错误。

```sh
nginx: [emerg] cannot load certificate "/etc/nginx/ssl/test.crt": BIO_new_file() failed (SSL: error:0200100D:system library:fopen:Permission denied:fopen('/etc/nginx/ssl/test.crt','r') error:2006D002:BIO routines:BIO_new_file:system lib)
```

* 确认使用 `sudo` 运行。
* 确认该文件可以 `cat` 打开。
* 确认文件权限与原Cert一致。
* `nginx -t` successful.


查了一下，原来是 SELinux 的问题。

`SELinux`，即 Security Enhanced Linux，是一种基于委任式存取控制 （Mandatory Access Control, MAC）的权限控制系统，比通常所理解的用户自主式存取控制 （Discretionary Access Control, DAC）更严格。

DAC 主要根据程序的拥有者和文件的rwx权限来决定用户可以进行的操作，但 root 可以控制一切，777文件可以被任何人操作。

MAC 可以通过规则限定特定的程序只能操作指定的文件，这样就算是 root 运行的程序，也不能随意访问其他不相关的文件了。

`SELinux` 默认使用 `targeted`模式。

```sh
getenforce

sestatus -v
```
检查 Audit log 可以发现，文件不能访问的原因，是程序与目标文件的 `scontext`(Security Context) 不一致。

Nginx 使用的是`httpd_t`，自己copy的文件使用的是`user_home_t`。

导致这个问题的操作是，先在 `home` 下创建了文件，然后再 `mv` 到当前目录，而 `scontext` 不会因复制移动而修改。

```sh
$ sudo ausearch -m avc -ts today

time->Thu Apr  9 12:00:42 2020
type=PROCTITLE msg=audit(1586404842.411:635786): proctitle=2F7573722F7362696E2F6E67696E78002D63002F6574632F6E67696E782F6E67696E782E636F6E66
type=SYSCALL msg=audit(1586404842.411:635786): arch=c000003e syscall=2 success=no exit=-13 a0=55ba2565c54d a1=0 a2=1b6 a3=24 items=0 ppid=1 pid=65228 auid=4294967295 uid=0 gid=0 euid=0 suid=0 fsuid=0 egid=0 sgid=0 fsgid=0 tty=(none) ses=4294967295 comm="nginx" exe="/usr/sbin/nginx" subj=system_u:system_r:httpd_t:s0 key=(null)
type=AVC msg=audit(1586404842.411:635786): avc:  denied  { read } for  pid=65228 comm="nginx" name="test.crt" dev="dm-0" ino=136402657 scontext=system_u:system_r:httpd_t:s0 tcontext=unconfined_u:object_r:user_home_t:s0 tclass=file permissive=0
```

查看测试 Cert 与原来版本的区别。

```sh
$ sudo ls -lrtZ /etc/nginx/ssl
-rw-r--r--. root root system_u:object_r:httpd_config_t:s0 origin.crt
-rw-r--r--. root root system_u:object_r:httpd_config_t:s0 origin.key
-rw-r--r--. root root unconfined_u:object_r:user_home_t:s0 test.crt
-rw-r--r--. root root unconfined_u:object_r:user_home_t:s0 test.key
```

使用 `restorecon` 让文件恢复正确的 SELinux type。

```sh
$ sudo restorecon -v -R /etc/nginx/ssl/test.*
restorecon reset /etc/nginx/ssl/test.crt context unconfined_u:object_r:user_home_t:s0->unconfined_u:object_r:httpd_config_t:s0
restorecon reset /etc/nginx/ssl/test.key context unconfined_u:object_r:user_home_t:s0->unconfined_u:object_r:httpd_config_t:s0
$ sudo ls -lrtZ /etc/nginx/ssl
-rw-r--r--. root root system_u:object_r:httpd_config_t:s0 origin.crt
-rw-r--r--. root root system_u:object_r:httpd_config_t:s0 origin.key
-rw-r--r--. root root unconfined_u:object_r:httpd_config_t:s0 test.crt
-rw-r--r--. root root unconfined_u:object_r:httpd_config_t:s0 test.key

```

可以使用 `semanage` 查询和修改默认的目录安全性本文。此即`restorecon` 恢复的所谓正确 SELinux type 的来源。

```sh
$ sudo semanage fcontext -l|grep etc/nginx
/etc/nginx(/.*)?                                   all files          system_u:object_r:httpd_config_t:s0
```

重启 Nginx ， 成功！
