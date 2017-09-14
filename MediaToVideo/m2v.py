import os
import sys
import time
from moviepy.editor import *
import click

# lazy way to import submodule whose path is in ../GetMediaFiles relative to
# the file path of this file (__file__)
sys.path.append(os.path.join(os.path.dirname(__file__), '../GetMediaFiles'))
from GetMediaFiles.get_media_files import GetMediaFiles


class MediaToVideo:
    def __init__(self, path=None, file_types=None, sort='st_ctime',
                 interval_duration=4, max_duration=300):
        """
        Description:
            Given a directory (path), get media files in path, convert &
            concatenate into clips where the duration of each is 
            interval_duration, until max_duration is reached, 
            but not exceeded with optional audio.
        
        Parameters:
            sort: value from os.stat(...) func, viable values: 
                https://docs.python.org/3/library/os.html#os.stat_result
            interval_duration: duration of each image shown in the video
            max_duration: total length (in seconds) of the video
        """
        # paths
        self.path = os.path.abspath(path) if path \
            else os.path.basename(os.path.abspath(__file__))
        # self.temp_path = os.path.join(self.path, 'temp-imgs')
        # if not os.path.isdir(self.temp_path):
        #     os.mkdir(self.temp_path)
        self.out_path = os.path.join(self.path, 'output') # output files stored here
        if not os.path.isdir(self.out_path):
            os.mkdir(self.out_path)

        self.interval_duration = interval_duration # duration of each media file in video
        self.max_duration = max_duration # maximum duration allowed
        # self.audio_files = audio_files # should be file path to audio file or None
        self.owidth = 1920  # output width
        self.oheight = 1080  # output height

        # Get list of media files with certain extension from path (sorted)
        track_types_image = ['Image']
        track_types_vid_audio = ['Video']
        self.media = GetMediaFiles(self.path)
        self.files_image = self.media.get_all(sort=sort, track_types=['Image'])
        self.files_video = self.media.get_all(sort=sort, track_types=['Video', 'Audio'])
        self.files = self.files_image + self.files_video
        print('files:')  # debug
        self.media.print_files(self.files)  # debug

    def render(self):
        """ The user using the API should call this method to render the images
        from the provided path as a video.
        """
        clips = self._get_clips()
        self._composite_clips(clips)

        ### secondary functions for writing final vid file ####
        # self._write_clips(clips)
        # self._concatenate_clips(clips)

    def _get_clips(self):
        """ Get list of Clip objects of videos & images """
        int_t = self.interval_duration
        img_clips = self._get_image_clips()
        clips = img_clips + self._get_video_clips(start_t=len(img_clips)*int_t)
        return clips

    def _get_image_clips(self, start_t=0):
        """ Creates moviepy clips for images & returns a list of them """
        files = self.files_image
        int_t = self.interval_duration
        max_t = self.max_duration
        transition_t = 0.3
        # path = self.path if not path else path
        clips = [ImageClip(clip_data[0], duration=self.interval_duration)
                .set_start(int_t * i + start_t).set_pos('center')
                .crossfadein(transition_t).set_duration(int_t)
                .resize(self._fit_img(clip_data[1]['Image']['size'][0], clip_data[1]['Image']['size'][1]))
                for i, clip_data in enumerate(files)
                if int_t*i < max_t]
        return clips

    def _get_video_clips(self, start_t=0):
        """ Creates moviepy clips for video & returns a list of them """
        files = self.files_video
        int_t = self.interval_duration #
        max_t = self.max_duration
        transition_t = 0.3
        # path = self.path if not path else path
        clips = [VideoFileClip(clip_data[0], audio=False)
                .set_start(int_t * i + start_t).set_pos('center')
                .crossfadein(transition_t).set_duration(int_t)
                .volumex(0.5).set_fps(30)
                .resize(self._fit_img(clip_data[1]['Video']['size'][0], clip_data[1]['Video']['size'][1]))
                for i, clip_data in enumerate(files)
                if int_t*i < max_t]
        return clips

    def _composite_clips(self, clips, ofname='output', audio_clip=None):
        """ Working option for creating video made of clips from get_clips(...) 
        """
        opath = os.path.join(self.out_path, str(int(time.time())) + '.mp4')
        width, height = self.owidth, self.oheight
        int_t = self.interval_duration
        max_t = self.max_duration
        video = CompositeVideoClip(clips, size=(width, height))
        video.write_videofile(opath, fps=30)

    def _concatenate_clips(self, clips, ofname='output', audio_clip=None):
        """ Takes list of VideoFileClip objects & concatenates them to make one video """
        opath = os.path.join(self.out_path, str(int(time.time())) + '.mp4')
        width, height = self.owidth, self.oheight
        video = concatenate(clips, transition=None, bg_color=None)
        video.write_videofile(opath, fps=30)

    def _write_clips(self, clips, ofnames=[]):
        """ Create an .mp4 of each clip individually """
        opath = os.path.join(self.out_path, str(int(time.time())) + '.mp4')
        temp = [clip.write_videofile(opath[:-4] + str(i) + opath[-4:], fps=30)
                for i, clip in enumerate(clips)]
        return temp  # probably returns [None] * len(clips)

    def _fit_img(self, w, h):
        """ Get width & height to scale image to to fit self.owidth & self.oheight """
        # assumes self.owidth > self.oheight (most aspect ratios work that way)
        if w > h:
            w2 = self.owidth
            ratio = float(w2)/w
            h2 = ratio * h
        elif h >= w:
            h2 = self.oheight
            ratio = float(h2)/h
            w2 = ratio * w
        return w2, h2


@click.command()
@click.argument('folder')
def main(folder):
    m2v = MediaToVideo(folder)
    m2v.render()


if __name__ == '__main__':
    main()
