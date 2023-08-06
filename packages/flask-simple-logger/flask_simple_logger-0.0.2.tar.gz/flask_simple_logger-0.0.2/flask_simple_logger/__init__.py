# -*-coding: utf-8-*-

import traceback
from functools import wraps
from typing import Callable

from flask import Flask


class Logger(object):

    def __init__(self, current_app: Flask):
        self.current_app = current_app

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
