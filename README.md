# MiscScripts
Various scripts I've found to be useful



`add_file_extensions.py` concatenates the user-given extension to each file
in the given folder. Useful for when there's lots of media files made on linux
w/o file name extension which need file name extension in windows.

`anti_afk.py` prevents player from being marked as afk in a video game by
moving the character forward and backward (`w` and `s` key presses) keys.

`bytes_to_image.py` converts the bytes located in a text file to an image. It
was only tested with the bytes of a PNG image.

`count_lines.py` counts the number of files given the extension of the files and
the total number of lines between all the files. Useful for checking how many
lines and files were used in some programming project.

`file_to_bytes.py` saves the bytes of a file to a text file.

`resize_images.py` resizes each image in a folder to a given width or height
while maintaining the original aspect ratio (makes backup copy by default).
Eventually this is intended to update annotations which contain
info on bounding boxes for the image additionally.

`tol_macros.py` macros made for a particular game, some of which can be used in
other games or have base class, Action, extended for use elsewhere. Includes:
auto item pickup (presses f), auto dirt digger (clicks and moves mouse),
and auto walker (holds w). All of these macros are assigned to the hotkeys
(`F2`, `F3`, `F4`) respectively.

`zip_folders.py` zips the content of each folder in a directory into their own
zip file. Useful for making folders (chapters) of a comic
readable by apps such as ComicRack.

### Requirements

Tested with *Python 3.5+*

### Install

```
git clone https://github.com/jtara1/MiscScripts.git && cd MiscScripts
pip install -r requirements.txt
```

### Usage

Depends on which script you're using. Most (or all?) of the scripts are using
click module for cli so you could just run it and check the help and cli
info in console

e.g.:
`python add_file_extensions.py`

returns
```
C:\Users\James\Documents\_Github-Projects\MiscScripts>python add_file_extensions.py
Usage: add_file_extensions.py [OPTIONS] FILE_PATH EXTENSION

Error: Missing argument "file_path".
```


#### Modules

- [check requirements.txt](https://github.com/jtara1/MiscScripts/blob/master/requirements.txt)
