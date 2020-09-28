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
        c = GameState(self.deck.deepcopy(), self.target_score, self.players.deepcopy())
        return c

    def draw_next(self, game):
        curr_state = game.deepcopy()
        new_state = curr_state.deepcopy()
        states = []
        possible = []
        for card in curr_state.curr_deck:
            if curr_state.curr_deck[card] != 0:
                possible.append(card)
        for i in range(len(possible)):
            new_state.players[0].add_card(curr_state.deck.draw_specific_card(i))
            states.append(new_state)
            new_state = curr_state.deepcopy()
        return states

    def fold_next(self, game):
        curr_state = game.deepcopy()
        minimum = min([player.points for player in game.players])
        game.players[0].points += minimum
        for player in game.players:
            game.deck.add_dict_discards(player.hand_state)
            player.reset()
        curr_state.players.rotate(1)
        return curr_state

    def ending_state(self):
        for i in range(len(self.players)):
            if self.players[i].points >= self.target_score:
                winners = np.ones(self.num_players)
                winners[i] = 0
                return winners
        return None

    def game_to_tuple(self):
        curr_deck_state = list(intMapper(self.deck.values(), self.deck.curr_deck.values()))
        curr_player_states = [intMapper(player.hand_capacity.values(), player.hand_state.values())
                              for player in self.players]
        curr_state = tuple(curr_deck_state.extend(curr_player_states))
        return curr_state



