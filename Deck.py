from random import shuffle
import itertools

card_suits = ["Spades", "Hearts", "Clubs", "Diamonds"]
card_faces = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]
number_faces = ["2", "3", "4", "5", "6", "7", "8", "9", "10"]
letter_faces = ["A", "J", "Q", "K"]



class Card:
    """
    Private class Card; only be constructed in class Deck
    """

    def __init__(self, suit, face):
        self.suit = suit
        self.face = face
        self.number = self.turn_into_number()

    def turn_into_number(self):
        if self.face in number_faces:
            return int(self.face)
        elif self.face == "J":
            return 11
        elif self.face == "Q":
            return 12
        elif self.face == "K":
            return 13
        elif self.face == "A":
            return 1
        else:
            raise Exception

    def add(self, another_card):
        """
        Add the number value of this card with another card
        :param another_card: a Card
        :return: an int
        """
        return self.number + another_card.number

    def check_same_face(self, another_card):
        """
        Check whether two cards have the same face
        :param another_card: a Card
        :return: True if two cards have same face; False otherwise
        """
        return self.face == another_card.face

    def check_discardable(self, another_card=None, discard_rules={"check_face":False, "discard_k":True}):
        """
        Check whether a card or two cards are discardable
        :param another_card: a Card; None if only check one card
        :param check_face: True if discard cards if they have the same face; False otherwise
        :param discard_k: True if discard card if its face is "K"; False otherwise
        """
        if another_card:
            if self.add(another_card) == 13:
                return True
            elif self.check_same_face(another_card):
                return discard_rules["check_face"]
            return False
        elif discard_rules["discard_k"]:
            return self.face == "K"
        return False

    def __str__(self, shorten=False):
        """
        Turn the card into its string form
        :param shorten: True then in shortened form (AS/9H);
                        False then not shortened (A of Spades/9 of Hearts)
        :return: a string that represent the card
        """
        if shorten:
            if self.face == "10":
                return "X" + self.suit[0]
            else:
                return self.face[0] + self.suit[0]
        else:
            return self.face + " of " + self.suit



class Game:
    def __init__(self, discard_rules= {"check_face":False, "discard_k":True}):
        self.cards = [Card(suit, face) for face in card_faces for suit in card_suits]
        self.shuffle()
        self.pyramid_cards = self.cards[:32]
        self.cards_in_hand = self.cards[-20:]
        self.discarded_cards = []
        self.pyramid = self.place_pyramid(self.pyramid_cards)
        self.discard_rules = discard_rules # a dict in the form { String : bool, }
        print(self.__str__())

    def shuffle(self):
        """
        Shuffles the current deck
        :return: None
        """
        shuffle(self.cards)

    def get_index(self, card):
        """
        Retrieve the index of the card in the pyramid in the form of (row, column) tuple;
        raise Exception if card is in hand
        :param card: a Card
        :return: an index tuple if card is in pyramid
        """
        if card in self.discarded_cards:
            raise ValueError("Card Already Discarded")
        for row in self.pyramid.keys():
            for col in self.pyramid[row].keys():
                if str(self.pyramid[row][col]) == str(card):
                    return (row, col)
        raise Exception("Card Not In Pyramid") # card in hand

    def discard(self, cards):
        """
        Discard card in cards from the pyramid
        :param *cards: a Card list
        :return: None
        """
        for card in cards:
            try:
                card_index = self.get_index(card)
                self.discarded_cards.append(card)
                self.pyramid[card_index[0]][card_index[1]] = None
            except Exception: 
                self.discarded_cards.append(card)
                self.cards_in_hand = self.cards_in_hand[1:]

    def match_and_discard(self, cards):
        """
        Self-check within cards and dicard cards if necessary
        :param cards: a list of unblocked Cards (length > 2)
        :return: the number of discarded within this function
        """
        if len(cards) < 2:
            raise ValueError("Need More Than 2 Cards, Missing %s." % (2-len(cards)))
        discard_count = 0
        for c in cards:
            if c.check_discardable(discard_rules=self.discard_rules):
                self.discard([c,])
        for cs in itertools.combinations(cards,2):
            if (not cs[0] in self.discarded_cards) and (not cs[1] in self.discarded_cards) and cs[0].check_discardable(cs[1], discard_rules=self.discard_rules):
                self.discard(cs)
                discard_count += 2
        return discard_count

    def next(self):
        """
        Perform one action and discard cards if necessary
        :return: None
        """
        while self.match_and_discard(self.get_all_unblocked(self.pyramid)): # some card discarded
            continue

        for card in self.get_all_unblocked(self.pyramid):
            if self.match_and_discard([self.cards_in_hand[0], card]):
                break

        self.cards_in_hand.append(self.cards_in_hand[0])
        self.cards_in_hand.remove(self.cards_in_hand[0])
        print(self.__str__())
        return None


    @staticmethod
    def place_pyramid(cards):
        """
        Place down the pyramid cards into a pyramid -> dictionary
        {1: {1: card},
         2: {1: card, 2: card},
         ...
         7: {1: card, ... 7: card}}
        :param cards: a list of 32 Cards
        :return: a pyramid dictionary
        """
        pyramid = {}
        if len(cards) != 32:
            raise Exception
        else:
            for i in range(1, 8):
                pyramid[i] = dict()
                for j in range(1, i + 1):
                    pyramid[i][j] = cards[0]
                    cards = cards[1:]
        return pyramid

    @staticmethod
    def check_blocked(pyramid, row, column):
        """
        Check if a card on a specific row and column is blocked
        :param pyramid: a pyramid dictionary
        :param row: a number between 1 and 7
        :param column: a number between 1 and 7
        :return: True if blocked; False if not blocked
        """
        if column > row:
            raise ValueError
        elif row == 7:
            return False
        elif pyramid[row + 1][column] == None and pyramid[row + 1][column + 1] == None:
            return False
        else:
            return True

    @staticmethod
    def get_all_unblocked(pyramid):
        """
        Retrieve all the current unblocked cards
        :param pyramid: a pyramid dictionary
        :return: a list of unblocked Cards
        """
        unblocked_cards = []
        for i in pyramid.keys():
            for j in pyramid[i].keys():
                if pyramid[i][j] and not Game.check_blocked(pyramid, i, j):
                    unblocked_cards.append(pyramid[i][j])
        return unblocked_cards

    def __str__(self):
        """
        Turn the current state of the game into a string
        :return: A string that represents the current state of the game
        """
        return_string = ""
        for i in range(1, 8):
            return_string += (7 - i) * " " + " ".join(map(lambda c: c.__str__(shorten=True) if c else "  ", list(self.pyramid[i].values()))) + (7 - i) * " " + "\n"
        return_string += "Cards in Hand: " + " ".join(map(lambda c: c.__str__(shorten=True), self.cards_in_hand)) + "\n"
        return_string += "Cards Discarded: " + " ".join(map(lambda c: c.__str__(shorten=True), self.discarded_cards)) + "\n\n"
        return return_string