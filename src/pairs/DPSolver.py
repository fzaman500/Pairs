from src.pairs.util import intMapper
import numpy as np
class DPSolver:
    def __init__(self, game):
        deck_states = intMapper(game.deck.values(), game.deck.values())
        player_states = intMapper(game.deck.values(), [1 for _ in range(len(game.deck.values()))])
        dim = [player_states] * game.numPlayers
        [deck_states].extend(dim)
        dim.extend([game.numPlayers])
        self.dp_table = np.zeros((tuple(dim)))
        self.game = game

    def game_to_tuple(self):
        curr_deck_state = intMapper(self.game.deck.values(), self.game.deck.curr_deck.values())
        curr_player_states = [intMapper(self.game.deck.values(), player.hand_state.values())
                              for player in self.game.players]
        curr_state = tuple(curr_deck_state.extend(curr_player_states))
        return curr_state


