# GetMediaFiles
Python class to return a list of local media files from a folder with metadata of the files

## Requirements

* Python 3

#### Modules

* pymediainfo

#### Dependencies

* [MediaInfo](https://mediaarea.net/en/MediaInfo/Download) (for pymediainfo module)

## Issues

* GetMedia.get_all(...) will raise an Exception if there's a file containing an odd character such as '/'. (e.g.: Exception raised if file "my/image.jpg" is encountered)

    * glob.glob(...) converts '/' to some codes or different type of codec

## GetMediaFiles.GetMediaFiles

Description: Returns list of files with data & file path of each file in its own list sorted by
creation/metadata change time (oldest to newest (ascending order)) by default

Input: path to media files

Output: list of lists each containing media info of each media file

#### Example/Usage

Suppose I have 2 image files, test2.jpg and test3.jpg, 1 text file, and 1 folder in the following path and

run the following code:

    from GetMediaFiles import GetMediaFiles

    path = '/home/j/Documents/_Github-Projects/MediaToVideo/temp-imgs'

    media = GetMediaFiles()

    files = media.get_all(path, track_types=['Image','Video'])

    media.print_files(files)


printed output:

    ['/home/j/Documents/_Github-Projects/MediaToVideo/temp-imgs/test2.jpg',
    {'Image':
        {'duration': None, 'format': 'JPEG', 'size': (1920, 1080)}},
    'Image',
    1473055449.7858396]
    ['/home/j/Documents/_Github-Projects/MediaToVideo/temp-imgs/test3.jpg',
    {'Image':
        {'duration': None, 'format': 'JPEG', 'size': (291, 1080)}},
    'Image',
    1473055449.921839]
