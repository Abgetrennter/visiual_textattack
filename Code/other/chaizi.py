from bs4 import BeautifulSoup
import os
import pickle
import json
from tqdm import tqdm
path = r"../../Data/Html"
r = os.listdir(path)
all_chara = {}
for c in tqdm(r):
    with open(path + "/" + c, "r", encoding="utf8") as f:
        soup = BeautifulSoup(f.read(), 'lxml')
    l = soup.div.div.table.td.find_next_sibling().table.find_all("td")
    q = [i.string.split("：") for i in l]
    if soup.div.div.em:
        p = soup.div.div.em.find_all("a")
        q.append(["异体字", "".join(i.string for i in p)])
    for i in q[:]:
        if i[0] == 'Unicode':
            q.remove(i)
    all_chara[c] = dict(q)

json.dump(all_chara, open("1.json", "w", encoding="utf8"))
pickle.dump(all_chara, open("1.pkl", "wb"))
