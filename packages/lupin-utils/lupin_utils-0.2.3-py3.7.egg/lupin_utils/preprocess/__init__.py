# -*- coding:utf-8 -*-
# @author: Henry
# @time: 2019-05-13 2:52 pm
# @dec: 预处理工具
# @file: lupin_utils


"""
    1、标准化
    2、最小-最大规范化
    3、规范化
    4、特征二值化
"""

import json
from sklearn.preprocessing import scale, normalize, Binarizer
from numpy import array
from pandas.io.json import json_normalize
from pandas import DataFrame

__all__ = [
    'standardization',
    'normalization',
    'binarizer',
    'normalize_json'
]


def standardization(data) -> array:
    """
    标准化
    :param data:
    :return:
    """
    return scale(data)


def normalization(data, norm: str = 'l2') -> array:
    """
    规范化
    :param data:
    :param norm: 默认l2
    :return:
    """
    return normalize(data, norm)


def binarizer(data) -> array:
    """
    特征二值化
    :param data:
    :return:
    """
    return Binarizer(data)


def normalize_json(data: json) -> DataFrame:
    """
    返回平坦化格式数据 通过访问列来获取所有数据
    :param data:
    :return:
    """
    return json_normalize(data)
