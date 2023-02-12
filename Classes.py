# Classes used

class Team:
    def __init__(self, team_name):
        self.name = team_name
        self.train_games = [[] for _ in range(2013, 2023)]
        self.val_games = []
        self.test_games = []
    
