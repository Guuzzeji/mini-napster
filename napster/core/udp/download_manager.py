import base64
import shutil
import os
import threading
from datetime import datetime

from napster.core.file_manager.folder_struct import create_base_folder
from napster.core.constants import BASE_EVERYTHING_FOLDER

DOWNLOAD_FOLDER = BASE_EVERYTHING_FOLDER + "/downloads"
SAVED_FOLDER = BASE_EVERYTHING_FOLDER + "/mp3"

class DownloadManager:
    def __init__(self) -> None:
        self.manager = {}
        self.thread_lock = threading.Lock()

    def __create_download_folder(self, file_name: str):
        if os.path.exists(DOWNLOAD_FOLDER + "/" + file_name.replace(".mp3", "")) is False:
            create_base_folder()
            os.makedirs(DOWNLOAD_FOLDER + "/" + file_name.replace(".mp3", ""))

    def __create_save_folder(self):
        if os.path.exists(SAVED_FOLDER) is False:
            create_base_folder()
            os.makedirs(SAVED_FOLDER)

    def file_exists(self, file_name: str, uuid: str):
        return os.path.exists(DOWNLOAD_FOLDER + "/" + file_name.replace(".mp3", "")) or f"{uuid}||{file_name}" in self.manager

    def get_number_of_chunks_saved(self, file_name: str):
        if not os.path.exists(DOWNLOAD_FOLDER + "/" + file_name.replace(".mp3", "")):
            self.__create_download_folder(file_name)
            self.__create_save_folder()
            return -1
        return len(os.listdir(DOWNLOAD_FOLDER + "/" + file_name.replace(".mp3", "")))
    
    def get_total_number_of_chunks(self, file_name: str, uuid: str):
        with self.thread_lock:
            if f"{uuid}||{file_name}" not in self.manager:
                return None
            return self.manager[f"{uuid}||{file_name}"].get("total_chunks", None)

    def add_file_metadata(self, uuid: str, file_name: str, username, number_of_chunks: int, checksum: str, server: tuple):
        with self.thread_lock:
            self.manager[f"{uuid}||{file_name}"] = {
                "uuid": uuid,
                "file_name": file_name,
                "file_checksum": checksum,
                "username": username,
                "total_chunks": number_of_chunks,
                "downloaded_chunks": 0,
                "ip": server[0],
                "port": server[1],
                "last_blast": datetime.now(),
                "just_created": True
            }

    def add_chunk(self, uuid: str, file_name: str, checksum: int, chunk_index: int, base64_chunk: str):
        if self.file_exists(file_name, uuid) is False or f"{uuid}||{file_name}" not in self.manager:
            return

        if checksum != len(base64_chunk):
            # ("Checksum does not match", checksum, len(base64_chunk))
            return

        self.__create_download_folder(file_name)
        chunk_path = DOWNLOAD_FOLDER + "/" + file_name.replace(".mp3", "") + "/" + str(chunk_index) + ".chunk"

        # Check if chunk already exists to avoid double-counting
        chunk_already_exists = os.path.exists(chunk_path)

        with open(chunk_path, "w") as f:
            f.write(base64_chunk)

        # Only increment counter if this is a new chunk
        if not chunk_already_exists:
            with self.thread_lock:
                self.manager[f"{uuid}||{file_name}"]["downloaded_chunks"] += 1

    def is_file_complete(self, file_name: str, uuid: str) -> bool:
        number_of_chunks = self.get_number_of_chunks_saved(file_name)
        total_chunks = self.get_total_number_of_chunks(file_name, uuid)

        if number_of_chunks == -1:
            return False
        
        if total_chunks is None:
            return False

        return number_of_chunks == total_chunks

    def assemble_file(self, file_name: str, uuid: str) -> bool:
        file = []
        total_chunks = self.get_total_number_of_chunks(file_name, uuid)
        if total_chunks is None:
            return False

        for i in range(total_chunks):
            with open(DOWNLOAD_FOLDER + "/" + file_name.replace(".mp3", "") + "/" + str(i) + ".chunk", "r") as f:
                file.append(f.read())
        combined_data = b"".join([base64.b64decode(file[i]) for i in range(total_chunks)])

        self.__create_save_folder()
        with open(SAVED_FOLDER + "/" + file_name, "wb") as f:
            f.write(combined_data)

        self.remove_file(file_name, uuid)
        return True

    def remove_file(self, file_name: str, uuid: str):
        if os.path.exists(DOWNLOAD_FOLDER + "/" + file_name.replace(".mp3", "")):
            shutil.rmtree(DOWNLOAD_FOLDER + "/" + file_name.replace(".mp3", ""))

        with self.thread_lock:
            del self.manager[f"{uuid}||{file_name}"]

    def file_missing_chunks(self, file_name: str, uuid: str) -> list[int]:
        missing_chunks = []
        total_chunks = self.get_total_number_of_chunks(file_name, uuid)

        if total_chunks is None:
            return missing_chunks

        for i in range(total_chunks):
            if not os.path.exists(DOWNLOAD_FOLDER + "/" + file_name.replace(".mp3", "") + "/" + str(i) + ".chunk"):
                missing_chunks.append(i)
        return missing_chunks
