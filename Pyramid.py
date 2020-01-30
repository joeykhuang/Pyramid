class Pyramid:
    def __init__(self, pyramid_cards):
        self.cards = pyramid_cards
        self.pyramid = {}
        self.place_pyramid()

    def place_pyramid(self):
        """
        Place down the pyramid cards into a pyramid -> dictionary
        {1: {1: card},
         2: {1: card, 2: card},
         ...
         7: {1: card, ... 7: card}}
        """
        if len(self.cards) != 32:
            raise Exception
        else:
            for i in range(1, 8):
                self.pyramid[i] = dict()
                for j in range(1, i + 1):
                    self.pyramid[i][j] = self.cards[0]
                    self.cards = self.cards[1:]

    def get_index(self, card, discarded_cards):
        """
        Retrieve the index of the card in the pyramid in the form of (row, column) tuple;
        raise Exception if card is in hand
        :param discarded_cards:
        :param card: a Card
        :return: an index tuple if card is in pyramid
        """
        if card in discarded_cards:
            raise ValueError("Card Already Discarded")
        for row in self.pyramid.keys():
            for col in self.pyramid[row].keys():
                if str(self.pyramid[row][col]) == str(card):
                    return (row, col)
        raise Exception("Card Not In Pyramid")  # card in hand

    def remove_card(self, row, column):
        """
        Remove a card from the pyramid
        :param row: the row of the card
        :param column: the column of the card
        :return: None
        """
        self.pyramid[row][column] = None

    def check_blocked(self, row, column):
        """
        Check if a card on a specific row and column is blocked
        :param row: a number between 1 and 7
        :param column: a number between 1 and 7
        :return: True if blocked; False if not blocked
        """
        if column > row:
            raise ValueError
        elif row == 7:
            return False
        elif self.pyramid[row + 1][column] is None and self.pyramid[row + 1][column + 1] is None:
            return False
        else:
            return True

    def get_all_unblocked(self):
        """
        Retrieve all the current unblocked cards
        :return: a list of unblocked Cards
        """
        unblocked_cards = []
        for i in self.pyramid.keys():
            for j in self.pyramid[i].keys():
                if self.pyramid[i][j] and not self.check_blocked(i, j):
                    unblocked_cards.append(self.pyramid[i][j])
        return unblocked_cards

    def check_cleared(self):
        """
        Check if the pyramid is cleared
        :return: True if the first card is None
        """
        return self.pyramid[1][1] is None

    def __str__(self):
        """
        Turn the current state of the game into a string
        :return: A string that represents the current state of the game
        """
        return_string = ""
        for i in range(1, 8):
            return_string += (7 - i) * " " + " ".join(
                map(lambda c: c.__str__(shorten=True) if c else "__", list(self.pyramid[i].values()))) + (
                                     7 - i) * " " + "\n"
        return return_string
