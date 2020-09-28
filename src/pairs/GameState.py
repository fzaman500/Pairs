from src.pairs.Player import Player
from src.pairs.util import intMapper
from collections import deque, Iterable
import numpy as np

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

    def deepcopy(self):
        c = GameState(self.deck.deepcopy(), self.target_score,
                      deque(player.deepcopy() for player in self.players))
        return c

    def next_draw_states(self):
        states = []
        for card_type in self.deck.curr_deck:
            if self.deck.curr_deck[card_type] > 0:
                new_state = self.deepcopy()
                new_state.deck.draw_specific_card(card_type)
                new_state.players[0].add_card(card_type)
                new_state.players.rotate(-1)
                states.append(new_state)
        return states

    def next_fold_state(self):
        curr_state = self.deepcopy()
        minimum = min(
            min(card_type for card_type, freq in player.hand_state.items() if freq > 0)
            for player in curr_state.players)
        curr_state.players[0].points += minimum
        for player in curr_state.players:
            curr_state.deck.add_dict_discards(player.hand_state)
            player.reset()
        curr_state.players.rotate(-1)
        return curr_state

    def ending_state(self):
        if any(player.points >= self.target_score for player in self.players):
            return np.array([float(player.points < self.target_score) for player in self.players])
        return None

    def game_to_tuple(self):
        curr_deck_state = list(intMapper(self.deck.values(), self.deck.curr_deck.values()))
        curr_player_states = [intMapper(player.hand_capacity.values(), player.hand_state.values())
                              for player in self.players]
        curr_state = tuple(curr_deck_state.extend(curr_player_states))
        return curr_state



