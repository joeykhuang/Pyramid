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
        """
        Turn the card into a number (11 for J, 12 for Q...)
        :return: A number that represents the card face
        """
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

    def check_discardable(self, another_card=None, discard_rules={"same_face": False, "same_number": False, "single_k": True}):
        """
        Check whether a card or two cards are discardable
        :param another_card: a Card; None if only check one card
        :param discard_rules: a dictionary with the following:
               same_face: whether discard cards with same faces
               single_k: whether to discard a single K
        """
        if another_card:
            if self.add(another_card) == 13:
                return True
            elif discard_rules["same_face"]:
                return self.face == another_card.face
            elif discard_rules["same_number"]:
                return self.number == another_card.number
            return False
        elif discard_rules["single_k"]:
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
