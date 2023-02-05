import OpenAttack
import datasets
from define import *
from SplitAttack import *
from meric import VisiualRate

OpenAttack.DataManager.data_path = {
        x: "../Data/" + x for x in OpenAttack.DataManager.data_path.keys()
}


# from OpenAttack.data_manager import DataManager
# a=DataManager.load("AttackAssist.SIM")

def dataset_mapping(x):
    return {
            "x": x["review_body"],
            "y": x["stars"],
    }


def main():
    print("New Attacker")
    attacker = SplitAttack(prob=0.2, attack_measure=char_sim)  # choose_measure="justone")
    # attacker = OpenAttack.attackers.PWWSAttacker(lang="chinese")
    print("Building model")
    clsf = OpenAttack.loadVictim("BERT.AMAZON_ZH")

    print("Loading dataset")
    dataset = datasets.load_dataset("amazon_reviews_multi", 'zh', split="train[60:100]").map(function=dataset_mapping)
    # print([i for i in dataset["review_body"]])
    print("Start attack")
    attack_eval = OpenAttack.AttackEval(attacker, clsf, metrics=[
            # OpenAttack.metric.Fluency(),
            OpenAttack.metric.GrammaticalErrors(),
            OpenAttack.metric.EditDistance(),
            OpenAttack.metric.ModificationRate(),
            VisiualRate()
    ])
    for i in (0.15,):
        attack_eval.attacker.prob = i
        print(f"prob={i}")
        print(attack_eval.eval(dataset, visualize=True, progress_bar=True))


if __name__ == "__main__":
    main()
    pass
