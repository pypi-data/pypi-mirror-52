# -*- coding:utf-8 -*-
# @author: Henry
# @time: 2019-05-16 2:27 pm
# @dec: multiple columns label-encoder and one-hot-encoder
# @WeChat: 13270593018

from .base import BaseTransformer
from pandas import DataFrame
from typing import List, Tuple
from lupin_utils.error import ParamTypeError
from sklearn.preprocessing import LabelEncoder, OneHotEncoder


class MultipleColumnLabelEncoder(BaseTransformer):
    """
    多维度特征label编码
    """

    def __init__(self, *args, **kwargs):
        BaseTransformer.__init__(self, *args, **kwargs)

    def fit(self, x: DataFrame, y: DataFrame) -> (DataFrame, DataFrame):
        output = x.copy()
        if 'columns' in self.kwargs:
            columns = self.kwargs['columns']
            param_type = type(columns)
            if param_type not in [List, Tuple]:
                raise ParamTypeError(
                    f'class: {MultipleColumnLabelEncoder.__name__} needs param type: {List} or {Tuple} but got {param_type}')

            for col in columns:
                output[col] = LabelEncoder().fit_transform(output[col])

        else:
            for col_name, col in output.iteritems():
                output[col_name] = LabelEncoder().fit_transform(col)

        return output, y


class LupinOneHotEncoder(BaseTransformer):
    """
    one-hot encode
    """

    def __init__(self, *args, **kwargs):
        BaseTransformer.__init__(self, *args, **kwargs)
        self.args = args

    def fit(self, x: DataFrame, y: DataFrame) -> (DataFrame, DataFrame):
        return OneHotEncoder(*self.args, **self.kwargs).fit_transform(x), y
