'''
Description: 爬虫主体
Author: Senkita
Date: 2021-12-20 23:41:21
LastEditors: Senkita
LastEditTime: 2021-12-22 22:28:01
'''
import os
import time
import json
import shutil
import requests
from PIL import Image
from src.Logger import Logger
from src.Tools import get_user_info, get_uuid, headers, time_break
from src.Interface import Interface

# 这个rich库需要自己装一下，用于进度条显示
# from rich.progress import track


class Crawler:
    def __init__(self, book_id: str) -> None:
        self.logger: Logger = Logger(book_id)

        self.dir_name: str = "./{}".format(book_id)
        self.file_name_list: list = []
        self.pic_list: list = []

        self.book_id: str = book_id
        self.user_id, self.accessToken = get_user_info()
        self.uuid: str = get_uuid(self.user_id, self.book_id)

        self.page_num: int = self.get_page_num()
        self.progress_window: Interface = Interface().progress_display(
            self.page_num * 2
        )
        self.progress_bar = self.progress_window['progress_bar']
        self.percentage = self.progress_window['percentage']

    # 获取页数
    def get_page_num(self) -> int:
        url: str = 'https://wkobwp.sciencereading.cn/asserts/{}/manifest?language=zh-CN'.format(
            self.uuid
        )
        return int(
            json.loads(
                json.loads(requests.get(url, headers=headers).content.decode('UTF-8'))[
                    'docinfo'
                ]
            )['PageCount']
        )

    # 下载页面图片
    def download_png(self, page_no: int) -> None:
        url: str = "https://wkobwp.sciencereading.cn/asserts/{}/image/{}/100?accessToken={}".format(
            self.uuid, page_no, self.accessToken
        )
        try:
            response: requests.Response = requests.get(url, headers=headers)
        except Exception as e:
            self.logger.warning(e)
            time.sleep(time_break)
            self.download_png(page_no)

        if b'{"error":-1}' in response.content:
            time.sleep(time_break)
            self.download_png(page_no)

        with open("{}/{}.png".format(self.dir_name, page_no), "wb") as f:
            f.write(response.content)
        time.sleep(time_break)

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
            self.download_png(0)
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
            "./{}.pdf".format(self.book_id),
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
            self.download_png(pic_no)
            return self.add_png(pic_no)

    def run(self) -> None:
        os.makedirs(self.dir_name, exist_ok=True)

        # for page_no in track(range(self.page_num), description="下载中，请稍候..."):
        for page_no in range(self.page_num):
            progress_event, _ = self.progress_window.read(timeout=time_break)
            if progress_event == '取消' or progress_event is None:
                self.progress_window.close()
                os._exit(0)
            self.download_png(page_no)

            progress: int = page_no + 1
            self.progress_bar.update_bar(progress)
            self.percentage.update(
                '{:.3}%'.format(progress / (self.page_num * 2) * 100)
            )

        self.list_file()
        self.generate_pdf()

        shutil.rmtree(self.dir_name)
        self.progress_window.close()
