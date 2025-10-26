from napster.core.database.db_manager import DBManager
from napster.core.file_manager.mp3_file import Mp3File

class SharingFilesManager:
    def __init__(self, db_manager_instance: DBManager) -> None:
        self.db_manager = db_manager_instance

    def add_client(self, client, uuid: str, file_name: str, username: str):
        ttl = str(10) # this is for testing currently not being used
        self.db_manager.insert_sharing_table(uuid, file_name, username, ttl, client[0], client[1])

    def remove_client(self, client):
        self.db_manager.remove_sharing_table(client[0])

    def __get_file_from_db(self, client):
        downloading_client = self.db_manager.select_sharing_table(client[0]).fetchone()
        if downloading_client is None:
            return None

        file = self.db_manager.select_shared_table(downloading_client[0], downloading_client[1]).fetchone()
        if file is None:
            return None

        return file

    def send_chunk(self, client, index: int):
        file = self.__get_file_from_db(client)
        if file is None:
            return None

        mp3_file = Mp3File(file[3])

        if index >= mp3_file.total_chunks:
            return None

        return mp3_file.get_chunk(index)

    def get_metadata(self, client) -> dict | None:
        file = self.__get_file_from_db(client)
        if file is None:
            return None

        mp3_file = Mp3File(file[3])
        return {
            "number_of_chunks": mp3_file.total_chunks,
            "checksum": mp3_file.checksum
        }
