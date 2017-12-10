from functools import reduce
from math import factorial
import click


@click.command()
@click.argument('trials', type=click.INT)
@click.argument('prob_of_success', type=click.FLOAT)
def bernolli_trials(trials, prob_of_success):
    def binomial_distribution(n, k):
        return factorial(n) / (factorial(k) * factorial(n - k))
    successes = 0
    prob = 1
    probabilities = []
    while prob >= 0.0001:
        prob_of_failure = 1 - prob_of_success
        prob = binomial_distribution(trials, successes) \
               * prob_of_success ** successes \
               * prob_of_failure ** (trials - successes)
        print("trials = {}, success = {}, successes = {}, probability = {:.3}"
              .format(trials, prob_of_success, successes, prob))
        successes += 1
        probabilities.append(prob)

    for i in range(1, len(probabilities) - 1):
        print("success >= {} is probability = {:.3}"
              .format(i, reduce(lambda x, y: x + y, probabilities[i:])))


if __name__ == '__main__':
    bernolli_trials()
    # bernolli_trials(10, 0.05)
