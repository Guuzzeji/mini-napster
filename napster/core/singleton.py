from napster.core.database.db_manager import DBManager
from napster.core.file_manager.file_manager import FileManager
from napster.core.udp.download_manager import DownloadManager
from napster.core.udp.sharing_files_manager import SharingFilesManager

class SingletonManager:
    DBManager_instance = DBManager()
    DownloadManager_instance = DownloadManager()
    FileManager_instance = FileManager(DBManager_instance)
    SharingFilesManager_instance = SharingFilesManager(DBManager_instance)