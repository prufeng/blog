Python打包迁移项目到离线机器，一种相对靠谱的Python离线pip安装方法。

1. 在线机器完成调试。

```
pip install --proxy http://www.proxy.net:8888 ldap3
pip freeze>requirements.txt
python test.py
```

2. 下载whl安装包到wheelfiles文件夹

`pip download -r requirements.txt -d wheelfiles --proxy http://www.proxy.net:8888`


3. 打包项目到新环境，使用wheelfiles里面的whl重新安装

```
pip install -r requirements.txt --no-index --find-link=./wheelfiles
pip freeze
python test.py
```

可使用虚拟环境来测试，比如conda。
```
conda create -n myenv python=3.11
conda activate myenv
pip freeze
# install and test
conda activate base
conda env remove --name myenv
```
