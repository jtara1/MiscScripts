import click
import os
from glob import glob


@click.command()
@click.argument('search_text', type=click.STRING)
@click.argument('replace_text', type=click.STRING)
@click.argument('folder', default=os.getcwd())
def main(folder, search_text, replace_text):
    print('-' * 20)
    print('searching for: ' + search_text)
    print('searching for: ' + replace_text)

    folder = os.path.abspath(folder)
    for file in glob(os.path.join(folder, '*')):
        if os.path.isdir(file):
            continue

        print('looking through: ' + str(file))
        with open(file, 'r+') as f:
            text = f.read()
            updated_text = text.replace(search_text, replace_text)
            f.seek(0)
            f.write(updated_text)

if __name__ == '__main__':
    main()
