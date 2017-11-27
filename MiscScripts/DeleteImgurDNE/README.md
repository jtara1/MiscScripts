# DeleteImgurDNE

Gets a list of all image files in the given directory, compares each one to that of imgur-dne.png,
and if the bytes are equal, delete the image.

Note: As of Sept. 10th, 2016, this program has very poor efficiency. I believe improving the efficiency  shouldn't be too difficult.

It took me:
* 26 seconds to delete 8 Imgur DNE images recursively in a directory with 10,000 images
* 745 seconds to delete 0 Imgur DNE images recursively in a dictory with 30,000 images

Just be warned this is not efficient for a large amount of images in a folder.

## Requirements

Python 3

Check [jtara1/GetMediaFiles](https://github.com/jtara1/GetMediaFiles#requirements)

## Installation

    git clone https://github.com/jtara1/DeleteImgurDNE.git

    cd DeleteImgurDNE

Optional, update GetMediaFiles submodule

    cd GetMediaFiles

    git pull


## Usage

The first argument should be the **path** containing image files to check, and the second argument
is converted to boolean and determines if GetMediaFiles searches for images **recursively** or not (default is False).

Examples

    python3 delete_dne.py test-case True

    python3 delete_dne.py test-case

    python3 delete_dne.py /home/j/Documents/_Github-Projects/DeleteImgurDNE/test-case True
