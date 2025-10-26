import os
import sqlite3

from napster.core.file_manager.folder_struct import create_base_folder
from napster.core.constants import BASE_EVERYTHING_FOLDER

DATABASE_FILE_NAME = BASE_EVERYTHING_FOLDER + "/napster.db"

class DBManager:
    def __init__(self):
        # Allow for multiple writers
        self.__create_db_file()
        self.con = sqlite3.connect(DATABASE_FILE_NAME, isolation_level=None, check_same_thread=False, autocommit=True)
        self.con.execute('PRAGMA journal_mode=wal')
        self.con.execute("PRAGMA busy_timeout=5000;")
        self.__create_tables()

    def __create_db_file(self):
        create_base_folder()
        if not os.path.exists(DATABASE_FILE_NAME):
            open(DATABASE_FILE_NAME, 'w').close()

    def __command_return(self, query: str, args: tuple = ()):
        cur = self.con.cursor()
        return cur.execute(query, args)
    
    def __command_commit(self, query: str, args: tuple = ()):
        cur = self.con.cursor()
        cur.execute(query, args)

    def __create_tables(self):
        self.__command_return("""
            CREATE TABLE IF NOT EXISTS shared (
                uuid TEXT PRIMARY KEY,
                file_checksum TEXT NOT NULL,
                file_name TEXT NOT NULL,
                full_file_path TEXT NOT NULL,
                total_chunks INTEGER NOT NULL
            );
        """)

        self.__command_return("""
            CREATE TABLE IF NOT EXISTS sharing (
                uuid TEXT PRIMARY KEY,
                file_name TEXT NOT NULL,
                username TEXT NOT NULL,
                ttl TEXT NOT NULL,
                ip TEXT NOT NULL,
                port INTEGER NOT NULL
            );
        """)

        self.__command_return("""
            CREATE INDEX IF NOT EXISTS idx_shared_checksum ON shared (file_checksum);
        """)

        self.__command_return("""
            CREATE INDEX IF NOT EXISTS idx_shared_name ON shared (file_name);
        """)

        self.__command_return("""
            CREATE INDEX IF NOT EXISTS idx_sharing_username ON sharing (username);
        """)

        self.__command_return("""
            CREATE INDEX IF NOT EXISTS idx_sharing_name ON sharing (file_name);
        """)

    def insert_shared_table(self, uuid: str, file_checksum: str, file_name: str, full_file_path: str, total_chunks: int):
        self.__command_commit(f"""
            INSERT OR IGNORE INTO shared (uuid, file_checksum, file_name, full_file_path, total_chunks) VALUES (?, ?, ?, ?, ?);
        """, (uuid, file_checksum, file_name, full_file_path, total_chunks))

    def remove_shared_table(self, uuid: str):
        self.__command_commit(f"""
            DELETE FROM shared WHERE uuid = ?;
        """, (uuid,))

    def select_all_shared_table(self):
        return self.__command_return("""
            SELECT uuid, file_checksum, file_name, full_file_path, total_chunks
            FROM shared;
        """)
    
    def select_shared_table(self, uuid: str, file_name: str):
        return self.__command_return(f"""
            SELECT uuid, file_checksum, file_name, full_file_path, total_chunks
            FROM shared
            WHERE uuid = ? AND file_name = ?;
        """, (uuid, file_name))

    def insert_sharing_table(self, uuid: str, file_name: str, username: str, ttl: str, ip: str, port: int):
        self.__command_commit(f"""
            INSERT OR IGNORE INTO sharing (uuid, file_name, username, ttl, ip, port) VALUES (?, ?, ?, ?, ?, ?);
        """, (uuid, file_name, username, ttl, ip, port))

    def remove_sharing_table(self, ip: str):
        self.__command_commit(f"""
            DELETE FROM sharing
            WHERE ip = ?;
        """, (ip,))

    def select_all_sharing_table(self):
        return self.__command_return("""
            SELECT uuid, file_name, username, ttl, ip, port
            FROM sharing;
        """)

    def select_sharing_table(self, ip: str):
        return self.__command_return(f"""
            SELECT uuid, file_name, username, ttl, ip, port
            FROM sharing
            WHERE ip = ?;
        """, (ip,))