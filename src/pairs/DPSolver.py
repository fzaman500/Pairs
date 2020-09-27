from src.pairs.util import intMapper
import numpy as np
class DPSolver:
    def __init__(self, game):
        deck_states = np.prod([card + 1 for card in game.deck.values]) + 1
        player_states = sum([value + 1 for value in game.players[0].hand_capacity.values()])
        dim = [player_states] * game.numPlayers
        [deck_states].extend(dim)
        dim.append(game.numPlayers)
        self.dp_table = np.zeros(tuple(dim))
        self.game = game



