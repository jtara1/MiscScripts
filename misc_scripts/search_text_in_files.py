from pprint import pformat
import re
import click
import os
from glob import glob


@click.command()
@click.option('-p', '--print-results', is_flag=True, default=True)
@click.option('-s', '--stand-alone', is_flag=True, default=False,
              help='search_text must be stand alone text (not part of another'
                   'word)')
@click.argument('search_text', type=click.STRING)
@click.argument('path', default=os.getcwd())
def search_text_in_files(path, search_text, stand_alone, print_results):
    print('-' * 20)
    print('searching for: ' + search_text)

    if stand_alone:
        pattern = re.compile('\b({})\b'.format(search_text), flags=re.DOTALL)
    else:
        pattern = re.compile('({})'.format(search_text))

    print('regex pattern used: ' + str(pattern))
    path = os.path.abspath(path)
    # e.g.: {'file.txt': [0, 11, 48]}
    output = {}
    for file in glob(os.path.join(path, '*')):
        output[file] = []
        # skip folders
        if os.path.isdir(file):
            continue

        # get text in file
        try:
            with open(file, 'r') as f:
                text = f.read()
        except UnicodeDecodeError:  # file can't be read, skip
            continue

        # contains the index of each match found in the file
        # e.g.: [0, 11, 48]
        indices = []
        start = 0
        while start < len(text):
            matches = pattern.search(text, start)
            if matches:
                start = matches.start(1)
                indices.append(start)
                start += len(search_text)
            else:
                break

        output[file] = indices
        # print([text[a:len(search_text) + a] for a in indices])

    if print_results:
        for file, indices in zip(output.keys(), output.values()):
            if indices != []:
                print("{}\n{}\n-------------------"
                      .format(file, pformat(indices)))
    return output


if __name__ == '__main__':
    search_text_in_files()
