import Game

deck = Game.Game()
trials = 0
while deck.play() != "Success!":
    trials += 1
    deck = Game.Game()
print(deck, trials)
