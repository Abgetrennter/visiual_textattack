from paddleocr import PaddleOCR, draw_ocr
from PIL import Image
import numpy as np
from pic import Font2pic
from define import sentence_example, sentence_changed, sentence_faltten

ocr = PaddleOCR()#rec_model_dir='C:\\Users\\abget/.paddleocr/whl\\rec\\ch\\ch_ppocr_server_v2.0_rec_infer')  # need to run only once to download and load model into memory

_font = Font2pic()

result = ocr.ocr(_font.to_vac(_font.draw(sentence_faltten)), cls=False)
for idx in range(len(result)):
    res = result[idx]
    for line in res:
        print(line)

# 显示结果

result = result[0]
boxes = [line[0] for line in result]
txts = [line[1][0] for line in result]
scores = [line[1][1] for line in result]

print("".join(txts))