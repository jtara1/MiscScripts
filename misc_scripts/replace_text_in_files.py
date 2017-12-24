import click
import os
from glob import glob


@click.command()
@click.option('-s', '--stand-alone', is_flag=True, default=False,
              help='search_text must be stand alone text (not part of another'
                   'word)')
@click.argument('search_text', type=click.STRING)
@click.argument('replace_text', type=click.STRING)
@click.argument('folder', default=os.getcwd())
def main(folder, search_text, replace_text, stand_alone):
    print('-' * 20)
    print('searching for: ' + search_text)
    print('replacing with: ' + replace_text)
    print('searching for stand alone text: ' + str(stand_alone))

    def is_whitespace(char):
        return char == ' ' or char == '\n' or char == '\t'

    folder = os.path.abspath(folder)
    for file in glob(os.path.join(folder, '*')):
        # skip folders
        if os.path.isdir(file):
            continue

        print('looking through: ' + str(file))
        # get text in file
        with open(file, 'r') as f:
            text = f.read()

        if not stand_alone:
            text = text.replace(search_text, replace_text)
        else:
            index = 0

            # search for occurances of search_text found in text
            while index < len(text) - len(search_text):
                index = text.find(search_text, index)
                if index == -1:
                    break  # search_text not found

                # index to left of search text
                l_index = index - 1
                # index to right of s. text
                r_index = index + len(search_text)

                # left side and right side is clear
                # (search_text is standalone)
                if (l_index < 0 or is_whitespace(text[l_index])) \
                        and (r_index >= len(text) or is_whitespace(
                            text[r_index])):
                    text = text[:index] + replace_text + text[r_index:]
                else:
                    index = r_index  # becomes the starting point to search

        # over write text in file with updated text
        with open(file, 'w') as f:
            f.write(text)


if __name__ == '__main__':
    main()
