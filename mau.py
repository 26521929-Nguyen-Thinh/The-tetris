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
        [[' ', 'I', ' ', ' '],
         [' ', 'I', ' ', ' '],
         [' ', 'I', ' ', ' '],
         [' ', 'I', ' ', ' ']],
        [[' ', 'I', ' ', ' '],
         [' ', 'I', ' ', ' '],
         [' ', 'I', ' ', ' '],
         [' ', 'I', ' ', ' ']],
        [[' ', ' ', ' ', ' '],
         [' ', 'O', 'O', ' '],
         [' ', 'O', 'O', ' '],
         [' ', ' ', ' ', ' ']],
        [[' ', ' ', ' ', ' '],
         [' ', 'O', 'O', ' '],
         [' ', 'O', 'O', ' '],
         [' ', ' ', ' ', ' ']],
        [[' ', ' ', ' ', ' '],
         [' ', 'O', 'O', ' '],
         [' ', 'O', 'O', ' '],
         [' ', ' ', ' ', ' ']],
        [[' ', ' ', ' ', ' '],
         [' ', 'O', 'O', ' '],
         [' ', 'O', 'O', ' '],
         [' ', ' ', ' ', ' ']],
        [[' ', ' ', ' ', ' '],
         [' ', 'O', 'O', ' '],
         [' ', 'O', 'O', ' '],
         [' ', ' ', ' ', ' ']],
        [[' ', ' ', ' ', ' '],
         [' ', 'O', 'O', ' '],
         [' ', 'O', 'O', ' '],
         [' ', ' ', ' ', ' ']],
        [[' ', ' ', ' ', ' '],
         [' ', 'O', 'O', ' '],
         [' ', 'O', 'O', ' '],
         [' ', ' ', ' ', ' ']],
        [[' ', ' ', ' ', ' '],
         ['I', 'I', 'I', 'I'],
         [' ', ' ', ' ', ' '],
         [' ', ' ', ' ', ' ']],
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


def initBoard():
    for i in range(H):
        for j in range(W):
            if i == 0 or i == H - 1 or j == 0 or j == W - 1:
                board[i][j] = '#'
            else:
                board[i][j] = ' '


def draw():
    os.system("cls")

    for i in range(H):
        for j in range(W):
            print(board[i][j], end='')
        print()


def removeLine():
    i = H - 2
    while i > 0:
        j = 0
        while j < W:
            if board[i][j] == ' ':
                break
            j += 1
        if j == W:
            ii = i
            while ii > 1:
                for jj in range(W):
                    board[ii][jj] = board[ii - 1][jj]
                ii -= 1
            for jj in range(W):
                if jj == 0 or jj == W - 1:
                    board[1][jj] = '#'
                else:
                    board[1][jj] = ' '
            i += 1
            draw()
            time.sleep(0.2)
        i -= 1


def main():
    global x, y, b

    random.seed(time.time())
    x = 5
    y = 0
    b = random.randint(0, 32767) % 7
    initBoard()
    while 1:
        boardDelBlock()
        if msvcrt.kbhit():
            c = msvcrt.getwch()
            if c == 'a' and canMove(-1, 0):
                x -= 1
            if c == 'd' and canMove(1, 0):
                x += 1
            if c == 'x' and canMove(0, 1):
                y += 1
            if c == 'q':
                break
        if canMove(0, 1):
            y += 1
        else:
            block2Board()
            removeLine()
            x = 5
            y = 0
            b = random.randint(0, 32767) % 7
        block2Board()
        draw()
        time.sleep(0.5)
    return 0


main()