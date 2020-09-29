import copy

class Player:
    def __init__(self, original_deck, points=0, hand_state=None, hand_capacity=None):
        self.original_deck = original_deck
        self.points = points
        if hand_state is None:
            hand_state = self.hand_state = {card_type: 0 for card_type in original_deck.original_deck}
        self.hand_state = hand_state
        if hand_capacity is None:
            hand_capacity = {card_type: 1 for card_type in original_deck.original_deck}
        self.hand_capacity = hand_capacity

    def increase_points(self, n):
        self.points += n

    def add_card(self, card):
        self.hand_state[card] += 1

    def reset(self):
        for card_type in self.hand_state:
            self.hand_state[card_type] = 0

    def deepcopy(self):
        c = Player(copy.deepcopy(self.original_deck), self.points, copy.deepcopy(self.hand_state),
                   copy.deepcopy(self.hand_capacity))
        return c


