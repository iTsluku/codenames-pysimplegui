import PySimpleGUI as sg
from codenames import *
from board import *
from collections import deque

initModel = False
stack = deque()
'''
state 0 : no active game
state 1 : team1 enter codename
state 2 : team1 guess names
state 3 : team2 enter codename
state 4 : team2 guess names
'''
state = 0  # default game-state
cc = ""  # current codename

colorBg = "#283b5b"
colorT0 = "#512d38"
colorT1 = "#89ce94"
colorT2 = "#92bcea"
colorT3 = "#4e4b5c"

tsh = 14  # textsize horizontal
tsv = 4  # textsize vertical
fs = 16  # fontsize

# init layout
layout = [[sg.Button('', size=(tsh, tsv), font=(
    "Helvetica", fs), k='out-text1'),
    sg.Button('', size=(tsh, tsv), font=(
        "Helvetica", fs), k='out-text2'),
    sg.Button('', size=(tsh, tsv), font=(
        "Helvetica", fs), k='out-text3'),
    sg.Button('', size=(tsh, tsv), font=(
        "Helvetica", fs), k='out-text4'),
    sg.Button('', size=(tsh, tsv), font=(
        "Helvetica", fs), k='out-text5')],
    [sg.Button('', size=(tsh, tsv), font=(
        "Helvetica", fs), k='out-text6'),
     sg.Button('', size=(tsh, tsv), font=(
         "Helvetica", fs), k='out-text7'),
     sg.Button('', size=(tsh, tsv), font=(
         "Helvetica", fs), k='out-text8'),
     sg.Button('', size=(tsh, tsv), font=(
         "Helvetica", fs), k='out-text9'),
     sg.Button('', size=(tsh, tsv), font=(
         "Helvetica", fs), k='out-text10')],
    [sg.Button('', size=(tsh, tsv), font=(
        "Helvetica", fs), k='out-text11'),
     sg.Button('', size=(tsh, tsv), font=(
         "Helvetica", fs), k='out-text12'),
     sg.Button('', size=(tsh, tsv), font=(
         "Helvetica", fs), k='out-text13'),
     sg.Button('', size=(tsh, tsv), font=(
         "Helvetica", fs), k='out-text14'),
     sg.Button('', size=(tsh, tsv), font=(
         "Helvetica", fs), k='out-text15')],
    [sg.Button('', size=(tsh, tsv), font=(
        "Helvetica", fs), k='out-text16'),
     sg.Button('', size=(tsh, tsv), font=(
         "Helvetica", fs), k='out-text17'),
     sg.Button('', size=(tsh, tsv), font=(
         "Helvetica", fs), k='out-text18'),
     sg.Button('', size=(tsh, tsv), font=(
         "Helvetica", fs), k='out-text19'),
     sg.Button('', size=(tsh, tsv), font=(
         "Helvetica", fs), k='out-text20')],
    [sg.Button('', size=(tsh, tsv), font=(
        "Helvetica", fs), k='out-text21'),
     sg.Button('', size=(tsh, tsv), font=(
         "Helvetica", fs), k='out-text22'),
     sg.Button('', size=(tsh, tsv), font=(
         "Helvetica", fs), k='out-text23'),
     sg.Button('', size=(tsh, tsv), font=(
         "Helvetica", fs), k='out-text24'),
     sg.Button('', size=(tsh, tsv), font=(
         "Helvetica", fs), k='out-text25')],
    [sg.HorizontalSeparator()],
    [sg.Button('Undo', k='undo'),
     sg.VerticalSeparator(),
     sg.Button('Skip', k='skip'),
     sg.VerticalSeparator(),
     sg.Text('Codename:'),
     sg.Text('', k='out-codename', size=(20, 1), font=("Helvetica", 14)),
     sg.Input(k='in-codename', visible=False),
     sg.Button('Apply', k='apply-codename', visible=False)],
    [sg.HorizontalSeparator()],
    [sg.Text('team tango', size=(20, 1), k='out-team1',
             font=("Helvetica", 11)),
     sg.Text('', k='score-team1',
             font=("Helvetica", 14), text_color=colorT1),
     sg.Text('', size=(35, 1), font=("Helvetica", 11), k='out-team1-list'),
     sg.Input(k='in-team1', visible=False),
     sg.Button('Clear', k='clear-1', visible=False)],
    [sg.Text('team zulu', size=(20, 1), k='out-team2',
             font=("Helvetica", 11)),
     sg.Text('', k='score-team2',
             font=("Helvetica", 14), text_color=colorT2),
     sg.Text('', size=(35, 1), font=("Helvetica", 11), k='out-team2-list'),
     sg.Input(k='in-team2', visible=False),
     sg.Button('Clear', k='clear-2', visible=False)],
    [sg.HorizontalSeparator()],
    [sg.Button('New', k='new-game'),
     sg.VerticalSeparator(),
     sg.Button('Edit', k='edit-teamname'),
     sg.Button('Apply', k='apply-teamname'),
     sg.VerticalSeparator(),
     sg.Button('Toggle', k='toggle-view'),
     sg.VerticalSeparator(),
     sg.Text('Filepath'),
     sg.Input(k='in-filepath'),
     sg.FileBrowse(),
     sg.Button('Apply', k='apply-file'),
     sg.VerticalSeparator(),
     sg.Text('Games:'),
     sg.Text('0', k='games-counter', size=(3, 1)),
     sg.VerticalSeparator(),
     sg.Button('Exit', k='exit')]]


