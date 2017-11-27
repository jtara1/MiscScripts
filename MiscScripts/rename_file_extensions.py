import click
from glob import glob
import os


@click.command()
@click.argument("file_path", type=click.Path())
@click.argument("ext_target", type=click.STRING)
@click.argument("ext_replacer", type=click.STRING)
@click.option("-r", is_flag=True, default=False)
def main(file_path, ext_target, ext_replacer, r):
    all_files = glob(os.path.join(file_path, "**"), recursive=r)

    for file in all_files:
        file_base_name = os.path.basename(file)
        print(file_base_name)

        if os.path.isfile(file) and file_base_name.endswith(ext_target):
            print('CHANGING: {}'.format(file))
            os.rename(file, "".join(file.split(ext_target)[:-1]) + ext_replacer)


if __name__ == "__main__":
    main()
