![Science_Reading_Book_Downloader](https://socialify.git.ci/Senkita/Science_Reading_Book_Downloader/image?description=1&font=Bitter&language=1&owner=1&pattern=Solid&theme=Light)

## Introduction

> 前情提要：[[Python] 顺着前文思路，借机水一段小爬虫](https://www.52pojie.cn/thread-1562830-1-1.html)

自用爬虫，用于下载科学文库电子书。

支持正版，请勿传播，谢谢。

## Features

1. 根据book_id自动获取电子书总页数
2. 对book_id做基本判别
3. 对页面图片下载有误的情况进行修复
4. 任务进度使用进度条可视化
5. 整编图片为PDF
6. 支持命令行脚本和GUI两版

## Installation

```bash
# 依赖项
pip install requests pillow rich pysimplegui pyinstaller pycrypto  
```

* [Requests](https://github.com/psf/requests)用于爬虫请求
* [Pillow](https://github.com/python-pillow/Pillow)用于PDF生成
* [Rich](https://github.com/willmcgugan/rich)用于命令行进度条展示
* [PySimpleGUI](https://github.com/PySimpleGUI/PySimpleGUI)用于GUI界面
* [PyInstaller](https://github.com/pyinstaller/pyinstaller)用于打包成exe
* [PyCrypto](https://github.com/pycrypto/pycrypto)用于PyInstaller打包加密

## Usage

```bash
# 命令行脚本直接运行
python main.py

# 打包成GUI程序
pyinstaller -F -w --key 'passwd' --hidden-import pillow --hidden-import requests --hidden-import pysimplegui -n 科学文库电子书下载器 -i icon.ico --clean --win-private-assemblies -y  main.py
```

## Maintainers

[Senkita](https://github.com/Senkita)

## License

[MIT](https://github.com/Senkita/Science_Reading_Book_Downloader/blob/main/LICENSE) © [Senkita](https://github.com/Senkita)
