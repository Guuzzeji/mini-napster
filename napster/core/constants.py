import os

# MOTE: Max file size is 10mb
MESSAGE_SIZE = 1024 * 2  # bytes
BASE_EVERYTHING_FOLDER = "nap-data"
TRACKER_SERVER_URL = "http://localhost:3030/"

def config_exists() -> bool:
    return os.path.exists(BASE_EVERYTHING_FOLDER + "/config.txt")

def get_config_file() -> list[str]:
    if not config_exists():
        raise FileNotFoundError("Config file does not exist")
    result = []
    with open(BASE_EVERYTHING_FOLDER + "/config.txt", "r", encoding="utf-8") as f:
        result.append(f.readline().strip())  # username
        result.append(f.readline().strip())  # ip
        result.append(f.readline().strip())  # port
    return result

config_data = get_config_file()
UDP_IP = config_data[1]
USERNAME = config_data[0]
UDP_PORT = int(config_data[2])