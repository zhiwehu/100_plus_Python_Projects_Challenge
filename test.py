from turtle import *
from math import ceil, floor
from random import randint

n = 10
gz = 40
bc = n * gz
win = False
dead = False
can_start = True
fx = [[-1, -1], [-1, 0], [-1, 1], [0, -1], [0, 1], [1, -1], [1, 0], [1, 1]]
# 随机生成地雷数量
booms = randint(n * n // 10, n * n // 2)
d = []
m = []
c = []
b = []

t = Turtle()
t.ht()
t.up()
t.speed(0)

judge = Turtle()
judge.ht()
judge.up()
judge.speed(0)


# 画边框
def draw():
    t.clear()
    t.seth(0)
    t.color("black")
    t.goto(-bc / 2, bc / 2)
    for i in range(n + 1):
        t.down()
        t.fd(bc)
        t.bk(bc)
        t.up()
        t.goto(-bc / 2, bc / 2 - (i + 1) * gz)
    t.goto(-bc / 2, bc / 2)
    t.rt(90)
    for i in range(n + 1):
        t.down()
        t.fd(bc)
        t.bk(bc)
        t.up()
        t.goto(-bc / 2 + (i + 1) * gz, bc / 2)


# 写地雷数
def write_booms():
    judge.clear()
    judge.goto(-gz, bc / 2 + gz - gz / 8)
    judge.color("red")
    judge.dot(20)
    judge.goto(0, bc / 2 + gz / 2)
    judge.write(": {}".format(booms), align="center", font=("Kai", 30, "bold"))


# 初始化列表
def init_list(n, default=0):
    lines = []
    for i in range(n):
        line = []
        for j in range(n):
            line.append(default)
        lines.append(line)
    return lines


# 打印列表
def print_list(lines):
    print()
    for line in lines:
        for item in line:
            print(item, end=' ')
        print()
    print()


# x,y -> i, j
def xytoij(x, y):
    ix = floor(x / gz) * gz
    iy = floor(y / gz) * gz
    j = (ix + bc / 2) / gz
    i = (bc / 2 - iy) / gz - 1
    return int(i), int(j)


# i, j -> x, y
def ijtoxy(i, j):
    x = -bc / 2 + gz / 2 + j * gz
    y = bc / 2 - gz / 2 - i * gz - gz / 4
    return x, y


def set_color(booms):
    if booms <= 1:
        t.color("green")
    elif booms == 2:
        t.color("blue")
    elif booms == 3:
        t.color("brown")
    elif booms == 4:
        t.color("orange")
    elif booms == 5:
        t.color("red")
    elif booms >= 6:
        t.color("purple")


def start():
    global d, m, c, b, booms, can_start, win, dead
    if can_start:
        win = False
        dead = False
        can_start = False
        draw()
        # 地雷列表：0表示没雷，1表示有雷
        d = init_list(n)
        # 标记列表：0表示没雷，1表示有雷
        m = init_list(n)
        # 点击列表：0表示没点击，1表示点击
        c = init_list(n)
        # 计算得出地雷数量列表：-1表示地雷，其他数字表示周围有多少地雷
        b = init_list(n)
        booms = randint(n * n // 10, n * n // 2)
        # 随机生成地雷
        for k in range(booms):
            i = randint(0, n - 1)
            j = randint(0, n - 1)
            d[i][j] = 1

        write_booms()

        # 计算每个位置周围有多少雷，存放b列表
        for i in range(n):
            for j in range(n):
                if d[i][j] == 1:
                    b[i][j] = -1
                    for f in fx:
                        ni = i + f[0]
                        nj = j + f[1]
                        if (ni >= 0 and ni < n and nj >= 0 and nj < n and b[ni][nj] != -1):
                            b[ni][nj] += 1


# 检查i, j周围8个方向(一圈)，如果没有雷或者已经全部正确标记，则返回True
def check_around(i, j):
    cnt = 0
    for f in fx:
        ni = i + f[0]
        nj = j + f[1]

        if (ni >= 0 and ni < n and nj >= 0 and nj < n):
            if d[ni][nj] == 1 and m[ni][nj] == 1:
                cnt += 1
    return b[i][j] == cnt


# 如果i, j位置周围已经全部确认，则在i, j的8个方向上的下一个位置，递归再检查
def check_and_auto_click(i, j):
    if (i >= 0 and i < n and j >= 0 and j < n and check_around(i, j)):
        for f in fx:
            ni = i + f[0]
            nj = j + f[1]
            if (ni >= 0 and ni < n and nj >= 0 and nj < n and b[ni][nj] != -1 and c[ni][nj] == 0):
                c[ni][nj] = 1
                check_and_auto_click(ni, nj)
                x, y = ijtoxy(ni, nj)
                t.goto(x, y)
                set_color(b[ni][nj])
                t.write(b[ni][nj], align="center", font=("Arial", 20, "normal"))


# 检查是否已经胜利
def check_win():
    for i in range(n):
        for j in range(n):
            if m[i][j] != d[i][j]:
                return False
    return True


# 鼠标左键点击扫雪
def click(x, y):
    global dead, win, can_start
    if not dead and not win:
        i, j = xytoij(x, y)
        if (i >= 0 and i < n and j >= 0 and j < n and c[i][j] == 0):
            c[i][j] = 1
            if d[i][j] == 1:
                t.goto(floor(x / gz) * gz + gz / 2, floor(y / gz) * gz + gz / 2)
                t.color("red")
                t.dot(20)
                dead = True
                can_start = True
                judge.clear()
                judge.color("red")
                judge.write("失败,按空格键重新开始", align="center", font=("Kai", 40, "bold"))
            else:
                t.goto(floor(x / gz) * gz + gz / 2, floor(y / gz) * gz + gz / 4)
                set_color(b[i][j])
                t.write(b[i][j], align="center", font=("Arial", 20, "normal"))
                check_and_auto_click(i, j)
                if check_win():
                    win = True
                    can_start = True
                    judge.clear()
                    judge.color("green")
                    judge.write("胜利,按空格键重新开始", align="center", font=("Kai", 40, "bold"))


# 右键标记雷
def mark(x, y):
    global booms, win, can_start
    if not dead and not win:
        i, j = xytoij(x, y)
        if (i >= 0 and i < n and j >= 0 and j < n and c[i][j] == 0):
            t.goto(floor(x / gz) * gz + gz / 2, floor(y / gz) * gz + gz / 2)
            if m[i][j] == 0:
                m[i][j] = 1
                t.color("green")
                t.dot(20)
                booms -= 1
            else:
                m[i][j] = 0
                t.color("white")
                t.dot(22)
                booms += 1
            write_booms()
            if check_win():
                win = True
                can_start = True
                judge.clear()
                judge.color("green")
                judge.write("胜利,按空格键重新开始", align="center", font=("Kai", 40, "bold"))


start()
screen = Screen()
screen.onscreenclick(click, 1)
screen.onscreenclick(mark, 2)
screen.onkey(start, "space")
screen.listen()
done()
