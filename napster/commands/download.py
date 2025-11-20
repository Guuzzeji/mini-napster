import time
from napster.core.client import NapsterClient
from napster.core.singleton import SingletonManager

def download(username: str, target_ip: str, target_port: int, file_id: str, file_name: str):
    """
    Download a file from another peer

    Args:
        username: Current user's username
        target_ip: IP address of the peer to download from
        target_port: Port of the peer to download from
        file_id: UUID of the file to download
        file_name: Name of the file to download
    """
    print(f"Connecting to {target_ip}:{target_port} to download {file_name} (ID: {file_id})...")

    try:
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
            checksum=""
        )

        # Wait for METADATA response (up to 5 seconds)
        print("Waiting for server response...")
        max_wait_time = 5
        wait_interval = 0.5
        total_waited = 0

        while total_waited < max_wait_time:
            time.sleep(wait_interval)
            total_waited += wait_interval

            # Check if file was added to download manager (METADATA received)
            if SingletonManager.DownloadManager_instance.file_exists(file_name, file_id):
                print(f"Download started for {file_name}")
                print(f"Check download progress with 'dls' command")
                return client  # Return client so it stays alive

        # Timeout - no response from server
        print(f"Error: No response from {target_ip}:{target_port}")
        print(f"Possible issues:")
        print(f"  - Server is not running at {target_ip}:{target_port}")
        print(f"  - File ID '{file_id}' does not exist on the server")
        print(f"  - Network connection issue")
        return None

    except Exception as e:
        print(f"Error: Failed to start download - {e}")
        return None
