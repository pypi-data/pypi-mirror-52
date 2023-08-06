# @author: henry
# @time: 2019-05-10
# @dec: 数据编码

from typing import Dict, List
from pandas.io.json import json_normalize
from pandas import DataFrame

__all__ = [
    'encode_feature'
]


def encode_feature(filepath: str, category: str, raw_features: List, start: int) -> (str, Dict, int):
    """
    :param filepath: 原始值写入写入的文件路径
    :param category: 类目
    :param raw_features: 原始特征值
    :param start: 标签编码开始值
    :return: 返回编码的截止值
    """
    i = start
    d = {}
    encoder = []

    for f in raw_features:
        d[f] = i
        encoder.append(i)
        i += 1

    with open(filepath, 'a') as file:
        file.write(f'{category}:' + '\n')
        file.write(f'   {raw_features}' + '\n')
        file.write(f'   {encoder}' + '\n')

    return category, d, i


# 实现点访问
def dict_to_json_normalize(d: Dict, filepath: str = '') -> DataFrame:
    """
    :param d:
    :param filepath: 需要保存成csv的路径
    :return:
    """
    res = json_normalize(d)
    if filepath != '':
        res.to_csv(filepath)
    return res
