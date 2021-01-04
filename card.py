class Card:

    def __init__(self, name, team, active):
        self.name = name
        self.team = team  # "teamid :: black=0, team1=1, team2=2, grey=3"
        self.active = active  # "known=False, unknown=True"
        self.toggle = True

    def __str__(self):
        return "[" + '{:^15}'.format(self.name) + '{:3}'.format(str(self.team)) + '{:6}'.format(str(self.active))+"]"
