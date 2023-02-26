from SplitAttack import *
from meric import VisiualRate
from tqdm import tqdm
import matplotlib.pyplot as plt
import OpenAttack
import datasets

OpenAttack.DataManager.data_path = {
        x: "../Data/" + x for x in OpenAttack.DataManager.data_path.keys()
}


# print(OpenAttack.DataManager.AVAILABLE_DATAS)


# from OpenAttack.data_manager import DataManager
# a=DataManager.load("AttackAssist.SIM")

def dataset_mapping(x):
    return {
            "x": x["review_body"],
            "y": x["stars"],
    }


def main():
    print("New Attacker")
    attack_measure = ((char_sim, 3), (char_flatten, 2), (char_mars, 4), (char_insert, 1))
    attacker = SplitAttack(prob=0.2, generations=40,
                           attack_measure=attack_measure)  # choose_measure="justone")
    # attacker1 = OpenAttack.attackers.PWWSAttacker(lang="chinese")
    print("Building model")
    clsf = OpenAttack.loadVictim("BERT.AMAZON_ZH")

    print("Loading dataset")
    dataset = datasets.load_dataset("amazon_reviews_multi", 'zh', split="train[20:40]").map(function=dataset_mapping)
    # print([_ for _ in dataset["review_body"]])
    print("Start attack")
    attack_eval = OpenAttack.AttackEval(attacker, clsf, metrics=[
            # OpenAttack.metric.Fluency(),
                 # OpenAttack.metric.GrammaticalErrors(),
            OpenAttack.metric.EditDistance(),
            OpenAttack.metric.ModificationRate(),
            VisiualRate()
    ])
    attack_eval.eval(dataset, visualize=False, progress_bar=True)
    # res = OpenAttack.AttackEval(attacker1, clsf, metrics=[
    #         # OpenAttack.metric.Fluency(),
    #         # OpenAttack.metric.GrammaticalErrors(),
    #         OpenAttack.metric.EditDistance(),
    #         OpenAttack.metric.ModificationRate(),
    #         VisiualRate()
    # ]).eval(dataset, visualize=False, progress_bar=True)

    # _____ = (.1, .2, .3, .4, .45, .5)
    #
    # # success_rate1 = [res["Attack Success Rate"] for _ in _____]
    # # edit_distance1 = [res["Avg. Levenshtein Edit Distance"] for _ in _____]
    # # queries1 = [res["Avg. Victim Model Queries"] for _ in _____]
    # # run_time1 = [res["Avg. Running Time"] for _ in _____]
    #
    # ret = {}
    # for i in _____:
    #     attack_eval.attacker.prob = i
    #     print(f"prob={i}")
    #     ret[i] = attack_eval.eval(dataset, visualize=False, progress_bar=True)
    # #
    # success_rate = [_["Attack Success Rate"] for _ in ret.values()]
    # edit_distance = [_["Avg. Levenshtein Edit Distance"] for _ in ret.values()]
    # queries = [_["Avg. Victim Model Queries"] for _ in ret.values()]
    # run_time = [_["Avg. Running Time"] for _ in ret.values()]
    #
    # x = list(ret.keys())
    # plt.plot(x, success_rate, color='orangered', marker='o', linestyle='-', label='uni')
    # # plt.plot(x, success_rate1, color='blueviolet', marker='D', linestyle='-.', label='pwws')
    # plt.legend()
    # plt.ylabel("Attack Success Rate")
    # plt.show()
    # #
    # plt.plot(x, edit_distance, color='orangered', marker='o', linestyle='-', label='uni')
    # # plt.plot(x, edit_distance1, color='blueviolet', marker='D', linestyle='-.', label='pwws')
    # plt.legend()
    # plt.ylabel("Avg. Levenshtein Edit Distance")
    # plt.show()
    # #
    # plt.plot(x, queries, color='orangered', marker='o', linestyle='-', label='uni')
    # # plt.plot(x, queries1, color='blueviolet', marker='D', linestyle='-.', label='pwws')
    # plt.legend()
    # plt.ylabel("Avg. Victim Model Queries")
    # plt.show()
    # #
    # plt.plot(x, run_time, color='orangered', marker='o', linestyle='-', label='uni')
    # # plt.plot(x, run_time1, color='blueviolet', marker='D', linestyle='-.', label='pwws')
    # plt.legend()
    # plt.ylabel("Avg. Running Time")
    # plt.show()


#
#
if __name__ == "__main__":
    main()
    pass