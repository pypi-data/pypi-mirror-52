# -*- coding:utf-8 -*-
# @author: Henry
# @time: 2019-05-17 11:28 am
# @dec: 加载原始文件数据 原始文件数据类型json
# @WeChat: 13270593018

import os
import pickle
import json
from lupin_utils.error import FileNotExistsError
from pandas.io.json import json_normalize
from pandas import DataFrame

__all__ = [
    'FileOperate'
]


class FileOperate:
    def __init__(self):
        pass

    @staticmethod
    def transform_pickle_as_json(filepath: str, savepath: str) -> json:
        if not os.path.exists(filepath):
            raise FileNotExistsError(f'pickle file not exists, file path:{filepath}')

        res = []
        with open(filepath, 'rb') as fp:
            while True:
                try:
                    res.append(pickle.load(fp))
                except:
                    break

        with open(savepath, 'w') as fj:
            fj.write(json.dumps(res))

    @staticmethod
    def load_json(filepath: str) -> json:
        if not os.path.exists(filepath):
            raise FileNotExistsError(f'json file not exists, file path:{filepath}')

        with open(filepath, 'rb') as file:
            return json.loads(file.read())

    @staticmethod
    def normalize_json(data: json) -> DataFrame:
        try:
            return json_normalize(data)
        except Exception as e:
            raise e
