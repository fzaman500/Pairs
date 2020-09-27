from Player import Player
from collections import deque

class Game_State:
    def __init__(self, deck, target_score, num_players=None, players=None):
        self.deck = deck
        self.target_score = target_score
        if num_players is None and players is None:
            num_players = 0
            players = deque()
        elif num_players is None and players is not None:
            num_players = len(players)
        elif num_players is not None and players is None:
            players = deque(Player(deck) for _ in range(num_players))
        elif num_players is not None and players is not None:
            num_players = len(players)
        self.num_players = num_players
        self.players = players


