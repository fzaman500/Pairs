from numpy.random import choice
import random

class Deck:
    # How are storing the cards structure? Is it a list? Is it a dict?
    # Array
    # Dictionary: Key (Card type) -> Value (Number of how many cards there are)
    # How do you randomly generate a card?
    # Use numpy.choice and pass in a probability distribution

    def __init__(self, num_cards, deck, discards, total_cards):
        self.num_cards = num_cards
        self.deck = deck
        self.discards = discards
        self.total_cards = total_cards
        deck = {}
        discards = {}
        for i in range(num_cards):
            deck[i+1] = i+1
            discards[i+1] = 0
        total_cards = sum(deck.values())

    def draw_card(self, player):
        if sum(self.deck.values()) > 5:
            probabilities = [float(i)/self.total_cards for i in range(1, self.num_cards+1)]
            draw = choice(list(self.deck.keys()), probabilities, 1)
            player.add_card(draw)
            self.discards[draw-1] = 1
        else:
            self.half_reset()
        pass

    def full_reset(self):
        self.deck = {}
        self.discards = {}
        for i in range(self.num_cards):
            self.deck[i + 1] = i + 1
            self.discards[i + 1] = 0
        pass

    def half_reset(self):
        for i in range(self.num_cards):
            if self.deck[i] == 0 and self.discards[i] == 1:
                self.deck[i] = 1
                self.discards[i] = 0
        pass

   # def triangular(self, m):
   #     self.num_cards = [i for i in range(1, m+1) for j in range(i)]

