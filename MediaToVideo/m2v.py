import fire
import os
import sys
import time
from moviepy.editor import *
from pprint import pprint

# lazy way to import submodule whose path is in ../GetMediaFiles relative to
# the file path of this file (__file__)
sys.path.append(os.path.abspath(
    os.path.join(
        os.path.abspath(__file__),
        '../..')))
from GetMediaFiles.get_media_files import GetMediaFiles
from MediaToVideo.serialization import RenderDatum, Serialization
from MediaToVideo.heap import Heap


class MediaToVideo:
    def __init__(
            self, src_path=os.path.dirname(os.path.abspath(__file__)),
            sort='st_ctime', sort_reverse=False, interval_duration=8,
            audio_index=0, audio_folder=None,
            renders_heap_file_path=os.path.join(os.path.dirname(__file__),
                                                'renders_heap.bin')):
        """
        Description:
            Given a directory (path), get media files in path, convert &
            concatenate into clips where the duration of each is 
            interval_duration or the duration of the src vid, 
            until max_duration is reached.
        
        Parameters:
            src_path: path containing sources of media files to use in video
            sort: value from os.stat(...) func, viable values: 
                https://docs.python.org/3/library/os.html#os.stat_result
            sort_reverse: Reverse after sorting; Default sorts from least to
                greatest (oldest to newest)
            interval_duration: duration of each image shown in the video
            # max_duration: total length (in seconds) of the video
            audio_index: The index used to choose the audio file from the 
                sorted list of audio_files in the src_path for the final 
                render
            audio_folder: only search for songs to use in the video in this
                folder, otherwise, search for songs in src_path
            renders_heap_file_path: file path of the renders heap that keeps
                track of the information of each rendered video
        """
        # source media to be used in final video is in this path
        self.src_path = os.path.abspath(src_path)

        # output files stored here
        self.out_path = os.path.join(self.src_path, 'output')
        Serialization.make_paths_for_file(self.out_path, is_file=False)

        # duration of each media file in video
        self.interval_duration = interval_duration
        # maximum duration allowed - determined by length of audio file
        self.max_duration = None

        self.owidth = 1920  # output width
        self.oheight = 1080  # output height

        # Get list of media files with certain extension from path (sorted)
        self.src_files = GetMediaFiles(self.src_path)
        # list of files paths for each diff media type
        self.image_files = self.src_files.get_all(
            sort=sort,
            sort_reverse=sort_reverse,
            track_types=['Image'])
        self.video_files = self.src_files.get_all(
            sort=sort,
            sort_reverse=sort_reverse,
            track_types=['Video'])
        self.sound_files = self.src_files.get_all(
            path=os.path.abspath(audio_folder)
            if audio_folder else self.src_path,
            sort=sort,
            sort_reverse=sort_reverse,
            track_types=['Audio']
        )
        print('songs found: ')
        self.src_files.print_files(self.sound_files)

        # files that can be used in the final rendered video
        self.media_files = self.image_files + self.video_files
        print('media files that can be used from src files:')  # debug
        self.src_files.print_files(self.media_files)  # debug

        self.vid_time = 0  # time a clip is placed in the timeline of final vid
        self.audio_index = audio_index

        self.renders_heap = Heap(file_path=renders_heap_file_path)
        self.renders_heap.deserialize()  # try to load from file
        if self.renders_heap.peek() is not None:
            pprint(dict(self.renders_heap.peek()), width=100)  # debug

        self.image_files_range = [0, 0]
        self.video_files_range = [0, 0]

    def render(self, continuous=False, resume=True, store_info=True):
        """ The user using the API should call this method to render the images
        and videos from the provided path as a video based on the length of
        the audio file used in self._get_audio_file().
        :param continuous: continuously render a video with the media available
        :param resume: load data to resume 
        :param store_info: Stores information of the render after it's done
        """
        if continuous:
            while True:
                try:
                    self._render(resume, store_info)
                except (KeyboardInterrupt, IndexError) as e:
                    print("{}: {}".format(type(e).__name__, e.args))
                    break
        else:
            self._render(resume, store_info)

    def _render(self, resume, store_info):
        """Render a single video"""
        datum = self.renders_heap.peek()

        if resume and datum is not None:
            self.audio_index, \
                self.image_files_range, \
                self.video_files_range = datum.get_next()

        # find the audio clip we're using to determine how long this rendered
        # video will be
        audio_clip = self._get_audio_clip()
        self.max_duration = audio_clip.duration

        # render the thing with all the media
        render_file_path = \
            self._composite_clips(self._get_clips(), audio_clip=audio_clip)

        if store_info and resume:
            data_file = os.path.join(os.path.dirname(render_file_path),
                                     'datum.json')
            datum = RenderDatum(
                    data_file=data_file, main_key=render_file_path,
                    date_created=os.stat(render_file_path).st_ctime,
                    images=self._image_files_used(),
                    videos=self._video_files_used(),
                    audio=self.sound_files[self.audio_index],
                    audio_index=self.audio_index,
                    images_range=self.image_files_range,
                    videos_range=self.video_files_range,
                    finished_render=True, uploaded_to=[]
                    )
            pprint(dict(datum), width=100)  # debug
            self.renders_heap.push(datum)
            self.renders_heap.serialize()

    def _get_clips(self):
        """ Get list of Clip objects of videos & images """
        return self._get_image_clips(self.image_files_range[1]) + \
            self._get_video_clips(self.video_files_range[1])

    def _get_image_clips(self, image_index=0):
        """ Creates moviepy clips for images & returns a list of them """
        transition_t = 0.3
        clips = []
        last_index = image_index
        for i, clip_data in enumerate(self.image_files[image_index:],
                                      start=image_index):
            last_index = i
            if self.vid_time < self.max_duration:
                clips.append(
                    ImageClip(clip_data[0], duration=self.interval_duration)
                    .set_start(self.vid_time)
                    .set_pos('center')
                    .crossfadein(transition_t)
                    .resize(self._fit_img(
                        clip_data[1]['Image']['size'][0],
                        clip_data[1]['Image']['size'][1]))
                    )
                self.vid_time += self.interval_duration
            else:
                # keep the index pointing to the index of the last media
                # file used
                # if i + 1 == len(self.video_files):
                #     i -= 1
                break

        self.image_files_range = [image_index, last_index]
        return clips

    def _get_video_clips(self, video_index=0):
        """ Creates moviepy clips for video & returns a list of them """
        transition_t = 0.3
        clips = []
        # i = 0
        last_index = video_index
        for i, clip_data in enumerate(self.video_files[video_index:],
                                      start=video_index):
            last_index = i
            if self.vid_time < self.max_duration:
                src_clip_duration = float(
                    clip_data[1]['Video']['duration']) / 1000
                clips.append(
                    VideoFileClip(clip_data[0], audio=True)
                    .set_start(self.vid_time)
                    .set_pos('center')
                    .crossfadein(transition_t)
                    .set_duration(src_clip_duration)
                    .volumex(1)
                    .set_fps(30)
                    .resize(self._fit_img(
                        clip_data[1]['Video']['size'][0],
                        clip_data[1]['Video']['size'][1]))
                    )
                self.vid_time += src_clip_duration
            else:
                # keep the index pointing to the index of the last media
                # file used
                # if i + 1 == len(self.video_files):
                #     i -= 1
                break

        self.video_files_range = [video_index, last_index]
        return clips

    def _get_audio_clip(self):
        """ Make audio clip from one of the files found in the main directory
        given
        """
        try:
            return AudioFileClip(self.sound_files[self.audio_index][0])\
                .set_start(0)\
                .volumex(1)
        except IndexError:
            raise IndexError("No more audio files available")

    def _composite_clips(self, clips, ofname='output', audio_clip=None):
        """ Renders and saves video made of clips from self._get_clips(...) 
        :returns opath: output_path of video file rendered 
        """
        if len(clips) == 0:
            raise IndexError("No more images or videos available")

        video = CompositeVideoClip(clips, size=(self.owidth, self.oheight))

        # combine audio if audio was already found in video
        if video.audio is not None:
            audio_clip = CompositeAudioClip([video.audio, audio_clip])

        video.audio = audio_clip

        opath = os.path.join(self.out_path, str(int(time.time())) + '.mp4')
        # pcm_s16le
        # libvorbis
        video.write_videofile(opath, fps=30,)
        return opath

    def _concatenate_clips(self, clips, ofname='output', audio_clip=None):
        """ Deprecated
        Takes list of VideoFileClip objects & concatenates them to make 
        one video. 
        """
        video = concatenate_videoclips(clips, transition=None, bg_color=None)
        video.set_audio(audio_clip)

        opath = os.path.join(self.out_path, str(int(time.time())) + '.mp4')
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
        w2, h2, = None, None
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

    def _image_files_used(self):
        """Should only be called after self._get_image_files() is called"""
        return self.image_files[
            self.image_files_range[0]:self.image_files_range[1]]

    def _video_files_used(self):
        """Should only be called after self._get_video_files() is called"""
        return self.video_files[
            self.video_files_range[0]:self.video_files_range[1]]


if __name__ == '__main__':
    fire.Fire(MediaToVideo)
