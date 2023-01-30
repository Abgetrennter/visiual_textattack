from PIL import ImageFont, Image, ImageDraw
import argparse
from fontTools.ttLib.ttFont import TTFont
import os, numpy as np

parse = argparse.ArgumentParser(description="将ttf字体文件转为图片")
parse.add_argument('-f', help="输入字体文件", default="data/fonts/simkai.ttf")
parse.add_argument('-o', help="图片输出目录,默认为当前目录下imgs", default="imgs")
parse.add_argument('-s', '--size', type=int, help="输出图片的像素大小", default=50)

args = parse.parse_args()
os.makedirs("data/fonts/simkai", exist_ok=True)


def uni_2_png(txt, font=args.f, img_size=args.size):
    img = Image.new('1', (img_size, img_size), 255)
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype(font, img_size)

    # x, y = draw.textsize(txt, font=font)
    # draw.text(((img_size - x) // 2, (img_size - y) // 2), txt, font=font, fill=0)
    draw.text((0, 0), txt, font=font, fill=0)
    file_name = f'simkai/{txt}.png'
    img.save(file_name)
    img.show()
    input()
    # return img


if __name__ == '__main__':
    f = TTFont(args.f)
    s = []
    ss = "abcdefghijklmnopqrstuvwxyz""ABCDEFGHIJKLMNOPQRSTUVWXYZ""0123456789"
    q="亷"
    for i in q:
        # uni_2_png(i)
        s.append(np.array(uni_2_png(i)).astype(int).reshape(args.size * args.size))
    # s=np.array(s)
    omega=[]
    for i in range(len(q)):
        for j in range(i+1,len(q)):
            print(q[i],q[j],':')
            vec1, vec2 = s[i], s[j]
            print(vec1.dot(vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2)))
            omega.append(((q[i],q[j]),vec1.dot(vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2))))
    print(sorted(omega,key=lambda x:x[1]))
# # for i in f.getBestCmap():
#     uni_2_png(chr(i))
