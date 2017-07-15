from zipfile import PyZipFile
import zipfile
import click
import os


@click.command()
@click.argument('folder', default=os.getcwd(), type=click.Path(),
                help='Directory of the folders containing the images.')
def main(folder):
    folder = os.path.abspath(folder)
    for f in os.listdir(folder):
        current_folder = os.path.join(folder, f)
        with zipfile.ZipFile(current_folder + ".zip", 'w') as z_file:
            for file in os.listdir(current_folder):
                z_file.write(os.path.join(current_folder, file))


if __name__ == "__main__":
    main()