def gameDone():
    global matrix
    team1sum = 0
    team2sum = 0
    for n in range(len(matrix)):
        for m in range(len(matrix[n])):
            card = matrix[n][m]
            if (card.team == 1 and card.active):
                team1sum += 1
            elif (card.team == 2 and card.active):
                team2sum += 1
    if (team1sum == 0 or team2sum == 0):
        # todo winner msg ...
        '''
        winnerMsg = ""
        if (team1sum == 0):
            winnerMsg = str(values['out-team1']) + " gewinnt!"
        else:
            winnerMsg = str(values['out-team2']) + " gewinnt!"
        window['out-codename'].update(winnerMsg)
        '''
        return True
    else:
        return False


def updateScore():
    global matrix
    team1sum = 0
    team2sum = 0
    for n in range(len(matrix)):
        for m in range(len(matrix[n])):
            card = matrix[n][m]
            if (card.team == 1 and card.active):
                team1sum += 1
            elif (card.team == 2 and card.active):
                team2sum += 1
    window['score-team1'].update(team1sum)
    window['score-team2'].update(team2sum)


def resetGameState():
    global state, stack, cc
    stack.clear()
    stateChange(1)
    updateScore()
    cc = ""


def guessCard(key):
    global state, matrix, stack, CONST_BOARDLENGTH

    if (state == 2 or state == 4):
        index = int(key.removeprefix('out-text'))
        row = int(index / CONST_BOARDLENGTH)
        if (index % CONST_BOARDLENGTH != 0):
            row += 1
        col = index - (row-1)*CONST_BOARDLENGTH
        card = matrix[row-1][col-1]

        if card.active:
            # push current board to stack
            stack.append(Board(copy.deepcopy(matrix),
                               state, cc))
            if card.team == 0:
                window[key].update(button_color=("white", colorT0))
            elif card.team == 1:
                window[key].update(button_color=("white", colorT1))
            elif card.team == 2:
                window[key].update(button_color=("white", colorT2))
            elif card.team == 3:
                window[key].update(button_color=("white", colorT3))
            card.active = False
            updateScore()
            if (gameDone() or card.team == 0):
                stateChange(0)
            elif (state == 2 and card.team != 1):
                stateChange(3)
            elif (state == 4 and card.team != 2):
                stateChange(1)


