'''
Description: 主入口
Author: Senkita
Date: 2021-12-20 23:40:59
LastEditors: Senkita
LastEditTime: 2022-02-19 22:29:17
'''
import os
import signal
import multitasking
from src.Processor.Handler import Handler
from src.UI.Interface import Interface

signal.signal(signal.SIGINT, multitasking.killall)
scaling: int = 150


def main() -> None:
    # 命令行运行
    # from src.Tools import get_args
    # book_id = get_args()

    # GUi版
    ui = Interface()
    try:
        book_id, scaling = ui.display()
    except Exception as e:
        print(e)
        os._exit(0)

    if book_id:
        handler: Handler = Handler(book_id, scaling)
        handler.run()


if __name__ == "__main__":
    main()
