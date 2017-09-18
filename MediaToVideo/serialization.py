import json
import os
import dill


class Serialization:
    @staticmethod
    def make_paths_for_file(file_path):
        """Make folders if needed for data file"""
        path = os.path.dirname(file_path)
        if not os.path.exists(path):
            os.makedirs(path)

    @staticmethod
    def serialize_as_json(data, data_file):
        Serialization.make_paths_for_file(data_file)
        json.dump(obj=data, fp=open(data_file, 'w'))

    @staticmethod
    def deserialize_from_json(data_file):
        return json.load(fp=open(data_file, 'r'))

    @staticmethod
    def serialize_as_binary(data, data_file):
        Serialization.make_paths_for_file(data_file)
        dill.dump(obj=data, file=open(data_file, 'wb'))

    @staticmethod
    def deserialize_from_binary(data_file):
        return dill.load(file=open(data_file, 'rb'))


class GeneralSchema:
    def __init__(self, data_file, main_key, **kwargs):
        """General Schema (like an abstract class)
        Create something like this, e.g.:
        {'video.mp4': {
            'date': '01-01-2017',
            'media': ['pic1.jpg', 'pic2.png', 'vid.mp4']
            }
        }
        end e.g. Where 'video.mp4' is the main key and its value are kwargs
        """
        self.data = {}
        self.main_key = main_key
        self.data[main_key] = {}

        self.data[main_key].update(kwargs)
        self.data_file = os.path.abspath(data_file)

    def serialize_as_json(self):
        Serialization.serialize_as_json(self.data, self.data_file)

    def deserialize_from_json(self):
        self.data = Serialization.deserialize_from_json(self.data_file)

    serialize = serialize_as_json  # alias
    deserialize = deserialize_from_json  # alias


class RenderDatum(GeneralSchema):
    def __init__(self, data_file, main_key, date_created, media, song,
                 media_indices, song_index, finished_render, uploaded_to):
        """All the data needed to be saved for a MediaToVideo render. 
        Not very elegant - just passing parameters as arguments 
        for the super constructor.
        """
        GeneralSchema.__init__(
            self, data_file=data_file, main_key=main_key,
            date_created=date_created, media=media, song=song,
            media_indices=media_indices, song_index=song_index,
            finished_render=finished_render, uploaded_to=uploaded_to)

    def __lt__(self, other):
        """Invert `<` operator so heapq from std lib becomes max_heap
        when used with objs of this class
        """
        return self.data[self.main_key]['date_created'] >= \
            other.data[self.main_key]['date_created']


if __name__ == '__main__':
    def test():
        import time
        path = '/home/j/Temp/ss_testing/ss.json'

        ss = RenderDatum(
            data_file=path,
            main_key='video.mp4',
            date_created=time.time(),
            media=['somevid.mp4', 'pic.png', 'pic2.jpg'],
            song='great_song.opus',
            media_indices=[0, 2],
            song_index=0,
            finished_render=True,
            uploaded_to=['yt/my_channel', 'vimeo/ch2']
        )
        ss.serialize()
        ss.deserialize()

    test()
