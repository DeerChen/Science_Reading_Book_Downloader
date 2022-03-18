'''
Description: 主入口
Author: Senkita
Date: 2021-12-20 23:40:59
LastEditors: Senkita
LastEditTime: 2022-03-17 23:03:39
'''
import os
from src.Processor.Handler import Handler
from src.UI.Interface import Interface


def main() -> None:
    # 命令行运行
    # from src.Tools import get_args
    # book_id = get_args()

    # GUI版
    ui = Interface()
    try:
        book_id, scaling, keep_pic_folder = ui.display()
    except Exception as e:
        print(e)
        os._exit(0)

    if book_id:
        handler: Handler = Handler(book_id, scaling, keep_pic_folder)
        handler.run()


if __name__ == "__main__":
    main()
