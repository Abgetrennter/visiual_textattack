from typing import Dict

from pic import *
from define import *
from define.load import *
from Code.define.cut import *

import re
from define.HanZi import HanZi, han_dict


def get_nearest_n(_char: str, n=5) -> Tuple[Tuple[str, float]]:
    _ = []
    for cnc in splits_sim:
        if _char in cnc:
            c = cnc[0] if cnc[1] == _char else cnc[1]
            if c not in "丨丿一丶丿丄龴丫乀":
                _.append((c, splits_sim[cnc]))
    _ = sorted(_, key=lambda x: x[1], reverse=True)
    return tuple(_[:n])


def char_flatten(_char: HanZi) -> str:
    """
    将一个汉字横向拆分成多个汉字
    :param _char: 字符
    :return: 列表形式拆分字符
    """
    c = _char.c
    if c in hanzi_splits:
        _ = hanzi_splits[c]
        match hanzi_structure_dict.get(c, HanziStructure.独体):
            case HanziStructure.左右:
                if len(_) == 2:
                    return "".join(_)
            case HanziStructure.左中右:
                return "".join(_)
            case HanziStructure.左下包围:
                """效果看起来不是很好"""
                ...
    # raise ValueError("char_flatten: 无拆分字符")
    return c


_font = Font2pic()


def get_sim_visial(_char: str, may_replace: Iterable[str]) -> str:
    """获取一个字符的相似字符"""
    _char_vec = _font.draw(_char)
    # _may_replace_vec = [(i, _font.draw(i)) for i in may_replace]
    _may_replace = [(i, compare(_char_vec, _font.draw(i))) for i in filter(lambda x: len(x) == 1, may_replace)]
    _may_replace = sorted(_may_replace, key=lambda x: x[1], reverse=True)
    print(_char, _may_replace[:5])
    if _may_replace:
        return _may_replace[0][0]
    else:
        return _char


# def get_sim_cal(_char: str, may_replace: Iterable[str]) -> str:
#     """获取一个字符的相似字符"""
#     _char_vec = character_dict[_char]
#     print(may_replace)
#     # _may_replace_vec = [(i, _font.draw(i)) for i in may_replace]
#     _may_replace = [(i, cal_递归(_char_vec, character_dict[i])) for i in filter(lambda x: len(x) == 1, may_replace)]
#     _may_replace = sorted(_may_replace, key=lambda x: x[1], reverse=True)
#     print(_char, _may_replace[:5])
#     if _may_replace:
#         return _may_replace[0][0]
#     else:
#         return _char


def char_sim(_char: HanZi) -> str:
    c = _char.c
    _sps = hanzi_splits.get(c, ())
    # 自己，偏旁一，偏旁二,,,,
    chars = []
    for _sp in _sps:
        if _sp in sp_chars:
            chars.extend(sp_chars[_sp])
    set_chars = [han_dict[i] for i in set(chars) if i != c]

    if not set_chars:
        return c

    replaces = [(i, cal_递归(_char, i)) for i in set_chars]
    replaces.sort(key=lambda x: x[1], reverse=True)
    # print(_char, replaces[:5])
    return replaces[0][0].c


def char_mars(_char: HanZi, func: int = 2) -> str:
    # 火星文版本,添加偏旁
    if _char.c in sp_chars:
        adds = sp_chars[_char.c]
        match func:
            case 1:
                return random.choice(adds)
            case 2:
                _l = [(i, abs((han_dict[i].count - _char.count) / _char.count)) for i in adds]
                _l=list(filter(lambda x: x[1] < 1, _l))
                _l.sort(key=lambda x: x[1])
                return _l[0][0] if _l else _char.c
            case 0 | _:
                return adds[0]
        # return get_sim_visial(_char, sp_chars[_char])
    # raise ValueError("char_mars: 无替代字符")
    else:
        return _char.c


