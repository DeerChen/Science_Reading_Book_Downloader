'''
Description: 爬虫主体
Author: Senkita
Date: 2021-12-20 23:41:21
LastEditors: Senkita
LastEditTime: 2022-03-17 23:06:25
'''
import re
import time
import json
import requests
from lxml import etree
from typing import Tuple
from string import Template
from bs4 import BeautifulSoup
from src.Tools.Logger import Logger
from src.Tools.Config import headers, time_break


class Crawler:
    def __init__(self, book_id: str, scaling: int = 150) -> None:
        self.logger: Logger = Logger(book_id)
        self.dir_name: str = "./{}".format(book_id)

        self.user_id, self.accessToken = self.get_user_info()
        self.uuid: str = self.get_uuid(self.user_id, book_id)

        self.scaling: int = scaling

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
        url: str = "https://wkobwp.sciencereading.cn/asserts/{}/image/{}/{}?accessToken={}".format(
            self.uuid, page_no, self.scaling, self.accessToken
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

    # 获取用户ID和accessToken
    @staticmethod
    def get_user_info() -> Tuple[str, str]:
        user_id_url: str = "https://wkobwp.sciencereading.cn/api/systemuser/info"

        params: dict = {"params": '{"heads":{"defaultuser":null}}'}
        response: str = requests.get(user_id_url, params=params).content.decode("UTF-8")

        try:
            resultBody: dict = json.loads(response)["resultBody"]

            user_id: str = resultBody["id"]
            accessToken: str = resultBody["accessToken"]
            return user_id, accessToken
        except Exception as e:
            raise Exception(e)

    # 获取uuid
    @staticmethod
    def get_uuid(user_id: str, book_id: str) -> str:
        uuid: str = None
        uuid_url: str = "https://wkobwp.sciencereading.cn/api/file/add"
        params: Template = Template(
            '{"params": {"userId": "$user_id","file": "http://159.226.241.32:81/$book_id.pdf"}}'
        )
        data: dict = {"params": params.substitute(user_id=user_id, book_id=book_id)}
        response: str = requests.post(
            uuid_url, data=data, headers=headers
        ).content.decode("UTF-8")
        if response != '':
            result: str = json.loads(response)["result"]
            if result != 'OutOfFileSizeLimit':
                uuid = result
        return uuid

    # 获取书名、ISBN及目录
    @staticmethod
    def get_book_info(book_id: str) -> Tuple[str, int, list]:
        book_name: str = None
        catalog_list: list = []
        book_name_url: str = (
            "https://book.sciencereading.cn/shop/book/Booksimple/show.do?id={}".format(
                book_id
            )
        )
        response: str = requests.get(book_name_url, headers=headers).content.decode(
            'UTF-8'
        )
        if response != '':
            soup: BeautifulSoup = BeautifulSoup(response, 'html.parser')

            book_name: str = soup.select(
                'body > div:nth-child(3) > div > div > div > div.row > div.col-md-8.col-sm-7 > div.book_detail_title > span > b:nth-child(1)'
            )[0].text

            book_ISBN: int = int(
                etree.HTML(str(soup))
                .xpath(
                    "/html/body/div[1]/div/div/div/div[1]/div[2]/div[3]/div[2]/div[2]/span"
                )[0]
                .text
            )

            pattern: re.Pattern = re.compile(
                r'"pId":"(.*?)".*?"name":"(.*?)".*?bookPageNum=(\d+)'
            )
            catalog_list = re.findall(pattern, response)

            symbol_pattern: re.Pattern = re.compile(r'\W+')
            book_name = re.sub(symbol_pattern, '_', book_name)

        return book_name, book_ISBN, catalog_list
