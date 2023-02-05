from define import *
from typing import Callable, List, Set, Tuple, Iterable
import random

sent_cut = None


class cut:

    def __init__(self, sentence, remain_pos=None):

        self.sent = sentence
        self.cut_sent = sent_cut.cut(sentence, text=False)
        self.pos_set = set(range(len(self.cut_sent)))
        self.pos_ed = set()
        if remain_pos is None:
            self.now_poses = sent_cut.cut(sentence, text=True)
        else:
            self.now_poses = [i[0] for i in sent_cut.cut(sentence, text=True) if i[1] in remain_pos]

    def __iter__(self):
        return self.now_poses


class Select:
    def __init__(self, sentence: list[str]):
        self.sent = list(sentence)
        self.range = [i for i, key in enumerate(self.sent) if key not in pun]
        self.now_poses = self.range.copy()
        # self.iter = None

    def __iter__(self) -> Iterable[tuple[str, bool]]:
        _iter = ((word, True) if i in self.now_poses else (word, False) for i,word in enumerate(self.sent))
        return _iter


class RandomSelect(Select):
    def __init__(self, sencence: str, prob=0.4):
        """

        :param sencence:
        :param prob: 抽取的概率
        """
        Select.__init__(self, list(sencence))
        self.remain = self.range.copy()
        self.prob = prob

    def random(self, _measure="get_many") -> Select:
        return getattr(self, _measure, self.get_many)()

    def just_one(self):
        """
        一次一个，不重复
        """
        self.now_poses = [random.choice(self.remain)]
        self.remain.remove(self.now_poses[0])

        return self

    def get_many(self, num=0):
        """
        一次多个，允许重复

        :param num: 指定抽取个数
        :return:
        """
        if num == 0:
            k = int(len(self.range) * self.prob)
        else:
            k = num
        self.now_poses = random.choices(self.range, k=k)

        return self


class CutSelect(RandomSelect):
    def __init__(self, sent, prob=0.4):
        global sent_cut
        if sent_cut is None:
            from thulac import thulac
            sent_cut = thulac()
        sentence, self.tag = zip(*sent_cut.cut(sent))
        RandomSelect.__init__(self, sentence, prob)

    def get_tag_pos(self, tag: tuple[str] = ("a", "d", "id")):
        self.remain = [i for i in self.range if self.tag[i] in tag]
        return self


if __name__ == "__main__":
    a = RandomSelect(sentence_example)
    print(RandomSelect.__dict__["random"](a))
    # print(list(iter(a.get_many())))
    # print(list(iter(a.just_one())))
    # print(list(iter(CutSelect(sentence_example).get_tag_pos().get_many())))
