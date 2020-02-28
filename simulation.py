import time

import statsmodels.api as sm

import strategies


# def take_sample(sample_size):
#     num_success = 0
#     for i in range(sample_size):
#         deck = State.State()
#         if deck.play() == "Success!":
#             num_success += 1
#     return num_success


def take_sample(strategy_function, sample_size, track_time=True):
    """
    Return the trials and their results
    :param strategy_function: the strategy function
    :param sample_size: total number of trials (sample size)
    :return: a list of the result of the functions
    """
    if track_time:
        start_time = time.time()
    result = [strategies.trial(strategy_function) for _ in range(sample_size)]
    if track_time:
        print(strategy_function.__name__ + " simulation with " +
              str(sample_size) + " times:")
        print('Elapsed Time: %s' % (time.time() - start_time))
    return result


def count_success(result_list):
    """
    Return the number of successes in the result list
    :param result_list type: State list
    :return type: int
    """
    return len(list(filter(lambda s: s.game_over(), result_list)))


def z_interval(confidence_level, strategy, sample_size):
    count = count_success(take_sample(strategy, sample_size))
    return sm.stats.proportion_confint(count, sample_size, alpha=1 - confidence_level)
