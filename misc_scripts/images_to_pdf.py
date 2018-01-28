from fpdf import FPDF
import os
import glob
import PIL
from PIL import Image
import click

__doc__ = """
saves each image in a directory on a page of a newly created PDF
"""


letter_width_inches = 8.5
letter_height_inches = 11


def images_to_pdf(path, offset_coords=(-5, 0), ext='.png'):
    path = os.path.abspath(path)
    image_files = glob.glob(os.path.join(path, "*"))
    image_files = sorted(image_files,
                         key=pull_int_from_path)

    # Assumes all the images are the same size
    size = Image.open(image_files[0]).size
    pdf = FPDF(format=size)

    # add a page containing a single image for each image
    for image in image_files:
        print(image)
        img_size = Image.open(image).size
        pdf.add_page(orientation='Portrait')
        pdf.image(image,
                  x=offset_coords[0],
                  y=offset_coords[1],
                  w=img_size[0],
                  h=img_size[1])

    print("Creating final PDF, this may take a while")
    pdf.output("output.pdf", "F")
    print("done")


def pull_int_from_path(path):
    filename = os.path.basename(path).split(".")[0]
    return int(extract_digits(filename))


def extract_digits(word):
    s = "0"
    for char in word:
        if char.isdigit():
            s += char
    return s


@click.command()
@click.argument('folder')
def main(folder):
    """
    Run the script to create a PDF from a sequence of images located in the given folder
    :param folder: folder path containing the images
    :return:
    """
    if os.path.isdir(folder):
        images_to_pdf(folder)


if __name__ == "__main__":
    main()
