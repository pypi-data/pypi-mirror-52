# -*- coding:utf-8 -*-
# @author: Henry
# @time: 2019-05-15 8:35 pm
# @dec: 封装数据处理
# @WeChat: 13270593018

from pandas import DataFrame
from typing import List, Tuple


class BaseTransformer:
    """
    数据预处理transformer基类
    在派生类里面需要完成fit的实现
    """

    def __init__(self, *args):
        """
        数据预处理模型参数选择
        :param args:
        """
        self.args = args

    def fit(self, x: DataFrame, y: DataFrame) -> (DataFrame, DataFrame):
        pass


class TransformerOperate:
    """
    类似于PipeLine， 用于数据预处理
    """

    def __init__(self, steps=List[Tuple[str, BaseTransformer()]]):
        self.steps = steps

    def fit(self, x_train: DataFrame, y_train: DataFrame) -> (DataFrame, DataFrame):
        x = x_train
        y = y_train
        for step in self.steps:
            transformer = step[1]
            x, y = transformer.fit(x, y)

        return x, y
