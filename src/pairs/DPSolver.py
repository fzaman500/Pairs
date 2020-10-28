from src.pairs.util import intMapper
import numpy as np


class DPSolver:
    def __init__(self, game):
        deck_states = np.prod([card + 1 for card in game.deck.original_deck.values()])
        player_states = np.prod([value + 1 for value in game.players[0].hand_capacity.values()]) * game.target_score
        dimensions = [deck_states] + [player_states] * game.num_players
        self.action_table = np.zeros(tuple(dimensions), dtype=bool)
        self.fifty_percent_action_table = np.zeros(tuple(dimensions), dtype=bool)
        self.expected_point_action_table = np.zeros(tuple(dimensions), dtype=bool)
        dimensions.append(game.num_players)
        self.dp_table = np.empty(tuple(dimensions))
        self.dp_table[:] = np.nan
        self.game = game

    # Solve will return a 1-dimensional numpy array
    # representing the probabilities of winning for each of the players
    def solve(self, game_state):
        # 1. Check if game state is an ending game state. If it is, return that probability array
        # 2. Check if game state already exists in the dp_table, if it doesn't, solve for the
        #       fold probabilities and hit probabilities and update action table and dp table
        # 3. Return answer
        ending_probabilities = game_state.ending_probabilities()
        if ending_probabilities is not None:
            return ending_probabilities
        table_index = game_state.game_to_tuple()
        if np.isnan(self.dp_table[table_index][0]):
            fold_state = game_state.next_fold_state()
            fold_probabilities = np.roll(self.solve(fold_state), 1) if fold_state is not None else None
            draw_probabilities = np.roll(
                sum(prob * self.solve(draw_state) for draw_state, prob in game_state.next_draw_states()), 1)
            self.fifty_percent(game_state, table_index)
            self.expected_point(game_state, table_index)
            if fold_probabilities is None or draw_probabilities[0] > fold_probabilities[0]:
                self.action_table[table_index] = True
                self.dp_table[table_index] = draw_probabilities
            else:
                self.action_table[table_index] = False
                self.dp_table[table_index] = fold_probabilities
        return self.dp_table[table_index]

    def fifty_percent(self, game_state, table_index):
        hit_fifty_probability = 0
        for card_type in game_state.players[0].hand_state:
            if game_state.players[0].hand_state[card_type] > 0:
                hit_fifty_probability += game_state.deck.curr_deck[card_type] / sum(game_state.deck.curr_deck.values())
        if hit_fifty_probability > .5:
            self.fifty_percent_action_table[table_index] = True
        else:
            self.fifty_percent_action_table[table_index] = False

    def expected_point(self, game_state, table_index):
        hit_expected_point = 0
        fold_expected_point = min((min(
            (card_type for card_type, freq in player.hand_state.items() if freq > 0), default=float('inf'))
            for player in game_state.players), default=float('inf'))
        for card_type in game_state.players[0].hand_state:
            if game_state.players[0].hand_state[card_type] > 0:
                hit_expected_point += card_type * \
                                         (game_state.deck.curr_deck[card_type] /
                                          sum(game_state.deck.curr_deck.values()))
        if hit_expected_point < fold_expected_point:
            self.expected_point_action_table[table_index] = True
        else:
            self.expected_point_action_table[table_index] = False

    def get_dp_table(self):
        return self.dp_table

    def get_action_table(self):
        return self.action_table

    def get_fifty_percent_table(self):
        return self.fifty_percent_action_table

    def get_expected_point_action_table(self):
        return self.expected_point_action_table
