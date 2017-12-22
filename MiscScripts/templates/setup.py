from setuptools import setup
import re
from os.path import join, dirname, basename


__file_path = dirname(__file__)
# get module name from parent folder name
# assumes the parent folder (repository name) is the same as the module name
module_name = basename(__file_path)

# -------------- Update the following variables --------------- #
version = '0.1.0'
github_user = 'jtara1'
author = 'James T'
author_email = 'jtara@tuta.io'
description = 'description_needed_from_dev'  # brief module description
# ------------------------------------------------------------- #

github_url = 'https://github.com/{}/{}'.format(github_user, module_name)
download_url = '{github_url}/archive/{version}.tar.gz'\
    .format(github_url=github_url, version=version)
try:
    with open(join(__file_path, 'README.rst')) as f:
        readme = f.read()
except (FileNotFoundError, FileExistsError):
    try:
        with open(join(__file_path, 'README.md')) as f:
            readme = f.read()
    except (FileExistsError, FileNotFoundError):
        readme = description


def get_install_requirements():
    requirements = []
    try:
        with open(join(__file_path, 'requirements.txt'), 'r') as req_file:
            for line in req_file:
                requirements.append(re.sub("\s", "", line))
    except (FileExistsError, FileNotFoundError):
        pass
    return requirements


setup(name=module_name,
      packages=[module_name],
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
