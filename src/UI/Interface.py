'''
Description: 界面
Author: Senkita
Date: 2021-12-22 12:17:30
LastEditors: Senkita
LastEditTime: 2022-03-17 20:28:01
'''
from types import FunctionType
from typing import Tuple, Union
import PySimpleGUI as sg
from src.Tools.Tools import verification


class Interface:
    def __init__(self) -> None:
        self.notice_layout = [
            [sg.T('书籍版权归科学文库(https://book.sciencereading.cn/)所有！')],
            [sg.T('此脚本仅供学习交流使用，不得用于商业用途，请支持正版！')],
            [sg.T('如果您不幸得到了该脚本，请低调使用，切勿传播！')],
            [sg.T('爬虫是个与服务器管理员斗智斗勇的游戏，因此具有时效性，失效不补！')],
            [sg.Submit('朕已阅！'), sg.Cancel('我不听！')],
        ]

    # 主体窗口
    def main_display(self) -> Union[Tuple[str, str], None]:
        main_layout = [
            [
                [sg.T('请输入book_id：', tooltip='book_id请在书籍页地址栏中查找'), sg.I()],
                [
                    sg.T('请选择缩放比：', tooltip='缩放比越大，则图页越清晰，但书籍体积也相应越大，爬取时间对应增长'),
                    sg.Combo([100, 150], default_value=150),
                    sg.T('%'),
                ],
                [
                    sg.Radio(
                        text='保留图片文件夹',
                        group_id='keep_pic_folder',
                        default=False,
                    ),
                    sg.Radio(
                        text='删除图片文件夹',
                        group_id='keep_pic_folder',
                        default=True,
                    ),
                ],
                [sg.Submit('下载'), sg.Cancel('退出')],
            ]
        ]
        main_window: sg.Window = sg.Window('下载科学文库电子书', main_layout)
        event, value = main_window.read()
        if event == '下载':
            main_window.close()
            if verification(value[0]):
                return value[0], value[1], value[2]
            else:
                sg.Popup('输入有误，请重新输入！')
                self.main_display()
        else:
            main_window.close()

    # 告知窗体
    def notice_display(self, fn: FunctionType) -> Union[FunctionType, None]:
        notice_window = sg.Window('用前须知', self.notice_layout)

        notice_event, _ = notice_window.read()
        if notice_event == '朕已阅！':
            notice_window.close()
            return fn()
        else:
            notice_window.close()

    # 用户界面
    def display(self) -> Union[Tuple[str, str], None]:
        return self.notice_display(self.main_display)

    # 进度条
    @staticmethod
    def progress_display(total: int) -> sg.Window:
        progress_layout = [
            [
                sg.ProgressBar(
                    total, orientation='h', size=(40, 10), key='progress_bar'
                ),
                sg.T('', key='percentage'),
            ],
            [sg.Cancel('取消')],
        ]
        return sg.Window('任务进度', progress_layout)
