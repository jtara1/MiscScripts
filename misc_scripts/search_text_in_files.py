import re
import click
import os
from glob import glob


@click.command()
@click.option('-s', '--stand-alone', is_flag=True, default=False,
              help='search_text must be stand alone text (not part of another'
                   'word)')
@click.argument('search_text', type=click.STRING)
@click.argument('path', default=os.getcwd())
def main(path, search_text, stand_alone):
    print('-' * 20)
    print('searching for: ' + search_text)
    print('searching for stand alone text: ' + str(stand_alone))

    if stand_alone:
        pattern = re.compile('\b({})\b'.format(search_text), flags=re.DOTALL)
    else:
        pattern = re.compile('({})'.format(search_text))

    def is_whitespace(char):
        return char == ' ' or char == '\n' or char == '\t'

    path = os.path.abspath(path)
    output = {}
    for file in glob(os.path.join(path, '*')):
        output[file] = []
        # skip folders
        if os.path.isdir(file):
            continue

        print('looking through: ' + str(file))
        # get text in file
        try:
            with open(file, 'r') as f:
                text = f.read()
        except UnicodeDecodeError:
            continue

        # contains the tuples of the start and the end of each match
        # e.g.: [(0, 1), (10, 11)]
        indices = []
        start = 0
        while start < len(text):
            matches = pattern.search(text, start)
            if matches:
                print(matches.group(0))
                start = matches.start(1)
                indices.append(start)
                start += len(search_text)
            else:
                break

        
        # print([text[a:len(search_text) + a] for a in indices])


if __name__ == '__main__':
    main()
