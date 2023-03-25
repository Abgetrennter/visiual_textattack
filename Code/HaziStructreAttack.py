import random
from typing import Callable, List

from OpenAttack.attackers.classification import ClassificationAttacker, Classifier, ClassifierGoal
from OpenAttack.tags import TAG_Chinese, Tag

from CharDeal import char_flatten, char_insert
from define.HanZi import HanZi, Hanzi_dict
from define.Select import RandomSelect, CutSelect
from define.Transfer import english_replace, hanzi_plus_replace, hanzi_repalce, number_cn2an, time_replace


# from collections import namedtuple
#
# Measure = namedtuple("measure", ["choose", "attack"])


class HanziStructureAttack(ClassificationAttacker):
    @property
    def TAGS(self):
        return {TAG_Chinese, Tag("get_pred", "victim")}

    def __init__(self, prob: float = 0.4,
                 generations: int = 120,
                 choose_measure="get_many",
                 attack_measure=((char_flatten, 1),), **kwargs):
        """
        汉字分割攻击的简单实现，呜呜呜呜你们怎么都搞完了。

        :param prob: The probability of changing a char in a sentence. **Default:** 0.3
        :param generations: Maximum number of sentences generated per attack. **Default:** 120
        :param measure: The measure used to evaluate the attack. **Default:** ""
        """
        self.prob = prob
        self.generations = generations
        self.choose_measure = choose_measure
        self.attack_measure = []
        for func, w in attack_measure:
            # 便宜实现带权重函数选择
            self.attack_measure.extend([func] * w)
        self.__dict__.update(kwargs)

    def attack(self, victim: Classifier, sentence: str, goal: ClassifierGoal):
        # 初步攻击
        v = vit(victim, goal)

        s = english_replace(hanzi_plus_replace(hanzi_repalce(time_replace(number_cn2an(sentence)))))

        if v.judge(s):
            return s

        # _select = ImportantSelect(s)
        match self.choose_measure:
            case "just_one" | "get_many":
                _select = RandomSelect(sentence, prob=self.prob, just_chinese=True)
            case "important_simple_select":
                _select = CutSelect(sentence, self.prob, just_chinese=True).get_important(victim)
            case _:
                _select = Select(sentence, just_chinese=True)
        _select.compare(s)
        # _select.get_important(victim)
        for _ in range(self.generations):
            # 更具破坏性的攻击
            ans = "".join(uni_filter_char(c, __f, fs=self.attack_measure)
                          for c, __f in _select(self.choose_measure)())
            # for c, __f in _select.random(self.choose_measure)())

            # 超级攻击
            if v.judge(ans):
                return ans

            if _ > self.generations * 0.6:
                # print("超级攻击失败")
                ans = "".join(filter_char(i, random.random() < 0.1, char_insert) for i in ans)
                if v.judge(ans):
                    return ans

            # print(sentence, "\n", ans)


class vit:
    def __init__(self, vi, goal):
        self.vi = vi
        self.goal = goal

    def judge(self, ans):
        pred = self.vi.get_pred([ans])[0]
        return self.goal.check(ans, pred)


def filter_char(_char: str, _flag: bool, func: Callable[[str], str]) -> str:
    if _flag:
        # q = list[c]
        return "".join(func(_c) for _c in _char)
    else:
        return _char


def uni_filter_char(_str: str, _flag: bool, fs: List[Callable[[HanZi], str]]) -> str:
    if _flag:
        # q = list[c]
        _f = random.choice(fs)
        return "".join(_f(Hanzi_dict[char]) for char in _str)
    else:
        return _str
