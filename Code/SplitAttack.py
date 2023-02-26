from define.transfer import *

from define.cut import *
from utils import *

from OpenAttack.attackers.classification import ClassificationAttacker, Classifier, ClassifierGoal
from OpenAttack.tags import TAG_Chinese, Tag


# from collections import namedtuple
#
# Measure = namedtuple("measure", ["choose", "attack"])


class SplitAttack(ClassificationAttacker):
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
        for f, w in attack_measure:
            # 便宜实现带权重函数选择
            self.attack_measure.extend([f] * w)
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
                          #for c, __f in _select.simple_select())
            for c, __f in _select.random(self.choose_measure)())

            pred = victim.get_pred([ans])[0]
            # 超级攻击
            if goal.check(ans, pred):
                # print(sentence, "\n", ans)
                return ans


if __name__ == '__main__':
    # thu1 = thulac.thulac()  # 默认模式
    # text = thu1.cut("我爱北京天安门", text=False)  # 进行一句话分词
    # print(text)
    select = RandomSelect(sentence_example, prob=0.4)
    for __measure in ["just_one", "get_many"]:
        print(__measure)
        for _f in [char_flatten, char_mars]:
            print(_f.__name__)
            for _ in range(5):
                print("".join(_f(char) if flag else char for char, flag in select.random(__measure)()))