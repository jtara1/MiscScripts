import re
import os
import PIL.Image
import glob
# import itertools # itertools.izip(...) is Python 2 only
from operator import attrgetter, itemgetter
from pymediainfo import MediaInfo


class GetMediaFiles:
    def __init__(self, path=os.path.basename(os.path.abspath(__file__)),
                 track_types=None):
        """
        Returns sorted list of files from param path
        """
        self.path = path
        # Any file with one of the follow MediaInfo "tracks" will be returned
        self.track_types = track_types if track_types \
            else ['Image', 'Video', 'Audio']

    def get_all(self, path=None, recursive=False,
                track_types=None, sort='st_ctime', sort_reverse=False,
                start_i=0, limit_i=-1, remove_audio=False):
        """
        Utilize pymediainfo to get media tracks, size, duration, & format
        Returns a list of lists with file info (see readme.md for more details)

        Arguments:
            path: folder path containing media files
            recursive: get files inside of folders inside of folders ...
            track_types: list containg 'Image' or 'Video' or 'Audio' or 
                'General'
            sort: os.stat(path) returns a tuple, access value 
                from that tuple with sort param
            sort_reverse: Reverse after sorting
            start_i: start index to begin getting files at
            limit_i: end index to stop getting files before
            remove_audio: removes files that are audio only if True (redundant)
        """
        path = path if path else self.path
        track_types = track_types if track_types else self.track_types
        # debug
        print('[GetMedia] Getting files with %s in %s' % (track_types, path))

        # get all files (and directories) in path
        all_files = glob.glob(os.path.join(path, '**'), recursive=recursive)
        limit_i = len(all_files) if limit_i == -1 else limit_i
        all_files = all_files[start_i:limit_i]

        # reorganize so we can append data with each file
        all_files = list([f] for f in all_files)

        # e.g.: '(Audio|Video|Image)'
        media_types = '|'.join(track_types)
        media_type_regex = re.compile('(' + media_types + ')')

        # Note: every file seems to have at least one track ('General')
        remove_indices = []
        for f in all_files:
            # print('f: ' + str(f))
            # print('----')

            # get Media Info of current file
            info = MediaInfo.parse(f[0])

            # append track info if it matches that given by track_types
            f.append({track.track_type: {
                        'size': (track.width, track.height),
                        'format': track.format,
                        'duration': track.duration
                        }
                        for track in info.tracks
                        if re.match(media_type_regex, str(track.track_type))
                    })

            # remove if folder, non media, or audio
            if (len(f) == 1 or f[1] == {}) or \
                    (remove_audio and 'Audio' in f[1].keys() and len(f) == 2):

                remove_indices.append(all_files.index(f))
                continue

            # this isn't really necessary to do this
            # get easy to read and access media
            # type at index 2 of each file in files (list)
            # temp_list = list(k for k, v in f[1].items())
            # media_type = '-'.join(temp_list)
            # f.append(media_type)

        # remove unwanted files in files list
        for count, index in enumerate(remove_indices):
            all_files.remove(all_files[index - count])

        # return if we don't care about sorting by creation date or
        # attaching creation date data
        if not sort:
            return all_files

        # attach stats (mutates files) then sort files
        self.attach_stats(all_files, stat_type=sort)
        all_files = sorted(all_files, key=itemgetter(-1), reverse=sort_reverse)

        return all_files

    def get_all_old(self, path=None, file_types=None, sort='st_ctime',
                    start_i=None, limit_i=None):
        """
        Returns list of files in path (or self.path) with an extension from
        the list from file_types, and sorts files by sort param given
        BUG: FAILS TO RETURN MEDIA FILE(S) WITHOUT ANY FILE EXTENSION
        """
        path = path if path else self.path
        file_types = file_types if file_types else [
            '.png', '.jpe?g', '.webm', '.mp4', '.gif'
        ]
        # debug
        print('[GetMedia] Getting files with %s in %s' % (file_types, path))

        ftypes = '|'.join(file_types)  # format for regex match group
        file_match_regex = re.compile('.*?(' + ftypes + ')')
        files = glob.glob(path + '/*.*')  # get all files in path
        files = [[f] for f in files if re.match(file_match_regex, f)]

        # attach stats then sort files
        files = sorted(self.attach_stats(files, stat_type=sort),
                       key=itemgetter(1))
        # files = self.attach_size(files)

        return files

    def get_stats(self, files, stat_type='st_ctime'):
        """ valid stat_type params https://docs.python.org/3/library/os.html#os.stat_result """
        stats = []
        return list(getattr(os.stat(f[0]), stat_type) for f in files)
        # for f in files:
        #     stats.append(getattr(os.stat(f[0]), stat_type))
        # return stats

    def attach_stats(self, files, stat_type='st_ctime'):
        """ mutate files with os.stat(path).stat_type """
        stats = self.get_stats(files, stat_type=stat_type)
        files = list(f.append(stat) for f, stat in zip(files, stats))

    def print_files(self, files):
        for f in files:
            print(f)


if __name__ == "__main__":
    # # tests
    import time
    import click
    init_t = time.time()

    @click.command()
    @click.argument('folder')
    @click.option('-r', '--recursive', default=False)
    @click.option('-t', '--track-types', default=['Image', 'Vide', 'Audio'])
    def main(folder, recursive, track_types):
        media = GetMediaFiles(path=folder, track_types=track_types)
        files = media.get_all(recursive=recursive, sort='st_ctime', start_i=0, limit_i=-1)
        print('----------------------------')
        # media.print_files(files)
        print('%s files found.' % len(files))
        print('%i seconds passed' % int(time.time() - init_t))
        media.print_files(files)

        # stats = media.get_stats(files)

    main()
