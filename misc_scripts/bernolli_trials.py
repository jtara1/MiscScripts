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
    output = ['trials = {}, success = {}'.format(trials, prob_of_success),
              ''.join(['-'] * 50)]
    prob_of_failure = 1 - prob_of_success

    while (prob >= 0.0001 or successes <= 2) and trials >= successes:
        prob = binomial_distribution(trials, successes) \
               * prob_of_success ** successes \
               * prob_of_failure ** (trials - successes)
        output.append("successes = {}, probability = {:.3}"
                      .format(successes, prob))
        successes += 1
        probabilities.append(prob)

    output.append(''.join(['-'] * 50))
    for i in range(1, len(probabilities) - 1):
        output.append("successes >= {}, probability = {:.3}"
                      .format(i, reduce(lambda x, y: x + y, probabilities[i:])))
    print('\n'.join(output))
    # return '\n'.join(output)
    # return output


if __name__ == '__main__':
    output = bernolli_trials()
    print(output)
    # bernolli_trials(10, 0.05)
