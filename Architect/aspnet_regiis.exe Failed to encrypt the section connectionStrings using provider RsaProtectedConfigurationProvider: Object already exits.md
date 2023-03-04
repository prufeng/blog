使用aspnet_regiis.exe加密web.config connectionStrings时奇奇怪怪的错误：

Failed to encrypt the section 'connectionStrings' using provider 'RsaProtectedConfigurationProvider'. Error message from the provider: Object already exits.

检查发现加密默认使用的Key Container不存在。
```
certutil -key NetFrameworkConfigurationKey
# Exporting an RSA Key Container
C:\Windows\Microsoft.NET\Framework64\v4.0.30319\aspnet_regiis.exe -px "NetFrameworkConfigurationKey" keys.xml -pri
```
相应的MahineKey也不存在：C:\ProgramData\Microsoft\Crypto\RSA\MachineKeys\d6d9*

建一个，加权限。
```
# Creating an RSA Key Container
# C:\Windows\Microsoft.NET\Framework64\v4.0.30319\aspnet_regiis.exe -pc "NetFrameworkConfigurationKey" -exp
# Granting Authority to Access an RSA Key Container
# C:\Windows\Microsoft.NET\Framework64\v4.0.30319\aspnet_regiis.exe -pa "NetFrameworkConfigurationKey" "NT AUTHORITY\NETWORK SERVICE"
```

可以看到相应的MahineKey生成出来：C:\ProgramData\Microsoft\Crypto\RSA\MachineKeys\d6d9*

有时候也可能MachineKeys已存在，只是访问权限有问题，加权限之后就表现正常。

```
icacls C:\ProgramData\Microsoft\Crypto\RSA\MachineKeys\d6d9*
```

加解密测试，测试目录下放web.config，包含connectionStrings。
```
# C:\Windows\Microsoft.NET\Framework64\v4.0.30319\aspnet_regiis.exe -pef connectionStrings C:\test -prov RsaProtectedConfigurationProvider
# C:\Windows\Microsoft.NET\Framework64\v4.0.30319\aspnet_regiis.exe -pdf connectionStrings C:\test -prov RsaProtectedConfigurationProvider
```

其他相关命令。
```
# Importing an RSA Key Container
# C:\Windows\Microsoft.NET\Framework64\v4.0.30319\aspnet_regiis.exe -pi "NetFrameworkConfigurationKey" keys.xml
# Deleting an RSA Key Container
# C:\Windows\Microsoft.NET\Framework64\v4.0.30319\aspnet_regiis.exe -pz "NetFrameworkConfigurationKey"
```
