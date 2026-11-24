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
            if cur[i][j] != ' ':
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
            if cur[i][j] != ' ':
                board[y + i][x + j] = cur[i][j]


def boardDelBlock():
    for i in range(4):
        for j in range(4):
            if cur[i][j] != ' ':
                board[y + i][x + j] = ' '


def rotate(m):
    rotated_m = [[' ' for _ in range(4)] for _ in range(4)]
    for i in range(4):
        for j in range(4):
            rotated_m[i][j] = m[3 - j][i]
    return rotated_m


def newBlock():
    global cur, nextB, x, y, b
    b = nextB
    cur = [row[:] for row in blocks[b]]
    nextB = random.randint(0, 6)
    x = 5
    y = 0


def handleKey(c):
    global x, y, cur
    
    if c == 'a' and canMove(-1, 0):
        x -= 1

    if c == 'd' and canMove(1, 0):
        x += 1

    if c == 's' and canMove(0, 1):
        y += 1

    if c == ' ':
        while(canMove(0, 1)):
            y += 1

    if c == 'w':
        old = cur
        cur = rotate(cur)
        if( not canMove(0, 0)):
            cur = old

    if c == 'p':
        print("Bạn đã tạm dừng trò chơi, vui lòng nhấn phím 'p' để tiếp tục")
        while(True):     
            if msvcrt.getwch() == 'p':
                break

    if c == 'q':
        print("Bạn đã ấn phím 'q' để thoát khỏi màn chơi")
        return 'quit'
    return None


#================================================================================================================
# Phát: xóa dòng, nâng level/tốc độ 
#================================================================================================================
def removeLine():
    r = H - 2
    n = 0
    
    while r >= 1:
        
        if all(cell != " " for cell in board[r]):
            del board[r]
            board.insert(1, ["#"] + [" "]*(W-2) + ["#"])
            n += 1
        
        else:
            r -= 1
    
    return n


def getLevel(totalLines):
    level = totalLines // 10 + 1
    return level


def getSpeed(level):
    speed = max(0.1, 0.5 - 0.05*(level-1))
    return speed


#================================================================================================================
# Nhân: tính điểm, game over, chơi lại
#================================================================================================================
def addScore(score, n, level):
    bang = [0, 100, 300, 500, 800]
    if n <= 0:
        return score
    if n > 4:
        n = 4
    return score + bang[n] * level


def isGameOver():
    return not canMove(0, 0)


def nhan_highscorePath():
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), "highscore.txt")


def nhan_readHighscore():
    try:
        with open(nhan_highscorePath(), "r") as f:
            return int(f.read().strip())
    except (OSError, ValueError):
        return 0


def nhan_writeHighscore(value):
    try:
        with open(nhan_highscorePath(), "w") as f:
            f.write(str(value))
    except OSError:
        pass


def gameOverScreen():
    high = nhan_readHighscore()
    if score > high:
        high = score
        nhan_writeHighscore(high)

    os.system("cls")
    print("=========================")
    print("        GAME OVER")
    print("=========================")
    print("Diem cua van nay :", score)
    print("Diem cao nhat    :", high)
    print()
    print("Bam r de choi lai, q de thoat")
    while msvcrt.kbhit():
        msvcrt.getwch()

    while True:
        c = msvcrt.getwch().lower()
        if c == 'r' or c == 'q':
            return c


def resetGame():
    global score, lines, level, speed
    initBoard()
    score = 0
    lines = 0
    level = 1
    speed = 0.5
    newBlock()



#================================================================================================================
# Thơ: giao dien 
#================================================================================================================
def draw():
    global board, score, level, lines
    os.system("cls")
    
    for i in range(len(board)):
        row_str = ""
        for j in range(len(board[i])):
            cell = board[i][j]
            if cell == '#':
                row_str += '▓▓'
            elif cell == ' ':
                row_str += '  '
            else:
                row_str += '██'
        
        if i == 0:
            row_str += "    Score: " + str(score)
        elif i == 1:
            row_str += "    Level: " + str(level)
        elif i == 2:
            row_str += "    Lines: " + str(lines)
            
        print(row_str)



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
