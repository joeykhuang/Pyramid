import Game
import statsmodels.api as sm


class Simulation:
    def __init__(self):
        pass

    @staticmethod
    def take_sample(sample_size):
        num_success = 0
        for i in range(sample_size):
            deck = Game.Game()
            if deck.play() == "Success!":
                num_success += 1
        return num_success

    @staticmethod
    def z_test(p, alpha):
        pass

    @staticmethod
    def z_interval(confidence_level, sample_size):
        count = Simulation.take_sample(sample_size)
        return sm.stats.proportion_confint(count, sample_size, alpha=1-confidence_level)
