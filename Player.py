from Deck import Deck

class Player:
    def __init__(self, deck=None, points=0, hand_state=None):
        self.deck = deck
        self.points = points
        self.hand_state = hand_state
        if self.hand_state is None and deck is not None:
            self.hand_state = [0] * deck.num_cards

    def update_points(self, n):
        self.points += n

    def add_card(self, new):
        self.hand_state[new-1] = 1

    def reset(self):
        self.hand_state = [0] * self.deck.num_cards


