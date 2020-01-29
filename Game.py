import itertools
from random import shuffle

import Card
import Pyramid

card_suits = ["Spades", "Hearts", "Clubs", "Diamonds"]
card_faces = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]


class Game:
    def __init__(self, discard_rules=None):
        if discard_rules is None:
            discard_rules = {"same_face": False, "single_k": True}
        self.cards = [Card.Card(suit, face) for face in card_faces for suit in card_suits]
        self.shuffle()
        self.pyramid_cards = self.cards[:32]
        self.cards_in_hand = self.cards[-20:]
        self.discarded_cards = []
        self.pyramid = Pyramid.Pyramid(self.pyramid_cards)
        self.discard_rules = discard_rules  # a dict in the form { String : bool, }

    def shuffle(self):
        """
        Shuffles the current deck
        :return: None
        """
        shuffle(self.cards)

    def discard(self, cards):
        """
        Discard card in cards from the pyramid
        :param cards:
        :return: None
        """
        for card in cards:
            try:
                card_index = self.pyramid.get_index(card, self.discarded_cards)
                self.discarded_cards.append(card)
                self.pyramid.remove_card(card_index[0], card_index[1])
            except Exception:
                self.discarded_cards.append(card)
                self.cards_in_hand = self.cards_in_hand[1:]

    def match_and_discard(self, cards):
        """
        Self-check within cards and discard cards if necessary
        :param cards: a list of unblocked Cards (length > 2)
        :return: the number of discarded within this function
        """
        if len(cards) < 2:
            if cards[0].check_discardable(discard_rules=self.discard_rules):
                self.discard([cards[0], ])
                return 1
            return 0
        else:
            discard_count = 0
            for c in cards:
                if c.check_discardable(discard_rules=self.discard_rules):
                    self.discard([c, ])
                    discard_count += 1
            for cs in itertools.combinations(cards, 2):
                if (not cs[0] in self.discarded_cards) and (not cs[1] in self.discarded_cards) and cs[0].check_discardable(
                        cs[1], discard_rules=self.discard_rules):
                    self.discard(cs)
                    discard_count += 2
            return discard_count

    def next(self):
        """
        Perform one action and discard cards if necessary
        :return: None
        """
        self.match_and_discard(self.pyramid.get_all_unblocked())  # some card discarded

        for card in self.pyramid.get_all_unblocked():
            if self.match_and_discard([self.cards_in_hand[0], card]):
                break

        self.cards_in_hand.append(self.cards_in_hand[0])
        self.cards_in_hand.remove(self.cards_in_hand[0])
        return self

    def play(self):
        """
        Play until game_over or run out of moves
        :return: "Success!" if game_over or the Game state if failed
        """
        self.next()
        plays = 0
        while not self.game_over() and plays < 100:
            self.next()
            plays += 1
        if self.game_over():
            return "Success!"
        return self

    def __str__(self):
        """
        Print the game state
        :return: The game state in three parts:
                 The Pyramid
                 Cards in Hand:
                 Cards Discarded:
        """
        return_string = self.pyramid.__str__()
        return_string += "Cards in Hand: " + " ".join(map(lambda c: c.__str__(shorten=True), self.cards_in_hand)) + "\n"
        return_string += "Cards Discarded: " + " ".join(
            map(lambda c: c.__str__(shorten=True), self.discarded_cards)) + "\n"
        return return_string

    def game_over(self):
        """
        Check if the game is over by looking at the first card
        :return: True if first card is None
        """
        return self.pyramid.check_cleared()
