from define import HanziStructure, pianpang
from define.count import char_count
from define.load import hanzi_splits, hanzi_structure_dict
from pic import Font2pic, compare
_font = Font2pic()


# from utils import char_flatten


class PartDict:
    def __init__(self):
        self._dict: dict[str, Part] = {}

    def double(self, c, cc):
        return self[c], self[cc]

    def __getitem__(self, item):
        temp: Part
        if item not in self._dict:
            temp = Part(item)
            self._dict[item] = temp
        else:
            temp = self._dict[item]
        return temp

    def __setitem__(self, key, value):
        self._dict[key] = value


my_dict = PartDict()


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
                self.c=c[0]
                self.char_deal(c[0])
            else:
                self.list_deal(c)
        else:
            raise ValueError("Part: 无效的参数")

    @staticmethod
    def pianpang(parts):
        if parts[-1] in pianpang:
            return my_dict.double(parts[:-1], parts[-1])
        else:
            # 默认切分最左边,理论上是找到能成字的最大部分,但是太麻烦了
            return my_dict.double(parts[0], parts[1:])

    def char_deal(self, c: str):
        self.struct = hanzi_structure_dict.get(c, HanziStructure.独体)
        parts: tuple[str] = hanzi_splits.get(c, ())
        if self.struct == HanziStructure.独体:
            self.count = char_count.get(c, 5)
            self.sub = ()
            return
        if len(parts) == 2:
            self.sub = my_dict.double(parts[0], parts[1])
        elif len(parts) > 2:
            # 一般认为最左边和最右边是偏旁,部首表验证一下
            self.sub = self.pianpang(parts)
        else:
            raise ValueError("Part: 无效的参数")
        self.count = char_count.get(c, sum(self.count for self in self.sub))

    def list_deal(self, c: tuple[str]):
        self.sub = self.pianpang(c)
        self.count = sum(self.count for self in self.sub)
        self.struct = HanziStructure.组合


def cal(c1, c2):
    return


def cal_递归(c1: Part, c2: Part):
    if c1.struct == HanziStructure.独体 or c2.struct == HanziStructure.独体:
        if c2.struct == HanziStructure.组合 or c1.struct == HanziStructure.组合:
            return 0
        else:
            return compare(_font.draw(c1.c), _font.draw(c2.c))

    return (cal_递归(c1.sub[0], c2.sub[0]) * c1.sub[0].count
            +
            cal_递归(c1.sub[1], c2.sub[1]) * c1.sub[1].count) \
        / (c1.count * (abs(c1.struct.value - c2.struct.value) + 1))


if __name__ == '__main__':
    _font = Font2pic()
    s = "拍啪帕柏把"
    l = []
    for i1 in range(len(s)):
        for i2 in range(i1 + 1, len(s)):
            l.append((s[i1], s[i2], cal_递归(my_dict[s[i1]], my_dict[s[i2]])))
    l.sort(key=lambda x: x[2],reverse=True)
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
