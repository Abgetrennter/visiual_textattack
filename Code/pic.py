from PIL import ImageFont, Image, ImageDraw
import argparse
from fontTools.ttLib.ttFont import TTFont
import os
import numpy as np
from define import sentence_example, FontsPATH, img_size
from fontTools.unicode import Unicode
from warnings import warn


def has_glyph(font, glyph):
    for table in font['cmap'].tables:
        if ord(glyph) in table.cmap.keys():
            return True
    return False


# os.makedirs("../data/fonts/simkai", exist_ok=True)
default_fonts = os.path.join(*FontsPATH, "wxkai.ttf")


# def char_2_Image(txt: str, font=default_fonts, img_size=50) -> Image.Image:
#     if len(txt) != 1:
#         raise ValueError("char_2_Image: 输入字符长度不为1")
#     img = Image.new('1', (img_size, img_size), 255)
#     draw = ImageDraw.Draw(img)
#     font = ImageFont.truetype(font, img_size)
#
#     # x, y = draw.textsize(txt, font=font)
#     # draw.text(((img_size - x) // 2, (img_size - y) // 2), txt, font=font, fill=0)
#     draw.text((0, 0), txt, font=font, fill=0)
#     # file_name = f'simkai/{txt}.png'
#     # img.save(file_name)
#     img.show()
#     # _input()
#     return np.array(img).astype(int).reshape(img_size ** 2)
#
#
# def str_2_Image(txt: str, font=default_fonts, img_size=50) -> Image.Image:
#     """
#
#     :param txt:
#     :param font:
#     :param img_size: 不同句子的长度不一样长怎么办
#     :return:
#     """
#     img_long_size = img_size * len(txt)
#     img = Image.new('1', (img_long_size, img_size), 255)
#     draw = ImageDraw.Draw(img)
#     font = ImageFont.truetype(font, img_size)
#
#     # x, y = draw.textsize(txt, font=font)
#     # draw.text(((img_size - x) // 2, (img_size - y) // 2), txt, font=font, fill=0)
#     draw.text((0, 0), txt, font=font, fill=0)
#     # file_name = f'simkai/{txt}.png'
#     # img.save(file_name)
#     img.show()
#     # _input()
#     return np.array(img).astype(int).reshape(img_long_size * img_size)


def compare(vec1: np.ndarray, vec2: np.ndarray):
    return vec1.dot(vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2))


def compare2(vec1: np.ndarray, vec2: np.ndarray):
    return 1 / (1 + np.linalg.norm(vec1 - vec2))


class Font2pic:
    def __init__(self, font=default_fonts, _img_size=img_size):
        self.font_name = font
        self.font = ImageFont.truetype(font, _img_size)
        self._font = TTFont(self.font_name)
        self.img_size = _img_size
        self.__dict = {}

    def has_char(self, _c):
        for table in self._font['cmap'].tables:
            if ord(_c) in table.cmap.keys():
                return True
        return False

    def change_font(self, font):
        self.font_name = font
        self.font = ImageFont.truetype(font, self.img_size)
        self._font = TTFont(self.font_name)

    def draw(self, _str: str, show=False) -> np.ndarray:
        """

        :param _str:
        :param show:
        :return:
        """
        if len(_str) == 1:
            if _str not in self.__dict:
                self.__dict[_str] = self.__draw(_str, (self.img_size, self.img_size), show)
            return self.__dict[_str]
        else:
            return self.__draw(_str, (self.img_size * len(_str), self.img_size), show)

    def __draw(self, _str: str, size,show=False) -> np.ndarray:
        """

        :param _str:
        :param show:
        :return:
        """
        img = Image.new('1', size, 255)
        draw = ImageDraw.Draw(img)
        # draw.textbbox(txt, font=font)
        if not all(self.has_char(c) for c in _str):
            warn("draw: 字体不支持部分字符")
        draw.text((0, 0), _str, font=self.font, fill=0)
        if show:
            img.show()
        return np.array(img).astype(int).reshape(size[0] * size[1])


if __name__ == '__main__':
    s = []
    ss = "abcdefghijklmnopqrstuvwxyz""ABCDEFGHIJKLMNOPQRSTUVWXYZ""0123456789"
    q = "亷"
    # wxf = os.path.join(*FontsPATH, "simSunb.ttf")
    # for fonts in os.listdir(os.path.join(*FontsPATH)):
    #     print(fonts)
    #     t = TTFont(os.path.join(*FontsPATH, fonts))
    #     for i in ['艳', '壯', '恬', '妟', '龟', '累', '贵', '越', '㝵', '埜','慧' ]:
    #         print(i, has_glyph(t, i))
    f = Font2pic(_img_size=30)  # (wxf, 50)
    # f.draw(q, show=True)
    # f.draw(ss, show=True)"丨亻亅丶氵十饣丅丫忄冫干丷衤亠彳千一礻"
    f.draw("".join(['艳', '壯', '拳', '妟', '捩', '累', '卙', '越', '㝵', '埜', '慧']), show=True)
    # for i in "𠤏㔾⺆𠔉龹":
    #     f.draw(i, show=True)

    # for i in q:
    #     # uni_2_png(i)
    #     s.append(np.array(uni_2_png(i)).astype(int).reshape(args.size * args.size))
    # # s=np.array(s)
    # omega = []
    # for i in range(len(q)):
    #     for j in range(i + 1, len(q)):
    #         print(q[i], q[j], ':')
    #         # vec1, vec2 = s[i], s[j]
    #         # print(vec1.dot(vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2)))
    #         # omega.append(((q[i], q[j]), vec1.dot(vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2))))
    # print(sorted(omega, key=lambda x: x[1]))
# # for i in f.getBestCmap():
#     uni_2_png(chr(i))
