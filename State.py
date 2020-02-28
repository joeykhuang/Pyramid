import itertools

card_suits = ["Spades", "Hearts", "Clubs", "Diamonds"]
card_faces = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]


class State:
    def __init__(self, stack, stock, pyramid, discard, rules=None):
        if rules is None:
            rules = {"same_face": False, "same_number": False, "single_k": True}

        self.cards = stock + stack
        self.stack = stack
        self.stock = stock
        self.pyramid = pyramid
        self.discard = discard
        self.rules = rules
        self.hashmap = self.get_hashmap()
        self.actions = self.get_actions()

    def get_hashmap(self):
        """
        Return a dictionary that maps every cards in self.cards to its current position
        :return: a tuple in the form of
                    ("Stack", rownum, colnum) or
                    ("Stock", index)
        """
        hashmap = {}
        for i, c in enumerate(self.stock):
            hashmap[c] = ("Stock", i)
        for c in self.stack:
            index = self.pyramid.get_index(c)
            hashmap[c] = ("Stack", index[0], index[1])
        return hashmap

    def duplicate(self):
        """
        Return a new State that is at the same stage of the current state
        """
        return State(self.stack[:], self.stock[:], self.pyramid.duplicate(),
                     self.discard[:], self.rules)

    def get_actions(self):  # TODO: buggy
        """
        Return all possible actions at the current stage
        :return: a list containing tuple in the form of
                    (card1, card2) or
                    (card)
                 without repetitions
        """
        unblocked = self.stock + self.pyramid.get_all_unblocked()
        result = [(c,) for c in filter(lambda c: c.check_discardable(
            discard_rules=self.rules), unblocked)]
        result += list(filter(lambda cs: cs[0].check_discardable(cs[1],
                                                                 discard_rules=self.rules),
                              itertools.combinations(unblocked, 2)))
        return result

    def score_state(self):
        """
        Score the state according to the greedy rule
        :return: unblocked * 5 + remaining * (-1)
        """
        unblocked = self.stock + self.pyramid.get_all_unblocked()
        remaining = self.cards
        return len(unblocked) * 5 + len(remaining) * (-1)

    def score_action(self, action):
        """
        Return the score of each action according to the greedy rule
        :return type: int
        """
        return self.execute(action).score_state()

    def execute(self, action):
        """
        Return a new State after the execution of action
        """
        stack = self.stack[:]
        stock = self.stock[:]
        pyramid = self.pyramid.duplicate()
        discard = self.discard[:]
        for c in action:
            position = self.hashmap[c]
            if position[0] == "Stock":
                stock.remove(c)
            elif position[0] == "Stack":
                stack.remove(c)
                pyramid.remove_card(position[1], position[2])
            else:
                raise Exception
            discard.append(c)
        return State(stack, stock, pyramid, discard, self.rules)

    def game_over(self):
        """
        Check if the game is over by looking at the first card
        :return: True if first card is None
        """
        return self.pyramid.check_cleared() or len(self.stock) == 0

    def __str__(self):
        """
        Print the state
        :return: The state in three parts:
                 The Pyramid
                 Cards in Hand:
                 Cards Discarded:
        """
        return_string = self.pyramid.__str__()
        return_string += "Cards in Hand: " + " ".join(
            map(lambda c: c.__str__(shorten=True), self.stock)) + "\n"
        return_string += "Cards Discarded: " + " ".join(
            map(lambda c: c.__str__(shorten=True), self.discard)) + "\n"
        return return_string
