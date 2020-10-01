from src.pairs.TriangularDeck import TriangularDeck
from src.pairs.util import intMapper
from src.pairs.GameState import GameState
from src.pairs.DPSolver import DPSolver
from src.pairs.Deck import Deck


def main():
    deck = TriangularDeck(3)
    game = GameState(deck, 5, 2)
    solver = DPSolver(game)
    solver.solve(game)
    #print(solver.get_dp_table())
    #print("action table: ")
    #print(solver.get_action_table())
    #print("fifty_percent table: ")
    #print(solver.get_fifty_percent_table())
    #print("expected point table: ")
    #print(solver.get_expected_point_action_table())


if __name__ == "__main__":
    main()
