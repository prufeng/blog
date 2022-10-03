# Issue
从一台机复制出另一台的时候，发现IIS的网页只能通过localhost访问，IP和hostname都不行。

# Solution
Event log发现还去绑定原来那台机。
```
Unable to bind to the underlying transport for 192.168.33.1:443. The IP Listen-Only list may contain a reference to an interface which may not exist on this machine.  The data field contains the error number.
```

重新绑定一下就可以。
```
netsh http show iplisten

IP addresses present in the IP listen list:
-------------------------------------------

    192.168.33.1
    127.0.0.0
    127.0.0.1


netsh http delete iplisten ipaddress=192.168.33.1
IP address successfully deleted

netsh http add iplisten ipaddress=192.168.33.2
IP address successfully added


netsh http show iplisten

IP addresses present in the IP listen list:
-------------------------------------------

    192.168.33.2
    127.0.0.0
    127.0.0.1
    
    
```
