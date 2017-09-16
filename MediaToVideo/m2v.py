import os
import sys
import time
from moviepy.editor import *
import wavefile
import click

# lazy way to import submodule whose path is in ../GetMediaFiles relative to
# the file path of this file (__file__)
sys.path.append(os.path.abspath(
    os.path.join(
        os.path.abspath(__file__),
        '../..')))
from GetMediaFiles.get_media_files import GetMediaFiles


class MediaToVideo:
    def __init__(self, src_path=os.path.basename(os.path.abspath(__file__)),
                 file_types=None, sort='st_ctime',
                 interval_duration=4, max_duration=300):
        """
        Description:
            Given a directory (path), get media files in path, convert &
            concatenate into clips where the duration of each is 
            interval_duration, until max_duration is reached, 
            but not exceeded with optional audio.
        
        Parameters:
            src_path: path containing sources of media files to use in video
            sort: value from os.stat(...) func, viable values: 
                https://docs.python.org/3/library/os.html#os.stat_result
            interval_duration: duration of each image shown in the video
            max_duration: total length (in seconds) of the video
        """
        # source media to be used in final video is in this path
        self.src_path = os.path.abspath(src_path)

        # output files stored here
        self.out_path = os.path.join(self.src_path, 'output')
        if not os.path.isdir(self.out_path):
            os.makedirs(self.out_path)

        # duration of each media file in video
        self.interval_duration = interval_duration
        self.max_duration = max_duration  # maximum duration allowed

        # should be file path to audio file or None
        # self.audio_files = audio_files

        self.owidth = 1920  # output width
        self.oheight = 1080  # output height

        # Get list of media files with certain extension from path (sorted)
        self.src_files = GetMediaFiles(self.src_path)
        self.image_files = self.src_files.get_all(
            sort=sort,
            track_types=['Image'])
        self.video_files = self.src_files.get_all(
            sort=sort,
            track_types=['Video'])
        self.sound_files = self.src_files.get_all(
            sort=sort,
            track_types=['Audio']
        )
        print('songs found: ')
        self.src_files.print_files(self.sound_files)

        # files that can be used in the final rendered video
        self.media_files = self.image_files + self.video_files
        print('media files that can be used from src files:')  # debug
        self.src_files.print_files(self.media_files)  # debug

        self.vid_time = 0  # time a clip is placed in the timeline of final vid

    def render(self):
        """ The user using the API should call this method to render the images
        from the provided path as a video.
        """
        clips = self._get_clips()
        self._composite_clips(clips, audio_clip=self._get_audio_clips()[0])

        ### secondary functions for writing final vid file ####
        # self._write_clips(clips)
        # self._concatenate_clips(clips)

    def _get_clips(self):
        """ Get list of Clip objects of videos & images """
        int_t = self.interval_duration
        img_clips = self._get_image_clips()
        clips = img_clips + self._get_video_clips()
        return clips

    def _get_image_clips(self, start_t=0):
        """ Creates moviepy clips for images & returns a list of them """
        transition_t = 0.3
        clips = []
        for i, clip_data in enumerate(self.image_files):
            if self.vid_time < self.max_duration:
                clips.append(
                    ImageClip(clip_data[0], duration=self.interval_duration)
                    .set_start(self.vid_time)
                    .set_pos('center')
                    .crossfadein(transition_t)
                    .set_duration(self.interval_duration)
                    .resize(self._fit_img(
                        clip_data[1]['Image']['size'][0],
                        clip_data[1]['Image']['size'][1]))
                    )
                self.vid_time += self.interval_duration
        return clips

    def _get_video_clips(self, start_t=0):
        """ Creates moviepy clips for video & returns a list of them """
        transition_t = 0.3
        clips = []
        for i, clip_data in enumerate(self.video_files):
            if self.vid_time < self.max_duration:
                src_clip_duration = float(clip_data[1]['Video']['duration'])/1000
                clips.append(
                    VideoFileClip(clip_data[0], audio=True)
                    .set_start(self.vid_time)
                    .set_pos('center')
                    .crossfadein(transition_t)
                    .set_duration(src_clip_duration)
                    .volumex(0.5)
                    .set_fps(30)
                    .resize(self._fit_img(
                        clip_data[1]['Video']['size'][0],
                        clip_data[1]['Video']['size'][1]))
                    )
                self.vid_time += src_clip_duration
        return clips

    def _get_audio_clips(self):
        # returns the contents of the wav file as a double precision float array
        def wav_to_floats(filename='file1.wav'):
            w = wavefile.load(filename)
            return w[1][0]

        clips = []
        # for i, clip_data in enumerate(self.sound_files):
        # signal = wav_to_floats(clip_data[0])
        signal = wav_to_floats('/home/j/Temp/m2v_pics/song.wav')
        clips.append(
            AudioClip(make_frame=lambda t: signal[t], duration=self.vid_time)
            .set_start(0)
            # .set_duration(self.vid_time)
        )
        return clips

    def _composite_clips(self, clips, ofname='output', audio_clip=None):
        """ Renders and saves video made of clips from self.get_clips(...) """
        opath = os.path.join(self.out_path, str(int(time.time())) + '.mp4')
        width, height = self.owidth, self.oheight
        video = CompositeVideoClip(clips, size=(width, height))
        video.set_audio(audioclip=audio_clip)
        video.write_videofile(opath, fps=30)

    def _concatenate_clips(self, clips, ofname='output', audio_clip=None):
        """ Takes list of VideoFileClip objects & concatenates them to make 
        one video 
        """
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
        """ Get width & height to scale image to to fit self.owidth & 
        self.oheight 
        """
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
