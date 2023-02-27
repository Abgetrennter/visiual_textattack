# from define import *
import random
from typing import Callable, Iterable

from .HanZi import judege_hanzi

sent_cut = None


# class cut:
#
#     def __init__(self, sentence, remain_pos=None):
#
#         self.sent = sentence
#         self.cut_sent = sent_cut.cut(sentence, text=False)
#         self.pos_set = set(range(len(self.cut_sent)))
#         self.pos_ed = set()
#         if remain_pos is None:
#             self.now_poses = sent_cut.cut(sentence, text=True)
#         else:
#             self.now_poses = [i[0] for i in sent_cut.cut(sentence, text=True) if i[1] in remain_pos]
#
#     def __iter__(self):
#         return self.now_poses

# 无状态->有状态
class Select:
    """
    默认情况下，所有的字符都被选的
    """

    def __init__(self, sentence: list[str]):
        self.sent = list(sentence)
        self.range = tuple(range(len(self.sent)))
        self.remain = list(self.range)
        # [i for i, key in enumerate(self.sent) if key not in pun]
        self.now_poses = list(self.range)
        # self.iter = None

    def __getitem__(self, item: int) -> str:
        return self.sent[item]

    def compare(self, o: str):
        # len(o) >=len(self.sent)
        for i, c in enumerate(self.sent):
            if c not in o:  # 可以认为修改后的词不可能在原句子中
                if i in self.remain:
                    self.remain.remove(i)

    def __iter__(self) -> Iterable[tuple[str, bool]]:
        _iter = ((word, True) if i in self.now_poses else (word, False) for i, word in enumerate(self.sent))
        return _iter


class RandomSelect(Select):
    """
    随机选取部分字符
    """

    def __init__(self, sencence: str, prob=0.4):
        """
        :param sencence:
        :param prob: 抽取的概率
        """
        Select.__init__(self, list(sencence))

        self.prob = prob

    def random(self, _measure="get_many") -> Callable:
        f_dict = {
                "get_many": self.get_many,
                "just_one": self.just_one,
        }
        return f_dict.get(_measure, self.get_many)

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
            k = int(len(self.remain) * self.prob)
        else:
            k = num
        self.now_poses = random.choices(self.remain, k=k)

        return self


class ChineseRandomSelect(RandomSelect):
    def __init__(self, sencence: str, prob=0.4):
        """
        :param sencence:
        :param prob: 抽取的概率
        """
        RandomSelect.__init__(self, sencence, prob)
        self.remain = [i for i in self.range if judege_hanzi(self[i])]


class ImportantSelect(Select):
    def __init__(self, sencence: str, replace_max=0.2):
        """
        :param sencence:
        :param prob: 抽取的概率
        """
        # from OpenAttack.attackers.classification import ClassifierGoal
        Select.__init__(self, list(sencence))
        self.remain = [i for i in self.range if judege_hanzi(self[i])]
        self.times = 1
        self.replace_max = replace_max

    def get_important(self, prev):
        important = {i: 0.1 for i in self.remain}
        o_prob = prev.get_prob(["".join(self.sent)])[0].tolist()
        o_k = (max(o_prob), o_prob.index(max(o_prob)))
        for i in self.remain:
            s = "".join(self.sent[:i] + self.sent[i + 1:])
            prob = prev.get_prob([s])[0].tolist()
            r_k = prob[o_k[1]]
            important[i] = o_k[0] - r_k

        self.remain.sort(key=lambda x: important[x], reverse=True)

        ...

    def simple_select(self, end=0):
        if end == 0:
            end = self.times
            if self.times < len(self.sent) * self.replace_max:
                self.times += 1

        self.now_poses = self.remain[:end]
        return self

        # class CutSelect(RandomSelect):
        #     # 同形字替换会不会对切分产生影响?
        #     def __init__(self, sent, prob=0.4):
        #         global sent_cut
        #         if sent_cut is None:
        #             from thulac import thulac
        #             sent_cut = thulac()
        #         sentence, self.tag = zip(*sent_cut.cut(sent))
        #         RandomSelect.__init__(self, sentence, prob)
        #
        #     def get_tag_pos(self, tag: tuple[str] = ("a", "n", "d", "id")):
        #         self.remain = [i for i in self.range if self.tag[i] in tag]
        #         return self


if __name__ == "__main__":
    a = RandomSelect(sentence_example)
    print(RandomSelect.__dict__["random"](a))
    # print(list(iter(a.get_many())))
    # print(list(iter(a.just_one())))
    # print(list(iter(CutSelect(sentence_example).get_tag_pos().get_many())))