def filter_char(_char: str, _flag: bool, f: Callable[[str], str]) -> str:
    if _flag:
        # q = list[_str]
        return "".join(f(_c) for _c in _char)
    else:
        return _char


def uni_filter_char(_str: str, _flag: bool, fs: List[Callable[[HanZi], str]]) -> str:
    if _flag:
        # q = list[_str]
        _f = random.choice(fs)
        return "".join(_f(han_dict[char]) for char in _str)
    else:
        return _str


def cal_all_sim(c2v: Dict[str, np.ndarray]):
    from tqdm import tqdm
    pp = {}
    qq = list(c2v.keys())
    for index in tqdm(range(len(qq))):
        c1 = qq[index]
        for iindex in range(index, len(qq)):
            c2 = qq[iindex]
            key = tuple(sorted((c1, c2)))
            pp[key] = compare2(c2v[c1], c2v[c2])
    with open(osp.join(*FPATH, "sim3.pkl"), "wb") as f:
        pickle.dump(pp, f)
    return pp


def draw_sp():
    omega = {}
    qq = list(hanzi_splits.keys())
    for _tt in ["wxkai.ttf", "KaiXinSongB.ttf", "中华书局宋体02平面_20221110.TTF"]:
        _font.change_font(osp.join(*FontsPATH, _tt))
        for cc in qq[:]:
            try:
                if _font.has_char(cc):
                    omega[cc] = _font.draw(cc)

                qq.remove(cc)

            except:
                print(cc)
        print(_tt, len(qq))

    return omega


def range_char(start, end):
    return (chr(c) for c in range(start, end))


def insert_char(_char: HanZi, strict_flag=False) -> str:
    if strict_flag:
        c = insert_bihua
    else:
        c = insert_japan
    return _char.c + random.choice(c)


class make_xlat:
    def __init__(self, _dict: dict[str, str]):
        self.adict = _dict
        self.rx = re.compile('|'.join(re.escape(i) for i in self.adict))

    def one_xlat(self, match):
        if len(l := self.adict[match.group(0)]) in (0, 1):
            return l
        else:
            # print(l)
            return random.choice(l)

    def __call__(self, text: str):
        return self.rx.sub(self.one_xlat, text)


hanzi_repalce = make_xlat(hanzi_transfer)


# def ___():
#     from sklearn.manifold import TSNE
#     import matplotlib.pyplot as plt
#
#
#     model = TSNE(n_components=2)
#     compress_embedding = model.fit_transform(np.array([_font.draw(_) for _ in all_splits]))
#     keys = list(all_splits)
#
#     plt.scatter(compress_embedding[:, 0], compress_embedding[:, 1], s=10)
#     # for x, y, key in zip(compress_embedding[:, 0], compress_embedding[:, 1], keys):
#     #     plt.text(x, y, key, ha='origin', rotation=0, c='black', fontsize=8)
#     plt.title("T-SNE")
#     plt.show()


def cal_mars(less: str, more: str):
    """谁爱处理报错谁处理"""
    less = han_dict[less]
    more = han_dict[more]
    out = [_ for _ in more.sub if _ is not less]


def cal_递归(origin: HanZi, replacer: HanZi):
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


if __name__ == '__main__':
    # print(hanzi_repalce("我是中国虎"))
    # print(get_nearest_n("吴",20))
    # draw_sp()
    # splits_sim = cal_all_sim(draw_sp())
    # print(sorted(splits_sim.items(), key=lambda x: splits_sim[x[0]], reverse=True)[:50])
    # get_sim_visial("拍", "啪帕柏把")
    select = RandomSelect(sentence_example, prob=0.4)
    for __measure in ["get_many"]:  # "just_one",
        print(__measure)
        # for _f in [insert_char]:  # char_flatten, char_mars,
        #     print(_f.__name__)
        for _ in range(5):
            print(
                    "".join(uni_filter_char(s, func, [char_mars]) for s, func in
                            select.random(__measure)))
