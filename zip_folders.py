import zipfile
import click
import os


@click.command()
@click.argument('folder', type=click.Path(), default=os.getcwd())
@click.option('-v', type=click.BOOL, is_flag=True)  # verbose, print extra info
def zip_folders(folder, v):
    folder = os.path.abspath(folder)
    # iterate over all the folders & files
    for f in os.listdir(folder):
        current_folder = os.path.join(folder, f)
        # this item is a file, not a folder
        if not os.path.isdir(current_folder):
            continue

        if v:
            print("ZIPPING FOLDER: {}".format(current_folder))
        # open a zip file (to write to)
        with zipfile.ZipFile(current_folder + ".zip", 'w') as z_file:
            # write each file or folder in the current_folder
            for file in os.listdir(current_folder):
                if v:
                    print('zipping: {}'.format(file))
                z_file.write(os.path.join(current_folder, file))


if __name__ == "__main__":
    zip_folders()
