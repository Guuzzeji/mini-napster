from datetime import datetime
import threading

from napster.core.udp.download_manager import DownloadManager
from napster.core.udp.udp import UDPClient
from napster.core.singleton import SingletonManager, UDP_IP, UDP_PORT
from napster.core.udp.messages import WantMsg, EndMsg, DataWantMsg

class NapsterClient(UDPClient):
    def __init__(self, target_ip: str, target_port: int, username: str, DownloadManager: DownloadManager) -> None:
        UDPClient.__init__(self, target_ip, target_port)
        self.username = username
        self.download_manager = DownloadManager
        self.start_receiver(self.handle_message)
        self.handle_downloads()

    def handle_message(self, message, addr):
        print("(client) received message: %s from %s" % (message, addr))

        if message[0] == "METADATA":
            print("Received METADATA message")
            metadata = message[1]
            self.download_manager.add_file_metadata(
                uuid=metadata.file_id,
                file_name=metadata.file_name,
                number_of_chunks=metadata.chunks,
                username=metadata.username,
                checksum=metadata.chunk_size,
                server=addr
            )

        if message[0] == "DATA":
            data_msg = message[1]
            self.download_manager.add_chunk(
                checksum=data_msg.checksum,
                uuid=data_msg.file_id,
                file_name=data_msg.file_name,
                chunk_index=data_msg.chunk_index,
                base64_chunk=data_msg.base64_chunk
            )

            if self.download_manager.get_number_of_chunks_saved(data_msg.file_name) == self.download_manager.get_total_number_of_chunks(data_msg.file_name, data_msg.file_id):
                print(f"File {data_msg.file_name} is complete")
                self.send_message(str(EndMsg(file_name=data_msg.file_name)))
                self.download_manager.assemble_file(data_msg.file_name, data_msg.file_id)

            if self.download_manager.get_total_number_of_chunks(data_msg.file_name, data_msg.file_id):
                print(
                    f"Received DATA message | chunk index: {message[1].chunk_index} out of {self.download_manager.get_number_of_chunks_saved(message[1].file_name)} / {self.download_manager.get_total_number_of_chunks(message[1].file_name, message[1].file_id)}")

    def download_file(self, file_name: str, file_id: str, checksum: str):
        self.send_message(
            str(
                WantMsg(
                    file_id=file_id,
                    checksum=checksum,
                    file_name=file_name,
                    username=self.username
                    )
                )
            )

    def handle_downloads(self):
        def process():
            print("UDP client download handler thread started")
            while self.thread_kill_event.is_set() is False:
                manager = list(self.download_manager.manager.keys())
                for file in manager:
                    try:
                        file_id, file_name = file.split("||")
                        missing_chunks = self.download_manager.file_missing_chunks(file_name, file_id)
                        last_blast = (datetime.now().minute - self.download_manager.manager[file]["last_blast"].minute) > 5 or self.download_manager.manager[file]["just_created"]
                        if last_blast:
                            self.download_manager.manager[file]["last_blast"] = datetime.now()
                            self.download_manager.manager[file]["just_created"] = False
                            for chunk in missing_chunks:
                                self.send_message(str(DataWantMsg(chunk_index=chunk, file_name=file_name, file_id=file_id)))
                    except Exception as e:
                        continue
            print("UDP client download handler thread ended")

        thread = threading.Thread(target=process, daemon=True)
        thread.name = "UDPClientDownloadHandlerThread"
        thread.start()
        self.threads.append(thread)


