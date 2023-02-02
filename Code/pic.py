from PIL import ImageFont, Image, ImageDraw
import argparse
from fontTools.ttLib.ttFont import TTFont
import os
import numpy as np
from define import sentence_example, FontsPATH, img_size

os.makedirs("../data/fonts/simkai", exist_ok=True)
default_fonts = os.path.join(*FontsPATH, "simkai.ttf")


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


class Font2pic:
    def __init__(self, font=default_fonts, _img_size=50):
        self.font = ImageFont.truetype(font, _img_size)
        self.img_size = _img_size

    def draw(self, _str: str, show=False) -> np.ndarray:
        img_long_size = self.img_size * len(_str)
        img = Image.new('1', (img_long_size, self.img_size), 255)
        draw = ImageDraw.Draw(img)
        draw.text((0, 0), _str, font=self.font, fill=0)
        if show:
            img.show()
        return np.array(img).astype(int).reshape(img_long_size * self.img_size)


if __name__ == '__main__':
    s = []
    ss = "abcdefghijklmnopqrstuvwxyz""ABCDEFGHIJKLMNOPQRSTUVWXYZ""0123456789"
    q = "亷"
    wxf = os.path.join(*FontsPATH, "wxkai.ttf")
    f = Font2pic(wxf, 50)
    # f.draw(q, show=True)
    # f.draw(ss, show=True)
    f.draw(sentence_example, show=True)

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
