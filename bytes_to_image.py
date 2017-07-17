from PIL import Image
import io
import ast
import click


@click.command()
@click.argument('file_name', default='output.txt', type=click.Path())
@click.option('--cat', default=False, help='concatenate each line in file_name',
              is_flag=True)
def bytes_to_image(file_name, cat):
    # read the string and evaluate 
    with open(file_name, 'r') as f:
        if not cat:
            file_bytes = ast.literal_eval(f.read())
        else:
            file_bytes = bytearray()
            for line in f:
                file_bytes += ast.literal_eval(line)

    image_bytes = io.BytesIO(file_bytes)
    # open image based on bytes from the file & save it
    image = Image.open(image_bytes)
    image.save("output_img.png")


if __name__ == "__main__":
    bytes_to_image()
