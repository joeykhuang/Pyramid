from random import shuffle

card_suits = ["Spades", "Hearts", "Clubs", "Diamonds"]
card_faces = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]
number_faces = ["2", "3", "4", "5", "6", "7", "8", "9", "10"]
letter_faces = ["A", "J", "Q", "K"]


class Game:
    def __init__(self):
        self.cards = [face + " of " + suit for face in card_faces for suit in card_suits]
        self.shuffle()
        self.pyramid_cards = self.cards[:32]
        self.cards_in_hand = self.cards[-20:]
        self.discarded_cards = []
        self.pyramid = self.place_pyramid(self.pyramid_cards)

    def shuffle(self):
        """
        Shuffles the current deck
        :return: None
        """
        shuffle(self.cards)

    def next(self):
        # TODO: Add self-check within unblocked cards
        """
        Perform one action and discard cards if necessary
        :return: None
        """
        for i in range(1, 8):
            for j in range(1, i + 1):
                if not self.check_blocked(self.pyramid, i, j):
                    if check_add_to_13(self.cards_in_hand[0], self.pyramid[i][j]):
                        self.discarded_cards.append(self.cards_in_hand[0])
                        self.discarded_cards.append(self.pyramid[i][j])
                        self.cards_in_hand = self.cards_in_hand[1:]
                        self.pyramid[i][j] = "  "
                        print(self.__str__())
                        return None

    @staticmethod
    def shorten(card_name):
        """
        Shorten the name of a card
        :param card_name: A of Spades/9 of Hearts
        :return: AS/9H
        """
        return card_name.split(" ")[0] + card_name.split(" ")[2][0]

    @staticmethod
    def place_pyramid(cards):
        """
        Place down the pyramid cards into a pyramid -> dictionary
        {1: {1: card},
         2: {1: card, 2: card},
         ...
         7: {1: card, ... 7: card}}
        :param cards: a list of 32 cards
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
            raise Exception
        elif row == 7:
            return False
        elif pyramid[row + 1][column] == "  " and pyramid[row + 1][column + 1] == "  ":
            return False
        else:
            return True

    def __str__(self):
        """
        Turn the current state of the game into a string
        :return: A string that represents the current state of the game
        """
        return_string = ""
        for i in range(1, 8):
            return_string += (7 - i) * " " + " ".join(map(self.shorten, list(filter(lambda x: x != "  ", self.pyramid[i].values())))) + (7 - i) * " " + "\n"
        return_string += "Cards in Hand: " + " ".join(map(self.shorten, self.cards_in_hand)) + "\n"
        return_string += "Cards Discarded " + " ".join(map(self.shorten, self.discarded_cards))
        return return_string


def check_add_to_13(first_card, second_card):
    first_card = turn_into_number(first_card)
    second_card = turn_into_number(second_card)
    return first_card + second_card == 13


def turn_into_number(card):
    card = card.split(" ")[0]
    if card in number_faces:
        return int(card)
    elif card == "J":
        return 11
    elif card == "Q":
        return 12
    elif card == "K":
        return 13
    elif card == "A":
        return 1
    else:
        raise Exception

