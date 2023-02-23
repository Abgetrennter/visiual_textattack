from PIL import ImageFont, Image, ImageDraw
import argparse
from fontTools.ttLib.ttFont import TTFont
import os.path as osp
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
default_fonts = osp.join(*FontsPATH, "wxkai.ttf")


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
        self._dict = {}
        self.etc = []
        for _tt in ("KaiXinSongB.ttf", "中华书局宋体02平面_20221110.TTF", "wxkai.ttf","simsunb.ttf"):
            p = osp.join(*FontsPATH, _tt)
            self.etc.append((TTFont(p), ImageFont.truetype(p, _img_size)))

    def has_char(self, _c, f=None):
        cmap = f if f else self._font
        for table in cmap['cmap'].tables:
            if ord(_c) in table.ttFont.getBestCmap():
                return True
        return False

    def change_font(self, font):
        self.font_name = font
        self.font = ImageFont.truetype(font, self.img_size)
        self._font = TTFont(self.font_name)

    def draw(self, _str: str, show=False, replace=True) -> np.ndarray:
        """

        :param replace:
        :param _str:
        :param show:
        :return:
        """
        if len(_str) == 1:

            if _str not in self._dict:
                font=None
                if not self.has_char(_str):
                    warn("draw: 字体不支持部分字符")
                    if replace:
                        warn("已更换为其他字体")
                    for cmap, f in self.etc:
                        if self.has_char(_str, cmap):
                            self._dict[_str] = self.__draw(_str, (self.img_size, self.img_size), show, font)
                            break
                    else:
                        warn("都没有")
                        self._dict[_str] = self.__draw(_str, (self.img_size, self.img_size), show)

                else:
                    self._dict[_str] = self.__draw(_str, (self.img_size, self.img_size), show)

            return self._dict[_str]
        else:
            if not all(self.has_char(c) for c in _str):
                warn("draw: 字体不支持部分字符")
            return self.__draw(_str, (self.img_size * len(_str), self.img_size), show)

    def __draw(self, _str: str, size, show=False, font=None) -> np.ndarray:
        """

        :param _str:
        :param show:
        :return:
        """
        img = Image.new('1', size, 255)
        draw = ImageDraw.Draw(img)
        # draw.textbbox(txt, font=font)
        draw.text((0, 0), _str, font=font if font else self.font, fill=0)
        if show:
            img.show()
        return np.array(img).astype(int).reshape(size[0] * size[1])


if __name__ == '__main__':
    s = []
    ss = "abcdefghijklmnopqrstuvwxyz""ABCDEFGHIJKLMNOPQRSTUVWXYZ""0123456789"
    # q = "亷"
    # wxf = os.path.join(*FontsPATH, "simSunb.ttf")
    # for fonts in os.listdir(os.path.join(*FontsPATH)):
    #     print(fonts)
    #     t = TTFont(os.path.join(*FontsPATH, fonts))
    #     for i in ['艳', '壯', '恬', '妟', '龟', '累', '贵', '越', '㝵', '埜','慧' ]:
    #         print(i, has_glyph(t, i))
    f = Font2pic(_img_size=30)  # (wxf, 50)
    # func.draw(q, show=True)
    # func.draw(ss, show=True)"丨亻亅丶氵十饣丅丫忄冫干丷衤亠彳千一礻"
    # f.draw("".join("丨亻亅丶氵十饣丅丫忄冫干丷衤亠彳千一礻"), show=True)
    for i in "亷䜥":#𠤏㔾⺆𠔉龹":
        f.draw(i, show=True)

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
# # for i in func.getBestCmap():
#     uni_2_png(chr(i))
