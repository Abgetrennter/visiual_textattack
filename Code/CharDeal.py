from random import choice
from typing import Iterable

from PictDeal import compare, str_draw
from define.Const import insert_bihua, insert_japan,insert_zero,insert_space
from define.HanZi import HanZi, Hanzi_dict, Hanzi_Splits_Prue, Splits_Hanzi_Prue
from define.HanziStructure import HanziStructure
from define.Load import Hanzi_Structure


# def get_sim_visial(_char: str, may_replace: Iterable[str]) -> str:
#     """获取一个字符的相似字符"""
#     _char_vec = str_draw.to_vac(str_draw[_char])
#     # _may_replace_vec = [(_, str_draw.draw(_)) for _ in may_replace]
#     _may_replace = [(_, compare(_char_vec, str_draw.to_vac(str_draw[_])))
#                     for _ in filter(lambda x: len(x) == 1, may_replace)]
#     _may_replace = sorted(_may_replace, key=lambda x: x[1], reverse=True)
#     print(_char, _may_replace[:5])
#     if _may_replace:
#         return _may_replace[0][0]
#     else:
#         return _char


def range_char(start, end):
    return (chr(c) for c in range(start, end))


def 递归计算相似度(origin: HanZi, replacer: HanZi) -> float:
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


# def char_flatten_simple(_char: HanZi) -> str:
#     """
#     将一个汉字横向拆分成多个汉字
#     :param _char: 字符
#     :return: 列表形式拆分字符
#     """
#     c = _char.c
#     if c in Hanzi_Splits:
#         _ = Hanzi_Splits[c]
#         match Hanzi_Structure.get(c, HanziStructure.独体):
#             case HanziStructure.左右:
#                 if len(_) == 2:
#                     return "".join(_)
#             case HanziStructure.左中右:
#                 return "".join(_)
#             case HanziStructure.左下包围:
#                 """效果看起来不是很好"""
#                 ...
#     # raise ValueError("char_flatten: 无拆分字符")
#     return c


def char_flatten(_char: HanZi) -> str:
    """
    将一个汉字横向拆分成多个汉字
    :param _char: 字符
    :return: 列表形式拆分字符
    """
    # splitable = ()
    ret = ""
    _l = [_char]
    while _l:
        c = _l.pop(0)
        match c.struct:
            case HanziStructure.左右 | HanziStructure.左中右:
                _l.extend(c.sub)
            case HanziStructure.组合:
                # ret += "".join(c.c)
                # continue
                return _char.c
            case _:
                ret += c.c
    return ret


def char_sim(_char: HanZi) -> str:
    c = _char
    _sps = Hanzi_Splits_Prue.get(c, ())
    # 自己，偏旁一，偏旁二,,,,
    chars = []
    for _sp in _sps:
        if _sp in Splits_Hanzi_Prue:
            chars.extend(Splits_Hanzi_Prue[_sp])
    set_chars = [cc for cc in set(chars) if cc != c]

    if not set_chars:
        return c.c
    replaces = sorted(set_chars, key=lambda char: 递归计算相似度(_char, char), reverse=True)
    return replaces[0].c


def char_mars(*args, **kwargs) -> str:
    return _char_mars(*args, **kwargs).c


def _char_mars(_char: HanZi, func: int = 2) -> HanZi:
    # 火星文版本,添加&删除偏旁
    if _char in Splits_Hanzi_Prue:
        adds = [i for i in Splits_Hanzi_Prue[_char]]
    elif _char.sub:
        adds = [i for i in _char.sub if i.struct != HanziStructure.组合]
    else:
        return _char

    match func:
        case 1:
            return choice(adds)
        case 2:

            __l = ((c, (c.count - _char.count)/_char.count) for c in adds)
            __l = sorted(filter(lambda x: x[1] < 1 if x[1]>0 else x[1]> -0.5, __l), key=lambda x: abs(x[1]))#, reverse=True)
            if __l:
                return __l[0][0]
            else:
                return _char
        case 0 | _:
            return adds[0]


c = None


def char_insert(_char: str, strict_flag=False) -> str:
    global c
    if not c:
        if strict_flag:
            c = insert_bihua
        else:
            c = insert_zero + insert_space  # insert_japan
    return _char + choice(c)


if __name__ == '__main__':
    # from Code.HaziStructreAttack import uni_filter_char
    # print(hanzi_repalce("我是中国虎"))
    # print(get_nearest_n("吴",20))
    # draw_sp()
    # splits_sim = cal_all_sim(draw_sp())
    # print(sorted(splits_sim.items(), key=lambda x: splits_sim[x[0]], reverse=True)[:50])
    # get_sim_visial("拍", "啪帕柏把")
    from define.Select import *

    print("begin")
    from define.Const import *

    sentence_example += "做儒徽"

    s = "".join(char_mars(Hanzi_dict[c]) for c in sentence_example)
    print(s)
    print(sentence_example)
    # c = CutSelect(sentence_example, replace_max=0.8)
    # c.compare(s)
    # print("".join(c.new_sent[i] for i in c.remain))
    # select = ChineseRandomSelect(sentence_example, prob=0.4)
    # # print([select[i] for i in select.remain])
    # # print([c for c, func in select.random("get_many")() if func])
    # for __measure in ["get_many"]:  # "just_one",
    #     print(__measure)
    #     # for _f in [insert_char]:  # char_flatten, char_mars,
    #     #     print(_f.__name__)
    #     for _ in range(5):
    #         print(
    #                 "".join(uni_filter_char(s, func, [char_mars]) for s, func in
    #                         select.random(__measure)()))
