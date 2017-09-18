import json
import os


class GeneralSS:
    def __init__(self, data_file, main_key, **kwargs):
        """General Serialization Schema (like an abstract class)
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
        # make folders if needed for data file
        path = os.path.dirname(self.data_file)
        if not os.path.exists(path):
            os.makedirs(path)

        json.dump(obj=self.data, fp=open(self.data_file, 'w'))

    def deserialize_from_json(self):
        self.data = json.load(fp=open(self.data_file, 'r'))

    serialize = serialize_as_json  # alias
    deserialize = deserialize_from_json  # alias


class SerializationSchema(GeneralSS):
    def __init__(self, data_file, main_key, date_created, media, song,
                 media_indices, song_index, uploaded_to):
        """All the data needed to be saved for MediaToVideo. Not very elegant
        - just passing parameters as arguments for super constructor.
        """
        GeneralSS.__init__(self, data_file=data_file, main_key=main_key,
                           date_created=date_created, media=media, song=song,
                           media_indices=media_indices, song_index=song_index,
                           uploaded_to=uploaded_to)

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
        # path = os.path.join(path, 'ss.json')

        ss = SerializationSchema(
            data_file=path,
            main_key='video.mp4',
            date_created=time.time(),
            media=['somevid.mp4', 'pic.png', 'pic2.jpg'],
            song='great_song.opus',
            media_indices=[0, 2],
            song_index=0,
            uploaded_to=['yt/my_channel', 'vimeo/ch2']
        )
        ss.serialize()

    test()
