from src.pairs.Player import Player
from src.pairs.util import intMapper
from collections import deque, Iterable
import numpy as np
import copy


class GameState:
    def __init__(self, deck, target_score, players):
        self.deck = deck
        self.target_score = target_score
        if isinstance(players, int):
            self.num_players = players
            self.players = deque(Player(deck.original_deck) for _ in range(self.num_players))
        elif isinstance(players, Iterable):
            self.players = deque(players)
            self.num_players = len(self.players)

    def deepcopy(self):
        c = GameState(copy.deepcopy(self.deck), self.target_score,
                      deque(copy.deepcopy(player) for player in self.players))
        return c

    def next_draw_states(self):
        states = []
        for card_type in self.deck.curr_deck:
            total_cards = sum(self.deck.curr_deck.values())
            if self.deck.curr_deck[card_type] > 0:
                new_state = copy.deepcopy(self)
                new_state.deck.draw_specific_card(card_type)
                new_state.players[0].add_card(card_type)
                if new_state.players[0].hand_state[card_type] > new_state.players[0].hand_capacity[card_type]:
                    new_state.player_scored(card_type)
                new_state.players.rotate(-1)
                states.append((new_state, self.deck.curr_deck[card_type] / total_cards))
        return states

    def next_fold_state(self):
        next_fold_state = copy.deepcopy(self)
        minimum = min((min(
            (card_type for card_type, freq in player.hand_state.items() if freq > 0), default=float('inf'))
            for player in next_fold_state.players), default=float('inf'))
        if minimum == float('inf'):
            return None
        next_fold_state.player_scored(minimum)
        next_fold_state.players.rotate(-1)
        return next_fold_state

    def player_scored(self, points):
        self.players[0].points += points
        for player in self.players:
            self.deck.add_dict_discards(player.hand_state)
            player.reset()

    # ending_state returns None if the game state is not an ending state
    # otherwise, it returns a numpy array representing the probabilities of winning
    # for each of the players in the game
    def ending_probabilities(self):
        if any(player.points >= self.target_score for player in self.players):
            return np.array([float(player.points < self.target_score) for player in self.players])
        return None

    def game_to_tuple(self):
        curr_deck_state = [intMapper(self.deck.original_deck.values(), self.deck.curr_deck.values())]
        curr_player_states = [intMapper(list(player.hand_capacity.values()) + [self.target_score],
                                        list(player.hand_state.values()) + [player.points])
                              for player in self.players]
        curr_state = tuple(curr_deck_state + curr_player_states)
        return curr_state

    @classmethod
    def tuple_to_game(cls):
        pass
