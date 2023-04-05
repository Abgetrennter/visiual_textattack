import os
import os.path as osp
from warnings import warn

import numpy as np
from PIL import Image, ImageDraw, ImageFont
from fontTools.ttLib.ttFont import TTFont
from bidi import algorithm
from define import FontsPATH, img_size, insert_space,insert_zero

# from define.transfer_data import hanzi_transfer, hanzi_plus_transfer, english_transfer, NUMBER_CN2AN, time_transfer


default_fonts = osp.join(*FontsPATH, "wxkai.ttf")  # )  #


def compare(vec1: np.ndarray, vec2: np.ndarray):
    return vec1.dot(vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2))


def compare2(vec1: np.ndarray, vec2: np.ndarray):
    return 1 / (1 + np.linalg.norm(vec1 - vec2))


class Font2pic:
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, '_instance'):
            orig = super(Font2pic, cls)
            cls._instance = orig.__new__(cls)
        return cls._instance

    @staticmethod
    def to_vac(p, flag: bool = True) -> np.ndarray:
        if flag:
            return np.array(p).astype(int).flatten()
        else:
            return np.array(p).astype(np.uint8)

    def __init__(self, font=default_fonts, _img_size=img_size):
        self.font_name = font
        self.font = ImageFont.truetype(font, _img_size)
        self._font = TTFont(self.font_name)
        self.img_size = _img_size
        self._dict: dict[str, Image.Image] = {}
        self.etc = []
        for _tt in [i for i in os.listdir(osp.join(*FontsPATH)) if str(i).endswith(".ttf")]:
            p = osp.join(*FontsPATH, _tt)
            self.etc.append((TTFont(p), ImageFont.truetype(p, _img_size)))

    def __getitem__(self, item):
        if item not in self._dict:
            self._dict[item] = self.draw_character(item)
        return self._dict[item]

    def __iter__(self):
        return iter(self._dict.items())

    def has_char(self, _c, font=None):
        cmap = font if font else self._font
        for table in cmap['cmap'].tables:
            if ord(_c) in table.ttFont.getBestCmap():
                return True
        return False

    def change_font(self, font):
        self.font_name = font
        self.font = ImageFont.truetype(font, self.img_size)
        self._font = TTFont(self.font_name)

    def draw(self, _str: str, size=None, show=False) -> Image.Image:
        """

        :param size:
        :param _str:
        :param show:
        :return:
        """
        if len(_str) == 1:
            img = self[_str]
        else:
            # if not all(self.has_char(c) for c in _str):
            #     warn("draw: 字体不支持部分字符")
            _str = algorithm.get_display(_str) # 解决一下超级攻击
            pics = tuple(self[c] for c in _str if not (c in insert_space or c in insert_zero))
            _long = len(pics)
            w = 20
            h = _long // w + bool(_long % w)
            size = size if size else self.img_size
            img = Image.new('1', (w * size, h * size), 255)  # 宽*高

            for index, picture in enumerate(pics):
                img.paste(picture, ((index % w) * size, (index // w) * size))
        if show:
            img.show()
        return img

    def draw_character(self, c: str, size=None) -> Image.Image:
        """

        :param size:
        :param c:
        :return:
        """

        font = self.font
        if not self.has_char(c):
            warn("draw: 字体不支持部分字符,已更换为其他字体")
            for cmap, _font in self.etc:
                if self.has_char(c, cmap):
                    font = _font
                    break
            else:
                warn("都没有")
        size = size if size else self.img_size
        img = Image.new('1', (size, size), 255)
        draw = ImageDraw.Draw(img)
        # draw.textbbox(txt, font=font)
        draw.text((0, 0), c, font=font, fill=0)
        return img


str_draw = Font2pic()

if __name__ == '__main__':
    s = []
    # ss = "abcdefghijklmnopqrstuvwxyz""ABCDEFGHIJKLMNOPQRSTUVWXYZ""0123456789""非常撒旦阿萨"
    # img = np.zeros((256,256,3), np.uint8)
    # font = cv2.FONT_HERSHEY_SIMPLEX
    # cv2.putText(img, 'bcdefghijklmn', (10, 100), font, 0.5, (255, 255, 0), 2)
    # cv2.imshow("lena", img )
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
    # keys = "亷"
    # wxf = os.path.join(*FontsPATH, "simSunb.ttf")
    # for Fonts in os.listdir(os.path.join(*FontsPATH)):
    #     print(Fonts)
    #     t = TTFont(os.path.join(*FontsPATH, Fonts))
    #     for i in ['艳', '壯', '恬', '妟', '龟', '累', '贵', '越', '㝵', '埜','慧' ]:
    #         print(i, has_glyph(t, i))
    f = Font2pic(_img_size=50)  # (wxf, 50)
    # _=[f[i] for i in ss]
    # print(list(f))
    # f['\U0001fab8'].show()
    f.draw("别人弓虽烈推荐他🏠的水煮⻥，只是我吃起來真的觉🉐很一般，亱是那个香🌶牛🐸比较🈴我的口味，水煮⻥吃起來很香，"
           "但是跟之前喜欢吃的水煮⻥比起來，好像口味偏清淡一些。还🆗吧，在天堻也没吃过别🏠的水煮⻥。").show()
    # f.draw("s"+insert_zero+"s").show()
    # "".join(chr(i) for i in range(0x1f000, 0x1f02c))
    # f.draw("🤠 牛仔 西部牛仔🤡 小丑 👻 鬼 🩸 血 血滴 血液🫀 心 心脏🫁 肺👑 皇冠 王冠💍 戒指 指环 结婚戒指 钻戒💋 吻 唇印👣 脚印 脚步 足印 足迹🌂 伞 雨伞☂ 太阳伞 阳伞⬅ 左 后⬆ 上 前⬇ 下 后↗ 右上 右前↘ 右下 右后↙ 左下 左后↖ 左上 左前🔄 循环↪ 重做↩ 撤销 撤回⤴ 转上⤵ 转下™ tm© c® rℹ 资讯 咨询🎵 音乐🎶 音符 旋律〰 波浪号➰ 打结 打圈 打旋✔ 通过 勾 对 正🔃 循环➕ 加➖ 减✖ 乘➗ 除🟰 等于").show()
    # w = ""✴八角星星型星号📳振动模式📴关机🆚vs🈶有🈚无🈸申🈺营🈷月🉑可🉐得💮白花㊙秘㊗祝🈴合🈵满🈲禁🅰A型血🅱B型血🆎AB型血🆑清空清除🅾O型血🈁这里🆖不好🆒酷🆓免费🆕新新款🆗好可以行🆙涨🔟十
    # for i in (hanzi_transfer, hanzi_plus_transfer):  # , english_transfer, NUMBER_CN2AN, time_transfer):
    #     f.draw("".join(f"{k}->{v}" for k, v in i.items()), show=True)
    # f.draw(sentence_faltten, show=True)
    # func.draw("丨亻亅丶氵十饣丅丫忄冫干丷衤亠彳千一礻", show=True)
    # func["常"].show()

    # func.draw(ss, show=True)"丨亻亅丶氵十饣丅丫忄冫干丷衤亠彳千一礻"
    # func.draw("".join("丨亻亅丶氵十饣丅丫忄冫干丷衤亠彳千一礻"), show=True)
    # for i in "亷䜥":  # 𠤏㔾⺆𠔉龹":
    #     func.draw(i, show=True)

    # for i in keys:
    #     # uni_2_png(i)
    #     s.append(np.array(uni_2_png(i)).astype(int).reshape(args.size * args.size))
    # # s=np.array(s)
    # omega = []
    # for i in range(len(keys)):
    #     for j in range(i + 1, len(keys)):
    #         print(keys[i], keys[j], ':')
    #         # vec1, vec2 = s[i], s[j]
    #         # print(vec1.dot(vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2)))
    #         # omega.append(((keys[i], keys[j]), vec1.dot(vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2))))
    # print(sorted(omega, key=lambda x: x[1]))

# # for i in func.getBestCmap():
#     uni_2_png(chr(i))
