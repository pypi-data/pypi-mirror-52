# -*- coding:utf-8 -*-
# @author: Henry
# @time: 2019-05-13 10:45 am
# @dec: one-hot encode
# @file: lupin_utils
# @WeChat: 13270593018

from typing import List, Dict
from sklearn.preprocessing import LabelEncoder
import json


def label_and_one_hot_encode(data: Dict, raw_file: str) -> LabelEncoder:
    """
    :param data:  k, v（str，List）分别为 需要提取的字段和对应的特征列表
    :param raw_file 原始值保存的位置
    :return:
    """
    raw = []
    for k, v in data.items():
        for fea in v:
            raw.append(f'{k}.{fea}')

    label_encoder = LabelEncoder()
    labels = label_encoder.fit_transform(raw)

    # 做一次排序
    labels = list(labels)
    length = len(labels)

    raw_range = []

    for i in range(length):
        index = labels.index(i)
        raw_range.append(raw[index])

    # save
    with open(raw_file, 'w') as file:
        json_data = json.dumps(raw_range)
        file.write(json_data)

    return label_encoder
