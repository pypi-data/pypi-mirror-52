import logging
import os
import pickle
import copy
import json
from typing import Dict, Tuple
from .data_operate import resolve_click_expose_data
from lupin_utils.config import read_config
from lupin_utils.error import ConfigError
from .libsvm import load_libsvm

__all__ = [
    'load_data',
    'load_libsvm'
]

CHECK = ['input', 'features', 'label', 'output']


def load_pickle_data(filepath: str):
    if not os.path.exists(filepath):
        logging.error(f'loading data file error, error file: {filepath}')
        return

    with open(filepath, 'rb') as f:
        res = []
        while True:
            try:
                res.append(pickle.load(f))
            except:
                break
        return res


def load_json_data(filepath: str):
    if not os.path.exists(filepath):
        logging.error(f'loading data file error, error file: {filepath}')
        return

    with open(filepath, 'rb') as f:
        res = json.loads(f.read())
        return res


def _load(filepath: str, param_config: Dict) -> Tuple:
    file_type = param_config['input']['file_type']
    config_features = param_config['features']['names'].replace(' ', '').split(',')
    raw_save_path = param_config['output']['raw_file']
    feature_save_path = param_config['output']['feature_file']
    label_name = param_config['label']['name']
    raw_file = ''
    feature_file = ''
    if file_type == 'pickle':
        res = load_pickle_data(filepath)
        raw_file, feature_file = resolve_click_expose_data(res, config_features, raw_save_path, feature_save_path,
                                                           label_name)
    if file_type.lower() == 'json':
        res = load_json_data(filepath)
        raw_file, feature_file = resolve_click_expose_data(res, config_features, raw_save_path, feature_save_path,
                                                           label_name)
    return raw_file, feature_file


# 加载数据 转换成向量
def load_data(source_data_path: str, config_name: str) -> Tuple:
    """
    :param source_data_path: 数据文件路径
    :param config_name: 配置参数名称
    :return:
    """
    if not os.path.exists(source_data_path):
        raise ConfigError(f'loading data from: {source_data_path}, file not exists')

    param_config = read_config(config_name)

    if len(param_config) == 0:
        raise ConfigError(f'loading data config:{param_config} failed, config is empty')

    check = copy.deepcopy(CHECK)
    # 做一配置参数次检查
    for k in param_config:
        if k in check:
            check.remove(k)
    if len(check) != 0:
        raise ConfigError(f'config missing params: {str(check)}')

    # 从这个地方开始交给子函数处理
    # 加载数据
    raw_file, feature_file = _load(source_data_path, param_config)
    return raw_file, feature_file
