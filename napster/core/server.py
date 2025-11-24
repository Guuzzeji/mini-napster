import socket
from time import sleep

from napster.core.udp.sharing_files_manager import SharingFilesManager
from napster.core.udp.udp import UDPServer
from napster.core.udp.messages import DataMsg, MetadataMsg

class NapsterServer(UDPServer):
    def __init__(self, ip: str, port: int, username: str, SharingFilesManager: SharingFilesManager):
        UDPServer.__init__(self, ip, port)
        self.UDPServer_instance = UDPServer
        self.SharingFilesManager_instance = SharingFilesManager
        self.username = username
        self.start(self.handle_message)
    
    def handle_message(self, sock: socket.socket, message, addr):
        # print("(server) received message: %s from %s" % (message, addr))

        if message[0] == "WANT":
            # print(f"Client at {addr} wants file {message[1].file_id} with checksum {message[1].checksum}")
            self.SharingFilesManager_instance.add_client(addr, message[1].file_id, message[1].file_name, message[1].username)
            meta_data = self.SharingFilesManager_instance.get_metadata(message[1].file_id)
            if meta_data is not None:
                metadata_msg = MetadataMsg(
                    username=self.username, 
                    file_id=message[1].file_id,
                    file_name=message[1].file_name, 
                    chunks=meta_data["number_of_chunks"], 
                    chunk_size=meta_data["checksum"])
                sock.sendto(str(metadata_msg).encode('utf-8'), addr)

        if message[0] == "DATA_WANT":
            message_index = message[1].chunk_index
            file_name = message[1].file_name
            file_id = message[1].file_id
            # print(f"Client at {addr} wants data chunk {message_index}")
            chunk = self.SharingFilesManager_instance.send_chunk(file_id, message_index)
            
            if chunk is None:
                return
            
            data_msg = DataMsg(file_id=file_id, file_name=file_name, chunk_index=message_index, checksum=len(chunk), base64_chunk=chunk)
            sock.sendto(str(data_msg).encode('utf-8'), addr)

            meta_data = self.SharingFilesManager_instance.get_metadata(file_id)
            if meta_data is None:
                return

        if message[0] == "END":
            # print(f"Client at {addr} ended the download")
            self.SharingFilesManager_instance.remove_client(addr)