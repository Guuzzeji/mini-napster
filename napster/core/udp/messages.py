class WantMsg:
    def __init__(self, file_id = None, checksum = None, file_name = None, username = None):
        self.file_id = file_id
        self.checksum = checksum
        self.file_name = file_name
        self.username = username

    def __str__(self):
        return f"WANT|{self.file_id}|{self.checksum}|{self.file_name}|{self.username}"

    def parse(self, message: str):
        parts = message.split('|')
        if parts[0] != "WANT" or len(parts) != 5:
            raise ValueError("Invalid WANT message format")
        return WantMsg(file_id=parts[1], checksum=(parts[2]), file_name=parts[3], username=parts[4])

class MetadataMsg:
    def __init__(self, file_id = None, file_name = None, username = None,chunks = None, chunk_size = None):
        self.file_id = file_id
        self.file_name = file_name
        self.username = username
        self.chunks = chunks
        self.chunk_size = chunk_size

    def __str__(self):
        return f"METADATA|{self.file_id}|{self.file_name}|{self.username}|{self.chunks}|{self.chunk_size}"

    def parse(self, message: str):
        parts = message.split('|')
        if parts[0] != "METADATA" or len(parts) != 6:
            raise ValueError("Invalid METADATA message format")
        return MetadataMsg(file_id=parts[1], file_name=parts[2], username=parts[3], chunks=int(parts[4]), chunk_size=parts[5])

class DataMsg:
    def __init__(self, file_id = None, file_name = None, chunk_index = None, checksum = None, base64_chunk = None):
        self.file_id = file_id
        self.file_name = file_name
        self.chunk_index = chunk_index
        self.checksum = checksum
        self.base64_chunk = base64_chunk

    def __str__(self):
        return f"DATA|{self.file_id}|{self.file_name}|{self.chunk_index}|{self.checksum}|{self.base64_chunk}"

    def parse(self, message: str):
        parts = message.split('|')
        if parts[0] != "DATA" or len(parts) != 6:
            raise ValueError("Invalid DATA message format")
        return DataMsg(file_id=parts[1], file_name=parts[2], chunk_index=int(parts[3]), checksum=int(parts[4]), base64_chunk=parts[5])

class DataWantMsg:
    def __init__(self, file_id = None, file_name = None, chunk_index = None):
        self.file_id = file_id
        self.file_name = file_name
        self.chunk_index = chunk_index

    def __str__(self):
        return f"DATA_WANT|{self.file_id}|{self.file_name}|{self.chunk_index}"

    def parse(self, message: str):
        parts = message.split('|')
        if parts[0] != "DATA_WANT" or len(parts) != 4:
            raise ValueError("Invalid DATA_WANT message format")
        return DataWantMsg(file_id=parts[1], file_name=parts[2], chunk_index=int(parts[3]))

class EndMsg:
    def __init__(self, file_name = None):
        self.file_name = file_name

    def __str__(self):
        return f"END|{self.file_name}"

    def parse(self, message: str):
        parts = message.split('|')
        if parts[0] != "END" or len(parts) != 2:
            raise ValueError("Invalid END message format")
        return EndMsg(file_name=parts[1])



class ConvertToMessageType:
    def __init__(self):
        self.message_type = {
            "WANT": WantMsg,
            "METADATA": MetadataMsg,
            "DATA": DataMsg,
            "DATA_WANT": DataWantMsg,
            "END": EndMsg,
        }

    def parse_message(self, message: str):
        parts = message.split('|')
        msg_type = parts[0]
        if msg_type in self.message_type:
            return (msg_type, self.message_type[msg_type]().parse(message))
        else:
            raise ValueError("Unknown message type")
