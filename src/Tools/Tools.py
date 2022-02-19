'''
Description: 一些独立函数
Author: Senkita
Date: 2021-12-20 23:44:20
LastEditors: Senkita
LastEditTime: 2022-02-19 19:49:48
'''
import re
import argparse
from typing import Tuple, Union
from src.Processor.Crawler import Crawler


# 目录分级
def catalog_grading(catalog_list: list) -> tuple:
    pid_dict: dict = {}
    catalog_dict: dict = {}

    level: int = 1

    for pid, title, page_num in catalog_list:
        if pid == '0':
            catalog_dict[title] = {'level': level, 'page_num': int(page_num) - 1}
            pid_dict[pid] = level
            level = 0
        elif pid in pid_dict:
            catalog_dict[title] = {
                'level': pid_dict[pid],
                'page_num': int(page_num) - 1,
            }
            level = pid_dict[pid]
        else:
            level += 1
            catalog_dict[title] = {'level': level, 'page_num': int(page_num) - 1}
            pid_dict[pid] = level

    return [(v['level'], k, v['page_num']) for k, v in catalog_dict.items()]


# 参数校验
def verification(book_id: str) -> bool:
    if re.match(r'^[A-Z0-9]{36}$', book_id) and Crawler.get_uuid(
        Crawler.get_user_info()[0], book_id
    ):
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
