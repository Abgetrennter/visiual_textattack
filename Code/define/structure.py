from enum import IntEnum, auto


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
