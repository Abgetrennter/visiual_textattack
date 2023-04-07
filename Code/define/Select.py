# from define import *
import random
from difflib import SequenceMatcher
from typing import Callable, Iterable

from .HanZi import judege_hanzi

sent_cut = None


# class cut:
#
#     def __init__(self, sentence, remain_pos=None):
#
#         self.ori_sent = sentence
#         self.cut_sent = sent_cut.cut(sentence, text=False)
#         self.pos_set = set(range(len(self.cut_sent)))
#         self.pos_ed = set()
#         if remain_pos is None:
#             self.select = sent_cut.cut(sentence, text=True)
#         else:
#             self.select = [i[0] for i in sent_cut.cut(sentence, text=True) if i[1] in remain_pos]
#
#     def __iter__(self):
#         return self.select

# 无状态->有状态
class Select:
    """
    默认情况下，所有的字符都被选的
    """

    def __init__(self, sentence: list[str], just_Chinese=False):
        # 所有序号按照最初的句子来
        self.ori_sent: tuple[str] = tuple(sentence)  # 原始句子,通过序号可以访问到原始的字词
        self.range: tuple[int] = tuple(range(len(self.ori_sent)))  # 0~len(self.ori_sent)
        self.new_sent = {i: self.ori_sent[i] for i in self.range}  # 通过原来的序号能够访问到修改后的字词
        self.select = list(self.range)  # 选中的序号,选择函数应该修改他
        # [i for i, key in enumerate(self.ori_sent) if key not in pun]

        # 可以被选择的范围
        if just_Chinese:
            self.remain = [i for i, key in enumerate(self.ori_sent) if judege_hanzi(key)]
        else:
            self.remain = list(self.range)

    def __getitem__(self, item: int) -> str:
        return self.ori_sent[item]

    def __call__(self, name):
        return getattr(self, name, self.default)

    def __iter__(self) -> Iterable[tuple[str, bool]]:
        _iter = ((word, True) if i in self.select else (word, False) for i, word in
                 self.new_sent.items())  # 被修改过的一定是False
        return _iter

    def default(self):
        return self

    def compare(self, r: str):
        # 和修改后的句子比较
        # len(self.ori_sent) >=len(r)

        for i in (i[1:] for i in SequenceMatcher(None, self.ori_sent, r).get_opcodes() if i[0] == 'replace'):
            # i[0]是原句子的起始位置，i[1]是原句子的结束位置，i[2]是修改后的句子的起始位置，i[3]是修改后的句子的结束位置
            self.new_sent[i[0]] = r[i[2]:i[3]]
            for index in range(i[0] + 1, i[1]):
                # 原句子中的剩余部分归零
                self.new_sent[index] = ""
            for index in range(i[0], i[1]):
                try:
                    self.remain.remove(index)
                except ValueError:
                    pass


class RandomSelect(Select):
    """
    随机选取部分字符
    """

    def __init__(self, sencence: str, prob=0.4, just_chinese=True):
        """
        :param sencence:
        :param prob: 抽取的概率
        """
        Select.__init__(self, list(sencence), just_Chinese=just_chinese)

        self.prob = prob

    # def random(self, _measure="get_many") -> Callable:
    #     f_dict = {
    #             "get_many": self.get_many,
    #             "just_one": self.just_one,
    #     }
    #     return f_dict.get(_measure, self.get_many)

    def just_one(self):
        """
        一次一个，不重复
        """
        self.select = [random.choice(self.remain)]
        self.remain.remove(self.select[0])

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
        self.select = random.choices(self.remain, k=k)

        return self


# class ChineseRandomSelect(RandomSelect):
#     def __init__(self, sencence: str, prob=0.4):
#         """
#         :param sencence:
#         :param prob: 抽取的概率
#         """
#         RandomSelect.__init__(self, sencence, prob)
#         self.remain = [i for i in self.range if judege_hanzi(self[i])]


