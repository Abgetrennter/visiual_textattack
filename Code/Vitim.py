import numpy as np

from OpenAttack.tags import TAG_Chinese, TAG_Classification, Tag
from OpenAttack.victim.classifiers import Classifier
from modelscope.pipelines import pipeline
from modelscope.utils.constant import Tasks
import paddlenlp


class StructBert(Classifier):
    @property
    def TAGS(self):
        return {TAG_Chinese, TAG_Classification, Tag("get_pred", "victim")}

    def __init__(self):
        self.model = pipeline(Tasks.text_classification, 'damo/nlp_structbert_sentiment-classification_chinese-tiny')

    def get_pred(self, x):
        """负面0 正面1"""
        x = x[0]
        pred: dict[str, any] = self.model(input=x)
        s = pred['scores']
        return pred['labels'][s.index(max(s))][0]

    def get_prob(self, x):
        x = x[0]
        pred: dict[str, any] = self.model(input=x)
        return [np.array(pred['scores'])]



class Erlangshen(Classifier):
    @property
    def TAGS(self):
        return {TAG_Chinese, TAG_Classification, Tag("get_pred", "victim")}

    def __init__(self):
        self.model = pipeline(Tasks.text_classification, 'Fengshenbang/Erlangshen-RoBERTa-110M-Sentiment')

    def get_pred(self, x):
        """负面0 正面1"""
        x = x[0]
        pred: dict[str, any] = self.model(input=x)
        s = pred['scores']
        return pred['labels'][s.index(max(s))][0]

    def get_prob(self, x):
        x = x[0]
        pred: dict[str, any] = self.model(input=x)
        return [np.array(pred['scores'])]



class Paddle(Classifier):

    @property
    def TAGS(self):
        return {TAG_Chinese, TAG_Classification, Tag("get_pred", "victim")}

    def __init__(self):
        self.model = paddlenlp.Taskflow("sentiment_analysis", model="uie-senta-nano")

    def get_pred(self, x):
        """负面0 正面1"""
        x = x[0]
        pred: dict[str, any] = self.model(x)[0]
        return pred['label']

    def get_prob(self, x):
        x = x[0]
        pred: dict[str, any] = self.model(x)[0]
        return [np.array((0, pred['score']))]


if __name__ == '__main__':
    q = StructBert()
    print(q.get_pred(['我是中国人']))
    print(q.get_pred_prob(['我是中国人']))
