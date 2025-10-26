import os
from napster.core.database.db_manager import DBManager
from napster.core.file_manager.folder_struct import BASE_EVERYTHING_FOLDER, create_base_folder
from napster.core.file_manager.mp3_file import Mp3File


SHARING_FOLDER = BASE_EVERYTHING_FOLDER + "/sharing"

class FileManager():
    def __init__(self, db_manager_instance: DBManager) -> None:
        self.db_manager = db_manager_instance
        self.__check_sharing_folder()
    
    def __put_file_into_db(self, full_file_path: str):
        mp3_file = Mp3File(full_file_path)
        test_id = "test" # TODO CHANGE THIS
        self.db_manager.insert_shared_table(test_id, mp3_file.checksum, mp3_file.file_name, full_file_path, mp3_file.total_chunks)

    def __check_sharing_folder(self):
        if not os.path.exists(SHARING_FOLDER):
            create_base_folder()
            os.makedirs(SHARING_FOLDER)
        else:
            for file in os.listdir(SHARING_FOLDER):
                if file.endswith(".mp3"):
                    self.__put_file_into_db(SHARING_FOLDER + "/" + file)