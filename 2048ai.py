from random import randint
import math

gameboard = [[0 for x in range(4)] for y in range(4)]

stop = 0

def place(board):
    if any(0 in sublist for sublist in board):
        a = randint(0,15)
        if gameboard[int(a/4)][a-int(a/4)*4] == 0:
            if randint(0,9) == 0:
                gameboard[int(a/4)][a-int(a/4)*4] = 2
            else:
                gameboard[int(a/4)][a-int(a/4)*4] = 1
        else:
            place(board)
        return(board)
    else:
        return(board)

gameboard = [[0,0,0,0],[0,0,0,1],[0,0,0,0],[1,0,0,0]]

listRight = []
listRightScores = []
listLeft = []
listLeftScores = []

def read_lists():
    global listRight
    global listLeft
    global listRightScores
    global listLeftScores
    f = open('right.txt', 'r')
    for line in f:
        for word in line.split():
            listRight.append(int(word))
    f.close()
    f = open('left.txt', 'r')
    for line in f:
        for word in line.split():
            listLeft.append(int(word))
    f.close()
    f = open('rightScores.txt', 'r')
    for line in f:
        for word in line.split():
            listRightScores.append(int(word))
    f.close()
    f = open('leftScores.txt', 'r')
    for line in f:
        for word in line.split():
            listLeftScores.append(int(word))
    f.close()

def right(board):
    for i in range(4):
        line = 0
        for j in range(4):
            line += board[i][j] << (4*(3-j))
        newLine = listRight[line]
        for j in range (4):
            board[i][j] = (newLine & (0xF << (4*(3-j)))) >> (4*(3-j))
    return(board)

def left(board):
    for i in range(4):
        line = 0
        for j in range(4):
            line += board[i][j] << (4*(3-j))
        newLine = listLeft[line]
        for j in range (4):
            board[i][j] = (newLine & (0xF << (4*(3-j)))) >> (4*(3-j))
    return(board)

def up(board):
    transposedBoard = [[0 for x in range(4)] for y in range(4)]
    for i in range(4):
        for j in range(4):
            transposedBoard[i][j] = board[j][i]
    for i in range(4):
        line = 0
        for j in range(4):
            line += transposedBoard[i][j] << (4*(3-j))
        newLine = listLeft[line]
        for j in range (4):
            transposedBoard[i][j] = (newLine & (0xF << (4*(3-j)))) >> (4*(3-j))
    for i in range(4):
        for j in range(4):
            board[i][j] = transposedBoard[j][i]
    return(board)

def down(board):
    transposedBoard = [[0 for x in range(4)] for y in range(4)]
    for i in range(4):
        for j in range(4):
            transposedBoard[i][j] = board[j][i]
    for i in range(4):
        line = 0
        for j in range(4):
            line += transposedBoard[i][j] << (4*(3-j))
        newLine = listRight[line]
        for j in range (4):
            transposedBoard[i][j] = (newLine & (0xF << (4*(3-j)))) >> (4*(3-j))
    for i in range(4):
        for j in range(4):
            board[i][j] = transposedBoard[j][i]
    return(board)

moveOptions = {0 : up,
           1 : right,
           2 : down,
           3 : left,
           }

def hodnoceni(board):
    score = 0
    for i in range(4):
        for j in range(4):
            score += (i*4)*pow(2,board[i][j])*j
            if board[i][j] == 0:
                score *= 1.1
    return(score)

def minmax(board, turn, depth):
    testBoard = [[0 for x in range(4)] for y in range(4)]
    for k in range(4):
        for l in range(4):
            testBoard[k][l] = board[k][l]

    heur = []
    moveOptions = {0 : up,
           1 : right,
           2 : down,
           3 : left,
           }
    if depth != 0:
        if turn == 0:
            for i in range(4):
                for k in range(4):
                    for l in range(4):
                        testBoard[k][l] = board[k][l]
                testBoard = moveOptions[i](testBoard)
                if testBoard != board:
                    heur.append(minmax(testBoard, 0, depth-1))
                else:
                    heur.append(-1)
            return(max(heur))
        else:
            for i in range(4):
                for j in range(4):
                    for k in range(4):
                        for l in range(4):
                            testBoard[k][l] = board[k][l]
                    if board[i][j] == 0:
                        testBoard[i][j] = 1
                        heur.append(minmax(testBoard, 0, depth-1))
                        testBoard[i][j] = 2
                        heur.append(minmax(testBoard, 0, depth-1))
            return(min(heur))
    else:
        for i in range(4):
            for k in range(4):
                for l in range(4):
                    testBoard[k][l] = board[k][l]
            testBoard = moveOptions[i](testBoard)
            if testBoard != board:
                heur.append(hodnoceni(testBoard))
            else:
                heur.append(-1)
        return(max(heur))

def firstCall(board):
    global stop
    top = -1
    move = 0
    current = -1
    trialBoard = [[0 for x in range(4)] for y in range(4)]
    for i in range(4):
        for j in range(4):
            trialBoard[i][j] = board[i][j]
    trialBoard = up(trialBoard)
    if trialBoard != board:
        current = minmax(trialBoard, 1, 8)
    else:
        current = -1
    if current > top:
        top = current
        move = 0
    for i in range(4):
        for j in range(4):
            trialBoard[i][j] = board[i][j]
    trialBoard = right(trialBoard)
    if trialBoard != board:
        current = minmax(trialBoard, 1, 8)
    else:
        current = -1
    if current > top:
        top = current
        move = 1
    for i in range(4):
        for j in range(4):
            trialBoard[i][j] = board[i][j]
    trialBoard = down(trialBoard)
    if trialBoard != board:
        current = minmax(trialBoard, 1, 8)
    else:
        current = -1
    if current > top:
        top = current
        move = 2
    for i in range(4):
        for j in range(4):
            trialBoard[i][j] = board[i][j]
    trialBoard = left(trialBoard)
    if trialBoard != board:
        current = minmax(trialBoard, 1, 8)
    else:
        current = -1
    if current > top:
        top = current
        move = 3
    if top > -1:
        return(move)
    else:
        stop = 1
        return(0)

read_lists()

for number in gameboard:
    print(number)
print("")

while(stop == 0):
    gameboard = moveOptions[firstCall(gameboard)](gameboard)
    for number in gameboard:
        print(number)
    print("")
    gameboard = place(gameboard)

for number in gameboard:
    print(number)
print("")
