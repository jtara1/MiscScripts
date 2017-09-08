import click
from PIL import Image
import os
import shutil


TARGET_DIM = None  # target dimensions. The size we're resizing imgs to


@click.command()
@click.option('-w', '--width', type=click.INT,
              help='Desired width for each image', default=None)
@click.option('-h', '--height', type=click.INT,
              help='Desired height for each image', default=None)
@click.option('-nb', '--no-backup', is_flag=True, default=False,
              help='Does not create a copy of images before overwriting them'
                   'with resize copy of themselves')
@click.argument('file_path', default=os.getcwd())
def main(width, height, file_path, no_backup):
    """
    Resize the image(s) in file_path.
    :param width: 
    :param height: 
    :param file_path: File path containing all the photos to resize
    :param no_backup: If true, does not create a backup copy of the images
        that're going to be resized
    :return: 
    """
    print('running ...')
    global TARGET_DIM
    TARGET_DIM = [width, height]

    if not no_backup:
        create_copy_of(file_path)

    file_path = os.path.abspath(file_path)
    for file in os.listdir(file_path):
        print('resizing: ' + file)
        resize_image(os.path.join(file_path, file))


def resize_image(_image_file_path):
    # load image and draw on canvas
    image = Image.open(_image_file_path)
    scaled_img_size = _fit_img(image.size[0], image.size[1])
    image.thumbnail(size=scaled_img_size)
    image.save(_image_file_path)


def create_copy_of(file_path):
    """
    Iteratively creates a copy of each file in the file_path into a new
    folder of the same name with '-backup' append it the end of it
    :param file_path: 
    :return: 
    """
    file_path = os.path.abspath(file_path)
    new_path = file_path
    if new_path.endswith(('/', '\\')):
        new_path = new_path[:-1]

    new_path += '-backup'
    if not os.path.isdir(new_path):
        os.makedirs(new_path)  # make the backup directory

    for file in os.listdir(file_path):
        # copy files into new path (src -> dest)
        shutil.copy(os.path.join(file_path, file),
                    os.path.join(file, new_path))


def _fit_img(w, h):
    """ Get width & height to scale image to to fit window size """
    w2 = w
    h2 = h
    # assumes wind. width > wind. height (most aspect ratios work that way)
    if w > h and TARGET_DIM[0]:
        w2 = TARGET_DIM[0]
        _scale_ratio = float(w2) / w
        h2 = _scale_ratio * h
    elif h >= w and TARGET_DIM[1]:
        h2 = TARGET_DIM[1]
        _scale_ratio = float(h2) / h
        w2 = _scale_ratio * w
    return w2, h2


if __name__ == '__main__':
    main()
