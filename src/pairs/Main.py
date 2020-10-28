from src.pairs.TriangularDeck import TriangularDeck
from src.pairs.util import intMapper
from src.pairs.GameState import GameState
from src.pairs.DPSolver import DPSolver
from src.pairs.Deck import Deck
import numpy as np


def main():
    deck = TriangularDeck(4)
    game = GameState(deck, 7, 3)
    solver = DPSolver(game)
    solver.solve(game)
    diff_dp_fifty = solver.get_action_table() == solver.get_fifty_percent_table()
    print(np.count_nonzero(diff_dp_fifty == 0))
    diff_dp_exp = solver.get_action_table() == solver.get_expected_point_action_table()
    print(np.count_nonzero(diff_dp_exp == 0))


if __name__ == "__main__":
    main()
