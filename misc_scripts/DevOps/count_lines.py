import click
from glob import glob
import os


@click.command()
@click.argument('file_path', type=click.Path())
@click.argument('file_ext', type=click.STRING)
@click.option('-r', help='recursive', is_flag=True, default=False)
@click.option('-i', help='ignore this directory or file if i in the path')
def main(file_path, file_ext, r, i):
    lines = 0
    files = 0
    all_files = glob(os.path.join(file_path, '**/*.'+file_ext), recursive=r) if r \
        else glob(os.path.join(file_path, '*.'+file_ext), recursive=r)

    for file in all_files:
        print(file)
        if i in file:
            continue
        files += 1
        for _ in open(file, 'r'):
            lines += 1
    print('files: {}\nlines: {}'.format(files, lines))


if __name__ == "__main__":
    main()
