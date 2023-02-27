import random
from typing import Callable, List

from OpenAttack.attackers.classification import ClassificationAttacker, Classifier, ClassifierGoal
from OpenAttack.tags import TAG_Chinese, Tag

from CharDeal import char_flatten
from define.HanZi import HanZi, Hanzi_dict
from define.Select import ChineseRandomSelect
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
        # state = State(sentence, prob=self.prob)  # 记录上一次替换的位置
        # _select = RandomSelect(sentence, prob=self.prob)
        # _select=CutSelect(sentence,prob=self.prob).get_tag_pos()
        #
        # 初步攻击
        s = english_replace(hanzi_plus_replace(hanzi_repalce(time_replace(number_cn2an(sentence)))))
        # _select = ImportantSelect(s)
        _select = ChineseRandomSelect(s, prob=self.prob)
        _select.compare(sentence)
        # _select.get_important(victim)
        for _ in range(self.generations):
            # ans = sentece_prob(sentence, char_flatten, self.prob)

            # ans = "".join(filter_char(*_, __f=self.attack_measure) for _ in _select.random(self.choose_measure))
            # ans = "".join(uni_filter_char(c, __f, fs=self.attack_measure)
            #               for c, __f in _select.random(self.choose_measure)())
            # ans = hanzi_repalce(ans)
            # 更具破坏性的攻击
            ans = "".join(uni_filter_char(c, __f, fs=self.attack_measure)
                          # for c, __f in _select.simple_select())
                          for c, __f in _select.random(self.choose_measure)())

            pred = victim.get_pred([ans])[0]
            # 超级攻击
            if goal.check(ans, pred):
                # print(sentence, "\n", ans)
                return ans


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
