import click
import os
import requests

__doc__ = """Create or append a .gitignore file at location 
             of `folder` containing the standard .gitignore for python
              concatenated with the std .gitignore for IntelliJ IDEs (Pycharm) 
             that are provided by github"""


def create_gitignore(folder):
    intellij_resp = requests.get('https://raw.githubusercontent.com/github/'
                                 'gitignore/master/Global/JetBrains.gitignore')
    py_response = requests.get('https://raw.githubusercontent.com/github/'
                               'gitignore/master/Python.gitignore')

    if not os.path.isdir(folder):
        os.makedirs(folder)

    with open(os.path.join(folder, '.gitignore'), 'a') as f:
        f.write("{}\n\n{}".format(py_response.text,
                                  intellij_resp.text))


@click.command()
@click.argument('folder')
def main(folder):
    create_gitignore(folder)


if __name__ == '__main__':
    main()
