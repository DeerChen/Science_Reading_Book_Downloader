'''
Description: PDF处理相关
Author: Senkita
Date: 2022-02-18 21:49:30
LastEditors: Senkita
LastEditTime: 2022-02-19 22:33:32
'''
import os
import time
import shutil
import multitasking
from PIL import Image
from PyPDF2 import PdfFileReader as reader, PdfFileWriter as writer
from src.UI.Interface import Interface
from src.Processor.Crawler import Crawler
from src.Tools.Logger import Logger
from src.Tools.Config import time_break
from src.Tools.Tools import catalog_grading

# 这个rich库需要自己装一下，用于进度条显示
# from rich.progress import track


class Handler:
    def __init__(self, book_id: str, scaling: int = 150) -> None:
        self.spider: Crawler = Crawler(book_id, scaling)

        self.logger: Logger = Logger(book_id)

        self.file_name_list: list = []

        self.book_name, self.book_ISBN, self.catalog_list = self.spider.get_book_info(
            book_id
        )
        self.dir_name: str = "./{}".format(book_id)
        self.pic_list: list = []

        self.page_num: int = self.spider.get_page_num()
        self.progress_window: Interface = Interface().progress_display(
            self.page_num * 2
        )
        self.progress_bar = self.progress_window['progress_bar']
        self.percentage = self.progress_window['percentage']

    # 文件名排序
    def list_file(self) -> None:
        for file_name in os.listdir(self.dir_name):
            if file_name[-4:] == ".png":
                self.file_name_list.append(file_name[:-4])

        self.file_name_list.sort(key=lambda ele: int(ele))

    # 拼接为PDF
    def generate_pdf(self) -> None:
        try:
            pdf: Image.Image = Image.open(
                "{}/{}.png".format(self.dir_name, self.file_name_list[0])
            )
        except Exception:
            self.logger.warning("首页下载有误，重试中...")
            time.sleep(time_break)
            self.spider.download_png(0)
            return self.generate_pdf()

        self.file_name_list.pop(0)
        self.progress_bar.update_bar(self.page_num + 1)

        # for pic_no in track(self.file_name_list, description="生成PDF中，请稍候..."):
        for pic_no in self.file_name_list:
            progress_event, _ = self.progress_window.read(timeout=time_break)
            if progress_event == '取消' or progress_event is None:
                self.progress_window.close()
                os._exit(0)

            self.add_png(pic_no)

            progress: int = self.page_num + self.file_name_list.index(pic_no) + 2
            self.progress_bar.UpdateBar(progress)
            self.percentage.update(
                '{:.3}%'.format(progress / (self.page_num * 2) * 100)
            )

        pdf.save(
            "./{}.pdf".format(self.book_ISBN),
            "PDF",
            resolution=100.0,
            save_all=True,
            append_images=self.pic_list,
        )

    # 添加页面
    def add_png(self, pic_no: int) -> None:
        try:
            img: Image.Image = Image.open("{}/{}.png".format(self.dir_name, pic_no))
            if img.mode == "RGBA":
                img = img.convert("RGB")
            self.pic_list.append(img)
        except Exception:
            self.logger.warning("图片{}.png下载有误，重试中...".format(pic_no))
            time.sleep(time_break)
            self.spider.download_png(pic_no)
            return self.add_png(pic_no)

    # 添加书签
    def add_bookmark(self) -> None:
        input_pdf: reader = reader("./{}.pdf".format(self.book_ISBN))
        output_pdf: writer = writer()

        for i in range(input_pdf.getNumPages()):
            output_pdf.addPage(input_pdf.getPage(i))

        parent_set = {}
        for bookmark in catalog_grading(self.catalog_list):
            parent = output_pdf.addBookmark(
                bookmark[1],
                bookmark[2],
                parent=parent_set.get(bookmark[0] - 1),
            )
            parent_set[bookmark[0]] = parent

        with open('./{}.pdf'.format(self.book_name), 'wb') as f:
            output_pdf.write(f)

    def run(self) -> None:
        os.makedirs(self.dir_name, exist_ok=True)

        # for page_no in track(range(self.page_num), description="下载中，请稍候..."):
        for page_no in range(self.page_num):
            progress_event, _ = self.progress_window.read(timeout=time_break)
            if progress_event == '取消' or progress_event is None:
                self.progress_window.close()
                os._exit(0)
            self.spider.download_png(page_no)

            progress: int = page_no + 1
            self.progress_bar.update_bar(progress)
            self.percentage.update(
                '{:.3}%'.format(progress / (self.page_num * 2) * 100)
            )
        multitasking.wait_for_tasks()

        self.list_file()
        self.generate_pdf()

        self.add_bookmark()

        # 清理
        shutil.rmtree(self.dir_name)
        os.remove("./{}.pdf".format(self.book_ISBN))
        self.progress_window.close()