def stateChange(s):
    global state
    # s : new state (to change to)
    if (s >= 0 and s <= 4):
        state = s
        if (state == 1 or state == 3):
            window['out-codename'].update("")
            window['in-codename'].update("")
            window['in-codename'].update(visible=True)
            window['apply-codename'].update(visible=True)
        elif (state == 0 or state == 2 or state == 4):
            window['in-codename'].update(visible=False)
            window['apply-codename'].update(visible=False)
        if (state == 1 or state == 2):
            window['out-team1'].update(background_color=colorT1)
            window['out-team2'].update(background_color=colorBg)
        elif (state == 3 or state == 4):
            window['out-team2'].update(background_color=colorT2)
            window['out-team1'].update(background_color=colorBg)


def updateView():
    global matrix
    cardNr = 1
    for n in range(len(matrix)):
        for m in range(len(matrix[n])):
            # currentCardStr = str(matrix[n][m])
            currentTextOutputName = "out-text" + str(cardNr)
            # window[currentTextOutputName].update(currentCardStr)
            window[currentTextOutputName].update(matrix[n][m].name)
            cardNr += 1
    window['out-team1-list'].update(teamStr(team1))
    window['out-team2-list'].update(teamStr(team2))
    # outputDebug()


def updateViewChange():
    cardNr = 1
    for n in range(len(matrix)):
        for m in range(len(matrix[n])):
            currentTextOutputName = "out-text" + str(cardNr)
            teamId = matrix[n][m].team
            active = matrix[n][m].active

            if teamId == 0 and not active:
                window[currentTextOutputName].update(
                    button_color=("white", colorT0))
            elif teamId == 1 and not active:
                window[currentTextOutputName].update(
                    button_color=("white", colorT1))
            elif teamId == 2 and not active:
                window[currentTextOutputName].update(
                    button_color=("white", colorT2))
            elif teamId == 3 and not active:
                window[currentTextOutputName].update(
                    button_color=("white", colorT3))
            else:
                window[currentTextOutputName].update(
                    button_color=("white", colorBg))
            cardNr += 1


toggleView = True


def toggleViewMode():
    global toggleView

    if (state == 1 or state == 3):
        cardNr = 1
        for n in range(len(matrix)):
            for m in range(len(matrix[n])):
                currentTextOutputName = "out-text" + str(cardNr)
                teamId = matrix[n][m].team
                active = matrix[n][m].active

                if toggleView:
                    if teamId == 0 and not active:
                        window[currentTextOutputName].update(
                            button_color=("white", colorT0))
                    elif teamId == 1 and not active:
                        window[currentTextOutputName].update(
                            button_color=("white", colorT1))
                    elif teamId == 2 and not active:
                        window[currentTextOutputName].update(
                            button_color=("white", colorT2))
                    elif teamId == 3 and not active:
                        window[currentTextOutputName].update(
                            button_color=("white", colorT3))
                    else:
                        window[currentTextOutputName].update(
                            button_color=("white", colorBg))
                else:
                    if teamId == 0:
                        window[currentTextOutputName].update(
                            button_color=("white", colorT0))
                    elif teamId == 1:
                        window[currentTextOutputName].update(
                            button_color=("white", colorT1))
                    elif teamId == 2:
                        window[currentTextOutputName].update(
                            button_color=("white", colorT2))
                    elif teamId == 3:
                        window[currentTextOutputName].update(
                            button_color=("white", colorT3))
                cardNr += 1
        toggleView = not toggleView


# init gui
window = sg.Window('codenames', layout, finalize=True)


