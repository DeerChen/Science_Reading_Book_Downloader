'''
Description: 自定义日志类
Author: Senkita
Date: 2021-12-22 09:36:07
LastEditors: Senkita
LastEditTime: 2021-12-22 20:21:28
'''
import logging


# 日志配置
class LoggerConfig:
    def __init__(self, book_id: str) -> None:
        self.logger: logging.Logger = logging.getLogger()
        self.formatter: logging.Formatter = logging.Formatter(
            fmt='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S',
        )

        # self.stream_handler: logging.StreamHandler = logging.StreamHandler()
        # self.stream_handler.setFormatter(self.formatter)
        # self.stream_handler.setLevel(logging.ERROR)

        self.file_handler: logging.FileHandler = logging.FileHandler(
            filename='{}.log'.format(book_id),
            mode='a',
        )
        self.file_handler.setFormatter(self.formatter)
        self.file_handler.setLevel(logging.DEBUG)

        # self.logger.addHandler(self.stream_handler)
        self.logger.addHandler(self.file_handler)


# 日志类
class Logger(LoggerConfig):
    def __new__(cls: logging.Logger, book_id: str) -> logging.Logger:
        super(Logger, cls).__init__(cls, book_id)
        return cls.logger
