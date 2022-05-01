VMWare虚拟机CentOS联网：主机能SSH连虚拟机，虚拟机能上网
====
这两天玩一下VMWare，配置虚拟机网络的时候，发现网上很多误导，还是稍微记录一下，以免反复被带坑里。

搜了几个方法，不是ping不进去就是ping出来，又或者上不了网。正确的方法却非常简单。

VMWare版本：`12.5.9 build-7535481`

CentOS版本：
```
# cat /etc/redhat-release
CentOS Linux release 7.8.2003 (Core)
```
# 选择桥接模式
选择桥接模式，看到自定义那里有得选，所以我就直接选了，效果应该是一样的。

主机上其他网络设置，都不需要改！

# 物理机网络配置
供虚拟机参考。
```
>ipconfig

以太网适配器 本地连接:
   IPv4 地址 . . . . . . . . . . . . : 192.168.31.95
   子网掩码  . . . . . . . . . . . . : 255.255.255.0
   默认网关. . . . . . . . . . . . . : 192.168.31.1
```
# 虚拟机网络配置
虚拟机IP地址要与物理机在同一网段。
```
# vi /etc/sysconfig/network-scripts/ifcfg-ens33
```
```
ONBOOT=yes
BOOTPROTO=static
IPADDR=192.168.31.191
NETMASK=255.255.255.0
GATEWAY=192.168.31.1
DNS1=192.168.31.1
ZONE=public
```

```
systemctl restart network
```

# CentOS SSH配置
CentOS 7.8 sshd默认是开的，所以不用管。
```
# yum install net-tools
# netstat -anpt|grep sshd
tcp        0      0 0.0.0.0:22              0.0.0.0:*               LISTEN      866/sshd
tcp        0     28 192.168.31.191:22       192.168.31.95:49909     ESTABLISHED 3893/sshd: root@pts
tcp        0      0 192.168.31.191:22       192.168.31.95:52616     ESTABLISHED 3813/sshd: admin [p
```
Firewall默认也是开的。可以先关掉试试。
如果可以，把端口打开。
```
systemctl stop firewalld
systemctl start firewalld
firewall-cmd --zone=public --add-port=22/tcp --permanent
firewall-cmd --list-ports
firewall-cmd --reload
```
