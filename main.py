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


results = simulation.take_sample(strategies.three_stage_rollout, 1)
print(simulation.count_success(results))






























