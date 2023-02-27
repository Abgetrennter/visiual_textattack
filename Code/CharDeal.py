from random import choice
from typing import Iterable

from PictDeal import str_draw
from define.Const import insert_bihua, insert_japan
from define.HanZi import HanZi, Hanzi_dict
from define.HanziStructure import HanziStructure
from define.Load import hanzi_splits, hanzi_structure_dict, sp_chars


def get_sim_visial(_char: str, may_replace: Iterable[str]) -> str:
    """获取一个字符的相似字符"""
    _char_vec = str_draw.to_vac(str_draw[_char])
    # _may_replace_vec = [(_, str_draw.draw(_)) for _ in may_replace]
    _may_replace = [(_, compare(_char_vec, str_draw.to_vac(str_draw[_])))
                    for _ in filter(lambda x: len(x) == 1, may_replace)]
    _may_replace = sorted(_may_replace, key=lambda x: x[1], reverse=True)
    print(_char, _may_replace[:5])
    if _may_replace:
        return _may_replace[0][0]
    else:
        return _char


def range_char(start, end):
    return (chr(c) for c in range(start, end))


def 递归计算相似度(origin: HanZi, replacer: HanZi):
    """
    递归计算两个字的相似度,不考虑形如 "也" "他" 这种的情况,假定 origin 是原始字, replacer 是目标.
    :param origin:
    :param replacer:
    :return:
    """
    if origin.struct == HanziStructure.独体 or replacer.struct == HanziStructure.独体:
        if replacer.struct == HanziStructure.组合 or origin.struct == HanziStructure.组合:
            # 懒得写解释了
            return .0
        else:
            return compare(str_draw.to_vac(str_draw[origin.c]), str_draw.to_vac(str_draw[replacer.c]))
    return (递归计算相似度(origin.sub[0], replacer.sub[0]) * origin.sub[0].count
            +
            递归计算相似度(origin.sub[1], replacer.sub[1]) * origin.sub[1].count) \
        / (origin.count * (abs(origin.struct.value - replacer.struct.value) + 1))


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


def char_sim(_char: HanZi) -> str:
    c = _char.c
    _sps = hanzi_splits.get(c, ())
    # 自己，偏旁一，偏旁二,,,,
    chars = []
    for _sp in _sps:
        if _sp in sp_chars:
            chars.extend(sp_chars[_sp])
    set_chars = [Hanzi_dict[c] for c in set(chars) if c != c]

    if not set_chars:
        return c

    replaces = [(c, 递归计算相似度(_char, c)) for c in set_chars]
    replaces.sort(key=lambda x: x[1], reverse=True)
    # print(_char, replaces[:5])
    return replaces[0][0].c


def char_mars(_char: HanZi, func: int = 2) -> str:
    # 火星文版本,添加偏旁
    if _char.c in sp_chars:
        adds = sp_chars[_char.c]
        match func:
            case 1:
                return choice(adds)
            case 2:
                _l = [(c, abs((Hanzi_dict[c].count - _char.count) / _char.count)) for c in adds]
                _l = list(filter(lambda x: x[1] < 1, _l))
                _l.sort(key=lambda x: x[1])
                return _l[0][0] if _l else _char.c
            case 0 | _:
                return adds[0]
        # return get_sim_visial(_char, sp_chars[_char])
    # raise ValueError("char_mars: 无替代字符")
    else:
        return _char.c


def char_insert(_char: HanZi, strict_flag=False) -> str:
    if strict_flag:
        c = insert_bihua
    else:
        c = insert_japan
    return _char.c + choice(c)


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


# def cal_mars(less: str, more: str):
#     """谁爱处理报错谁处理"""
#     less = Hanzi_dict[less]
#     more = Hanzi_dict[more]
#     # out = [_ for _ in more.sub if _ is not less]


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
            return compare(_font[origin.c], _font[replacer.c])
    return (cal_递归(origin.sub[0], replacer.sub[0]) * origin.sub[0].count
            +
            cal_递归(origin.sub[1], replacer.sub[1]) * origin.sub[1].count) \
        / (origin.count * (abs(origin.struct.value - replacer.struct.value) + 1))


if __name__ == '__main__':
    from Code.HaziStructreAttack import uni_filter_char
    # print(hanzi_repalce("我是中国虎"))
    # print(get_nearest_n("吴",20))
    # draw_sp()
    # splits_sim = cal_all_sim(draw_sp())
    # print(sorted(splits_sim.items(), key=lambda x: splits_sim[x[0]], reverse=True)[:50])
    # get_sim_visial("拍", "啪帕柏把")
    from define.Select import *

    select = ChineseRandomSelect(sentence_example, prob=0.4)
    # print([select[i] for i in select.remain])
    # print([c for c, func in select.random("get_many")() if func])
    for __measure in ["get_many"]:  # "just_one",
        print(__measure)
        # for _f in [insert_char]:  # char_flatten, char_mars,
        #     print(_f.__name__)
        for _ in range(5):
            print(
                    "".join(uni_filter_char(s, func, [char_mars]) for s, func in
                            select.random(__measure)()))
