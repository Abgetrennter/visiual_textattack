from OpenAttack.metric.algorithms.base import AttackMetric
from OpenAttack.tags import TAG_Chinese, Tag
from pic import Font2pic, compare
from define import sentence_example, sentence_changed, sentence_faltten


class VisiualRate(AttackMetric):
    def __init__(self, **arg):
        self.font = Font2pic(**arg)

    NAME = "Visiual Rate"

    @property
    def Tag(self):
        return {TAG_Chinese}

    def after_attack(self, _input, adversarial_sample):
        fpic = Font2pic()
        if adversarial_sample is not None:
            # s_list = [_input["x"], adversarial_sample]
            s = ["".join(_input["x"]), "".join(adversarial_sample)]
            s = [fpic.draw(i, size=50,show=True) for i in s]


if __name__ == "__main__":
    # import itertools

    s = [sentence_example, sentence_changed, sentence_faltten]
    for i in range(len(s)):
        for ii in range(i + 1, len(s)):
            print(i, ii, VisiualRate().after_attack({"x": s[i]}, s[ii]))
    # print(VisiualRate().after_attack({"x": sentence_example}, sentence_faltten))
