from os import path as osp

from OpenAttack.metric.algorithms.base import AttackMetric
from OpenAttack.tags import TAG_Chinese
# from paddleocr import PaddleOCR, draw_ocr
from PIL import Image

from PictDeal import Font2pic
from define.Const import OutPicturePATH, sentence_changed, sentence_example, sentence_faltten


# ocr = PaddleOCR()


class VisiualRate(AttackMetric):
    def __init__(self, **arg):
        self.font = Font2pic(**arg)

    NAME = "Visiual Rate"

    @property
    def Tag(self):
        return {TAG_Chinese}

    def after_attack(self, _input, adversarial_sample):
        fpic = Font2pic()
        name = _input['review_id']
        if adversarial_sample is not None:
            # s_list = [_input["x"], adversarial_sample]
            s1, s2 = _input["x"], adversarial_sample
            img1 = fpic.draw(s1, size=50)  # .save(f"{name}1.jpg")
            img2 = fpic.draw(s2, size=50)  # .save(f"{name}2.jpg")
            img = Image.new('1', (img1.size[0], img2.size[1] + img1.size[1] + 50), 255)  # 宽*高
            img.paste(img1, (0, 0))
            img.paste(img2, (0, img1.size[1] + 50))
            # img.show()
            img.save(osp.join(*OutPicturePATH, f"{name}.jpg"))
            # fpic.draw("\n".join((s1,s2)), size=50).show()
            # res = ocr.ocr("2.jpg", cls=False)[0]
            # print("".join(adversarial_sample))
            # print("".join(line[1][0] for line in res))


if __name__ == "__main__":
    # import itertools

    s = [1, sentence_example, sentence_changed, sentence_faltten]
    print(VisiualRate().after_attack({"x": s[1]}, s[2]))
    print(VisiualRate().after_attack({"x": s[2]}, s[3]))
    print(VisiualRate().after_attack({"x": s[3]}, s[1]))

    # print(VisiualRate().after_attack({"x": sentence_example}, sentence_faltten))
