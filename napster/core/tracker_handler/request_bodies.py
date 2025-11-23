class UploadMetadataRequestBody:
    def __init__(self, 
                 song_name: str, 
                 artist: str, 
                 album: str = '', 
                 duration: int = 0, 
                 file_size: int = 0, 
                 year: str = '', 
                 checksum: str = '', 
                 username: str = '', 
                 ip: str = '', 
                 port: int = 0,
                 file_id: str = ''):
        self.song_name = song_name
        self.artist = artist
        self.album = album
        self.duration = duration
        self.file_size = file_size
        self.year = year
        self.checksum = checksum
        self.username = username
        self.ip = ip
        self.port = port
        self.file_id = file_id

    def to_json(self) -> dict:
        return {
            'song_name': self.song_name,
            'artist': self.artist,
            'album': self.album,
            'duration': self.duration,
            'file_size': self.file_size,
            'year': self.year,
            'checksum': self.checksum,
            'user_id': f'{self.username}|{self.ip}|{str(self.port)}',
            'file_id': self.file_id
        }
    
class UploadMetadataResponseBody:
    def __init__(self, file_id: str):
        self.file_id = file_id

    @classmethod
    def from_json(cls, data: dict):
        return cls(file_id=data.get('file_id', ''))
    
class SearchFile:
    def __init__(self, 
                 file_id: str,
                 song_name: str,
                 artist: str,
                 album: str = '',
                 duration: int = 0,
                 file_size: int = 0,
                 year: str = '',
                 user_id: str = ''):
        self.file_id = file_id
        self.song_name = song_name
        self.artist = artist
        self.album = album
        self.duration = duration
        self.file_size = file_size
        self.year = year
        self.user_id = user_id

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            file_id=data.get('file_id', ''),
            song_name=data.get('song_name', ''),
            artist=data.get('artist', ''),
            album=data.get('album', ''),
            duration=data.get('duration', 0),
            file_size=data.get('file_size', 0),
            year=data.get('year', ''),
            user_id=data.get('user_id', '')
        )

class SearchFileResponseBody:
    def __init__(self, data: list[SearchFile]):
        self.data = data
    
    @classmethod
    def from_json(cls, data: list[dict]):
        files = [SearchFile.from_json(item) for item in data]
        return cls(data=files)
    
class DownloadInfoResponseBody:
    def __init__(self, 
                 file_id: str,
                 port: int,
                 user_ip: str,
                 username: str,
                 checksum: str,
                 file_name: str):
        self.file_id = file_id
        self.port = port
        self.ip = user_ip
        self.file_name = file_name
        self.username = username
        self.checksum = checksum

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            file_id=data.get('file_id', ''),
            port=data.get('port', 0),
            user_ip=data.get('user_ip', ''),
            username=data.get('username', ''),
            checksum=data.get('checksum', ''),
            file_name=data.get('file_name', '')
        )
