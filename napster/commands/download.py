import time
from napster.core.client import NapsterClient
from napster.core.singleton import SingletonManager
from napster.core.tracker_handler.tracker import get_download_info

def download_command(command_input, download_clients, username):
    if len(command_input) != 2:
        print("Usage: download <file-id>")
        print("Example: download abc-123")
    else:
        file_id = command_input[1]

        user = get_download_info(file_id)
        if user is None:
            print(f"Error: Could not get download info for file ID '{file_id}' from tracker")
            return

        peer_key = (user.ip, user.port)

        # Reuse existing client for this peer, or create a new one
        if peer_key not in download_clients:
            client = download(username, user.ip, user.port, file_id, user.file_name)
            if client:
                download_clients[peer_key] = client
                print(f"Created new connection to peer {user.ip}:{user.port}")
        else:
            # Reuse existing client connection
            client = download_clients[peer_key]
            client.download_file(file_name="", file_id=file_id, checksum="")
            print(f"Reusing existing connection to peer {user.ip}:{user.port}")
            print(f"Download started for {user.file_name}")
            print(f"Check download progress with 'dls' command")

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
