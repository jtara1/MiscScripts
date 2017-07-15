import zipfile
import click
import os


@click.command()
@click.argument('folder', type=click.Path(),
                help='Directory of the folders containing the images.')
def main(folder):
    folder = os.path.abspath(folder)
    # iterate over all the folders & files
    for f in os.listdir(folder):
        current_folder = os.path.join(folder, f)
        # open a zip file (to write to)
        with zipfile.ZipFile(current_folder + ".zip", 'w') as z_file:
            # write each file or folder in the current_folder
            for file in os.listdir(current_folder):
                z_file.write(os.path.join(current_folder, file))


if __name__ == "__main__":
    main()
