# misc_scripts
Various scripts I've found to be useful.

`delete_imgur_dne/delete_dne.py` takes an argument from command line to use
as folder to search for copies of the *imgur does not exist* image and deletes
them.

`DevOps/count_lines.py` counts the number of files given the extension of the files and
the total number of lines between all the files. Useful for checking how many
lines and files were used in some programming project.

`DevOps/create_and_push_next_tag.sh` creates and pushes the next git tag following the
MAJOR.MINOR.PATCH naming convention. Increments PATCH by default or MAJOR or MINOR
with --major or --minor cli args respectively.

`DevOps/create_python_gitignore.py` create or append a .gitignore file at location 
of `folder` containing the standard .gitignore for python
concatenated with the std .gitignore for IntelliJ IDEs (Pycharm) 
that are provided by github

`HTML/blk-bg.html` is a simple HTML file with a black background that I use
on my 2nd monitor so I don't have this glaring bright white thing to my side.

`MuchAssemblyRequired/` directory containing the ASM programs for the game MAR I made.

`PrepCenterScript/` a program that automated part of a previous job of mine using this
particular software.

`startup/` directory containing some scripts I run after I log in to my computer

`python_setup_py_template/setup.py` is my go to setup.py file I include in 
every python module I want
to distribute through `pip install git+https://github.com/jtara/my_repo` or through
`pip install my_repo`  
It uses **setuptools_scm** which will use the version (tag) from git for the project 
to define the version within the setup.py.
In other words, you need to `git tag 0.1.0` (or whichever tag you want) and 
`git push --tags` before trying to install the module or 
upload it to be installed.
My setup.py will also **infer the name of the module** to be the  
same name as the parent directory (github project name)
so the directory should look something like this

my_module

- images
- my_module
    - \_\_main\_\_.py
- setup.py
- setup.cfg
- README.md

`WinCMDTools/` contains scripts for adding hotkeys to make cmd or powershell
usage more similar to default hotkeys for konsole on linux. Also includes 
scripts to switch to using python 2 or 3 since you'd need to change your
environment variables then open new powershell everytime otherwise.

`add_file_extensions.py` concatenates the user-given extension to each file
in the given folder. Useful for when there's lots of media files made on linux
w/o file name extension which need file name extension in windows.

`alphabet_positive_closure.py` given any set of symbols, generate the
alphabet positive closure (+) set of the alphabet of symbols. (Useful in
formal language and automata).
e.g.: `$ python alphabet_positive_closure.py --max-length 4
--output-file out.txt a b c`

`add_ssh_key_for_github.sh` creates a new SSH key and copies it to the clip
board using xclip. Requires 1st command line argument to be email associated
with SSH key.

`anti_afk.py` prevents player from being marked as afk in a video game by
moving the character forward and backward (`w` and `s` key presses) keys.

`bernoulli_trials.py` calculates the probability of n successes after so many
trials or attempts for a given probability of success of a single trial.
Better version: https://jtara1.github.io/bernoulli.html

`bytes_to_image.py` converts the bytes located in a text file to an image. It
was only tested with the bytes of a PNG image.

`file_to_bytes.py` saves the bytes of a file to a text file.

`images_to_pdf.py` takes a folder containing images and puts them all in a
single pdf sorted by the number in the filename of each image.

`formula_to_jflap_grammar.py` convert a libre office forumla into an XML .jff file accepted by JFLAP
uses \"|\" (literal: "|") as separator. and literal: newline as newline
separator. Removes all whitespace (" "). Uses literal -> as production rule
symbol.

`images_to_pdf.py` saves each image in a directory on a page of a newly created PDF

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

`surround_with_quotes_and_append_commas.sh` surrounds each line in the given 
file with quotes and appends a comma to it; takes 1 positional argument, input file

`tol_macros.py` macros made for a particular game, some of which can be used in
other games or have base class, Action, extended for use elsewhere. Includes:
auto item pickup (presses f), auto dirt digger (clicks and moves mouse),
and auto walker (holds w). All of these macros are assigned to the hotkeys
(`F2`, `F3`, `F4`) respectively.

`UpdateOSTime.cs` is a program that fetches the time from a website then updates
the OS system time with the fetched time (for Windows OS).

`zip_folders.py` zips the content of each folder in a directory into their own
zip file. Useful for making folders (chapters) of a comic
readable by apps such as ComicRack.

### Requirements

Depends on the script you're running.

Using languages: Python, Bash, Batch, C#, AutoIt3, and others

#### Dependencies

- `delete_imgur_dne/` require
[MediaInfo installer](https://mediaarea.net/en/MediaInfo/Download)
- other scripts may use **tkinter**, **wx**, or **Qt** GUI modules which
may require external downloads of their own

#### Python Modules

- [check requirements.txt](https://github.com/jtara1/misc_scripts/blob/master/requirements.txt)

### Install

```
git clone https://github.com/jtara1/misc_scripts.git && cd misc_scripts
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
j@j-pc ~/_Github-Projects/misc_scripts $ python3.5 add_file_extensions.py --help
Usage: add_file_extensions.py [OPTIONS] FILE_PATH EXTENSION

Options:
  -r      Enable op recursively
  --help  Show this message and exit.

```
