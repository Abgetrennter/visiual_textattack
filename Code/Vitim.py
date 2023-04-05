import numpy as np
import paddlenlp
from OpenAttack.tags import TAG_Chinese, TAG_Classification, Tag
from OpenAttack.victim.classifiers import Classifier
from modelscope.pipelines import pipeline
from modelscope.utils.constant import Tasks


class StructBert(Classifier):
    @property
    def TAGS(self):
        return {TAG_Chinese, TAG_Classification, Tag("get_pred", "victim")}

    def __init__(self):
        self.model = pipeline(Tasks.text_classification, 'damo/nlp_structbert_sentiment-classification_chinese-tiny')

    def get_pred(self, x: list[str]):
        """负面0 正面1"""
        pred: list[dict[str, any]] = self.model(input=x)
        s = [i['scores'] for i in pred]
        return [i.index(max(i)) for i in s]

    def get_prob(self, x):
        pred: list[dict[str, any]] = self.model(input=x)
        return [np.array(i['scores']) for i in pred]


class Erlangshen(Classifier):
    @property
    def TAGS(self):
        return {TAG_Chinese, TAG_Classification, Tag("get_pred", "victim")}

    def __init__(self):
        self.model = pipeline(Tasks.text_classification, 'Fengshenbang/Erlangshen-RoBERTa-110M-Sentiment')

    def get_pred(self, x: list[str]):
        """负面0 正面1"""
        x = x[0]
        pred: list[dict[str, any]] = self.model(input=x)
        s = [i['scores'] for i in pred]
        return [i.index(max(i)) for i in s]

    def get_prob(self, x):
        pred: list[dict[str, any]] = self.model(input=x)
        return [np.array(i['scores']) for i in pred]


class Paddle(Classifier):

    @property
    def TAGS(self):
        return {TAG_Chinese, TAG_Classification, Tag("get_pred", "victim")}

    def __init__(self):
        self.model = paddlenlp.Taskflow("sentiment_analysis", model="uie-senta-nano", schema=['情感倾向[正向，负向]'])

    def get_pred(self, x: list[str]):
        """负面0 正面1"""
        pred: list[dict[str, any]] = self.model(x)
        label = [1 if i['情感倾向[正向，负向]'][0]['text'] == '正向' else 0 for i in pred]
        return label

    def get_prob(self, x: list[str]):
        pred: list[dict[str, any]] = self.model(x)
        probability = [i['情感倾向[正向，负向]'][0]['probability'] for i in pred]
        label = [1 if i['情感倾向[正向，负向]'][0]['text'] == '正向' else '负向' for i in pred]
        return [np.array([0, p]) if i == '正向' else np.array([p, 0]) for i, p in zip(label, probability)]


if __name__ == '__main__':
    q = Paddle()
    print(q.get_pred(['我是中国人', '你才是中国人']))
    print(q.get_prob(['我是中国人','你才是中国人']))
