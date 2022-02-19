![Science_Reading_Book_Downloader](https://socialify.git.ci/Senkita/Science_Reading_Book_Downloader/image?description=1&font=Bitter&language=1&owner=1&pattern=Solid&theme=Light)

## Introduction

> 前情提要：[[Python] 顺着前文思路，借机水一段小爬虫](https://www.52pojie.cn/thread-1562830-1-1.html)

自用爬虫，用于下载科学文库电子书。

支持正版，请勿传播，谢谢。

## Features

1. 根据 book_id 自动获取电子书总页数
2. 对 book_id 做基本判别
3. 对页面图片下载有误的情况进行修复
4. 任务进度使用进度条可视化
5. 整编图片为 PDF
6. 支持命令行脚本和 GUI 两版
7. 为下载图书添加书签
8. 文件名显示为书名
9. 支持下载清晰度选择
10. 支持多线程下载

## Installation

```bash
# 依赖项
pip install requests pillow rich pysimplegui pyinstaller pycrypto beautifulsoup4 pypdf2 lxml multitasking
```

-   [Requests](https://github.com/psf/Requests)用于爬虫请求
-   [Pillow](https://github.com/Python-Pillow/Pillow)用于 PDF 生成
-   [Rich](https://github.com/willmcgugan/Rich)用于命令行进度条展示
-   [PySimpleGUI](https://github.com/PySimpleGUI/PySimpleGUI)用于 GUI 界面
-   [PyInstaller](https://github.com/PyInstaller/PyInstaller)用于打包成 exe
-   [PyCrypto](https://github.com/PyCrypto/PyCrypto)用于 PyInstaller 打包加密
-   [BeautifulSoup4](https://www.crummy.com/software/BeautifulSoup)用于网页解析
-   [PyPDF2](https://github.com/mstamy2/PyPDF2)用于 PDF 添加书签
-   [lxml](https://lxml.de)用于解析 XPath
-   [MultiTasking](https://github.com/ranaroussi/MultiTasking)用于多线程下载

## Usage

```bash
# 命令行脚本直接运行
python main.py

# 打包成GUI程序
pyinstaller -F -w --key 'passwd' --hidden-import pillow --hidden-import requests --hidden-import pysimplegui --hidden-import beautifulsoup4 --hidden-import pypdf2 --hidden-import lxml --hidden-import multitasking -n 科学文库电子书下载器 -i icon.ico --clean --win-private-assemblies -y  main.py
```

### Q&A

1. Q: ![KeyError: 'docinfo'](https://karasu.oss-cn-chengdu.aliyuncs.com/Senkita/报错.png)
   A: Try again.

## Maintainers

[Senkita](https://github.com/Senkita)

## License

[MIT](LICENSE) © [Senkita](https://github.com/Senkita)
