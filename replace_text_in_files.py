import click
import os


@click.command()
@click.argument('replace_text')
@click.argument('search_text')
@click.argument('folder', default=os.getcwd())
def main(folder, search_text, replace_text):
    folder = os.path.abspath(folder)
    for file in os.listdir(folder):
        with open(file, 'r+') as f:
            text = f.read()
            updated_text = text.replace(search_text, replace_text)
            text.write(updated_text)


if __name__ == '__main__':
    main()