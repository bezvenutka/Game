opponents = {
    'rock': 'paper',
    'scissors': 'rock',
    'paper': 'scissors',
    'bilateral_sharp_samurai_sword': None
}


class RPSGame:
    choices = ['rock', 'paper', 'scissors', 'bilateral_sharp_samurai_sword']

    def __init__(self, players_count=2, round_count=1):
        self.players_count = players_count
        self.players = []
        self.scores = {}
        self.current_round = 1
        self.moves = {}
        self.rounds = []
        self.is_started = False
        self.current_round_moves = {}
        self.round_winners = []
        self.round_count = round_count

    def add_player(self, username):
        self.players.append(username)
        if len(self.players) == self.players_count:
            self.is_started = True

    def make_move(self, username, move):
        self.moves[username] = move
        if len(self.moves) == self.players_count:
            self.find_winner()

    def find_winner(self):
        for k, v in self.moves.items():
            if opponents[v] not in self.moves.values():
                self.round_winners.append(k)
                self.scores[k] = self.scores.get(k, 0) + self.current_round
