import socket
import multiprocessing

from kombu import Connection

class Queue(object):
    def __init__(self, url=None, hostname=None, userid=None, password=None, queue_name="basic_queue", serializer="pickle", compression=None):
        # current_queue
        self.is_local = True
        self.localized = None
        self.distributed = None
        if (hostname is None or userid is None or password is None) and url is None:
            self.localized = multiprocessing.Queue()
        else:
            self.is_local = False
            self.serializer = serializer
            self.compression = compression
            self.connection = Connection(url, heartbeat=5)
            self.distributed = self.connection.SimpleQueue(queue_name)
    
    def __len__(self):
        return self.qsize()

    def join(self):
        pass
    
    def qsize(self) -> int:
        if self.is_local == True:
            return self.localized.qsize()
        return self.distributed.qsize()

    def clear_queue(self):
        if self.is_local:
            while not self.empty():
                self.get_nowait()
        else:
            self.distributed.clear()
    def empty(self) -> bool:
        if self.is_local:
            return self.localized.empty()
        else:
            current_size = self.distributed.qsize()
            if current_size == 0:
                return True
            return False

    def put(self, item, block=True, timeout=None):
        if self.is_local == True:
            self.localized.put(item, block=block, timeout=timeout)
        else:
            self.distributed.put(item, serializer=self.serializer,compression=self.compression)

    
    def get(self, block=True, timeout=None):
        if self.is_local == True:
            return self.localized.get(block=block, timeout=timeout)
        else:
            return self.distributed.get()

    def put_nowait(self, item):
        if self.is_local == True:
            self.localized.put_nowait(item)
        else:
            self.distributed.put_nowait(item, serializer=self.serializer,compression=self.compression)

    def get_nowait(self):
        if self.is_local == True:
            return self.localized.get_nowait()
        else:
            return self.distributed.get_nowait()
    
    def close(self):
        """ Closes the distributed queue if it's distributed with redis or any other library. """
        if self.is_local == False:
            self.distributed.close()