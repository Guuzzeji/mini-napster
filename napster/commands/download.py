from napster.core.client import NapsterClient
from napster.core.singleton import SingletonManager

def download(username: str, target_ip: str, target_port: int, file_id: str, file_name: str, checksum: str = ""):
    """
    Download a file from another peer

    Args:
        username: Current user's username
        target_ip: IP address of the peer to download from
        target_port: Port of the peer to download from
        file_id: UUID of the file to download
        file_name: Name of the file to download
        checksum: Checksum of the file (optional, can be empty string)
    """
    print(f"Connecting to {target_ip}:{target_port} to download {file_name} (ID: {file_id})...")

    # Create a client to connect to the target peer
    client = NapsterClient(
        target_ip=target_ip,
        target_port=target_port,
        username=username,
        DownloadManager=SingletonManager.DownloadManager_instance
    )

    # Initiate the download
    client.download_file(
        file_name=file_name,
        file_id=file_id,
        checksum=checksum
    )

    print(f"Download started for {file_name}")
    print(f"Check download progress with 'dls' command")

    return client  # Return client so it stays alive
