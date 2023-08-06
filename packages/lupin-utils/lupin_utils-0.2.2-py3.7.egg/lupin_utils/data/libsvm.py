# -*- coding:utf-8 -*-
# @author: Henry
# @time: 2019-05-14 09:44 am
# @dec: 加载libsvm格式数据
# @WeChat: 13270593018

from sklearn.datasets import load_svmlight_file
from sklearn.model_selection import train_test_split
from typing import Tuple
from lupin_utils.error import FileNotExistsError
import os
import logging
import pandas as pd


def load_libsvm(filepath: str, test_size: float = 0.25, random_state=None) -> Tuple:
    """
    加载libsvm 数据并且进行转换
    :param filepath: libsvm 数据文件
    :param test_size: 测试数据占比
    :param random_state: int, RandomState instance or None, optional (default=None)
        If int, random_state is the seed used by the random number generator;
        If RandomState instance, random_state is the random number generator;
        If None, the random number generator is the RandomState instance used
        by `np.random`.
    :return: 如果float 大于零 则返回长度为4的Tuple (X_train, X_test, y_train, y_test) 否则返回长度为2Tuple (X, y)
    """
    if not os.path.exists(filepath):
        logging.error(f'file - {filepath} - not exists')
        raise FileNotExistsError()

    x_load, y_load = load_svmlight_file(filepath)
    x = pd.DataFrame(x_load.todense())
    y = pd.DataFrame(y_load)
    if test_size > 0.0:
        x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=test_size, random_state=random_state)
        return x_train, x_test, y_train, y_test

    return x, y
