from fontTools.ttLib.ttFont import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.path import Path
import matplotlib._color_data as mcd


font = TTFont('simkai.ttf')

# 获取包含字形名称和字形对象的--字形集对象glyphset
glyphset = font.getGlyphSet()
# 获取pen的基类
pen = SVGPathPen(glyphset)
# 查找"马"的字形对象
glyph = glyphset['uni9A6C']
# 绘制"马"的字形对象
glyph.draw(pen)
# 提取"马"的绘制语句
commands = pen.commands
total_commands = []
command = []
for i in commands:
    # 每一个命令语句
    if i == 'Z':
        # 以闭合路径指令Z区分不同轮廓线
        command.append(i)
        total_commands.append(command)
        command = []
    else:
        command.append(i)
# [' 4 4', ' 5 1 2  2.0', ' 00 3   8', '         .0', '      .0  .0', '          ', '          ', '         .0',
# '     0.0   ', ' 9   0   .0', ' 2   0  ', ' 9   3.0  .0', '   80     .0', '        90.0', '      .0  .0',
# '          ', '     70.0   ', '     60    ', '     50 9', '      .0   ', '          ', '   00  .0 5 ', '   1 20.0
# 6.0', '   1  .0 5.0', '   9 10  4 ', '   0  .0  ', '         5 ', '    4  .0  4 ', '      .0 .0', '   9  .0 2.0',
# '       0.0', ' 90 5  .0 8.0', '   1    4.0', '   7    1.0', '   5    4 ', '   4  .0 0 ', '   7 9.0 4 ',
# ' 7 2 2.0 7 ', ' 7 3 1  2.0', ' 6 1 9.0 3.0', ' 2 5 5.0   ', ' 8   9.0   ', ' 0   6   .0', ' 3   1   .0',
# ' 0   4   .0', ' 9   6.0  .0', ' 3   4 4', 'Z', ' 2 1', '   8    1.0', '   4    1.0', '   8 70  3.0', '   8  .0 7
# ', '   7  .0 2 ', ' 8 8 5  5.0', ' 3 2 3.0 9.0', ' 3 6 7.0 5 ', ' 1 5 2 1', 'Z']
xMin = font['head'].xMin
yMin = font['head'].yMin
xMax = font['head'].xMax
yMax = font['head'].yMax

