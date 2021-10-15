# Python Serial

Lenor

## Intro

Python的serial库是一个基于python调用串口的库(pure python)，主模块名为“pyserial”(for windows)，调用时使用serial模块，将会在不同的系统自动匹配所需要的后端。

包括了绝大部分需要的基本功能：

* 查找串口
* 以某一个配置模式打开一个串口
* 收发数据

基本使用方式可以参考File/Code: SerialTest里面的程序，注意其中的几个函数和相关的注释。

## 库简介



## 开发难点

1. 由于pyserial只提供了阻塞式的串口读取，因此需要使用python极为恶心的多线程来实现更高级的读取