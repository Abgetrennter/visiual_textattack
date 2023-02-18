from define import HanziStructure
from define.load import hanzi_splits, hanzi_structure_dict
from utils import char_flatten


class Part:
    def __init__(self, c: str | list[str] = None):
        self.struct: HanziStructure = hanzi_structure_dict.get(c, HanziStructure.独体)
        if self.struct == HanziStructure.独体:
            self.count = 1
            self.sub = ()
        self.count: int
        if isinstance(c, str):
            if c in char_count:
                self.count = char_count[c]
            else:
                self.count = sum(self.count for self in self.sub)

        self.sub: tuple[Part]


from collections import Counter
import matplotlib.pyplot as plt


def pie(_d):
    plt.pie(_d.values(),
            labels=[int(_) for _ in _d.keys()],  # 设置饼图标签
            # autopct='%.2f%%',  # 格式化输出百分比
            )
    plt.show()


# _ = Counter(len(i) for i in hanzi_splits.values())
# print(_)
print(sorted(
        (t for t in hanzi_splits.items()
         if (len(t[1]) > 2
             and
             hanzi_structure_dict.get(t[0], HanziStructure.独体)!=HanziStructure.独体)
         ),
        key=lambda x: len(x[1]), reverse=True))
# pie(Counter(len(i) for i in hanzi_splits.values()))
