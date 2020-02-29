from random import shuffle

import Card
import Pyramid
import State

card_suits = ["Spades", "Hearts", "Clubs", "Diamonds"]
card_faces = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]


# setup functions
def new_deck():
    """
    Setup a new random deck
    :return type: State
    """
    cards = [Card.Card(suit, face) for face in card_faces for suit in card_suits]
    shuffle(cards)
    stack = cards[:28]
    stock = cards[-24:]
    pyramid = Pyramid.Pyramid(stack)
    return State.State(stack, stock, pyramid, [])


def test_deck():
    cards = [Card.Card(suit, face) for face in card_faces for suit in card_suits]
    stack = cards[-28:]
    stock = cards[:24]
    pyramid = Pyramid.Pyramid(stack)
    return State.State(stack, stock, pyramid, [])


# trial function
def trial(strategy, deck=None):
    """
    Construct a trial function
    :param strategy: the action-choosing strategy function that maps an action list
        to an action list with equal highest priority
    :param deck: initial state
    :return: end state
    """
    if deck is None:
        deck = new_deck()
    while deck.get_actions():
        deck = deck.discard_k()
        action = strategy(deck)[0]
        deck = deck.execute(action)
    # print('.', end="")
    return deck


# helper functions
def get_all_mins(l, f):
    """
    # helper function
    Return all min values from a list
    :param l: the list ('a list)
    :param f: evaluation function ('a --> int)
    :return: a list with all min values in list l ('a list)
    """
    min_val = min(map(f, l))
    return [item for item in l if f(item) == min_val]


def one_more_rollout(function, deck):
    """
    # helper function
    One more stage rollout strategy
    :param function: one-less rollout function (action list -> action list)
    :param deck: current deck
    :return: action list with equally maximized prioritized actions
    """
    actions = get_all_mins(function(deck), lambda a: trial(function,
                                                           deck.execute(a)).score_state())
    return actions


# strategies
def simple(deck):
    """
    Simple strategy
    :param type: State
    :return type: action list
    """
    return [deck.get_actions()[0]]


def greedy(deck):
    """
    Greedy strategy
    :param type: State
    :return type: action list
    """
    return get_all_mins(deck.get_actions(), deck.score_action)


def rollout(deck):
    """
    Basic one-stage rollout strategy
    :param type: State
    :return type: action list
    """
    return one_more_rollout(greedy, deck)


def two_stage_rollout(deck):
    """
    Two-stage rollout strategy
    :param type: State
    :return type: action list
    """
    return one_more_rollout(rollout, deck)


def three_stage_rollout(deck):
    """
    Three-stage rollout strategy
    :param type: State
    :return type: action list
    """
    return one_more_rollout(two_stage_rollout, deck)


def four_stage_rollout(deck):
    """
    Four-stage rollout strategy
    :param type: State
    :return type: action list
    """
    return one_more_rollout(three_stage_rollout, deck)
