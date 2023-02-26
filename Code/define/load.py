from .const import FPATH
from .structure import HanziStructure
import pickle
import os.path as osp


def open_pkl(name):
    return pickle.load(open(osp.join(*FPATH, name), "rb"))


hanzi_structure_dict: dict[str, HanziStructure] = open_pkl("HanziStructure.pkl")
hanzi_structure_dict = {k: HanziStructure(v) for k, v in hanzi_structure_dict.items()}
hanzi_splits: dict[str, tuple[str]] = open_pkl("HanziSplit.pkl")
splits_sim: dict[tuple[str, str], float] = open_pkl("sim.pkl")
splits_sim2: dict[tuple[str, str], float] = open_pkl("sim2.pkl")
_sp_chars = {}
for chara, splits in hanzi_splits.items():
    for sp in splits:
        if sp in _sp_chars:
            _sp_chars[sp].append(chara)
        else:
            _sp_chars[sp] = [chara]
sp_chars: dict[str, tuple[str]] = {name: tuple(chars) for name, chars in _sp_chars.items()}

del _sp_chars

all_splits = set(sp_chars.keys())
