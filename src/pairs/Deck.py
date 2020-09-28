from numpy.random import choice
import random

class Deck:
    # How storing the cards structure? Is it a list? Is it a dict?
    # Dictionary: Key (Card type) -> Value (Number of how many cards there are)
    # How do you randomly generate a card?
    # Use numpy.choice and pass in a probability distribution

    def __init__(self, original_deck, curr_deck=None, discards=None, shuffling_limit=0):
        self.original_deck = original_deck
        if curr_deck is None:
            curr_deck = original_deck.copy()
        self.curr_deck = curr_deck
        if discards is None:
            discards = {card_type: 0 for card_type in original_deck}
        self.discards = discards
        self.num_distinct_cards = len(self.original_deck)
        self.num_total_cards = sum(self.original_deck.values())
        self.shuffling_limit = shuffling_limit

    def draw_specific_card(self, draw_card):
        if self.curr_deck[draw_card] <= 0:
            raise ValueError("Draw card {} is not present in the current deck {}".format(draw_card, self.curr_deck))
        self.curr_deck[draw_card] -= 1
        if sum(self.curr_deck.values()) <= self.shuffling_limit:
            self.shuffle_discards()

    def draw_random_card(self):
        probabilities = [float(card_frequency) / sum(self.curr_deck.values())
                         for card_type, card_frequency in self.curr_deck.items()]
        draw = choice(list(self.curr_deck.keys()), 1, False, probabilities)
        self.curr_deck.draw_specific_card(draw)

    def shuffle_discards(self):
        for card_type in self.curr_deck:
            self.curr_deck[card_type] += self.discards[card_type]
        for card_type in self.discards:
            self.discards[card_type] = 0

    def add_single_discard(self, card):
        self.discards[card] += 1

    def add_dict_discards(self, cards):
        for card_type, freq in cards.items():
            self.discards[card_type] += freq

    def deepcopy(self):
        c = Deck(self.original_deck.deepcopy(), self.curr_deck.deepcopy(), self.discards.deepcopy(), self.shuffling_limit)
        return c


   # def triangular(self, m):
   #     self.num_cards = [i for i in range(1, m+1) for j in range(i)]

