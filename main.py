import simulation
import strategies

# deck = Game.Game()
# trials = 0
# while deck.play() != "Success!":
#     trials += 1
#     print(deck)
#     deck = Game.Game()
# print(deck, trials)
#
# print(Simulation.Simulation.z_interval(0.9, 100))

basic = simulation.z_interval(0.95, strategies.simple, 1000)
print(basic)
greedy = simulation.z_interval(0.95, strategies.greedy, 100)
print(greedy)
one_rollout = simulation.z_interval(0.95, strategies.rollout, 10)
print(one_rollout)

