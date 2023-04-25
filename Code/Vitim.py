import numpy as np
import random
from OpenAttack.tags import TAG_Chinese, TAG_Classification, Tag
from OpenAttack.victim.classifiers import Classifier


class StructBert(Classifier):

    @property
    def TAGS(self):
        return {TAG_Chinese, TAG_Classification, Tag("get_pred", "victim"), Tag("get_prob", "victim")}

    def __init__(self):
        from modelscope.pipelines import pipeline
        from modelscope.utils.constant import Tasks
        self.model = pipeline(Tasks.text_classification, 'damo/nlp_structbert_sentiment-classification_chinese-tiny')

    def get_pred(self, x: list[str]):
        """负面0 正面1"""
        from modelscope.pipelines import pipeline
        from modelscope.utils.constant import Tasks
        pred: list[dict[str, any]] = self.model(input=x)
        s = [i['scores'] for i in pred]
        return np.array([0 if i['labels'][0] == '负面' else 1 for i in pred])

    def get_prob(self, x):
        pred: list[dict[str, any]] = self.model(input=x)
        return np.array([np.array(i['scores']) if i['labels'][0] == '负面' else np.array(i['scores'][::-1]) for i in pred])


class Erlangshen(Classifier):

    @property
    def TAGS(self):
        return {TAG_Chinese, TAG_Classification, Tag("get_pred", "victim"), Tag("get_prob", "victim")}

    def __init__(self):
        from modelscope.pipelines import pipeline
        from modelscope.utils.constant import Tasks
        self.model = pipeline(Tasks.text_classification, 'Fengshenbang/Erlangshen-RoBERTa-110M-Sentiment')

    def get_pred(self, x: list[str]):
        """负面0 正面1"""
        x = x[0]
        pred: list[dict[str, any]] = self.model(input=x)
        s = [i['scores'] for i in pred]
        return np.array([i.index(max(i)) for i in s])

    def get_prob(self, x):
        pred: list[dict[str, any]] = self.model(input=x)
        return np.array([np.array(i['scores']) for i in pred])


class Paddle(Classifier):

    @property
    def TAGS(self):
        return {TAG_Chinese, TAG_Classification, Tag("get_pred", "victim"), Tag("get_prob", "victim")}

    def __init__(self):
        import paddlenlp
        self.model = paddlenlp.Taskflow("sentiment_analysis", model="uie-senta-nano", schema=['情感倾向[正向，负向]'])

    def get_pred(self, x: list[str]):
        """负面0 正面1"""
        pred: list[dict[str, any]] = self.model(x)
        try:
            label = [1 if i and i['情感倾向[正向，负向]'][0]['text'] == '正向' else 0 for i in pred]
            return label
        except KeyError:
            print(pred)
            return np.array([random.choice([0, 1])])  # 模拟最差情况

    def get_prob(self, x: list[str]):
        pred: list[dict[str, any]] = self.model(x)
        # pred=[{'情感倾向[正向，负向]': [{'text': '负向', 'probability': 0.977683341160116}]}, {}]
        try:
            probability = [i['情感倾向[正向，负向]'][0]['probability'] if i else 0.5 for i in pred]
            label = [1 if i and i['情感倾向[正向，负向]'][0]['text'] == '正向' else 0 for i in pred]
            return np.array([np.array([0, p]) if i == 1 else np.array([p, 0]) for i, p in zip(label, probability)])
        except KeyError:
            return np.array([np.array([0.5 + random.uniform(-0.1, 0.1), 0.5 + random.uniform(-0.1, 0.1)])])


if __name__ == '__main__':
    q = StructBert()#Paddle()
    print(q.get_pred(
        ['低价RMB4599,表面烤漆工艺好，整体配置不错，独显256M带有HDMI高清接口，自带喇叭声音不错，另有附送鼠标及包包',
         'asoc !!∠rffsd234😅😭😭🤬@#$#@#@%$@%ninaoiv']))
    print(q.get_prob(
        ['低价RMB4599,表面烤漆工艺好，整体配置不错，独显256M带有HDMI高清接口，自带喇叭声音不错，另有附送鼠标及包包',
         'ascc !!∠rffsd234@#$😅😭😭🤬#@#@%$@%naaoiv']))
