import OpenAttack
import matplotlib.pyplot as plt
from Vitim import StructBert, Paddle, Erlangshen
from CharDeal import char_flatten, char_mars, char_sim
from HaziStructreAttack import HanziStructureAttack
from Data import amazon_reviews, dianping, paddle
from Meric import VisiualRate

OpenAttack.DataManager.data_path = {
        x: "../Data/" + x for x in OpenAttack.DataManager.data_path.keys()
}


# print(OpenAttack.DataManager.AVAILABLE_DATAS)


# from OpenAttack.data_manager import DataManager
# a=DataManager.load("AttackAssist.SIM")
# amazon_reviews()
# paddle()
# dianping()


def attack(ack, vit):
    print("Start attack")
    attack_eval = OpenAttack.AttackEval(ack, vit, metrics=[
            # OpenAttack.metric.Fluency(),
            # OpenAttack.metric.GrammaticalErrors(),
            OpenAttack.metric.Levenshtein(),
            OpenAttack.metric.JaccardChar(),
            OpenAttack.metric.ModificationRate(),
            # VisiualRate()
    ])
    return attack_eval


def some_prob(attack_eval, dataset):
    ret = {}
    for i in (.4, .5):
        attack_eval.attacker.prob = i
        print(f"prob={i}")
        ret[i] = attack_eval.eval(dataset, visualize=False, progress_bar=True)

    return ret


def draw(ret, example=None):
    def get_values(key, r):
        return [_[key] for _ in r.values()]

    x = list(ret.keys())

    for label in next(iter(ret.values())).keys():
        plt.plot(x, get_values(label, ret), color='orangered', marker='o', linestyle='-', label='uni')
        if example:
            plt.plot(x, get_values(label, example), color='blueviolet', marker='D', linestyle='-.', label='pwws')
        plt.legend()
        plt.ylabel(label)
        plt.show()


def main():
    print("New Attacker")
    attack_measure = ((char_sim, 1), (char_flatten, 2), (char_mars, 3))
    attacker = HanziStructureAttack(prob=0.4, generations=120,
                                    attack_measure=attack_measure, choose_measure="important_simple_select")
    # attacker1 = OpenAttack.attackers.PWWSAttacker(lang="chinese")
    print("Building model")
    # clsf = StructBert()
    # clsf = Paddle()
    # clsf = Erlangshen()
    clsfs = (OpenAttack.loadVictim("BERT.AMAZON_ZH"), StructBert(), Paddle())

    print("Loading dataset")
    drange = {"begin": 0, "end": 20}
    datasets = (amazon_reviews(**drange), dianping(**drange), paddle(**drange))


    for clsf, dataset in zip(clsfs, datasets):
        attack_eval = OpenAttack.AttackEval(attacker, clsf, metrics=[
                # OpenAttack.metric.Fluency(),
                # OpenAttack.metric.GrammaticalErrors(),
                OpenAttack.metric.Levenshtein(),
                OpenAttack.metric.JaccardChar(),
                OpenAttack.metric.ModificationRate(),
                # VisiualRate()
        ])
        #ret = some_prob(attack_eval, dataset)
        ret = attack_eval.eval(dataset, visualize=False, progress_bar=True)
        print(ret)
        break
        # draw(ret)


#
#
if __name__ == "__main__":
    main()
