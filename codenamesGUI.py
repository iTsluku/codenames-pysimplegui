import PySimpleGUI as sg
from codenames import *

initModel = False

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
    [sg.Text('team tango', size=(20, 1), k='out-team1'),
     sg.Text('team1-list', size=(35, 1), k='out-team1-list'),
     sg.Input(k='in-team1', visible=False),
     sg.Button('Clear', k='clear-1', visible=False)],
    [sg.Text('team zulu', size=(20, 1), k='out-team2'),
     sg.Text('team2-list', size=(35, 1), k='out-team2-list'),
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


def updateView():
    cardNr = 1
    for n in range(len(matrix)):
        for m in range(len(matrix[n])):
            # currentCardStr = str(matrix[n][m])
            currentTextOutputName = "out-text" + str(cardNr)
            # window[currentTextOutputName].update(currentCardStr)
            window[currentTextOutputName].update(matrix[n][m].name)
            cardNr += 1
    window['out-team1-list'].update(team1)
    window['out-team2-list'].update(team2)
    # outputDebug()


toggleView = True


def toggleViewMode():
    global toggleView
    cardNr = 1
    for n in range(len(matrix)):
        for m in range(len(matrix[n])):
            currentTextOutputName = "out-text" + str(cardNr)
            teamId = matrix[n][m].team

            if toggleView:
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

window['out-team1'].update(
    background_color=colorT1)
window['out-team2'].update(
    background_color=colorT2)


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

            if not initModel:
                # override template
                toggleViewMode()

            initModel = True
            window['in-filepath'].update("")
            window['games-counter'].update('{:3}'.format(
                str(int(len(words) / CONST_BOARDSIZE))))
        except FileNotFoundError as e:
            print("Error! Wrong path")

window.close()
