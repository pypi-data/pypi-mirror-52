# -*- coding:utf-8 -*-
# @author: Henry
# @time: 2019-05-16 10:24 am
# @dec: 多特征标签编码
# @WeChat: 13270593018

from sklearn.preprocessing import LabelEncoder, OneHotEncoder


class MultiColumnEncoder:
    def __init__(self, columns=None):
        self.columns = columns

    def transform(self, x):
        output = x.copy()
        if self.columns is not None:
            for col in self.columns:
                output[col] = LabelEncoder().fit_transform(output[col])
        else:
            for col_name, col in output.iteritems():
                output[col_name] = LabelEncoder().fit_transform(col)

        return output

    def fit_transform(self, x):
        return self.transform(x)
