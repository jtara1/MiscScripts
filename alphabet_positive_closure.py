import os
import itertools
import fire
import functools


class Symbol:
    def __init__(self, symbol):
        """Makes sorting better for get_permutations function"""
        self.symbol = symbol

    def __cmp__(self, other):
        if len(self.symbol) == len(other.symbol):
            return self - other
        return len(self.symbol) - len(other.symbol)

    def __sub__(self, other):
        """Returns 1 if other symbol is further in alphabet, -1 if this symbol
        is further in alphabet than other.symbol and 0 if they're equal symbols
        """
        if self.symbol == other.symbol:
            return 0
        return 1 if self.symbol > other.symbol else -1

    def __lt__(self, other):
        return self.__cmp__(other) < 0

    def __str__(self):
        return self.symbol

    def concatenate(self, other):
        """Returns the new Symbol concatenated with this Symbol and the other
        one"""
        return Symbol(self.symbol + other.symbol)


def get_products(max_length=2, output_file=None, *symbols):
    """
    Given an arbitrary number of symbols (single character strings),
    create a set from these symbols and get the products of them.
    :param max_length: max length of the products (e.g.: 3 for set('a','b')
        -> ['a', 'b', 'ab', 'ba', 'aaa', 'aab', 'aba', 'baa', 'abb', 'bab',
            'bba', 'bbb']
    :param output_file: file path in which each product generated will be
        saved to separated by newline characters if output_file is given
    :param symbols: any number of single character strings
    :return: the products of the alphabet
    """
    def write_if_avail(data):
        if out_file:
            out_file.write(str(data) + '\n')

    alphabet = set(Symbol(symbol) for symbol in symbols)
    # using list over set to preserve order
    products = sorted(list(alphabet))

    # open output file and write initial alphabet set to it if it's available
    out_file = open(os.path.abspath(output_file), 'w') if output_file else None
    list(write_if_avail(symbol) for symbol in products)

    for length in range(2, max_length):
        # iterable of tuples of length length of the products of all the
        # products so far
        p = set(itertools.product(products, repeat=2))  # product of self

        # reduce tuple of symbols to string and make all products union
        # of the products and this new products of length length
        for product in p:
            product = functools.reduce(
                lambda x, y: x.concatenate(y),
                product)

            write_if_avail(product)
            products.append(product)
        # products.extend(list(''.join(product) for product in p))

    if out_file:
        out_file.close()

    products = sorted(products)
    # print(products)
    return products


def main():
    fire.Fire(get_products)


if __name__ == '__main__':
    # get_permutations(3, 'output.txt', 'a', 'b')
    main()
