VSCode集成Git Bash作为Terminal
===
Windows下想用Git Bash作为VSCode Terminal，可尝试以下方法。

# 方法一
* Ctrl+Shift+P
* Select Default Shell
* Select Git Bash

默认为cmd，也可选powershell。

（我本机VSCode识别不到Git，Git Bash选项没出现。）

# 方法二
* Ctrl+Shift+P
* Open User Settings
* Change terminal.integrated.shell.windows
```
"terminal.integrated.shell.windows": "C:\\windows\\System32\\cmd.exe",
```
改为
```
"terminal.integrated.shell.windows": "C:\\swdtools\\Git\\bin\\bash.exe",
```

# 进阶
加启动参数。

```
"terminal.integrated.shellArgs.windows": ["-l"],
```

e.g.   
~目录下建立.bash_profile，输入以下内容。

```
alias gss='git status -s'
```

重启Terminal，即可输入gss查看效果。

我主要使用该功能来建立[Git Command Alias](https://blog.csdn.net/prufeng/article/details/85001682)。

# 参考
https://code.visualstudio.
com/docs/editor/integrated-terminal
