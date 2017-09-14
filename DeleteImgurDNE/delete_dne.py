import os
import sys

# lazy way to import submodule whose path is in ../GetMediaFiles relative to
# the file path of this file (__file__)
sys.path.append(os.path.join(os.path.dirname(__file__), '../GetMediaFiles'))
from GetMediaFiles.get_media_files import GetMediaFiles

import time
import hashlib
import click


def are_files_equal(file1, file2):
    """ given two file objects, checks to see if their bytes are equal """
    if bytearray(file1.read()) == bytearray(file2.read()):
        return True
    else:
        return False


def is_imgur_dne_image(img_path):
        """ takes full image path & checks if bytes are equal to that of imgur does not exist image """
        prg_path = os.path.abspath(os.path.dirname(__file__))
        dne_img = os.path.join(prg_path, 'imgur-dne.png') # edit location if needed
        with open(dne_img, 'rb') as f:
            dne_data = bytearray(f.read())
        with open(img_path, 'rb') as f:
            data = bytearray(f.read())
            if data == dne_data:
                return True
            else:
                return False


def hashfile(afile, hasher, blocksize=65536):
    buf = afile.read(blocksize)
    while len(buf) > 0:
        hasher.update(buf)
        buf = afile.read(blocksize)
    return hasher.hexdigest()


def delete_dne_hash_cmp(path, recursive=False, verbose=False):
    """Delete file if its hash matches that of the reference file"""

    media = GetMediaFiles()
    files = media.get_all(path=path, recursive=recursive, track_types=['Image'],
                            sort=False)

    if verbose:
        media.print_files(files) # debug
    print('%s files found' % len(files)) # debug
    print('-------------------------') # debug

    init_t = time.time()

    # imgur dne image hashlib
    dne_hash = hashfile(open('imgur-dne.png', 'rb'), hashlib.sha256())

    # list of hashes
    hashes = list((hashfile(open(fname[0], 'rb'), hashlib.sha256())) for fname in files)
    amount_deleted = 0
    for index in range(len(hashes)):
        if hashes[index] == dne_hash:
            amount_deleted += 1
            print('%s' % (os.path.split(f[0])[1]))
            os.remove(files[index][0])

    print("delete_dne_hash_cmp func took %d seconds\n" % (int(time.time() - init_t)))

    return amount_deleted


def delete_dne(path, recursive=False, verbose=False):
    """Delete duplicate file if its byte array matches that of the reference
    """

    media = GetMediaFiles()
    files = media.get_all(path=path, recursive=recursive,
                          track_types=['Image'], sort=False)

    init_t = time.time()

    if verbose:
        media.print_files(files)  # debug
    print('%s files found' % len(files))  # debug
    print('-------------------------')  # debug

    amount_deleted = 0
    # loop over files & check if it's an Imgur DNE image
    for f in files:
        if verbose:
            print(f[0])  # debug

        if is_imgur_dne_image(f[0]):
            amount_deleted += 1
            print('%s' % (os.path.split(f[0])[1]))
            os.remove(f[0])

    print("delete_dne func took %d seconds\n" % (int(time.time() - init_t)))
    return amount_deleted


if __name__ == "__main__":
    @click.command()
    @click.argument('folder')
    @click.option('-r', '--recursive', default=False, is_flag=True)
    def main(folder, recursive):
        init_t = time.time()

        folder = os.path.abspath(folder)
        amount_deleted = delete_dne(folder, recursive, verbose=True)

        # test_path = 'test-case'
        # delete_dne(test_path, recursive=True)

        print('[DeleteImgurDNE] %i seconds passed' %
              (time.time() - init_t))
        print('[DeleteImgurDNE] %i DNE images found & deleted' %
              amount_deleted)

    main()
