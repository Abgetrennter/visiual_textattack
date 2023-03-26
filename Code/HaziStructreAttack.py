import random
from typing import Callable, List, Sequence
import numpy as np
from OpenAttack.attackers.classification import ClassificationAttacker, Classifier, ClassifierGoal
from OpenAttack.tags import TAG_Chinese, Tag

from CharDeal import char_flatten, char_insert
from define.HanZi import HanZi, Hanzi_dict
from define.Select import RandomSelect, CutSelect
from define.Transfer import english_replace, hanzi_plus_replace, hanzi_repalce, number_cn2an, time_replace

from sklearn.gaussian_process import GaussianProcessRegressor
from bayes_opt import BayesianOptimization, UtilityFunction

utility = UtilityFunction(kind="ucb", kappa=2.5, xi=0.0)


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
                 attack_measure=((char_flatten, 1.0),),
                 dymatic=False,
                 **kwargs):
        """
        汉字分割攻击的简单实现，呜呜呜呜你们怎么都搞完了。

        :param prob: The probability of changing a char in a sentence. **Default:** 0.3
        :param generations: Maximum number of sentences generated per attack. **Default:** 120
        :param measure: The measure used to evaluate the attack. **Default:** ""
        """
        self.prob = prob
        self.generations = generations
        self.choose_measure = choose_measure
        self.attack_measure = attack_measure
        self.dymatic = dymatic
        # for func, w in attack_measure:
        #     # 便宜实现带权重函数选择
        #     self.attack_measure.extend([func] * w)
        self.__dict__.update(kwargs)

        self.dymatic_measure: List[list[Callable[[HanZi], str], float]] = [[*i] for i in self.attack_measure]

        # 用多元回归计算每个函数的权重
        self.p_combo: List[List[float]] = []  # prob_combo(dymatic_measure)
        self.aacs: List[float] = []
        self.optimizer = BayesianOptimization(
                f=None,
                pbounds={i[0].__name__: (1, 5) for i in self.dymatic_measure},
                verbose=len(self.dymatic_measure),
                random_state=1,
        )

    def attack(self, victim: Classifier, sentence: str, goal: ClassifierGoal):

        # v = vit(victim, goal)
        # 初步攻击
        s = english_replace(hanzi_plus_replace(hanzi_repalce(time_replace(number_cn2an(sentence)))))
        if goal.check(s, victim.get_pred([s])[0]):
            return s

        ori_p = max(victim.get_prob([s])[0])
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
            ans = "".join(uni_filter_char(c, __f, fs=self.dymatic_measure)
                          for c, __f in _select(self.choose_measure)())
            # for c, __f in _select.random(self.choose_measure)())

            # 超级攻击

            if _ < 5:  # 每次攻击前5轮进行优化
                if goal.check(ans, victim.get_pred([ans])[0]):
                    return ans
            else:
                p = victim.get_prob([ans])[0].tolist()
                pmax = max(p)
                label = p.index(pmax)
                if goal.check(ans, label):
                    delta = ori_p
                else:
                    delta = pmax - ori_p
                self.optimizer.register(params=prob_combo(self.dymatic_measure), target=delta)
                str_float = self.optimizer.suggest(utility)
                print(str_float)
                for name, prob in str_float.items():
                    for i in self.dymatic_measure:
                        if i[0].__name__ == name:
                            i[1] = prob

            if _ > self.generations * 0.6:
                # print("超级攻击失败")
                ans = "".join(filter_char(i, random.random() < 0.1, char_insert) for i in ans)
                if goal.check(ans, victim.get_pred([ans])[0]):
                    return ans

            # print(sentence, "\n", ans)


def prob_combo(m: List[tuple | list[Callable[[HanZi], str], float]]) -> dict[str, float]:
    return {i[0].__name__: i[1] for i in m}


class vit:
    def __init__(self, vi, goal):
        self.vi = vi
        self.goal = goal
        self.last_prob = 0.5

    def judge(self, ans):
        return self.goal.check(ans, self.vi.get_pred([ans])[0])


def filter_char(_char: str, _flag: bool, func: Callable[[str], str]) -> str:
    if _flag:
        # q = list[c]
        return "".join(func(_c) for _c in _char)
    else:
        return _char


def uni_filter_char(_str: str, _flag: bool, fs: List[tuple | list[Callable[[HanZi], str], float]]) -> str:
    if _flag:
        # q = list[c]
        _f = weight_choice(fs)
        return "".join(_f(Hanzi_dict[char]) for char in _str)
    else:
        return _str


def weight_choice(item_weight: List[tuple[any, float]]) -> any:
    _sum = sum(w for _, w in item_weight)
    _rand = random.uniform(0, _sum)
    for i, w in item_weight:
        _rand -= w
        if _rand < 0:
            return i
    return item_weight[-1][0]

# class Bys:
#     def __init__(self):
#         self.GP = GaussianProcessRegressor()
#
#
# def PI(x, gp, y_max, xi):
#     mean, std = gp.predict(x, return_std=True)
#     z = (mean - y_max - xi) / std
#     return norm.cdf(z)
#
#
# def EI(x, gp, y_max, xi):
#     mean, std = gp.predict(x, return_std=True)
#     a = (mean - y_max - xi)
#     z = a / std
#     return a * norm.cdf(z) + std * norm.pdf(z)
#
#
# def UCB(x, gp, kappa):
#     mean, std = gp.predict(x, return_std=True)
#     return mean + kappa * std
#
#
# def acq_max(ac, gp, y_max, bounds, random_state, n_warmup=10000):
#     # 随机采样选择最大值
#     x_tries = np.random.uniform(bounds[:, 0], bounds[:, 1],
#                                 size=(n_warmup, bounds.shape[0]))
#     ys = ac(x_tries, gp=gp, y_max=y_max)
#     x_max = x_tries[ys.argmax()]
#     max_acq = ys.max()
#     return x_max
