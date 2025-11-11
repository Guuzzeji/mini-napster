from tinytag import TinyTag
import hashlib
import os
import math
import base64

# compress file and save into chunks in folder 'chunks' -> "chunks/file_name/chunk_index.chunk"

from napster.core.file_manager.folder_struct import create_base_folder
from napster.core.constants import MESSAGE_SIZE, BASE_EVERYTHING_FOLDER


CHUNK_FOLDER_BASE = BASE_EVERYTHING_FOLDER + "/sharing/chunks"

class Mp3File:
    def __init__(self, full_file_path: str):
        self.file_path = full_file_path
        self.name = os.path.basename(full_file_path)
        self.tinytag = TinyTag.get(full_file_path)
        
        with open(full_file_path, 'rb') as f:
            data_raw = f.read()
            self.checksum = str(hashlib.md5(data_raw).hexdigest())

        # File info
        self.file_name = os.path.basename(full_file_path)
        self.duration = self.tinytag.duration
        self.size = os.path.getsize(full_file_path)
        self.album = self.tinytag.album[0] if self.tinytag.album else "unknown"
        self.title = self.tinytag.title[0] if self.tinytag.title else "unknown"
        self.artist = self.tinytag.artist[0] if self.tinytag.artist else "unknown"
        self.year = self.tinytag.year[0] if self.tinytag.year else 0
        self.total_chunks = math.ceil(self.size / MESSAGE_SIZE)

    def __create_chunks(self):
        with open(self.file_path, 'rb') as f:
            data = f.read()
            for i in range(self.total_chunks):
                start = i * MESSAGE_SIZE
                end = start + MESSAGE_SIZE
                chunk_data = data[start:end]
                with open(CHUNK_FOLDER_BASE + "/" + self.name + "/" + str(i) + ".chunk", "wb") as f:
                    f.write(base64.b64encode(chunk_data))
    
    def __chunk_folder_exist(self):
        create_base_folder()
        if not os.path.exists(CHUNK_FOLDER_BASE + "/" + self.name):
            os.makedirs(CHUNK_FOLDER_BASE + "/" + self.name)
            self.__create_chunks()
        else:
            for i in range(self.total_chunks):
                if not os.path.exists(CHUNK_FOLDER_BASE + "/" + self.name + "/" + str(i) + ".chunk"):
                    self.__create_chunks()

    def get_chunk(self, index: int) -> str:
        self.__chunk_folder_exist()
        with open(CHUNK_FOLDER_BASE + "/" + self.name + "/" + str(index) + ".chunk", "r") as f:
            return f.read()

