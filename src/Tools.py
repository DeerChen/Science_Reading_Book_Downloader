'''
Description: 一些独立函数
Author: Senkita
Date: 2021-12-20 23:44:20
LastEditors: Senkita
LastEditTime: 2021-12-22 20:35:02
'''
import re
import json
import requests
import argparse
from string import Template
from typing import Tuple, Union

headers: dict = {'Connection': 'close'}
time_break: int = 2


# 获取用户ID和accessToken
def get_user_info() -> Tuple[str, str]:
    user_id_url: str = "https://wkobwp.sciencereading.cn/api/systemuser/info"

    params: dict = {"params": '{"heads":{"defaultuser":null}}'}
    response: requests.Response = requests.get(
        user_id_url, params=params
    ).content.decode("UTF-8")

    try:
        resultBody: dict = json.loads(response)["resultBody"]

        user_id: str = resultBody["id"]
        accessToken: str = resultBody["accessToken"]
        return user_id, accessToken
    except Exception as e:
        raise Exception(e)


# 获取uuid
def get_uuid(user_id: str, book_id: str) -> str:
    uuid: str = None
    uuid_url: str = "https://wkobwp.sciencereading.cn/api/file/add"
    params: Template = Template(
        '{"params": {"userId": "$user_id","file": "http://159.226.241.32:81/$book_id.pdf"}}'
    )
    data: dict = {"params": params.substitute(user_id=user_id, book_id=book_id)}
    response: requests.Response = requests.post(
        uuid_url, data=data, headers=headers
    ).content.decode("UTF-8")
    if response != '':
        result: str = json.loads(response)["result"]
        if result != 'OutOfFileSizeLimit':
            uuid = result
    return uuid


# 参数校验
def verification(book_id: str) -> bool:
    if re.match(r'^[A-Z0-9]{36}$', book_id) and get_uuid(get_user_info()[0], book_id):
        return True
    return False


# 命令行参数解析
def get_args() -> Union[Tuple[str, int], Exception]:
    parser: argparse.ArgumentParser = argparse.ArgumentParser()
    parser.add_argument("book_id", type=str, help="科学文库电子书ID")

    args: argparse.Namespace(str, int) = parser.parse_args()
    if verification(args.book_id):
        return args.book_id
    else:
        raise Exception('参数错误')
