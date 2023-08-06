# -*- coding:utf-8 -*-
# @author: Henry
# @time: 2019-05-15 9:48 am
# @dec: mlflow封装
# @WeChat: 13270593018
# @requirements: mlflow==0.8.2

import mlflow
import mlflow.sklearn
from sklearn.pipeline import Pipeline
from lupin_utils.error import MlflowConfigError

__all__ = [
    'LupinMlflow'
]


class LupinMlflow:
    def __init__(self, tracing_host=None, tracing_port=None, use_https=False):
        """
        初始化远程服务地址
        :param tracing_host: 远程 mlflow host
        :param tracing_port: 远程 mlflow port
        """
        self.tracing_host = tracing_host
        self.tracing_port = tracing_port
        self.mlflow = mlflow
        self.use_https = use_https
        self.tracing_init()

    def tracing_init(self):
        if self.tracing_host is None or self.tracing_port is None:
            raise MlflowConfigError(
                f'tracing url missing right config, host:{self.tracing_host}, port:{self.tracing_port}')
        if self.use_https:
            url = f'https://{self.tracing_host}:{self.tracing_port}'
        else:
            url = f'http://{self.tracing_host}:{self.tracing_port}'
        self.mlflow.set_tracking_uri(url)

    def log_model(self, model: Pipeline, name: str):
        """
        上传训练模型
        :param model:
        :param name:
        :return:
        """
        self.mlflow.sklearn.log_model(model, name)

    def log_metrics(self, **kwargs):
        """
        上传计算结果
        :param kwargs:
        :return:
        """
        for k, v in kwargs.items():
            self.mlflow.log_metric(k, v)

    def log_params(self, **kwargs):
        """
        上传参数
        :param kwargs:
        :return:
        """
        for k, v in kwargs.items():
            self.mlflow.log_param(k, v)
