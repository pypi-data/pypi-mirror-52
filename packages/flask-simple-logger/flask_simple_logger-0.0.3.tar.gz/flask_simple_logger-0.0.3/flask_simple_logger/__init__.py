# -*-coding: utf-8-*-

import logging
import sys
import traceback
from functools import wraps
from logging.handlers import RotatingFileHandler
from typing import Callable, Optional

from flask import Flask


class InfoFilter(logging.Filter):
    def filter(self, record):
        """
        筛选, 只需要 INFO 级别以上log
        :param record:
        """
        if logging.INFO <= record.levelno < logging.ERROR:
            return super(InfoFilter, self).filter(record)
        else:
            return 0


class Log(object):
    def __init__(self, app, log_path_error, log_path_info, log_file_max_bytes,
                 log_file_backup_count, log_formatter_info, log_formatter_error):
        self.app = app
        self.log_path_error = log_path_error
        self.log_path_info = log_path_info
        self.log_file_max_bytes = log_file_max_bytes
        self.log_file_backup_count = log_file_backup_count
        self.log_formatter_info = log_formatter_info
        self.log_formatter_error = log_formatter_error
        self.filter_info = InfoFilter()
        self.level_info = logging.INFO
        self.level_error = logging.ERROR
        self._handler_file_info = None
        self._handler_file_error = None
        self._handler_screen_info = None
        self._handler_screen_error = None

    @property
    def handler_file_info(self):
        if not self._handler_file_info:
            file_handler_info = RotatingFileHandler(filename=self.log_path_info)
            file_handler_info.setFormatter(self.log_formatter_info)
            file_handler_info.setLevel(self.level_info)
            file_handler_info.addFilter(self.filter_info)
            self._handler_file_info = file_handler_info
        return self._handler_file_info

    @property
    def handler_file_error(self):
        if not self._handler_file_error:
            file_handler_error = RotatingFileHandler(filename=self.log_path_error)
            file_handler_error.setFormatter(self.log_formatter_error)
            file_handler_error.setLevel(logging.ERROR)
            self._handler_file_error = file_handler_error
        return self._handler_file_error

    @property
    def handler_screen_info(self):
        if not self._handler_screen_info:
            self._handler_screen_info = logging.StreamHandler(sys.stdout)
            # log_filter = LogFilter(logging.NOTSET)
            # self._handler_screen_info.addFilter(log_filter)
            self._handler_screen_info.setFormatter(self.log_formatter_info)
            self._handler_screen_info.setLevel(logging.DEBUG)
        return self._handler_screen_info

    @property
    def handler_screen_error(self):
        if not self._handler_screen_error:
            self._handler_screen_error = logging.StreamHandler(sys.stderr)
            self._handler_screen_error.setLevel(logging.DEBUG)
            self._handler_screen_error.setFormatter(self.log_formatter_error)
        return self._handler_screen_error

    def init(self):
        self.app.logger.addHandler(self.handler_file_info)
        self.app.logger.addHandler(self.handler_file_error)
        # self.app.logger.addHandler(self.handler_screen_info)
        # self.app.logger.addHandler(self.handler_screen_error)
        self.app.logger.setLevel(self.level_info)


class Logger(object):

    def __init__(self, current_app: Optional[Flask] = None):
        self.current_app = current_app

    def init_app(self, app):
        if not self.current_app:
            self.current_app = app

    @property
    def info(self):
        return self.current_app.logger.info

    @property
    def info_exception(self):
        return self.current_app.logger.info

    @property
    def error(self):
        return self.current_app.logger.error

    @property
    def exception(self):
        return self.current_app.logger.exception

    @property
    def traceback(self):
        return traceback.format_exc


def log_output(logger):
    def decorate(func: Callable):
        @wraps(func)
        def wrap(*args, **kwargs):
            result = func(*args, **kwargs)
            logger.info(f'{[func.__name__]} output is {result}')
            return result

        return wrap

    return decorate


def log_input(logger):
    def decorate(func: Callable):
        @wraps(func)
        def wrap(*args, **kwargs):
            logger.info(f'{[func.__name__]} input is args {args} kwargs {kwargs}')
            return func(*args, **kwargs)

        return wrap

    return decorate


if __name__ == '__main__':
    pass
