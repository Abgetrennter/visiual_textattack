from .const import pianpang
from .count import char_count
from .load import hanzi_splits, hanzi_structure_dict
from .structure import HanziStructure


class HanZiDict:
    """缓存用,避免生成大量重复的"""

    def __init__(self):
        self._dict: dict[str, HanZi] = {}

    def __ceil__(self, c):
        return self[c]

    def double(self, c, cc):
        return self[c], self[cc]

    def __getitem__(self, item):
        if item not in self._dict:
            if isinstance(item, tuple) and len(item) == 1:
                self._dict[item[0]] = HanZi(item[0])
            else:
                self._dict[item] = HanZi(item)

        return self._dict[item]

    def __setitem__(self, key, value):
        self._dict[key] = value

    def __repr__(self):
        _s = ""
        for i, k in enumerate(self._dict):
            _s += f"{i}:{self._dict[k]}\n"
        return _s


han_dict = HanZiDict()


class HanZi:
    def __init__(self, c: str | tuple[str] = None):
        self.c = c
        self.count = 0
        self.struct = HanziStructure.独体
        self.sub: tuple = (HanZi, HanZi)
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
            raise ValueError("HanZi: 无效的参数")

    @staticmethod
    def pianpang(parts):
        if len(parts) == 2:
            return han_dict.double(parts[0], parts[1])
        elif parts[-1] in pianpang:
            return han_dict.double(parts[:-1], parts[-1])
        else:
            # 默认切分最左边,理论上是找到能成字的最大部分,但是太麻烦了
            return han_dict.double(parts[0], parts[1:])

    def char_deal(self, c: str):
        self.struct = hanzi_structure_dict.get(c, HanziStructure.独体)
        parts: tuple[str] = hanzi_splits.get(c, ())
        if self.struct == HanziStructure.独体:
            self.count = char_count.get(c, 5)
            self.sub = ()
            return
        if len(parts) == 2:
            self.sub = han_dict.double(parts[0], parts[1])
        elif len(parts) > 2:
            # 一般认为最左边和最右边是偏旁,部首表验证一下
            self.sub = self.pianpang(parts)
        else:
            self.struct = HanziStructure.独体
            self.count = char_count.get(c, 5)
            self.sub = ()
            return
            # raise ValueError("HanZi: 无效的参数")
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
        return f"{self.c}->HanZi({self.count}, {self.struct.name}, {''.join(i.c for i in self.sub)})"

    def __str__(self):
        return "".join(self.c)

    # def __getitem__(self, item):
    #     return self.sub[item]
