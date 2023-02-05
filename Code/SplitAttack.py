from OpenAttack.attackers.classification import ClassificationAttacker, Classifier, ClassifierGoal
from OpenAttack.tags import TAG_Chinese, Tag
from typing import Callable, Iterator, List
from define import *
from utils import *
from cut import *


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
                 attack_measure=char_flatten, **kwargs):
        """
        汉字分割攻击的简单实现，希望还没人搞过。

        :param prob: The probability of changing a char in a sentence. **Default:** 0.3
        :param generations: Maximum number of sentences generated per attack. **Default:** 120
        :param measure: The measure used to evaluate the attack. **Default:** ""
        """
        self.prob = prob
        self.generations = generations
        self.choose_measure = choose_measure
        self.attack_measure = attack_measure
        self.__dict__.update(kwargs)

    def attack(self, victim: Classifier, sentence: str, goal: ClassifierGoal):
        # state = State(sentence, prob=self.prob)  # 记录上一次替换的位置
        _select = RandomSelect(sentence, prob=self.prob)
        # _select=CutSelect(sentence,prob=self.prob).get_tag_pos()
        for _ in range(self.generations):
            # ans = sentece_prob(sentence, char_flatten, self.prob)

            ans = "".join(filter_char(*_, f=self.attack_measure) for _ in _select.random(self.choose_measure))
            pred = victim.get_pred([ans])[0]

            if goal.check(ans, pred):
                # print(sentence, "\n", ans)
                return ans


# class State:
#     """不重复的随机数"""
#
#     def __init__(self, sentence: str, **kwargs):
#         """
#
#         :param sentence: 一个列表，每个元素是一个字符或者词语
#         :param kwargs:
#         """
#         self.sent = sentence
#         self.range = list((i for i in range(len(sentence)) if sentence[i] not in pun))
#         self.pos_set = set(self.range)
#         self.pos_ed = set()
#         self.now_poses: List[int] | None = None
#         self.__dict__.update(kwargs)
#
#     def get_from_cut(self):
#         """从分词结果中获取"""
#         pass
#
#     def get_pos_random(self, _measure: str, again=0):
#         """
#
#         :param _measure: 选择的方式
#         :param again: 重新抽取的个数
#         :return:
#         """
#         _state = list(self.pos_set - self.pos_ed)
#         if len(_state) == 0:
#             raise RuntimeError("No more pos to change")
#         match _measure:
#             case "just_one":
#                 self.now_poses = [random.choice(_state)]
#                 self.pos_ed.add(self.now_poses[0])
#             case "get_many":
#                 if again == 0:
#                     k = int(len(self.range) * self.prob)
#                 else:
#                     k = again
#                 self.now_poses = random.choices(self.range, k=k)
#                 # self.pos_ed.update(self.now_poses)
#
#             # case "just_one2":
#
#     # def now_pos(self, pos: List[int]):
#     #     self.now_poses = pos
#     #     self.pos_set.difference(pos)
#
#     def char_iter(self, _f: Callable[[str], str], measure="", over=False):
#         """
#         不该出现在这的函数，但是我懒得写了
#         :param _f: 处理函数
#         :param measure: 处理方法
#         :param over: 是否坚持缺少的字符
#         :return:
#         """
#         ret = self.sent.copy()
#         self.get_pos_random(measure)
#         while True:
#             false_count = 0
#             for index, c in enumerate(ret[:]):
#                 if index in self.now_poses:
#                     try:
#                         ret[index] = _f(c)
#                     except ValueError:
#                         if over:
#                             false_count += 1
#             if false_count == 0:
#                 break
#             else:
#                 self.get_pos_random(measure, again=false_count)
#         return ret
#
#     # def __str__(self):
#     #     return "".join(self.char_iter(char_flatten))


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
                print("".join(_f(char) if flag else char for char, flag in select.__dict__[__measure]()))
