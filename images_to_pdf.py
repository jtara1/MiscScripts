from fpdf import FPDF
import os
import glob
import PIL
from PIL import Image
import click


letter_width_inches = 8.5
letter_height_inches = 11


def images_to_pdf(path, offset_coords=(-5, 0), ext='.png'):
	path = os.path.abspath(path)
	image_files = glob.glob(os.path.join(path, "*"))
	image_files = sorted(
                image_files,
                key=pull_int_from_path)

	# print(image_files)
	pdf = FPDF()
	# imagelist is the list with all image filenames
	for image in image_files:
		print(image)
		new_size = scale_image_to_letter_size(image)
		print(new_size)
		pdf.add_page(orientation='Portrait')
		pdf.image(
                        image,
                        x=offset_coords[0],
                        y=offset_coords[1],)
                        #w=new_size[0],
                        #h=new_size[1])
	pdf.output("yourfile.pdf", "F")


def pull_int_from_path(path):
	filename = os.path.basename(path).split(".")[0]
	return int(extract_digits(filename))


def extract_digits(word):
	s = "0"
	for char in word:
		if char.isdigit():
			s += char
	return s


def get_letter_size_scaled(size):
        """Gets new size closest to param size while maintaining letter aspect ratio"""
        size_ratio = float(size[0]) / size[1]
        letter_ratio = letter_width_inches / letter_height_inches
        if size[0] >= size[1]:
                width = size[0]
                height = int(width * (1/letter_ratio))
        else:
                height = size[1]
                width = int(height * letter_ratio)
        return width, height


def scale_image_to_letter_size(img_path, dpi=72):
        def get_new_size(image):
                """Scales image size to letter size while maintaining img aspect ratio"""
                width, height = 0, 0
                image_aspect_ratio = image.size[0] / float(image.size[1])
                if image.size[0] >= image.size[1]:
                        width = int(letter_width_inches * dpi)
                        height = int(width * (1/image_aspect_ratio))
                else:
                        height = int(letter_height_inches * dpi)
                        width = int(height * image_aspect_ratio)
                return width, height

        try:
            im = Image.open(img_path)
            new_size = get_new_size(im)
            #new_size = get_letter_size_scaled(im.size)
            if new_size != im.size:
                    im.thumbnail(new_size, Image.ANTIALIAS)
                    im.save(img_path, "PNG")
            return new_size
        except IOError:
            print("cannot create thumbnail for '%s'" % infile)


@click.command()
@click.argument('folder')
def main(folder):
	if os.path.isdir(folder):
		images_to_pdf(folder)


if __name__ == "__main__":
	main()
