import os
import time
import random
import msvcrt  # tuong duong conio.h (kbhit, getch)

H = 20
W = 15
board = []
for i in range(H):
    board.append([' '] * W)

x = 0
y = 0
b = 0

blocks = [
        [[' ', ' ', ' ', ' '],
         [' ', 'I', ' ', ' '],
         [' ', 'I', ' ', ' '],
         [' ', 'I', ' ', ' ']],
        [[' ', ' ', ' ', ' '],
         [' ', 'O', 'O', ' '],
         [' ', 'O', 'O', ' '],
         [' ', ' ', ' ', ' ']],
        [[' ', ' ', ' ', ' '],
         [' ', 'T', ' ', ' '],
         ['T', 'T', 'T', ' '],
         [' ', ' ', ' ', ' ']],
        [[' ', ' ', ' ', ' '],
         [' ', 'S', 'S', ' '],
         ['S', 'S', ' ', ' '],
         [' ', ' ', ' ', ' ']],
        [[' ', ' ', ' ', ' '],
         ['Z', 'Z', ' ', ' '],
         [' ', 'Z', 'Z', ' '],
         [' ', ' ', ' ', ' ']],
        [[' ', ' ', ' ', ' '],
         ['J', ' ', ' ', ' '],
         ['J', 'J', 'J', ' '],
         [' ', ' ', ' ', ' ']],
        [[' ', ' ', ' ', ' '],
         [' ', ' ', 'L', ' '],
         ['L', 'L', 'L', ' '],
         [' ', ' ', ' ', ' ']]
]

cur = blocks[0]  # khoi dang roi (ma tran 4x4)
nextB = 0        # so thu tu khoi tiep theo trong blocks
score = 0
level = 1
lines = 0        # tong so dong da xoa
speed = 0.5      # so giay cho moi lan khoi roi



#================================================================================================================
# Lâm: chỉnh lại khối, điều khiển, xoay
#================================================================================================================
def canMove(dx, dy):
    for i in range(4):
        for j in range(4):
            if blocks[b][i][j] != ' ':
                xt = x + j + dx
                yt = y + i + dy
                if xt < 1 or xt >= W - 1 or yt >= H - 1:
                    return False
                if board[yt][xt] != ' ':
                    return False
    return True


def block2Board():
    for i in range(4):
        for j in range(4):
            if blocks[b][i][j] != ' ':
                board[y + i][x + j] = blocks[b][i][j]


def boardDelBlock():
    for i in range(4):
        for j in range(4):
            if blocks[b][i][j] != ' ':
                board[y + i][x + j] = ' '


def rotate(m):
    return m


def newBlock():
    global cur, nextB, x, y, b
    b = nextB
    cur = blocks[b]
    nextB = random.randint(0, 6)
    x = 5
    y = 0


def handleKey(c):
    global x, y
    if c == 'a' and canMove(-1, 0):
        x -= 1
    if c == 'd' and canMove(1, 0):
        x += 1
    if c == 'q':
        return 'quit'
    return None



#================================================================================================================
# Phát: xóa dòng, nâng level/tốc độ 
#================================================================================================================
def removeLine():
    return 0


def getLevel(totalLines):
    return 1


def getSpeed(level):
    return 0.5



#================================================================================================================
# Nhân: tính điểm, game over, chơi lại
#================================================================================================================
def addScore(score, n, level):
    return score


def isGameOver():
    return False


def gameOverScreen():
    return 'q'


def resetGame():
    pass



#================================================================================================================
# Thơ: giao dien 
#================================================================================================================
def draw():
    os.system("cls")

    for i in range(H):
        for j in range(W):
            print(board[i][j], end='')
        print()



#================================================================================================================
# Thịnh
#================================================================================================================
def initBoard():
    for i in range(H):
        for j in range(W):
            if i == 0 or i == H - 1 or j == 0 or j == W - 1:
                board[i][j] = '#'
            else:
                board[i][j] = ' '


def main():
    global y, nextB, score, level, lines, speed

    random.seed(time.time())
    nextB = random.randint(0, 6)
    initBoard()
    newBlock()
    while True:
        boardDelBlock()
        if msvcrt.kbhit():
            if handleKey(msvcrt.getwch()) == 'quit':
                break
        if canMove(0, 1):
            y += 1
        else:
            block2Board()
            n = removeLine()
            lines += n
            score = addScore(score, n, level)
            level = getLevel(lines)
            speed = getSpeed(level)
            newBlock()
            if isGameOver():
                if gameOverScreen() == 'q':
                    break
                resetGame()
        block2Board()
        draw()
        time.sleep(speed)
    return 0


main()
