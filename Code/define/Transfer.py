import random
import re
import difflib
from .Transfer_data import *


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
hanzi_plus_replace = make_xlat(hanzi_plus_transfer)
english_replace = make_xlat(english_transfer)
number_cn2an = make_xlat(NUMBER_CN2AN)
time_replace = make_xlat(time_transfer)
emoji_tranfer = make_xlat(emoji_tranfer)

