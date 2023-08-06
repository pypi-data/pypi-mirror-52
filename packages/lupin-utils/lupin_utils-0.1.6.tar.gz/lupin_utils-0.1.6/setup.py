from setuptools import setup, find_packages

setup(
    name='lupin_utils',
    version='0.1.6',
    author='Henry',
    license='MIT',
    find_packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'Cython==0.29.10',
        'numpy==1.16.4',
        'scikit-learn==0.21.2',
        'pandas==0.24.2',
        'mlflow==0.8.2',
        'xgboost==0.90',
        'fastFM==0.2.11',
        'odps==3.5.1',
        'redis==3.2.1',
        'pymysql==0.9.3',
        'pymongo==3.7.2',
        'pyyaml==5.1',
        'scipy==1.1.0',
        'implicit==0.3.8',
        'gensim==3.5.0',
        'tensorflow==1.14.0',
        'oss2==2.6.1',
        'matplotlib==3.1.1',
        'psutil==5.6.3',
        'pyhdfs== 0.2.2'
    ]

)
