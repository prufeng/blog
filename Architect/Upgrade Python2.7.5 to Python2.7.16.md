Upgrade Python2.7.5 to Python2.7.16
===
Python has already been installed in Linux by default, but the version is usually not up to date.

# Install Python 2.7.16
Download from https://www.python.org/ftp/python/2.7.16/Python-2.7.16.tgz

Specify prefix and use altinstall in case overwriting the default Python.
```bash
tar zxvf Python-2.7.16.tgz
cd Python-2.7.16

sudo ./configure --prefix=/usr/local
sudo make
sudo make altinstall
```

```
mv /usr/bin/python /usr/bin/python2.7.5
ln -s /usr/local/bin/python2.7 /usr/bin/python
```

We can find the different version `python` under `usr/bin`.
```
$ python -V
Python 2.7.16
$ python2.7.5 -V
Python 2.7.5
$ python2.7 -V
Python 2.7.16
$ python2 -V
Python 2.7.5
```

替换旧`python`的操作，如非真的必要，不建议。

因为替换后发现一些系统命令会出问题，范围似乎也无法预知，有些风险。

## No module named yum
Yum does not work after Python upgrade.

```
$ sudo yum install zlib
There was a problem importing one of the Python modules
required to run yum. The error leading to this problem was:

   No module named yum

Please install a package which provides this module, or
verify that the module is installed correctly.

It's possible that the above module doesn't match the
current version of Python, which is:
2.7.16 (default, Aug 30 2019, 16:44:16)
[GCC 4.8.5 20150623 (Red Hat 4.8.5-39)]

If you cannot solve this problem yourself, please go to
the yum faq at:
  http://yum.baseurl.org/wiki/Faq
```
```
sudo vi /usr/bin/yum
```
Change `#! /usr/bin/python` to `#! /usr/bin/python2`

# ImportError: No module named urlgrabber.grabber
```
Downloading packages:
Traceback (most recent call last):
  File "/usr/libexec/urlgrabber-ext-down", line 22, in <module>
    from urlgrabber.grabber import \
ImportError: No module named urlgrabber.grabber
Traceback (most recent call last):
  File "/usr/libexec/urlgrabber-ext-down", line 22, in <module>
    from urlgrabber.grabber import \
ImportError: No module named urlgrabber.grabber

sudo vi /usr/libexec/urlgrabber-ext-down

```
Change `#! /usr/bin/python` to `#! /usr/bin/python2`

vi Python-2.7.16/Modules/Setup.dist
```py
#zlib zlibmodule.c -I$(prefix)/include -L$(exec_prefix)/lib -lz
zlib zlibmodule.c -I$(prefix)/include -L$(exec_prefix)/lib -lz
```
Install Python again.
```
sudo ./configure --prefix=/usr/local
sudo make
sudo make altinstall
```
# ImportError: No module named _ssl
```
sudo yum install openssl-devel

sudo vi /Modules/Setup
```
```py
#_socket socketmodule.c timemodule.c
_socket socketmodule.c timemodule.c
```

Install Python again.

