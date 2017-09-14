# MediaToVideo

Convert your images and videos into videos.

Each media file will have a duration of 4 seconds by default & videos have their audio disabled.

**work in progress**



### Issues

* GetMedia.get_all(...) will raise an Exception if there's a file containing an odd character such as '/'. (e.g.: Exception raised if file "my/image.jpg" is encountered)

    * glob.glob(...) converts '/' to some codes or different type of codec




### Bugs

* when resizing moviepy Clip object, an error stating tostring() function is no longer supported
is shown, to **fix**, go to .../python2.7/dist-packages/moviepy/video/fx/resize.py and replace
tostring with tobytes on line 32

* image files with transparency as a border may be resized to the wrong size (problem with pymediainfo possibly)



## Requirements

* Python 3

#### Modules

* moviepy

* pymediainfo

#### Dependencies

* [MediaInfo](https://mediaarea.net/en/MediaInfo/Download) (for pymediainfo module)



## Install

    git clone https://github.com/jtara1/MediaToVideo.git

    cd MediaToVideo

    git clone https://github.com/jtara1/GetMediaFiles.git



## m2v.MediaToFiles

Description: Takes media files from a folder, concatenates them, and writes them to a file using GetMedia class and moviepy module.

Input: list of files (paths) returns from GetMedia.get_all(...)

Output: None
