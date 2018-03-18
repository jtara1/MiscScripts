from setuptools import setup, find_packages
import re
from os.path import join, dirname, basename


# -------------- Update the following variables --------------- #
version = '0.1.0'
github_user = 'jtara1'
author = 'James T'
author_email = 'jtara@tuta.io'
description = 'description_needed_from_dev'
# ------------------------------------------------------------- #

__path = dirname(__file__)  # path to this file but not including this file
# get module name from parent folder name
# assumes the parent folder (repository name) is the same as the module name
module_name = basename(__path)
github_url = 'https://github.com/{}/{}'.format(github_user, module_name)
download_url = '{github_url}/archive/{version}.tar.gz'\
    .format(github_url=github_url, version=version)


def change_rst_to_md_extension_in_cfg():
    """Replaces README.rst with README.md in setup.cfg"""
    try:
        with open(join(__path, 'setup.cfg'), 'r+') as config:
            text = config.read()
            text = re.sub('README.rst', 'README.md', text)
            config.write(text)
    except (FileNotFoundError, FileExistsError):
        print('[setup.py] Warning: No setup.cfg found')


# Store text from README.rst or README.md to use in long description and
# update setup.cfg to point to the correct readme if needed
try:
    with open(join(__path, 'README.rst')) as f:
        readme = f.read()
except (FileNotFoundError, FileExistsError):
    try:
        with open(join(__path, 'README.md')) as f:
            readme = f.read()
            change_rst_to_md_extension_in_cfg()
    except (FileExistsError, FileNotFoundError):
        readme = description


def get_install_requirements():
    """Returns the parsed list of strings of required modules listed in
    requirements.txt.txt"""
    requirements = []
    try:
        with open(join(__path, 'requirements.txt.txt'), 'r') as req_file:
            for line in req_file:
                requirements.append(re.sub("\s", "", line))
    except (FileExistsError, FileNotFoundError):
        print('[setup.py] Note: No requirements.txt.txt found')
    return requirements


setup(name=module_name,
      packages=find_packages(),  # find all dependencies for this module
      version=version,
      description=description,
      long_description=readme,
      author=author,
      author_email=author_email,
      url=github_url,
      download_url=download_url,
      keywords=[],
      install_requires=get_install_requirements(),
      # list of strs https://pypi.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[]
      )
