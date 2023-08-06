# -*- coding:utf-8 -*-
# @author: Henry
# @time: None
# @dec: Error Class
# @WeChat: 13270593018

__all__ = [
    'FileNotExistsError',
    'ConfigError',
    'MlflowConfigError',
    'ParamTypeError'
]


class LupinException(Exception):
    def __init__(self, *args):
        self.args = args


class FileNotExistsError(LupinException):
    def __init__(self, *args):
        self.args = args
        self.message = '文件不存在'
        self.code = 1


class ConfigError(LupinException):
    def __init__(self, args):
        self.args = args
        self.message = 'yaml 配置错误'
        self.code = 2


class MlflowConfigError(LupinException):
    def __init__(self, *args):
        self.args = args
        self.message = 'mlflow 配置错误'
        self.code = 3


class ParamTypeError(LupinException):
    def __init__(self, *args):
        self.args = args
        self.message = '参数类型错误'
        self.code = 4
