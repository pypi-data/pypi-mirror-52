import datetime
from zipfile import ZipFile


def show(t: datetime.datetime = datetime.datetime.now()):
    print(t.strftime("%Y%m%d%H%M%S"))


def test_zip(fp: str, sp: str):
    with ZipFile(fp, 'r') as myzip:
        myzip.write(sp)


if __name__ == '__main__':
    # show()
    fp = '/Users/henry/PycharmProjects/lupin_utils/models/best_estimator'
    sp = '/Users/henry/PycharmProjects/lupin_utils/model/best_estimator'
    test_zip(fp, sp)