# 7.1.2  将TTF中的绘制命令转换成matplotlib可以看懂的命令语句
# 笔的当前位置
preX = 0.0
preY = 0.0
# 笔的起始位置
startX = 0.0
startY = 0.0
# 所有轮廓点
total_verts = []
# 所有指令
total_codes = []
# 转换命令
for i in total_commands:
    # 每一条轮廓线
    verts = []
    codes = []
    for command in i:
        # 每一条轮廓线中的每一个命令
        code = command[0]  # 第一个字符是指令
        vert = command[1:].split(' ')  # 其余字符是坐标点，以空格分隔
        #  M  =  路径起始  -  参数  -  起始点坐标  (x  y)+
        if code == 'M':
            codes.append(Path.MOVETO)  # 转换指令
            verts.append((float(vert[0]), float(vert[1])))  # 提取x和y坐标
            # 保存笔的起始位置
            startX = float(vert[0])
            startY = float(vert[1])
            # 保存笔的当前位置(由于是起笔，所以当前位置就是起始位置)
            preX = float(vert[0])
            preY = float(vert[1])
        #  Q  =  绘制二次贝塞尔曲线  -  参数  -  曲线控制点和终点坐标(x1  y1  x  y)+
        elif code == 'Q':
            codes.append(Path.CURVE3)  # 转换指令
            verts.append((float(vert[0]), float(vert[1])))  # 提取曲线控制点坐标
            codes.append(Path.CURVE3)  # 转换指令
            verts.append((float(vert[2]), float(vert[3])))  # 提取曲线终点坐标
            # 保存笔的当前位置--曲线终点坐标x和y
            preX = float(vert[2])
            preY = float(vert[3])
        #  C  =  绘制三次贝塞尔曲线  -  参数  -  曲线控制点1，控制点2和终点坐标(x1  y1  x2  y2  x  y)+
        elif code == 'C':
            codes.append(Path.CURVE4)  # 转换指令
            verts.append((float(vert[0]), float(vert[1])))  # 提取曲线控制点1坐标
            codes.append(Path.CURVE4)  # 转换指令
            verts.append((float(vert[2]), float(vert[3])))  # 提取曲线控制点2坐标
            codes.append(Path.CURVE4)  # 转换指令
            verts.append((float(vert[4]), float(vert[5])))  # 提取曲线终点坐标
            # 保存笔的当前位置--曲线终点坐标x和y
            preX = float(vert[4])
            preY = float(vert[5])
        #  L  =  绘制直线  -  参数  -  直线终点(x,  y)+
        elif code == 'L':
            codes.append(Path.LINETO)  # 转换指令
            verts.append((float(vert[0]), float(vert[1])))  # 提取直线终点坐标
            # 保存笔的当前位置--直线终点坐标x和y
            preX = float(vert[0])
            preY = float(vert[1])
        #  V  =  绘制垂直线  -  参数  -  直线y坐标  (y)+
        elif code == 'V':
            # 由于是垂直线，x坐标不变，提取y坐标
            x = preX
            y = float(vert[0])
            codes.append(Path.LINETO)  # 转换指令
            verts.append((x, y))  # 提取直线终点坐标
            # 保存笔的当前位置--直线终点坐标x和y
            preX = x
            preY = y
        #  H  =  绘制水平线  -  参数  -  直线x坐标  (x)+
        elif code == 'H':
            # 由于是水平线，y坐标不变，提取x坐标
            x = float(vert[0])
            y = preY
            codes.append(Path.LINETO)  # 转换指令
            verts.append((x, y))  # 提取直线终点坐标
            # 保存笔的当前位置--直线终点坐标x和y
            preX = x
            preY = y
        #  Z  =  路径结束，无参数
        elif code == 'Z':
            codes.append(Path.CLOSEPOLY)  # 转换指令
            verts.append((startX, startY))  # 终点坐标就是路径起点坐标
            # 保存笔的当前位置--起点坐标x和y
            preX = startX
            preY = startY
        # 有一些语句指令为空，当作直线处理
        else:
            codes.append(Path.LINETO)  # 转换指令
            verts.append((float(vert[0]), float(vert[1])))  # 提取直线终点坐标
            # 保存笔的当前位置--直线终点坐标x和y
            preX = float(vert[0])
            preY = float(vert[1])
    # 整合所有指令和坐标
    total_verts.append(verts)
    total_codes.append(codes)
# 7.1.3  绘制PNG图片
# 获取matplotklib中的颜色列表
color_list = list(mcd.CSS4_COLORS)
# 获取所有的轮廓坐标点
total_x = []
total_y = []
for contour in total_verts:
    # 每一条轮廓曲线
    x = []
    y = []
    for i in contour:
        # 轮廓线上每一个点的坐标(x,y)
        x.append(i[0])
        y.append(i[1])
    total_x.append(x)
    total_y.append(y)
# 创建画布窗口
fig, ax = plt.subplots()
# 按照'head'表中所有字形的边界框设定x和y轴上下限
ax.set_xlim(xMin, xMax)
ax.set_ylim(yMin, yMax)
# 设置画布1:1显示
ax.set_aspect(1)
# 添加网格线
ax.grid(alpha=0.8, linestyle='--')
# 画图
for i in range(len(total_codes)):
    # (1)绘制轮廓线
    # 定义路径
    path = Path(total_verts[i], total_codes[i])
    # 创建形状，无填充，边缘线颜色为color_list中的颜色，边缘线宽度为2
    patch = patches.PathPatch(path, facecolor='none', edgecolor=color_list[i + 10], lw=2)
    # 将形状添到图中
    ax.add_patch(patch)
    # (2)绘制轮廓点--黑色,点大小为10
    ax.scatter(total_x[i], total_y[i], color='black', s=10)
# 保存图片
plt.savefig("simkai-马.png")
