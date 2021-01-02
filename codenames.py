import copy
import random
from card import *

lineCollection = []
currentLine = []
players = []
words = []
gameWords = []
team1 = []
team2 = []
matrix = []
teamMask = []
CONST_BOARDLENGTH = 5
CONST_BOARDSIZE = CONST_BOARDLENGTH * CONST_BOARDLENGTH


def teamStr(teamList):
    if isinstance(teamList, list):
        teamStr = ""
        for l in range(len(teamList)):
            teamStr += teamList[l]
            if (l < len(teamList)-1):
                teamStr += ", "
        return teamStr


def outputDebug():
    print(team1)
    print(team2)
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
                        token in team1) or (token in team2)
                    if not dublicateP:
                        players.append(token)
                else:
                    dublicateW = (token in words)
                    if not dublicateW:
                        words.append(token.upper())


def setupTeams():
    global team2, team1, players
    assert (len(team2) == 0) and (len(team1) == 0) and (len(players) != 0)

    selectTeam1 = True
    while len(players) > 0:
        random.shuffle(players)
        if selectTeam1:
            team1.append(players.pop())
            selectTeam1 = False
        else:
            team2.append(players.pop())
            selectTeam1 = True


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
    global players, gameWords, team1, team2, teamMask
    while (len(team2) > 0):
        players.append(team2.pop())
    while (len(team1) > 0):
        players.append(team1.pop())
    gameWords.clear()
    matrix.clear()
    teamMask = [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2,
                2, 2, 2, 2, 2, 2, 2, 3, 3, 3, 3, 3, 3, 3]
    setupTeams()
    setupGameWords()
    setupMatrix()


def execute(filepath):
    global lineCollection, currentLine, players, words, team1, team2

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
