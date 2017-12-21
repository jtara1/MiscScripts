from distutils.core import setup
import re
from os.path import join, dirname, basename


version = '0.1.0'
__file_path = dirname(__file__)
# get module name from parent folder name
# assumes the parent folder (repository name) is the same as the module name
module_name = basename(dirname(__file_path))
github_user = 'jtara1'
github_url = 'https://github.com/{}/{}'.format(github_user, module_name)
try:
    with open(join(__file_path, 'README.rst')) as f:
        readme = f.read()
except (FileNotFoundError, FileExistsError):
    readme = ''
description = 'description_needed'


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
      long_description=readme if readme is not '' else description,
      author='James T',
      author_email='jtara@tuta.io',
      url=github_url,
      download_url='{github_url}/archive/{version}.tar.gz'
      .format(github_url=github_url, version=version),
      keywords=[],
      install_requires=get_install_requirements(),
      classifiers=[]
      )