class ImportantSelect(Select):
    def __init__(self, sencence: str, replace_max=0.2, just_chinese=True):
        """
        :param sencence:
        :param prob: 抽取的概率
        """
        # from OpenAttack.attackers.classification import ClassifierGoal
        Select.__init__(self, list(sencence), just_Chinese=just_chinese)
        # self.remain = [i for i in self.range if judege_hanzi(self[i])]
        self.times = 1
        self.replace_max = replace_max

    def get_important(self, prev):
        important = {i: 0.1 for i in self.remain}
        o_prob = prev.get_prob(["".join(self.ori_sent)])[0].tolist()
        o_k = (max(o_prob), o_prob.index(max(o_prob)))
        for i in self.remain:
            s = "".join(self.ori_sent[:i] + self.ori_sent[i + 1:])
            prob = prev.get_prob([s])[0].tolist()
            r_k = prob[o_k[1]]
            important[i] = o_k[0] - r_k

        self.remain.sort(key=lambda x: important[x], reverse=True)

    def important_simple_select(self, end=0):
        if end == 0:
            end = self.times
            if self.times < len(self.ori_sent) * self.replace_max:
                self.times += 1

        self.select = self.remain[:end]
        return self


    def important_random_select(self, end=0):
        if end == 0:
            end = int(self.times)
            if self.times < len(self.ori_sent) * self.replace_max:
                self.times += 0.75
        end = max(2, end)
        ra = self.remain[:min(self.times * 1.4, len(self.ori_sent))]
        random.shuffle(ra)

        self.select = ra[:end]
        return self


class CutSelect(ImportantSelect):
    def __init__(self, sencence: str, replace_max=0.8, just_chinese=True):
        ImportantSelect.__init__(self, sencence, replace_max, just_chinese=just_chinese)
        global sent_cut
        if sent_cut is None:
            from thulac import thulac
            sent_cut = thulac()
        self.words, self.tag = zip(*sent_cut.cut(sencence))
        # self.remain = list(range(len(self.words)))

    def get_important(self, prev):
        important = [0.1 for _ in range(len(self.words))]  # [0.1,]
        o_prob = prev.get_prob(["".join(self.ori_sent)])[0].tolist()
        o_k = (max(o_prob), o_prob.index(max(o_prob)))
        for i in range(len(self.words)):
            s = "".join(self.words[:i] + self.words[i + 1:])
            prob = prev.get_prob([s])[0].tolist()
            r_k = prob[o_k[1]]
            important[i] = o_k[0] - r_k
        num_words = [[i, []] for i in range(len(self.words))]  # [[1,2],[3,4]]
        p = 0
        for i, char in enumerate(self.ori_sent):
            if char not in self.words[p]:
                p += 1
            num_words[p][1].append(i)

        num_words.sort(key=lambda x: important[x[0]], reverse=True)
        self.remain = [ii for i in num_words for ii in i[1] if ii in self.remain]

        return self
        # self.remain.sort(key=lambda x: important[x], reverse=True)
        # [i for i, c in enumerate("".join(self.words)) if judege_hanzi(self[i])]


# class CutSelect(RandomSelect):
#     # 同形字替换会不会对切分产生影响?
#     def __init__(self, ori_sent, prob=0.4):
#         global sent_cut
#         if sent_cut is None:
#             from thulac import thulac
#             sent_cut = thulac()
#         sentence, self.tag = zip(*sent_cut.cut(ori_sent))
#         RandomSelect.__init__(self, sentence, prob)
#
#     def get_tag_pos(self, tag: tuple[str] = ("a", "n", "d", "id")):
#         self.remain = [i for i in self.range if self.tag[i] in tag]
#         return self


if __name__ == "__main__":
    from Const import sentence_example

    a = CutSelect(sentence_example)
    print(RandomSelect.__dict__["random"](a))
    # print(list(iter(a.get_many())))
    # print(list(iter(a.just_one())))
    # print(list(iter(CutSelect(sentence_example).get_tag_pos().get_many())))
