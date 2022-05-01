指定Python安装包下载地址
===
有时安装包从pypi.org下载不了，或者网络限制或使用内部仓库。

# Pip Configure.

Windows: ~\pip\pip.ini

Linux: ~\.pip\pip.conf

```
[global]
index-url= http://mirrors.aliyun.com/pypi/simple/
extra-index-url= https://pypi.org/simple

[install]
trusted-host=mirrors.aliyun.com
```

# Pip Install
命令行里再指定也可以。

也支持本地安装。不过，这是个痛苦的过程，就像Maven、Npm等其他依赖管理工具一样。

```
pip install --help


Package Index Options:
  -i, --index-url <url>       Base URL of Python Package Index (default 
                              https://pypi.org/simple). This should point
                              to a repository compliant with PEP 503 (the simple repository API) or a local directory
                              laid out in the same format.
  --extra-index-url <url>     Extra URLs of package indexes to use in addition to --index-url. Should follow the same
                              rules as --index-url.
  --no-index                  Ignore package index (only looking at --find-links URLs instead).
  -f, --find-links <url>      If a url or path to an html file, then parse for links to archives. If a local path or
                              file:// url that's a directory, then look for archives in the directory listing.
```