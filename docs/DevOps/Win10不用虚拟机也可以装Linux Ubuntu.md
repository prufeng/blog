Win10不用虚拟机也可以装Linux（Ubuntu）
===
想在Windows下玩Linux，下了个虚拟机。

突然想起Win10好像有虚拟机，找一下，果然！

可是，这个`适用于Linux的Windows子系统`，是什么鬼？

难道是自带Linux？

果断试一下，选择，需要重启。

打开Microsoft Store，搜索Ubuntu。

看到有Ubuntu 20和Ubuntu 18，20提示不兼容，那就安装18好了。

应该是系统版本号的限制，不行可能要升级自身系统。

安装完成之后，直接打开，是一个命令行窗口，像模像样。

需要设置用户名和密码，但是不能是root。

没有默认的root用户，su不过去。

需要先这样设置root用户密码。
```
$ sudo passwd
Enter new UNIX password:
Retype new UNIX password:
passwd: password updated successfully
```
设置完后root就出来了。

Win10磁盘在`/mnt/c/`。
```
$ ll /mnt/
total 0
drwxr-xr-x 1 root root 4096 Dec  9 19:52 ./
drwxr-xr-x 1 root root 4096 Dec  9 19:52 ../
drwxrwxrwx 1 feng feng 4096 Dec 10 22:57 c/
```
另外试了一下，是可以联网的。

```
# curl baidu.com
<html>
<meta http-equiv="refresh" content="0;url=http://www.baidu.com/">
</html>
```

貌似没有什么bug，明天装点软件试试。