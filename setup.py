from distutils.core import setup
import sys
import re


def get_install_requirements():
    requirements = []
    with open('requirements.txt', 'r') as f:
        for line in f:
            # rm comments and whitespace chars
            line = re.sub("(\s|#.*)", "", line)
            requirements.append()
    print(requirements)
    return requirements

if __name__ == "__main__":
    pass

setup(name='misc_scripts',
      version='v0.1',
      description='jtara1\'s scripts to automate small tasks',
      author='James T',
      author_email='jtara@tuta.io',
      url='https://github.com/jtara1/misc_scripts',
      install_requires=get_install_requirements(),
      )
