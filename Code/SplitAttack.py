from OpenAttack.attackers.classification import ClassificationAttacker, Classifier, ClassifierGoal
from OpenAttack.tags import TAG_Chinese, Tag
from typing import Callable, Iterator, List
from define import *
from utils import *


# from collections import namedtuple
#
# Measure = namedtuple("measure", ["choose", "attack"])


class SplitAttack(ClassificationAttacker):
    @property
    def TAGS(self):
        return {TAG_Chinese, Tag("get_pred", "victim")}

    def __init__(self, prob: float = 0.4,
                 generations: int = 120,
                 choose_measure="getmany",
                 attack_measure="char_flatten"):
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

    def attack(self, victim: Classifier, sentence: str, goal: ClassifierGoal):
        state = State(sentence, prob=self.prob)  # 记录上一次替换的位置
        for _ in range(self.generations):
            # ans = sentece_prob(sentence, char_flatten, self.prob)
            ans = "".join(state.char_iter(char_flatten, self.choose_measure))
            pred = victim.get_pred([ans])[0]

            if goal.check(ans, pred):
                return ans


class State:
    """不重复的随机数"""

    def __init__(self, sentence: str, **kwargs):
        self.sent = sentence
        self.pos_set = set(range(len(sentence)))
        # self.pos_list = list(self.pos_set)
        self.now_poses: List[int] | None = None
        self.dict = kwargs

    def get_pos(self, _measure: str, again=0):
        _state = list(self.pos_set)
        if len(_state) == 0:
            raise RuntimeError("No more pos to change")
        match _measure:
            case "just_one":
                self.now_poses = [random.choice(_state)]
                self.pos_set -= set(self.now_poses)
            case "get_many" | _:
                if again == 0:
                    k = int(len(_state) * self.dict["prob"])
                else:
                    k = again
                self.now_poses = random.choices(_state, k=k)

    # def now_pos(self, pos: List[int]):
    #     self.now_poses = pos
    #     self.pos_set.difference(pos)

    def char_iter(self, _f: Callable[[str], str], measure=""):
        ret = list(self.sent)
        self.get_pos(measure)
        while True:
            false_count = 0
            for index, c in enumerate(ret[:]):
                if index in self.now_poses:
                    try:
                        ret[index] = _f(c)
                    except ValueError:
                        false_count += 1

            if false_count == 0:
                break
            else:
                self.get_pos(measure, again=false_count)
        return ret

    # def __str__(self):
    #     return "".join(self.char_iter(char_flatten))


if __name__ == '__main__':
    a = State("旨在定义一个稳定、最小化、可移植的语言版本以及相应的标准库，以用于教学和作为将来扩展的基础。", prob=0.25)
    for __measure in ["just_one", "get_many"]:
        print(measure)
        for _f in [char_flatten, char_mars]:
            print(_f.__name__)
            for _ in range(5):
                print("".join(a.char_iter(_f, __measure)))
