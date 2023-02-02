import pickle
import os.path as osp
from typing import Dict, Tuple, Set, List, Iterable, Callable, Any
import random
from pic import Font2pic, compare
from define import *
import jieba

hanzi_structure_dict: Dict[str, HanziStructure] = pickle.load(open(osp.join(*FPATH, "HanziStructure.pkl"), "rb"))
hanzi_splits: Dict[str, Tuple[str]] = pickle.load(open(osp.join(*FPATH, "HanziSplit.pkl"), "rb"))

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
    raise ValueError("char_flatten: 无拆分字符")


_font = Font2pic()


def get_sim_visial(_char: str, may_replace: Iterable[str]) -> str:
    """获取一个字符的相似字符"""
    _char_vec = _font.draw(_char)
    # _may_replace_vec = [(i, _font.draw(i)) for i in may_replace]
    _may_replace = sorted(may_replace, key=lambda x: compare(_char_vec, _font.draw(x)), reverse=True)
    return _may_replace[0]


def char_sim(_char: str) -> str:
    return _char


def char_mars(_char: str) -> str:
    if _char in sp_chars:
        return get_sim_visial(_char, sp_chars[_char])
    raise ValueError("char_mars: 无替代字符")
    # else:
    #     return _char


def sentece_prob(_sentence: str, prob: float, deal_char: Callable[[str], str]
                 , get_char: str = "get_many") -> str:
    pos_list = list(range(len(_sentence)))
    match get_char:
        case "get_many":
            pos_list = random.choices(pos_list, k=int(len(_sentence) * prob))
        case "just_one":
            pos_list = random.choice(pos_list)

    return "".join(deal_char(c) if index in pos_list else c for index, c in enumerate(_sentence))


def sentece_cut_prob(_sentence: str, _f: Callable[[str], str], prob: float) -> str:
    word_list = jieba.cut(_sentence)


if __name__ == '__main__':
    for f in (char_sim, char_flatten, char_mars):
        print(sentece_prob(sentence_example
                           , 0.4, f))
