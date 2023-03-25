import csv
from os import path as osp
import paddlenlp
import datasets

from Code.define import DATAPATH


def luntai() -> list[dict[str, any]]:
    li = []
    # content_id,content,subject,sentiment_value,sentiment_word
    for row in csv.reader(open(osp.join(*DATAPATH, "轮胎.csv"), encoding="utf-8")):
        li.append({'x': row[1], 'y': row[-2]})
    return li


def dianping(begin=0, end=-1) -> list[dict[str, str]]:
    li = []
    # sentence,label,dataset
    ymap = ['负', '正']
    for row in csv.reader(open(osp.join(*DATAPATH, "点评.csv"), encoding="utf-8")):
        li.append({'x': row[0].replace('\\n', ''), 'y': ymap[int(row[1])]})
    return li[begin:end]


def amazon_reviews(begin=10, end=20):
    def dataset_mapping(x):
        return {
                "x": x["review_body"],
                "y": x["stars"],
        }

    return datasets.load_dataset("amazon_reviews_multi", 'zh', split=f"train[{begin}:{end}]").map(function=dataset_mapping)


def paddle(begin=0, end=-1):

    train_ds = paddlenlp.datasets.load_dataset('chnsenticorp', splits=['train'])
    li = []
    for i in train_ds:
        li.append({'x': i['text'], 'y': i['label']})
    return li[begin:end]


if __name__ == "__main__":
    print(dianping()[:5])
