import OpenAttack
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import numpy as np
import datasets
# nltk.set_proxy(r'http://127.0.0.1:7890/')
# # nltk.download()
# import ssl
#
# try:
#     _create_unverified_https_context = ssl._create_unverified_context
# except AttributeError:
#     pass
# else:
#     ssl._create_default_https_context = _create_unverified_https_context
#
# nltk.download('vader_lexicon')
import urllib.request

# proxy = urllib.request.ProxyHandler({'http': "127.0.0.1:7890", 'https': "127.0.0.1:7890"})
# opener = urllib.request.build_opener(proxy, urllib.request.HTTPHandler)
# urllib.request.install_opener(opener)


def make_model():
    class MyClassifier(OpenAttack.Classifier):
        def __init__(self):
            try:
                self.model = SentimentIntensityAnalyzer()
            except LookupError:
                nltk.download('vader_lexicon')
                self.model = SentimentIntensityAnalyzer()

        def get_pred(self, input_):
            return self.get_prob(input_).argmax(axis=1)

        def get_prob(self, input_):
            ret = []
            for sent in input_:
                res = self.model.polarity_scores(sent)
                prob = (res["pos"] + 1e-6) / (res["neg"] + res["pos"] + 1e-6)
                ret.append(np.array([1 - prob, prob]))
            return np.array(ret)

    return MyClassifier()


def dataset_mapping(x):
    return {
            "x": x["sentence"],
            "y": 1 if x["label"] > 0.5 else 0,
    }


def main():
    print("New Attacker")
    attacker = OpenAttack.attackers.PWWSAttacker()

    print("Build model")
    clsf = make_model()
    # datasets.load_dataset("stanfordSentimentTreebank")
    dataset = datasets.load_dataset("sst", split="train[:100]").map(function=dataset_mapping)

    print("Start attack")
    attack_eval = OpenAttack.AttackEval(attacker, clsf, metrics=[
            OpenAttack.metric.Fluency(),
            OpenAttack.metric.GrammaticalErrors(),
            OpenAttack.metric.SemanticSimilarity(),
            OpenAttack.metric.EditDistance(),
            OpenAttack.metric.ModificationRate()
    ])
    attack_eval.eval(dataset, visualize=True, progress_bar=True)


if __name__ == "__main__":
    main()