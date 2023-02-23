from Code.utils import cal_递归
from define.HanZi import han_dict
from define.load import sp_chars
from pic import Font2pic

_font = Font2pic()


# from utils import char_flatten


# map(hanzi_splits, han_dict)
# __ = [han_dict[i] for i in hanzi_splits.keys()]
if __name__ == '__main__':
    # q = list()
    # for i in q:
    #     # fp.write(i + '\n')
    #     _ = han_dict[i]

    s = sp_chars['平']

    # import pickle
    #
    # pickle.dump(han_dict._dict, open("han_dict.pickle", "wb"))
    # han_dict['噙']

    # print(list(han_dict['噙'].my_iter()))
    l = []
    for i1 in range(len(s)):
        for i2 in range(i1 + 1, len(s)):
            l.append((s[i1], s[i2], cal_递归(han_dict[s[i1]], han_dict[s[i2]])))
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
