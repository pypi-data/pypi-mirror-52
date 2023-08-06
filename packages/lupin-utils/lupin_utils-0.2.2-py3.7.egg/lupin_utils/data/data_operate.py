from typing import List, Tuple
from .operate import label_and_one_hot_encode
import gc


def resolve_click_expose_data(data: List, config_features: List, raw_save_path: str,
                              feature_save_path: str, label_name: str
                              ) -> Tuple:
    """
    保存格式: label1 feature1:value1 feature2:value2 feature3:value3 ......
    :param data:  读取的原始的值 这个是一个list 每个元素里面有相应的dict 存放需要读取的特征
    :param config_features: 配置里需要提取的特征
    :param raw_save_path: 原始数据存储文件名
    :param feature_save_path: 特征编码转换存储的位置
    :param label_name: label 字段
    :return:
    """
    # 提取所有feature 按类目配置提取的字段提取 存储方式 [set(), set(), set()] 每一个set() 对应一个需要提取的配置的特征
    features = {}
    for f in config_features:
        features[f'{f}'] = set()

    for item in data:
        for k, v in item.items():
            if k == 'response_body':
                for target in v['target']:
                    # 遍历指定feature
                    for f in config_features:
                        try:
                            for sub_feature in target[0][f]:
                                features[f].add(sub_feature)
                        except:
                            continue

    for k, v in features.items(): features[k] = list(v)

    label_encoder = label_and_one_hot_encode(features, raw_save_path)
    check_label = []
    with open(feature_save_path, 'w') as file:
        file.write('')
    for item in data:
        for k, v in item.items():
            if k == 'response_body':
                for target in v['target']:
                    try:
                        # 提取label 这里为spu
                        label = target[0][label_name]
                        if label not in check_label:
                            check_label.append(label)
                            encoder_list = []
                            for fea in config_features:
                                sub_feature = [f'{fea}.{x}' for x in list(set(target[0][fea]))]
                                encoder_list += list(label_encoder.transform(sub_feature))
                            sorted_encoder = sorted(encoder_list)
                            with open(feature_save_path, 'a+') as file:
                                if label < 200000:
                                    line = f'{0} '
                                else:
                                    line = f'{1} '
                                # line = f'{label} '
                                for i in sorted_encoder:
                                    line = line + f' {i}:{1}'
                                file.write(line + '\n')
                        else:
                            pass
                    except:
                        continue

    gc.collect()

    return raw_save_path, feature_save_path
