# -*-coding: utf-8-*-

import traceback
from functools import wraps
from typing import Callable

from flask import current_app


class Logger(object):

    @property
    def info(self):
        return current_app.logger.info

    @property
    def info_exception(self):
        return current_app.logger.info

    @property
    def error(self):
        return current_app.logger.error

    @property
    def exception(self):
        return current_app.logger.exception

    @property
    def traceback(self):
        return traceback.format_exc


logger = Logger()


def log_output(func: Callable):
    @wraps(func)
    def wrap(*args, **kwargs):
        result = func(*args, **kwargs)
        logger.info(f'{[func.__name__]} output is {result}')
        return result

    return wrap


def log_input(func: Callable):
    @wraps(func)
    def wrap(*args, **kwargs):
        logger.info(f'{[func.__name__]} input is args {args} kwargs {kwargs}')
        return func(*args, **kwargs)

    return wrap


if __name__ == '__main__':
    pass
