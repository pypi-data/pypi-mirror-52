# -*- coding:utf-8 -*-
# @author: Henry
# @time: 2019-05-17 5:52 pm
# @dec: 处理配置数据
# @WeChat: 13270593018


from lupin_utils.config import read_config
from pandas import DataFrame
from typing import Dict, List


class Preprocessor:
    """
    只用于抽出配置需要的直接数据和间接数据 其中的行列扩展操作留给转换器操作
    """

    def __init__(self, name: str):
        self.direct_features: Dict = {}
        self.indirect_features: Dict = {}
        self.label: str = ''
        self.get_config(name)

    def get_config(self, name: str):
        """
        获取配置文件
        :param name:
        :return:
        """
        configs = read_config(name)
        extraction = configs['extraction']
        self.direct_features = extraction['direct_features']
        self.indirect_features = extraction['indirect_features']
        self.label = configs['label']

    def resolve_direct_features(self, data: DataFrame) -> DataFrame:
        """
        解析直接获取的字段
        :param data:
        :return:
        """
        names = self.direct_features['names'].replace(' ', '').split(',')
        columns = data.columns
        drop_columns = []
        for col_name in columns:
            if col_name not in names:
                drop_columns.append(col_name)

        return data.drop(columns=drop_columns, axis=1)

    def resolve_indirect_features(self, data: DataFrame) -> DataFrame:
        """
        解析间接获取的字段
        :param data:
        :return:
        """
        name = self.indirect_features.get('names', None)
        dtype = self.indirect_features.get('type', None)
        top = self.indirect_features.get('top', None)
        sub_features = self.indirect_features.get('sub_features', None)
        sub_features_type = self.indirect_features.get('sub_features_type', None)
        if sub_features is not None:
            sub_features = sub_features.replace(' ', '').split(',')

        if sub_features_type is not None:
            sub_features_type = sub_features_type.replace(' ', '').split(',')

        extend_dimension_list = []
        print(sub_features)
        count = 0
        for sft in sub_features_type:
            if sft.lower() == 'list':
                extend_dimension_list.append(sub_features[count])
            count += 1

        drop_data = data[name].to_frame()
        set_columns = [f'{name}.{sub_name}' for sub_name in sub_features]
        print(set_columns)
        print(extend_dimension_list)

        return drop_data
