from MediaToVideo.serialization import Serialization
from heapq import *
import os


class Heap:
    def __init__(self, init_data=None,
                 file_path=os.path.join(os.getcwd(), 'heap_data.bin')):
        """
        Wrapper for python heapq functions
        :param init_data: Initial data to store in heap
        :param file_path: path of file that stores this heaps serialized data
        """
        self.heap = heapify(init_data) if init_data else []
        self.file_path = file_path

    def push(self, datum):
        heappush(self.heap, datum)

    def pop(self):
        return heappop(self.heap)

    def serialize(self):
        Serialization.serialize_as_binary(data=self.heap,
                                          data_file=self.file_path)

    def deserialize(self):
        self.heap = Serialization.deserialize_from_binary(self.file_path)


if __name__ == '__main__':
    def test():
        h = Heap()
        h.push(2)
        h.push(3)
        h.push(0)
        print(h.pop())

        h.serialize()
        h.deserialize()
        print(h.pop())

    test()
