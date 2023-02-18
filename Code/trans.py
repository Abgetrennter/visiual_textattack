import re
import random
import cn2an
from define import insert_japan


def _(s: str, p: float = 0.1):
    w = ""
    for i in s:
        if random.random() < p:
            w += i + random.choice(insert_japan)
        else:
            w += i
    return w


class make_xlat:
    def __init__(self, _dict: dict[str, str]):
        self.adict = _dict
        self.rx = re.compile('|'.join(re.escape(i) for i in self.adict))

    def one_xlat(self, match):
        if len(l := self.adict[match.group(0)]) in (0, 1):
            return l
        else:
            print(l)
            return random.choice(l)

    def __call__(self, text: str):
        return self.rx.sub(self.one_xlat, text)


if __name__ == "__main__":
    w = "他说，2022 年，我们一路砥砺前行，一路开拓奋进。在这极不平凡的一年中，全校上下坚定步伐、同心协力，各项工作取得显著成绩," \
        " 呈现出良好发展势头。站在党的二十大胜利召开的重大历史节点，学校全面贯彻党的教育方针，落实立德树人根本任务，" \
        "积极回应加快推进高等教育高质量发展的时代要求，推动各项事业向更高水平跃升。" \
        "今天，我们欢聚一堂，通过举办新春茶话会的形式，共同迎接武汉大学建校 130 周年这个特殊年份的新春佳节。"
    q = "从我住的地方，可以看到几百台发动机喷出的等离子体光柱。你想像一个巨大的宫殿，有雅典卫城上的神殿那么大，殿中有无数根顶天立地的巨柱，每根柱子像一根巨大的日光灯管那样发出蓝白色的强光。而你，是那巨大宫殿地板上的一个细菌，这样，你就可以想像到我所在的世界是什么样子了。其实这样描述还不是太准确，是地球发动机产生的切线推力分量刹住了地球的自转，因此地球发动机的喷射必须有一定的角度，这样天空中的那些巨型光柱是倾斜的，我们是处在一个将要倾倒的巨殿中！南半球的人来到北半球后突然置身于这个环境中，有许多人会精神失常的。"
    print(_(q))
    # b = make_xlat(time_transfer)
    # print(b(cn2an.transform('二月十九号19时')))
    # c = make_xlat(hanzi_transfer)
    # print(c("龙马精神"))
    # e = make_xlat(english_transfer)
    # print(
    #         e("Innovative software solutions for day-to-day management needs and decision-making processes in any "
    #           "industry. The ease and speed of access and analysis of"))