toggle = True
while True:
    event, values = window.read()

    if event == 'exit' or event == sg.WIN_CLOSED:
        break

    if event == 'new-game' and initModel:
        initNewGame()
        updateView()
        toggleView = True
        toggleViewMode()
        window['games-counter'].update('{:3}'.format(
            str(int(len(words) / CONST_BOARDSIZE))))
        resetGameState()
        updateViewChange()

    if event == 'undo':
        if stack:
            # stack not empty
            boardPop = stack.pop()
            applyMatrix(boardPop.matrix)
            stateChange(boardPop.state)
            window['out-codename'].update(boardPop.codename)
            print(boardPop.codename)

            if (boardPop.state == 1 or boardPop.state == 2):
                window['out-codename'].update(text_color=colorT1)
            elif(boardPop.state == 3 or boardPop.state == 4):
                window['out-codename'].update(text_color=colorT2)
            updateViewChange()
            updateScore()

    if event == 'apply-codename':
        if values['in-codename'] != '':
            window['out-codename'].update(values['in-codename'])
            cc = values['in-codename']
            if toggleView:
                toggleViewMode()
            if state == 1:
                window['out-codename'].update(text_color=colorT1)
                stateChange(2)
            elif state == 3:
                window['out-codename'].update(text_color=colorT2)
                stateChange(4)

    if event == 'skip':
        if (state != 0):
            # push current board to stack
            stack.append(Board(copy.deepcopy(matrix),
                               state, cc))
            if (state == 1 or state == 2):
                stateChange(3)
            else:
                stateChange(1)

    if event == 'edit-teamname':
        window['in-team1'].update(visible=toggle)
        window['in-team2'].update(visible=toggle)
        window['clear-1'].update(visible=toggle)
        window['clear-2'].update(visible=toggle)
        toggle = not toggle

    if event == 'apply-teamname':
        window['in-team1'].update(visible=False)
        window['in-team2'].update(visible=False)
        window['clear-1'].update(visible=False)
        window['clear-2'].update(visible=False)
        toggle = True
        # toto check if in-team1 or in-team2 is equal to ""-> then dont update
        if values['in-team1'] != '':
            window['out-team1'].update(values['in-team1'])
        if values['in-team2'] != '':
            window['out-team2'].update(values['in-team2'])

    if event == 'clear-1':
        window['in-team1'].update("")

    if event == 'clear-2':
        window['in-team2'].update("")

    if event == 'toggle-view' and initModel:
        toggleViewMode()

    if event == 'apply-file':
        try:
            execute(values['in-filepath'])
            updateView()
            resetGameState()

            if not initModel:
                # override template
                toggleViewMode()

            initModel = True
            window['in-filepath'].update("")
            window['games-counter'].update('{:3}'.format(
                str(int(len(words) / CONST_BOARDSIZE))))
        except FileNotFoundError as e:
            print("Error! Wrong path")

    if event == 'out-text1':
        guessCard('out-text1')
    if event == 'out-text2':
        guessCard('out-text2')
    if event == 'out-text3':
        guessCard('out-text3')
    if event == 'out-text4':
        guessCard('out-text4')
    if event == 'out-text5':
        guessCard('out-text5')
    if event == 'out-text6':
        guessCard('out-text6')
    if event == 'out-text7':
        guessCard('out-text7')
    if event == 'out-text8':
        guessCard('out-text8')
    if event == 'out-text9':
        guessCard('out-text9')
    if event == 'out-text10':
        guessCard('out-text10')
    if event == 'out-text11':
        guessCard('out-text11')
    if event == 'out-text12':
        guessCard('out-text12')
    if event == 'out-text13':
        guessCard('out-text13')
    if event == 'out-text14':
        guessCard('out-text14')
    if event == 'out-text15':
        guessCard('out-text15')
    if event == 'out-text16':
        guessCard('out-text16')
    if event == 'out-text17':
        guessCard('out-text17')
    if event == 'out-text18':
        guessCard('out-text18')
    if event == 'out-text19':
        guessCard('out-text19')
    if event == 'out-text20':
        guessCard('out-text20')
    if event == 'out-text21':
        guessCard('out-text21')
    if event == 'out-text22':
        guessCard('out-text22')
    if event == 'out-text23':
        guessCard('out-text23')
    if event == 'out-text24':
        guessCard('out-text24')
    if event == 'out-text25':
        guessCard('out-text25')


window.close()
