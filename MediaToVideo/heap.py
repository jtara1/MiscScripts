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
        """Add datum to the heap"""
        heappush(self.heap, datum)

    def pop(self):
        """Get top (smallest) value removing it in the process"""
        try:
            return heappop(self.heap)
        except IndexError:
            return None  # heap was empty

    def peek(self):
        """Get top (smallest) value without removing it"""
        try:
            return self.heap[0]
        except (IndexError, TypeError):
            return None  # heap was empty

    def serialize(self):
        """Save heap to a file"""
        Serialization.serialize_as_binary(data=self.heap,
                                          data_file=self.file_path)

    def deserialize(self):
        """Try to load heap from file; prints a warning if file not found"""
        try:
            self.heap = Serialization.deserialize_from_binary(self.file_path)
        except (FileNotFoundError, FileExistsError):
            print("[Heap] Warning: attempted to deserialize from file that did"
                  " not exist.")

    def __repr__(self):
        return repr(list(self.heap))

    def __iter__(self):
        # if self.heap is None:
        #     return 'None'
        for item in self.heap:
            yield item


if __name__ == '__main__':
    def test():
        h = Heap()
        h.push(2)
        h.push(3)
        h.push(0)
        print(h)
        print(list(h))
        print(h.pop())

        h.serialize()
        h.deserialize()
        print(h.pop())

    test()
