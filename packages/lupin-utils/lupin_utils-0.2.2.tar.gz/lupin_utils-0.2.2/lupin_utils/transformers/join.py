# -*- coding:utf-8 -*-
# @author: Henry
# @time: 2019-05-20 10:23 pm
# @dec: dataframe 连接
# @WeChat: 13270593018

import json
from pandas import DataFrame
from typing import List, Tuple, Dict
from .base import JoinData
from sklearn.preprocessing import LabelEncoder


def get_index(idx: int, value: List[int]) -> int:
    """
    计算偏移量
    :param idx:
    :param value:
    :return:
    """
    offset = 0
    if idx == 0:
        return idx
    for i in range(0, idx - 1):
        offset += value[i]

    return offset


def calculate_range_label(value: float, range_array: List):
    for i in range_array:
        if i < 0:
            raise Exception('range label exits value negative')
    label = 0
    for i in range_array:
        if value < i:
            return label
        else:
            label += 1

    return label


def file_write(fp: str, way: str, data: str):
    with open(fp, way) as f:
        if data == '':
            f.write(data)
        else:
            f.write(data + '\n')


class Extraction:
    """
   提取源文件
    """

    def __init__(self, direct_config_features: List, indirect_config_features: List, indirect_config_sub_features: List,
                 indirect_config_sub_features_type: List, top: int, positive: str, others: Dict):
        self.direct_features_dict = {}
        self.indirect_features_dict = {}
        self.direct_config_features = direct_config_features
        self.indirect_config_features = indirect_config_features
        self.indirect_config_sub_features = indirect_config_sub_features
        self.indirect_config_sub_features_type = indirect_config_sub_features_type
        self.top = top
        self.others = others
        self.multiple_fields = []
        self.single_fields = []
        self.continuous_fields = []
        self.positive = positive

    @staticmethod
    def extract__(raw_data: DataFrame, config_features: List, raw_path: str, coded_path: str):
        """
        抽取字段
        :param raw_data:
        :param config_features
        :param raw_path:
        :param coded_path:
        :return:
        """
        columns = raw_data.columns
        # 去除不需要的列元素
        drop_columns = []
        for name in columns:
            if name not in config_features:
                drop_columns.append(name)

        # 保存计算的值
        data = raw_data.drop(columns=drop_columns, axis=1)
        columns = data.columns
        # 排序一次
        columns = sorted(columns)
        # 设置特征映字典
        features = {col: set() for col in columns}
        for col_name in columns:
            col = [str(item) for item in data[col_name]]
            for c in col:
                features[col_name].add(c)

        # 对多维特征进行一次排序
        features = {k: sorted(list(features[k])) for k in features}

        # 文件初始化为空
        file_write(raw_path, 'w', '')
        file_write(coded_path, 'w', '')

        # 写入原始数据 该数据存入顺序为 配置提取字段的顺序
        for seg in config_features:
            file_write(raw_path, 'a', f'{seg}:')
            file_write(raw_path, 'a', f'{str(features[seg])}')

        # 编码值 行循环计算 这里索引值就是编码值
        for _, row in data.iterrows():
            index_lable = []
            # 拿到每一个特征编码值反编码
            for col in config_features:
                value = data[col]
                code_value = features[col].index(value)
                index_lable.append(code_value)

            line = ''
            for i in range(0, len(index_lable)):
                v = index_lable[i]
                line += f'{i}:{v} '

            file_write(coded_path, 'a', line)

    def direct_extract(self, raw_data: DataFrame):
        """
        抽取原始值并且编码 存储方式为dict
        :param raw_data:
        :return:
        """
        config_features = self.direct_config_features
        columns = raw_data.columns
        # 去除不需要的列元素
        drop_columns = []
        for name in columns:
            if name not in config_features:
                drop_columns.append(name)

        # 保存计算的值
        data = raw_data.drop(columns=drop_columns, axis=1)
        columns = data.columns
        # 设置特征集合
        features = {col: {} for col in columns}
        columns = data.columns
        for col in columns:
            cols = list(data[col])
            label_code = LabelEncoder().fit_transform(cols)
            for i in range(0, len(cols)):
                features[col][cols[i]] = int(label_code[i])

        self.direct_features_dict = features
        # # 文件初始化为空
        # file_write(raw_path, 'w', '')
        # file_write(coded_path, 'w', '')
        # file_write(raw_path, 'a', json.dumps(features))

    @staticmethod
    def split_dimension(config_features: List, config_types: List) -> Tuple:
        """
        拆分单维特征和多维特征的字段以及连续字段
        :return:
        """

        multiple_fields = []
        single_fields = []
        continuous_fields = []

        if len(config_features) != len(config_types):
            raise Exception('length not matches')
        for i in range(0, len(config_features)):
            cn = config_features[i]
            cnt = config_types[i]
            if cnt.lower() == 'list':
                multiple_fields.append(cn)
            elif cnt.lower() == 'continuous':
                continuous_fields.append(cn)
            else:
                single_fields.append(cn)

        return multiple_fields, single_fields, continuous_fields

    def indirect_extract(self, raw_data: DataFrame):
        """
        间接提取的字段值 目前只能为单个字段 使用时用List表示
        提取单个
        :return:
        """
        segments = self.indirect_config_features
        config_features = self.indirect_config_sub_features
        config_type = self.indirect_config_sub_features_type
        top = self.top

        prefix_feature = segments[0]

        columns = raw_data.columns
        # 去除不需要的列元素
        drop_columns = []
        for name in columns:
            if name not in segments:
                drop_columns.append(name)

        # 保存计算的值
        data = raw_data.drop(columns=drop_columns, axis=1)

        # 抽取出单维度字段和多维度字段
        multiple_fields, single_fields, continuous_fields = self.split_dimension(config_features, config_type)

        self.multiple_fields = multiple_fields
        self.single_fields = single_fields
        self.continuous_fields = continuous_fields

        # 给所有特征编码 并且存储
        single_features = {sf: set() for sf in single_fields}
        multiple_features = {mf: set() for mf in multiple_fields}
        for item in data[prefix_feature]:
            top_data = item[0:top]
            # 遍历前top每一条数据
            for td in top_data:
                # 获取每一个single_field 值
                for s in single_fields:
                    value = td[0][s]
                    single_features[s].add(value)

                for m in multiple_fields:
                    value_list = td[0][m]
                    for f in value_list:
                        multiple_features[m].add(f)

        # 处理单维度特征
        single_feature_dict = {sf: {} for sf in single_fields}
        for f in single_features:
            raw = list(single_features[f])
            label_code = LabelEncoder().fit_transform(raw)
            for i in range(0, len(raw)):
                k = raw[i]
                v = label_code[i]
                single_feature_dict[f][k] = v

        # 给multiple_features 做一次值处理 主要是为了处理列位置
        for k, v in multiple_features.items():
            multiple_features[k] = {}
            for i, element in enumerate(v):
                multiple_features[k][element] = i

        indirect_features_dict = {prefix_feature: {}}
        for k in single_feature_dict:
            indirect_features_dict[prefix_feature][k] = single_feature_dict[k]

        for k in multiple_features:
            indirect_features_dict[prefix_feature][k] = multiple_features[k]

        self.indirect_features_dict = indirect_features_dict

    def layout(self):
        """
        排版libsvm的排列格式
        :return:
        """
        column_range = []
        column_range += self.direct_config_features
        for f in self.single_fields:
            column_range.append(f'{self.indirect_config_features[0]}.{f}')

        print(column_range)

    def save_raw(self, raw_path: str):
        """
        保存原始值以及其对应关系
        顺序依次为 直接提取参数顺序 + 加间接提取单维度字段 + 间接提取连续字段 + 间接提取多维度字段
        其中各个配置顺序按给定的配置顺序编排

        :return:
        :return:
        """
        file_write(raw_path, 'w', '')
        columns = self.direct_config_features + [f'{self.indirect_config_features[0]}.{i}' for i in
                                                 self.single_fields + self.continuous_fields + self.multiple_fields]
        file_write(raw_path, 'a', json.dumps(columns))

        file_write(raw_path, 'a', json.dumps(self.direct_features_dict))

        d = {}
        fixed_prefix = self.indirect_config_features[0]
        d[fixed_prefix] = {}
        for k in self.multiple_fields:
            d[fixed_prefix][k] = self.indirect_features_dict[self.indirect_config_features[0]][k]

        file_write(raw_path, 'a', json.dumps(d))

    def extract(self, raw_data: DataFrame, code_path: str):
        file_write(code_path, 'w', '')
        drop_columns = []
        columns = raw_data.columns
        save_columns = self.direct_config_features + self.indirect_config_features
        for col in columns:
            if col not in save_columns:
                drop_columns.append(col)

        data = raw_data.drop(columns=drop_columns, axis=1)

        for _, row in data.iterrows():
            direct_value = []
            # 提取直接字段特征
            for col_name in self.direct_config_features:
                # 如果是直接提取的数据
                value = row[col_name]
                direct_value.append(self.direct_features_dict[col_name][value])

                # print(direct_dict)
            # 该字段只有一个
            indirect_col_name = self.indirect_config_features[0]
            indirect_value = row[indirect_col_name]
            top_data = indirect_value[0:self.top]
            # 计算实际取到的长度 用于行扩展
            for item in top_data:
                # 单维度处理
                single_value = []
                for index_name in self.single_fields:
                    # 拿到编码值
                    value = item[0][index_name]
                    single_value.append(self.indirect_features_dict[indirect_col_name][index_name][value])

                # 连续数据处理
                continuous_value = []
                for index_name in self.continuous_fields:
                    value = item[0][index_name]
                    discrete_rule = self.others[index_name]
                    if index_name == 'sales_stat':
                        encode_value = calculate_range_label(float(value['30']['salesCount']), discrete_rule)
                    else:
                        encode_value = calculate_range_label(float(value), discrete_rule)
                    continuous_value.append(encode_value)

                single_line = ''
                to_file = direct_value + single_value + continuous_value
                for i in range(0, len(to_file)):
                    single_line += f'{i}:{to_file[i]} '

                # 多维度处理
                tmp_length = len(to_file)
                multiple_line = ''
                for index_name in self.multiple_fields:
                    value = item[0][index_name]
                    value = set(value)
                    label = []
                    for tag in value:
                        # 计算出编码值
                        label.append(self.indirect_features_dict[indirect_col_name][index_name][tag])
                    label = sorted(label)
                    for l in label:
                        multiple_line += f'{l + tmp_length}:{1} '

                    tmp_length += len(self.indirect_features_dict[indirect_col_name][index_name])
                line = single_line + multiple_line
                # 标签输出值
                if item[1] == self.positive:
                    line = f'{1}  ' + line
                else:
                    line = f'{0}  ' + line

                file_write(code_path, 'a', line)
