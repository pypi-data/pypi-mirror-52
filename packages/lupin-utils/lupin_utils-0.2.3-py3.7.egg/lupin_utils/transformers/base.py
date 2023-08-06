# -*- coding:utf-8 -*-
# @author: Henry
# @time: 2019-05-15 8:35 pm
# @dec: 封装数据处理
# @WeChat: 13270593018

from pandas import DataFrame
from typing import List, Tuple


class JoinData:
    """
    data frame 数据join
    """

    @staticmethod
    def left_join(x: DataFrame, y: DataFrame) -> DataFrame:
        """
        左连接
        :param x:
        :param y:
        :return:
        """
        return x.join(y)

    @staticmethod
    def merge(x: DataFrame, y: DataFrame) -> DataFrame:
        """
        merge
        :param x:
        :param y:
        :return:
        """
        return x.join(y, how='outer')


class BaseTransformer:
    """
    数据预处理transformer基类
    在派生类里面需要完成fit的实现
    """

    def __init__(self, *args, **kwargs):
        """
        数据预处理模型参数选择
        :param args:
        """
        self.args = args
        self.kwargs = kwargs

    def fit(self, x: DataFrame, y: DataFrame) -> (DataFrame, DataFrame):
        pass


class PipeDataTransformer:
    """
       类似于PipeLine， 用于数据预处理
       """

    def __init__(self, steps: List[Tuple[str, BaseTransformer]]):
        self.steps = steps

    def fit(self, x_train: DataFrame, y_train: DataFrame) -> (DataFrame, DataFrame):
        """
        按steps顺序依次处理并传递数据
        :param x_train:
        :param y_train:
        :return:
        """
        x = x_train
        y = y_train
        for step in self.steps:
            transformer = step[1]
            x, y = transformer.fit(x, y)

        return x, y
