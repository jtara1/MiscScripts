import shutil
from setuptools import setup, find_packages
import re
from os.path import join, dirname, basename, abspath


__doc__ = """This template setup.py file was intended to be generic enough
for use in any of my python modules on github. It will create setup.cfg and  
update the metadata that is required there. It'll automatically determine the 
name of the module by using the parent folder name of this setup.py file.
It pulls the text inside the README.md or README.rst to use in the 
long_descriptiion of the setup function
Fill out the information below with your own for your module.
The version 

Author: https://github.com/jtara1
Source: 
https://github.com/jtara1/misc_scripts/blob/master/misc_scripts/templates/setup.py
"""

# path to this file but not including this file
__path = dirname(abspath(__file__))
# get module name from parent folder name
# assumes the parent folder (repository name) is the same as the module name
module_name = basename(__path)
# attempt to find variable module_name.__init__.__version__
__version__ = '0.1.0'
try:
    this_module = __import__(module_name + '.__init__')
    __version__ = this_module.__version__
except ImportError:
    print('[setup.py] Note: There was no __init__.py found within module')
except AttributeError:
    print('[setup.py] Note: There was no __version__ variable within the '
          '__init__.py of the module')

# -------------- Update the following variables --------------- #
# prioritize using __version__ in module_name.__init__ if it's there
version = '0.1.0' if '__version__' not in locals().keys() else __version__
github_user = 'jtara1'
author = 'James T'
author_email = 'jtara@tuta.io'
description = 'description_needed_from_dev'
# ------------------------------------------------------------- #

github_url = 'https://github.com/{}/{}'.format(github_user, module_name)
download_url = '{github_url}/archive/{version}.tar.gz'\
    .format(github_url=github_url, version=version)


def create_setup_cfg(callback=None):
    """Creates the setup.cfg file with basic metadata and calls the callback"""
    with open(join(__path, 'setup.cfg'), 'w') as config:
        config.write(
            "[metadata]\nname = {module_name}\ndescription-file = {readme}"
            .format(module_name=module_name, readme=readme))
    if callback is not None:
        callback()


def change_rst_to_md_extension_in_cfg():
    """Replaces README.rst with README.md in setup.cfg"""
    try:
        with open(join(__path, 'setup.cfg'), 'r+') as config:
            text = config.read()
            text = re.sub('README.rst', 'README.md', text)
            config.seek(0)
            config.write(text)
    except (FileNotFoundError, FileExistsError):
        create_setup_cfg(change_rst_to_md_extension_in_cfg)
        # print('[setup.py] Warning: No setup.cfg found')


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
    requirements.txt"""
    requirements = []
    try:
        with open(join(__path, 'requirements.txt'), 'r') as req_file:
            for line in req_file:
                requirements.append(re.sub("\s", "", line))
    except (FileExistsError, FileNotFoundError):
        print('[setup.py] Note: No requirements.txt found')
    return requirements


def update_cfg_module_name():
    """Replaces the module name in setup.cfg with module_name"""
    try:
        with open(join(__path, 'setup.cfg'), 'r+') as config:
            text = config.read()
            text = re.sub('name = module_name(_setup_cfg)?',
                          'name = {}'.format(module_name),
                          text)
            config.seek(0)
            config.write(text)
    except (FileNotFoundError, FileExistsError):
        create_setup_cfg(update_cfg_module_name)
        # print('[setup.py] Warning: No setup.cfg found')


update_cfg_module_name()

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