# -*- coding:utf-8 -*-
# @author: Henry
# @time: unknown
# @dec: 模型评估
# @WeChat: 13270593018
# @modify: 2019-05-15

from sklearn.metrics import accuracy_score
from sklearn.metrics import cohen_kappa_score
from sklearn.metrics import confusion_matrix
from sklearn.metrics import hamming_loss
from sklearn.metrics import precision_score
from sklearn.metrics import recall_score
from pandas import DataFrame
from numpy import ndarray

__all__ = [
    'score_accuracy',
    'score_cohen_kappa',
    'score_hamming_loss',
    'calculate_confusion_matrix'
]


def score_accuracy(y_true: DataFrame, y_pred: DataFrame) -> float:
    """
    计算准确率
    :param y_true:
    :param y_pred:
    :return:
    """
    return accuracy_score(y_true, y_pred)


def score_cohen_kappa(y_true: DataFrame, y_pred: DataFrame) -> float:
    """
    计算 Kappa系数 衡量数据的一致性
    :param y_true:
    :param y_pred:
    :return:
    """
    return cohen_kappa_score(y_true, y_pred)


def score_hamming_loss(y_true: DataFrame, y_pred: DataFrame) -> float:
    """
    计算hamming loss
    :param y_true:
    :param y_pred:
    :return:
    """
    return hamming_loss(y_true, y_pred)


def calculate_confusion_matrix(y_true: DataFrame, y_pred: DataFrame) -> ndarray:
    """
    计算混淆矩阵
    :param y_true:
    :param y_pred:
    :return:
    """
    return confusion_matrix(y_true, y_pred)


def score_precision(y_true: DataFrame, y_pred: DataFrame) -> float:
    """
    计算准确率
    :param y_true:
    :param y_pred:
    :return:
    """
    return precision_score(y_true, y_pred)


def score_recall(y_true: DataFrame, y_pred: DataFrame) -> float:
    """
    计算召回率
    :param y_true:
    :param y_pred:
    :return:
    """
    return recall_score(y_true, y_pred)
