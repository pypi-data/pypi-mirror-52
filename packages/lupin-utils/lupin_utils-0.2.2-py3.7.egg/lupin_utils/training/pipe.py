# -*- coding:utf-8 -*-
# @author: Henry
# @time: 2019-05-14 10:53 am
# @dec: 使用sklearn PipeLine 做封装
# @WeChat: 13270593018


from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from typing import List, Tuple
from pandas.core.frame import DataFrame


def fit(x_train: DataFrame, y_train: DataFrame, transformers: List, models: List[Tuple]) -> Pipeline:
    """
    训练模型
    :param x_train: 训练样本X
    :param y_train: 训练样本y
    :param transformers: 数据转换器 一般做处理加载数据里的坏值 例如Nan值 不需要处理 transformers=[]
    :param models: 模型
                例如：models = [('classifier', RandomForestClassifier())] 选择随机森林分类器
                如果是包含了多个模型， 则按照pipeline的处理顺序依次处理 例如:
                    models = [('classifier_1', MyClassifier_1), ('classifier_2', MyClassifier_2),....,('classifier_n', MyClassifier_n)]
                则 classifier_1 计算出的结果传递给classifier_2,计算结果依次传递
    :return: 返回pipeline
    """
    steps = []
    if len(transformers) != 0:
        preprocessor = ColumnTransformer(
            transformers=transformers
        )
        steps.append(('preprocessor', preprocessor))
    for m in models:
        steps.append(m)
    rf = Pipeline(steps=steps)

    # 训练模型
    rf.fit(x_train, y_train)

    return rf
