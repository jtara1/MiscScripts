import click
from glob import glob
import os


@click.command()
@click.argument("file_path", type=click.Path())
@click.argument("extension", type=click.STRING)
@click.option("-r", is_flag=True, default=False)
def main(file_path, extension, r):
    all_files = glob(os.path.join(file_path, "**"), recursive=r)

    for file in all_files:
        file_base_name = os.path.basename(file)
        print(file_base_name)

        if os.path.isfile(file) and '.' not in file_base_name:
            print('CHANGING: {}'.format(file))
            os.rename(file, file + extension)


if __name__ == "__main__":
    main()