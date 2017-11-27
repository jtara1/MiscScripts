from distutils.core import setup
import sys
import re


def get_install_requirements():
    requirements = []
    with open('requirements.txt', 'r') as f:
        for line in f:
            requirements.append(re.sub("\s", "", line))
    print(requirements)
    return requirements

if __name__ == "__main__":
    pass

setup(name='MiscScripts',
      version='v0.1',
      description='jtara1\'s scripts to automate small tasks',
      author='James T',
      author_email='jtara@tuta.io',
      url='https://github.com/jtara1/MiscScripts',
      install_requires=get_install_requirements(),
      )