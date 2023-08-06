import yaml
import os

config_path = os.path.abspath(os.path.join(__file__, '../../config/config.yaml'))


def read_key(key: str):
    print(config_path)
    config = yaml.load(open(config_path, 'r', encoding="utf-8"))
    res = config.get(key, None)
    if res is None:
        raise KeyError(f'{key} not in config.yaml')
    return res
