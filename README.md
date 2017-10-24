# MiscScripts
Various scripts I've found to be useful.


`HTML/blk-bg.html` is a simple HTML file with a black background that I use
on my 2nd monitor so I don't have this glaring bright white thing to my side.

 `Startup/win_start_bash.bat` is a script that I have a windows task start after
 login to start powershell and cd into my projects directory.

`add_file_extensions.py` concatenates the user-given extension to each file
in the given folder. Useful for when there's lots of media files made on linux
w/o file name extension which need file name extension in windows.

`alphabet_positive_closure.py` given any set of symbols, generate the
alphabet positive closure (+) set of the alphabet of symbols. (Useful in
formal language and automata).
e.g.: `$ python alphabet_positive_closure.py --max-length 4
--output-file out.txt a b c`

`anti_afk.py` prevents player from being marked as afk in a video game by
moving the character forward and backward (`w` and `s` key presses) keys.

`bytes_to_image.py` converts the bytes located in a text file to an image. It
was only tested with the bytes of a PNG image.

`count_lines.py` counts the number of files given the extension of the files and
the total number of lines between all the files. Useful for checking how many
lines and files were used in some programming project.

`file_to_bytes.py` saves the bytes of a file to a text file.

`images_to_pdf.py` takes a folder containing images and puts them all in a
single pdf sorted by the number in the filename of each image.

`rename_file_extensions.py` replaces the file extensions of each file in a given
folder with desired replacement.

`replace_text_in_files.py` replaces each search_text found in each file in the
desired folder with replace_text (params passed through cli).

`resize_images.py` resizes each image in a folder to a given width or height
while maintaining the original aspect ratio (makes backup copy by default).
Eventually this is intended to update annotations which contain
info on bounding boxes for the image additionally.

`screenshot_book_pages.py` takes a screenshot then press right arrow key to
go to next page. Variables are hard coded atm.

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

#### Dependencies

- `DeleteImgurDNE/` and `GetMediaFiles/` require
[MediaInfo installer](https://mediaarea.net/en/MediaInfo/Download)
- other scripts may use **tkinter**, **wx**, or **Qt** GUI modules which
may require external downloads of their own

#### Modules

- [check requirements.txt](https://github.com/jtara1/MiscScripts/blob/master/requirements.txt)

### Install

```
git clone https://github.com/jtara1/MiscScripts.git && cd MiscScripts
pip install -r requirements.txt
```

### Usage

Depends on which script you're using. Most of the scripts are using
click module for cli so you could just run it with `--help` and check the
help and cli info in console

e.g.:
`python add_file_extensions.py --help`

returns
```
j@j-pc ~/_Github-Projects/MiscScripts $ python3.5 add_file_extensions.py --help
Usage: add_file_extensions.py [OPTIONS] FILE_PATH EXTENSION

Options:
  -r      Enable op recursively
  --help  Show this message and exit.

```
