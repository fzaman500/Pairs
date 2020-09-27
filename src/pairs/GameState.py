from src.pairs.Player import Player
from src.pairs.util import intMapper
from collections import deque, Iterable

class GameState:
    def __init__(self, deck, target_score, players):
        self.deck = deck
        self.target_score = target_score
        if isinstance(players, int):
            self.num_players = players
            self.players = deque(Player(deck) for _ in range(self.num_players))
        elif isinstance(players, Iterable):
            self.players = deque(players)
            self.num_players = len(self.players)

    def copy(self):
        c = GameState(self.deck, self.target_score, self.players)
        return c

    def draw_next(self):
        pass

    def fold_next(self):
        pass

    def game_to_tuple(self):
        curr_deck_state = list(intMapper(self.deck.values(), self.deck.curr_deck.values()))
        curr_player_states = [intMapper(self.deck.values(), player.hand_state.values())
                              for player in self.players]
        curr_state = tuple(curr_deck_state.extend(curr_player_states))
        return curr_state



