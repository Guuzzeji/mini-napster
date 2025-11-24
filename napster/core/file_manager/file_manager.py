import os
from napster.core.database.db_manager import DBManager
from napster.core.file_manager.folder_struct import BASE_EVERYTHING_FOLDER, create_base_folder
from napster.core.file_manager.mp3_file import Mp3File
from napster.core.tracker_handler.tracker import upload_metadata
from napster.core.tracker_handler.request_bodies import UploadMetadataRequestBody
from napster.core.constants import UDP_IP, UDP_PORT, USERNAME

SHARING_FOLDER = BASE_EVERYTHING_FOLDER + "/sharing"

class FileManager():
    def __init__(self, db_manager_instance: DBManager) -> None:
        self.db_manager = db_manager_instance
        self.__check_sharing_folder()
    
    def __put_file_into_db(self, full_file_path: str):
        mp3_file = Mp3File(full_file_path)

        existing_uuid_for_file = self.db_manager.get_uuid_from_file_name(mp3_file.file_name) 
        existing_uuid_for_file = '' if existing_uuid_for_file is None else existing_uuid_for_file

        file_metadata = UploadMetadataRequestBody(
            song_name=mp3_file.file_name,
            artist=mp3_file.artist,
            album=mp3_file.album,
            duration=mp3_file.duration,
            file_size=mp3_file.size,
            year=str(mp3_file.year),
            checksum=mp3_file.checksum,
            username=USERNAME, 
            ip=UDP_IP, 
            port=UDP_PORT,
            file_id=existing_uuid_for_file
        ) 

        response = upload_metadata(file_metadata)
        if response is None:
            print(f"Error: Could not upload metadata for file '{mp3_file.file_name}' to tracker")
            return

        if response.file_id == '':
            return    
    
        self.db_manager.insert_shared_table(response.file_id, mp3_file.checksum, mp3_file.file_name, full_file_path, mp3_file.total_chunks)

    def __check_sharing_folder(self):
        if not os.path.exists(SHARING_FOLDER):
            create_base_folder()
            os.makedirs(SHARING_FOLDER)
        else:
            for file in os.listdir(SHARING_FOLDER):
                if file.endswith(".mp3"):
                    self.__put_file_into_db(SHARING_FOLDER + "/" + file)