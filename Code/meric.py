from OpenAttack.metric.algorithms.base import AttackMetric
from OpenAttack.tags import TAG_Chinese, Tag
from pic import str_2_Image, compare


class VisiualRate(AttackMetric):
    def __init__(self):
        pass

    NAME = "Visiual Rate"

    @property
    def Tag(self):
        return {TAG_Chinese}

    def after_attack(self, input, adversarial_sample):
        if adversarial_sample is not None:
            return compare(str_2_Image(input["x"]), str_2_Image(adversarial_sample))
