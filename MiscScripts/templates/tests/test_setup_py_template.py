import sys
from os.path import dirname, join, abspath
import shutil


path = dirname(__file__)
parent_path = dirname(path)
base_module_path = join(path, '../../..')
sys.path.append(base_module_path)


def test():
    dest_folder = join(path, 'my_module')
    shutil.copy(join(parent_path, 'setup.py'), dest_folder)
    shutil.copy(join(parent_path, 'setup.cfg'), dest_folder)

    from MiscScripts.MiscScripts.templates.tests.my_module.setup import \
        change_rst_to_md_extension_in_cfg

    expected = """
    [metadata]
    name = get_media_files
    description-file = README.md
    """

    change_rst_to_md_extension_in_cfg()
    with open(abspath('my_module/README.md'), 'r') as f:
        text = f.read()
        print(text)

    assert(text == expected)


if __name__ == '__main__':
    test()
