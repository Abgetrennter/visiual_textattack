import pickle
import os.path as osp
from typing import Dict, Tuple, Set, List, Iterable, Callable, Any
import random

import numpy as np

from pic import *
from define import *
from cut import *


def open_pkl(name):
    return pickle.load(open(osp.join(*FPATH, name), "rb"))


hanzi_structure_dict: Dict[str, HanziStructure] = open_pkl("HanziStructure.pkl")
hanzi_splits: Dict[str, Tuple[str]] = open_pkl("HanziSplit.pkl")
splits_sim: Dict[Tuple[str, str], float] = open_pkl("sim.pkl")
splits_sim2: Dict[Tuple[str, str], float] = open_pkl("sim2.pkl")
_sp_chars = {}
for chara, splits in hanzi_splits.items():
    for sp in splits:
        if sp in _sp_chars:
            _sp_chars[sp].append(chara)
        else:
            _sp_chars[sp] = [chara]
sp_chars: Dict[str, Tuple[str]] = {name: tuple(chars) for name, chars in _sp_chars.items()}
del _sp_chars

all_splits = set(sp_chars.keys())


def get_nearest_n(_char: str, n=5) -> Tuple[Tuple[str, float]]:
    _ = []
    for cnc in splits_sim:
        if _char in cnc:
            c = cnc[0] if cnc[1] == _char else cnc[1]
            if c not in "丨丿一丶丿丄龴丫乀":
                _.append((c, splits_sim[cnc]))
    _ = sorted(_, key=lambda x: x[1], reverse=True)
    return tuple(_[:n])


def char_flatten(_char: str) -> str:
    """
    将一个汉字横向拆分成多个汉字
    :param _char: 字符
    :return: 列表形式拆分字符
    """
    structure = hanzi_structure_dict.get(_char, HanziStructure.独体)
    if _char in hanzi_splits:
        _ = hanzi_splits[_char]
        match structure:
            case HanziStructure.左右:
                if len(_) == 2:
                    return "".join(_)
            case HanziStructure.左中右:
                return "".join(_)
            case HanziStructure.左下包围:
                """效果看起来不是很好"""
                ...
    # raise ValueError("char_flatten: 无拆分字符")
    return _char


_font = Font2pic()


def get_sim_visial(_char: str, may_replace: Iterable[str]) -> str:
    """获取一个字符的相似字符"""
    _char_vec = _font.draw(_char)
    # _may_replace_vec = [(i, _font.draw(i)) for i in may_replace]
    _may_replace = [(i, compare(_char_vec, _font.draw(i))) for i in filter(lambda x: len(x) == 1, may_replace)]
    _may_replace = sorted(_may_replace, key=lambda x: x[1], reverse=True)
    # print(_char,_may_replace[:5])
    if _may_replace:
        return _may_replace[0][0]
    else:
        return _char


def char_sim(_char: str) -> str:
    _sps = [*hanzi_splits.get(_char, ()), _char]
    # 自己，偏旁一，偏旁二,,,,
    chars = []
    for _sp in _sps:
        if _sp in sp_chars:
            chars.extend(sp_chars[_sp])
    set_chars = set(chars)
    if _char in set_chars:
        set_chars.remove(_char)
    return get_sim_visial(_char, set_chars)


def char_mars(_char: str) -> str:
    if _char in sp_chars:
        return get_sim_visial(_char, sp_chars[_char])
    # raise ValueError("char_mars: 无替代字符")
    else:
        return _char


def filter_char(_char: str, _flag: bool, f: Callable[[str], str]) -> str:
    if _flag:
        q = list[_char]
        return "".join(f(_c) for _c in _char)
    else:
        return _char


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


def insert_char(_char: str) -> str:
    ...


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
#     #     plt.text(x, y, key, ha='left', rotation=0, c='black', fontsize=8)
#     plt.title("T-SNE")
#     plt.show()


if __name__ == '__main__':
    # print(get_nearest_n("吴",20))
    # draw_sp()
    # splits_sim = cal_all_sim(draw_sp())
    # print(sorted(splits_sim.items(), key=lambda x: splits_sim[x[0]], reverse=True)[:50])
    select = RandomSelect(sentence_example, prob=0.1)
    for __measure in ["just_one", "get_many"]:
        print(__measure)
        for _f in [char_sim]:  # char_flatten, char_mars,
            print(_f.__name__)
            for _ in range(5):
                print("".join(filter_char(*_, _f) for _ in select.random(__measure)))
