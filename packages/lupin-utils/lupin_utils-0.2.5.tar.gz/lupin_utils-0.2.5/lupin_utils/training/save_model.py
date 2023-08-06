# -*- coding:utf-8 -*-
# @author: Henry
# @time: 2019-05-14 4:40 pm
# @dec: 保存训练好的模型
# @WeChat:13270593018

import os
from sklearn.externals import joblib
from sklearn.pipeline import Pipeline

FILE_ROOT = os.getcwd()

MODEL_PATH = os.path.abspath(os.path.join(FILE_ROOT, 'models'))


def save_training_model(model: Pipeline, model_name: str):
    """
    保存训练的模型
    :param model:
    :param model_name:
    :return:
    """
    file_path = os.path.join(MODEL_PATH, model_name)
    joblib.dump(model, file_path, compress=1)
