import click
import os
import requests

__doc__ = """Create a .gitignore file at location of `folder` containing the
             standard .gitignore for python concatenated with the std
             .gitignore for IntelliJ IDEs (Pycharm) 
             that are provided by github"""


def create_gitignore(folder):
    response = requests.get('https://raw.githubusercontent.com/github/'
                            'gitignore/master/Global/JetBrains.gitignore')
    response2 = requests.get('https://raw.githubusercontent.com/github/'
                             'gitignore/master/Python.gitignore')

    if not os.path.isdir(folder):
        os.makedirs(folder)

    with open(os.path.join(folder, '.gitignore'), 'w') as f:
        f.write("{}\n\n{}".format(response.content, response2.content))


@click.command()
@click.argument('folder')
def main(folder):
    create_gitignore(folder)


if __name__ == '__main__':
    main()
