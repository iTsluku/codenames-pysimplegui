import PySimpleGUI as sg
from codenames import *

initModel = False

# init layout
layout = [[sg.Text('text1', size=(20, 1), k='out-text1'),
           sg.Text('text2', size=(20, 1), k='out-text2'),
           sg.Text('text3', size=(20, 1), k='out-text3'),
           sg.Text('text4', size=(20, 1), k='out-text4'),
           sg.Text('text5', size=(20, 1), k='out-text5')],
          [sg.Text('text6', size=(20, 1), k='out-text6'),
           sg.Text('text7', size=(20, 1), k='out-text7'),
           sg.Text('text8', size=(20, 1), k='out-text8'),
           sg.Text('text9', size=(20, 1), k='out-text9'),
           sg.Text('text10', size=(20, 1), k='out-text10')],
          [sg.Text('text11', size=(20, 1), k='out-text11'),
           sg.Text('text12', size=(20, 1), k='out-text12'),
           sg.Text('text13', size=(20, 1), k='out-text13'),
           sg.Text('text14', size=(20, 1), k='out-text14'),
           sg.Text('text15', size=(20, 1), k='out-text15')],
          [sg.Text('text16', size=(20, 1), k='out-text16'),
           sg.Text('text17', size=(20, 1), k='out-text17'),
           sg.Text('text18', size=(20, 1), k='out-text18'),
           sg.Text('text19', size=(20, 1), k='out-text19'),
           sg.Text('text20', size=(20, 1), k='out-text20')],
          [sg.Text('text21', size=(20, 1), k='out-text21'),
           sg.Text('text22', size=(20, 1), k='out-text22'),
           sg.Text('text23', size=(20, 1), k='out-text23'),
           sg.Text('text24', size=(20, 1), k='out-text24'),
           sg.Text('text25', size=(20, 1), k='out-text25')],
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
    window['out-team1-list'].update(teamRed)
    window['out-team2-list'].update(teamBlue)
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
                    background_color="#63768d")
            else:
                if teamId == 0:
                    window[currentTextOutputName].update(
                        background_color="#191716")
                elif teamId == 1:
                    window[currentTextOutputName].update(
                        background_color="#9A031E")
                elif teamId == 2:
                    window[currentTextOutputName].update(
                        background_color="#101D42")
                elif teamId == 3:
                    window[currentTextOutputName].update(
                        background_color="#3E363F")
            cardNr += 1
    toggleView = not toggleView


# init gui
window = sg.Window('codenames', layout, finalize=True)

window['out-team1'].update(
    background_color="#9A031E")
window['out-team2'].update(
    background_color="#101D42")

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
