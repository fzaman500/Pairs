from src.pairs.util import intMapper
import numpy as np


class DPSolver:
    def __init__(self, game):
        deck_states = np.prod([card + 1 for card in game.deck.original_deck.values()])
        player_states = np.prod([value + 1 for value in game.players[0].hand_capacity.values()]) * game.target_score
        dimensions = [deck_states] + [player_states] * game.num_players
        self.action_table = np.zeros(tuple(dimensions), dtype=bool)
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
        print(table_index)
        print(self.dp_table.shape)
        if np.isnan(self.dp_table[table_index][0]):
            print('recursing?')
            fold_state = game_state.next_fold_state()
            fold_probabilities = np.roll(self.solve(fold_state), 1) if fold_state is not None else None
            draw_probabilities = np.roll(
                sum(prob * self.solve(draw_state) for draw_state, prob in game_state.next_draw_states()), 1)
            if fold_probabilities is None or draw_probabilities[0] > fold_probabilities[0]:
                self.action_table[table_index] = True
                self.dp_table[table_index] = draw_probabilities
            else:
                self.action_table[table_index] = False
                self.dp_table[table_index] = fold_probabilities
        return self.dp_table[table_index]

    def get_dp_table(self):
        return self.dp_table

    def get_action_table(self):
        return self.action_table
