import copy
import random
from card import *

lineCollection = []
currentLine = []
players = []
words = []
gameWords = []
teamRed = []
teamBlue = []
matrix = []
teamMask = []
CONST_BOARDLENGTH = 5
CONST_BOARDSIZE = CONST_BOARDLENGTH*CONST_BOARDLENGTH


def outputDebug():
    print(teamRed)
    print(teamBlue)
    printMatrix()


def printMatrix():
    global matrix
    print()
    for v in range(len(matrix)):
        for w in range(len(matrix[v])):
            print(str(matrix[v][w]), end='      ')
        print()
    print()


def setupMatrix():
    global gameWords, matrix, teamMask, CONST_BOARDLENGTH
    random.shuffle(teamMask)

    for k in range(CONST_BOARDLENGTH):
        row = []
        for l in range(CONST_BOARDLENGTH):
            cardNr = k*CONST_BOARDLENGTH+l
            row.append(Card(gameWords[cardNr - 1], teamMask[cardNr - 1], True))
        matrix.append(row)


def parseWordsPlayers():
    global currentLine, players, words, lineCollection
    status = 0  # 0:nichts,1:players,2:words
    for line in lineCollection:
        currentLine = line
        if (len(currentLine) == 2 and currentLine[0] == "#####"):
            if (currentLine[1] == "players"):
                status = 1
            elif (currentLine[1] == "words"):
                status = 2
            else:
                status = 0
        elif (len(currentLine) > 0 and status != 0):
            for token in currentLine:
                if (status == 1):
                    dublicateP = (token in players) or (
                        token in teamRed) or (token in teamBlue)
                    if not dublicateP:
                        players.append(token)
                else:
                    dublicateW = (token in words)
                    if not dublicateW:
                        words.append(token)


def setupTeams():
    global teamBlue, teamRed, players
    assert (len(teamBlue) == 0) and (len(teamRed) == 0) and (len(players) != 0)

    selectTeamRed = True
    while len(players) > 0:
        random.shuffle(players)
        if selectTeamRed:
            teamRed.append(players.pop())
            selectTeamRed = False
        else:
            teamBlue.append(players.pop())
            selectTeamRed = True


def setupGameWords():
    global CONST_BOARDSIZE, gameWords, words
    assert (len(gameWords) == 0 and len(words) >=
            CONST_BOARDSIZE)  # add error msg gui
    i = 0
    while (i < CONST_BOARDSIZE):
        index = random.randint(0, len(words)-1)
        gameWords.append(words[index])
        words.remove(words[index])
        i += 1


def initNewGame():
    global players, gameWords, teamRed, teamBlue, teamMask
    while (len(teamBlue) > 0):
        players.append(teamBlue.pop())
    while (len(teamRed) > 0):
        players.append(teamRed.pop())
    gameWords.clear()
    matrix.clear()
    teamMask = [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2,
                2, 2, 2, 2, 2, 2, 2, 3, 3, 3, 3, 3, 3, 3]
    setupTeams()
    setupGameWords()
    setupMatrix()


def execute(filepath):
    global lineCollection, currentLine, players, words, teamRed, teamBlue

    file = open(filepath, 'r')
    for line in file:
        tokens = line.strip().split()
        for token in tokens:
            currentLine.append(token)
        lineCollection.append(copy.deepcopy(currentLine))
        currentLine.clear()
    file.close
    parseWordsPlayers()
    initNewGame()
