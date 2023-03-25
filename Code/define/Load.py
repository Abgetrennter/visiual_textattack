import os.path as osp
import pickle

from .Const import FPATH
from .HanziStructure import HanziStructure


def open_pkl(name):
    try:
        return pickle.load(open(osp.join(*FPATH, name), "rb"))
    except FileNotFoundError:
        return pickle.load(open(osp.join('..', *FPATH, name), "rb"))


Hanzi_Structure: dict[str, HanziStructure] = open_pkl("HanziStructure.pkl")
Hanzi_Structure = {k: HanziStructure(v) for k, v in Hanzi_Structure.items()}
Hanzi_Splits: dict[str, tuple[str]] = open_pkl("HanziSplit.pkl")
splits_sim: dict[tuple[str, str], float] = open_pkl("sim.pkl")
splits_sim2: dict[tuple[str, str], float] = open_pkl("sim2.pkl")
_sp_chars = {}
for chara, splits in Hanzi_Splits.items():
    for sp in splits:
        if sp in _sp_chars:
            _sp_chars[sp].append(chara)
        else:
            _sp_chars[sp] = [chara]
Splits_Hanzi: dict[str, tuple[str]] = {name: tuple(chars) for name, chars in _sp_chars.items()}

del _sp_chars

AllSplits = set(Splits_Hanzi.keys())
