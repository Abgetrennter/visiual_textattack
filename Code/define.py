from enum import IntEnum, auto

FPATH = ("..", "Data", "MyHanziData")
FontsPATH = ("..", "Data", "Fonts")
sentence_example = "旨在定义一个稳定、最小化、可移植的语言版本以及相应的标准库，以用于教学和作为将来扩展的基础。"
sentence_faltten = "旨在定义一个稳定、最小化、可移植白勺语言版本以及相应的木示准库，以用于教学和作为将来扩展的基础。"
sentence_changed = "指在定议一个稳定、最小化、苛移植的语言版本以及相应的标准库，笖苚于教学和作伪将来扩展的基础。"
img_size=50

class HanziStructure(IntEnum):
    """
    汉字结构枚举，用于描述汉字的结构
    """
    独体 = 0
    左右 = auto()
    上下 = auto()
    左中右 = auto()
    上中下 = auto()
    右上包围 = auto()
    左上包围 = auto()
    左下包围 = auto()
    上三包围 = auto()
    下三包围 = auto()
    左三包围 = auto()
    全包围 = auto()
    镶嵌 = auto()
    品字 = auto()
