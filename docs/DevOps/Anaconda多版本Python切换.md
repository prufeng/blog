Anaconda多版本Python切换
===
安装Anaconda3，就自带了Python3.

这时可以用Conda建一个Python2的env。

```
conda create --name py2 python=2.7
activate py2
python -V
deactivate

conda create --name py3 python=3.7
activate py3
python -V

C:\Users\pan>conda env list
# conda environments:
#
base                  *  C:\swdtools\anaconda3
py2                      C:\swdtools\anaconda3\envs\py2
py3                      C:\swdtools\anaconda3\envs\py3
```