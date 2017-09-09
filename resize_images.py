import click
from PIL import Image
import os
import shutil
from bs4 import BeautifulSoup
import bs4
from pprint import pformat
import re


__doc__ = """This script was built to lower the resolution of images that
             were setup to be used to train a model to classify objects
             in an image. It can also be used as a stand-alone bulk image
             resizer.
          """

TARGET_DIM = None  # target dimensions. The size we're resizing imgs to
# e.g.: { 'image_name' : 0.20 }
IMG_RESIZED_SCALE = {}  # the coef multiple used to scale the image


@click.command()
@click.option('-a', '--annotations',
              default=os.path.join(os.getcwd(), 'annotations'),
              help='Updates the info about bounding boxes in XML annotation'
                   'files expected formatting is '
                   'Pascal Visual Object Classes (VOC)')
@click.option('-w', '--width', type=click.INT,
              help='Desired width for each image', default=None)
@click.option('-h', '--height', type=click.INT,
              help='Desired height for each image', default=None)
@click.option('-nb', '--no-backup', is_flag=True, default=False,
              help='Does not create a copy of images before overwriting them'
                   'with resize copy of themselves')
@click.argument('file_path', default=os.getcwd())
def main(file_path, width, height, annotations, no_backup):
    """
    Resize the image(s) in file_path.
    :param file_path: File path containing all the photos to resize
    :param width: target width all images are resized to
    :param height: target height all images are resized to
    :param annotations: File path containing all of the Pascal VOC formatted
        annotations containing info on bounding boxes of each of the images
    :param no_backup: If true, does not create a backup copy of the images
        that're going to be resized
    :return: 
    """
    if width and height:
        raise Exception("Please provide only a width xor only a height for "
                        "the new size of each image")

    print('running ...')
    global TARGET_DIM
    TARGET_DIM = [width, height]

    # create copy backup of all images
    if not no_backup:
        create_copy_of(file_path)

    file_path = os.path.abspath(file_path)
    # resize the images
    for file in os.listdir(file_path):
        print('resizing: ' + file)
        resize_image(os.path.join(file_path, file))

    # resize the bounding boxes associated with previous images
    annotations = os.path.abspath(annotations)
    if os.path.isdir(annotations):
        # make the copy backup
        if not no_backup:
            print('creating annotations backup')
            create_copy_of(annotations)

        # resize info in each annotation
        for file in os.listdir(annotations):
            anno_path = os.path.join(annotations, file)
            if os.path.isfile(anno_path) and file.endswith('.xml'):
                print('resizing anno: ' + file)
                resize_annotation(anno_path)


def resize_image(image_file_path):
    """Changing the size of a single image"""
    # load, get new resolution, convert, save img
    try:
        image = Image.open(image_file_path)
    except OSError:
        # the file opened was probably a non-image file
        return
    orig_width = image.width
    scaled_img_size = _fit_img(image.size[0], image.size[1])
    image.thumbnail(size=scaled_img_size)
    image.save(image_file_path)

    # keep track of the scale used for resizing for annotations later
    # assumes the only period in file name is for file extension (or there is
    # no extension or period)
    img_name = get_file_name(image_file_path)
    IMG_RESIZED_SCALE[img_name] = float(image.width) / orig_width


def _fit_img(w, h):
    """Get width & height to scale image to to fit new size whilst 
    maintaining the original aspect ratio
    """
    w2 = w
    h2 = h
    # assumes wind. width > wind. height (most aspect ratios work that way)
    if w > h and TARGET_DIM[0]:
        w2 = TARGET_DIM[0]
        scale_ratio = float(w2) / w
        h2 = scale_ratio * h
    elif h >= w and TARGET_DIM[1]:
        h2 = TARGET_DIM[1]
        scale_ratio = float(h2) / h
        w2 = scale_ratio * w
    return w2, h2


def resize_annotation(anno_path):
    """Change the values inside the size tag and bndbox tags to match the 
    resized image
    """
    def cleanse_tag_string(string):
        string.replace('\n', '')
        return string

    with open(anno_path, 'r+') as f:
        text = ''
        # if 'xml' not in f.readline():
        #     text = '<?xml version="1.0" ?>\n'
        #
        # f.seek(0)
        text += f.read()

        soup = BeautifulSoup(text, 'lxml')
        anno_name = get_file_name(anno_path)

        global IMG_RESIZED_SCALE
        # change size values (info on width and height of image)
        for tag in soup.find('size').children:
            if tag.name == 'depth' or isinstance(tag, bs4.element.NavigableString):
                continue
            tag.string = str(int(int(cleanse_tag_string(tag.string))
                             * IMG_RESIZED_SCALE[anno_name]))

        # change bounding box info
        for obj_tag in soup.find_all('object'):
            for tag in obj_tag.find('bndbox').children:
                if not isinstance(tag, bs4.element.NavigableString):
                    tag.string = str(int(int(cleanse_tag_string(tag.string))
                                     * IMG_RESIZED_SCALE[anno_name]))

    # save changes in original file
    with open(anno_path, 'w') as f:
        # rm the tags bs4 inserted
        soup = str(soup)
        for s in ('<html>', '<body>', '</html>', '</body>'):
            soup = soup.replace(s, '')
        f.write(soup)


def get_file_name(file_path):
    """Get the name of the file without the extension"""
    return os.path.basename(file_path).split('.')[0]


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
        try:
            # copy files into new path (src -> dest)
            shutil.copy(os.path.join(file_path, file),
                        os.path.join(file, new_path))
        except IsADirectoryError:
            # don't backup folders inside the file_path
            continue


if __name__ == '__main__':
    main()
