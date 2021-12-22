'''
Description: 主入口
Author: Senkita
Date: 2021-12-20 23:40:59
LastEditors: Senkita
LastEditTime: 2021-12-22 17:18:38
'''
from src.Crawler import Crawler
from src.Interface import Interface


def main() -> None:
    # 命令行运行
    # from src.Tools import get_args
    # book_id = get_args()
    ui = Interface()
    book_id: str = ui.display()
    if book_id:
        spider: Crawler = Crawler(book_id)
        spider.run()


if __name__ == "__main__":
    main()
