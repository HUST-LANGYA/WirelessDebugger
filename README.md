# WirelessDebugger

Lenor

## 文件结构介绍

Code文件夹为代码文件夹，其中每个次级目录为一个方案的代码

Script文件夹为文稿文件夹，方案、笔记（如果整理了）都会放在此文件夹内。

## 开发环境配置

如果某个代码项目存在requirements文件，则直接使用pip安装此文件即可

```Shell
pip install -r requirements.txt
```

如果不存在requirements文件，那自己生成一个再安装吧

```Shell
pip install pipreqs #如果没有安装过
pipreqs ./ --encoding=utf8
```

python版本：cpython 3.8

