from define import HanziStructure, pianpang
from define.count import char_count
from define.load import hanzi_splits, hanzi_structure_dict, sp_chars
from pic import Font2pic, compare

_font = Font2pic()


# from utils import char_flatten


class PartDict:
    """缓存用,避免生成大量重复的"""

    def __init__(self):
        self._dict: dict[str, Part] = {}

    def __ceil__(self, c):
        return self[c]

    def double(self, c, cc):
        return self[c], self[cc]

    def __getitem__(self, item):
        if item not in self._dict:
            if isinstance(item, tuple) and len(item) == 1:
                self._dict[item[0]] = Part(item[0])
            else:
                self._dict[item] = Part(item)

        return self._dict[item]

    def __setitem__(self, key, value):
        self._dict[key] = value

    def __repr__(self):
        _s = ""
        for i, k in enumerate(self._dict):
            _s += f"{i}:{self._dict[k]}\n"
        return _s


character_dict = PartDict()


class Part:
    def __init__(self, c: str | tuple[str] = None):
        self.c = c
        self.count = 0
        self.struct = HanziStructure.独体
        self.sub: tuple = (Part, Part)
        # 糊弄IDE检查

        if isinstance(c, str):
            self.char_deal(c)
        elif isinstance(c, tuple):
            if len(c) == 1:
                self.c = c[0]
                self.char_deal(c[0])
            else:
                self.list_deal(c)
        else:
            raise ValueError("Part: 无效的参数")

    @staticmethod
    def pianpang(parts):
        if len(parts) == 2:
            return character_dict.double(parts[0], parts[1])
        elif parts[-1] in pianpang:
            return character_dict.double(parts[:-1], parts[-1])
        else:
            # 默认切分最左边,理论上是找到能成字的最大部分,但是太麻烦了
            return character_dict.double(parts[0], parts[1:])

    def char_deal(self, c: str):
        self.struct = hanzi_structure_dict.get(c, HanziStructure.独体)
        parts: tuple[str] = hanzi_splits.get(c, ())
        if self.struct == HanziStructure.独体:
            self.count = char_count.get(c, 5)
            self.sub = ()
            return
        if len(parts) == 2:
            self.sub = character_dict.double(parts[0], parts[1])
        elif len(parts) > 2:
            # 一般认为最左边和最右边是偏旁,部首表验证一下
            self.sub = self.pianpang(parts)
        else:
            self.struct = HanziStructure.独体
            self.count = char_count.get(c, 5)
            self.sub = ()
            return
            # raise ValueError("Part: 无效的参数")
        if c in char_count:
            self.count = char_count[c]
        else:
            self.count = sum(self.count for self in self.sub)

    def list_deal(self, c: tuple[str]):
        self.sub = self.pianpang(c)
        self.count = sum(self.count for self in self.sub)
        self.struct = HanziStructure.组合

    def __iter__(self):
        return iter(self.sub)

    def my_iter(self):
        _q = [self]
        while _q:
            _ = _q.pop(0)
            yield _.c
            if _.sub:
                _q.extend(_.sub)

    def __repr__(self):
        return f"{self.c}->Part({self.count}, {self.struct.name}, {''.join(i.c for i in self.sub)})"

    # def __getitem__(self, item):
    #     return self.sub[item]


def cal_mars(less: str, more: str):
    """谁爱处理报错谁处理"""
    less = character_dict[less]
    more = character_dict[more]
    out = [i for i in more.sub if i is not less]


def cal_递归(origin: Part, replacer: Part):
    """
    递归计算两个字的相似度,不考虑形如 "也" "他" 这种的情况,假定 origin 是原始字, replacer 是目标.
    :param origin:
    :param replacer:
    :return:
    """
    if origin.struct == HanziStructure.独体 or replacer.struct == HanziStructure.独体:
        if replacer.struct == HanziStructure.组合 or origin.struct == HanziStructure.组合:
            # 懒得写解释了
            return 0
        else:
            return compare(_font.draw(origin.c), _font.draw(replacer.c))
    return (cal_递归(origin.sub[0], replacer.sub[0]) * origin.sub[0].count
            +
            cal_递归(origin.sub[1], replacer.sub[1]) * origin.sub[1].count) \
        / (origin.count * (abs(origin.struct.value - replacer.struct.value) + 1))


# map(hanzi_splits, character_dict)
# __ = [character_dict[i] for i in hanzi_splits.keys()]
if __name__ == '__main__':
    # q = list()
    # for i in q:
    #     # fp.write(i + '\n')
    #     _ = character_dict[i]

    s = sp_chars['平']

    # import pickle
    #
    # pickle.dump(character_dict._dict, open("character_dict.pickle", "wb"))
    # character_dict['噙']

    # print(list(character_dict['噙'].my_iter()))
    l = []
    for i1 in range(len(s)):
        for i2 in range(i1 + 1, len(s)):
            l.append((s[i1], s[i2], cal_递归(character_dict[s[i1]], character_dict[s[i2]])))
    l.sort(key=lambda x: x[2], reverse=True)
    print(l)
    # print(cal_递归(a, b))
    # p = [a]
    # while p:
    #     a = p.pop()
    #     print(a.c, a.count, a.struct)
    #     if a.sub:
    #         p.extend(a.sub)
# print(a.count, a.struct, a.sub)
# from collections import Counter
# import matplotlib.pyplot as plt
#
#
# def pie(_d):
#     plt.pie(_d.values(),
#             labels=[int(_) for _ in _d.keys()],  # 设置饼图标签
#             # autopct='%.2f%%',  # 格式化输出百分比
#             )
#     plt.show()
#
#
# # _ = Counter(len(i) for i in hanzi_splits.values())
# # print(_)
# print(sorted(
#         (t for t in hanzi_splits.items()
#          if (len(t[1]) > 2
#              and
#              hanzi_structure_dict.get(t[0], HanziStructure.独体) != HanziStructure.独体)
#          ),
#         key=lambda x: len(x[1]), reverse=True))
# pie(Counter(len(i) for i in hanzi_splits.values()))
