from os import path as osp
from difflib import SequenceMatcher
from OpenAttack.metric.algorithms.base import AttackMetric
from OpenAttack.tags import TAG_Chinese

from PIL import Image

from PictDeal import Font2pic, compare2
from define.Const import OutPicturePATH, sentence_changed, sentence_example, sentence_faltten


# ocr = PaddleOCR()


class VisiualRateSimple(AttackMetric):
    def __init__(self, **arg):
        self.font = Font2pic(**arg)

    NAME = "Visiual Rate Simple"

    @property
    def Tag(self):
        return {TAG_Chinese}

    def after_attack(self, _input, adversarial_sample):
        if adversarial_sample is not None:
            s1, s2 = _input["x"], adversarial_sample
            img1 = self.font.draw(s1, size=50)
            img2 = self.font.draw(s2, size=50)
            return compare2(self.font.to_vac(img1), self.font.to_vac(img2))


_id = 0


class VisiualRateOCR(AttackMetric):
    from paddleocr import PaddleOCR, draw_ocr
    def __init__(self, **arg):
        self.font = Font2pic(**arg)
        self.ocr = PaddleOCR(use_angle_cls=True, lang="ch")

    NAME = "Visiual Rate Simple"

    @property
    def Tag(self):
        return {TAG_Chinese}

    def after_attack(self, _input, adversarial_sample):
        global _id
        if adversarial_sample is not None:
            s1, s2 = _input["x"], adversarial_sample
            name = osp.join(*OutPicturePATH, str(_id) + ".png")
            self.font.draw(s2, size=50).save(name)
            _id += 1
            s3 = self.ocr.ocr(name, cls=True)
            for idx in range(len(s3)):
                res = result[idx]
                for line in res:
                    print(line[-1][0])

            return SequenceMatcher(None, s2, "".join(line[1][0] for line in s3)).ratio()


class VisiualRate(AttackMetric):

    def __init__(self, **arg):
        self.font = Font2pic(**arg)

    def after_attack(self, _input, adversarial_sample):
        # name = _input['review_id']

        if adversarial_sample is not None:
            # s_list = [_input["x"], adversarial_sample]
            s1, s2 = _input["x"], adversarial_sample
            print(s1,'\n',s2)
            img1 = self.font.draw(s1, size=50)  # .save(f"{name}1.jpg")
            img2 = self.font.draw(s2, size=50)  # .save(f"{name}2.jpg")
            img = Image.new('1', (img1.size[0], img2.size[1] + img1.size[1] + 50), 255)  # 宽*高
            img.paste(img1, (0, 0))
            img.paste(img2, (0, img1.size[1] + 50))
            img.show()
            # img.save(osp.join(*OutPicturePATH, f"{name}.jpg"))
            # fpic.draw("\n".join((s1,s2)), size=50).show()
            # res = ocr.ocr("2.jpg", cls=False)[0]
            # print("".join(adversarial_sample))
            # print("".join(line[1][0] for line in res))


if __name__ == "__main__":
    # import itertools

    s = [1, sentence_example, sentence_changed, sentence_faltten]
    # print(VisiualRateSimple().after_attack({"x": s[1]}, s[2]))
    print(VisiualRate().after_attack({"x": s[1]}, s[2]))
    #
    # print(VisiualRate().after_attack({"x": s[3]}, s[1]))

    # print(VisiualRate().after_attack({"x": sentence_example}, sentence_faltten))
