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
    attacker = SplitAttack(prob=0.2   )  # choose_measure="justone")

    print("Building model")
    clsf = OpenAttack.loadVictim("BERT.AMAZON_ZH")

    print("Loading dataset")
    dataset = datasets.load_dataset("amazon_reviews_multi", 'zh', split="train[:50]").map(function=dataset_mapping)

    print("Start attack")
    attack_eval = OpenAttack.AttackEval(attacker, clsf, metrics=[
            # OpenAttack.metric.Fluency(),
            OpenAttack.metric.GrammaticalErrors(),
            OpenAttack.metric.EditDistance(),
            OpenAttack.metric.ModificationRate(),
            VisiualRate()
    ])
    attack_eval.eval(dataset, visualize=True, progress_bar=True)


if __name__ == "__main__":
    main()
    pass
