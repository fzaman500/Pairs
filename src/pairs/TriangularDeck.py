from src.pairs.Deck import Deck


class TriangularDeck(Deck):
    def __init__(self, num_distinct):
        original_deck = {i: i for i in range(1, num_distinct+1)}
        super().__init__(original_deck)
