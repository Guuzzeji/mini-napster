from napster.commands.print_table import print_table
from napster.core.singleton import SingletonManager

def downloads():
    """Display all active downloads with progress information"""
    manager = SingletonManager.DownloadManager_instance.manager

    if not manager:
        print("No active downloads")
        return

    clean_table = []
    for _, download_info in manager.items():
        file_name = download_info.get("file_name", "Unknown")
        total_chunks = download_info.get("total_chunks", 0)
        downloaded_chunks = download_info.get("downloaded_chunks", 0)
        username = download_info.get("username", "Unknown")
        ip = download_info.get("ip", "Unknown")
        port = download_info.get("port", "Unknown")

        # Calculate progress percentage
        progress_pct = (downloaded_chunks / total_chunks * 100) if total_chunks > 0 else 0
        progress_str = f"{downloaded_chunks}/{total_chunks} ({progress_pct:.1f}%)"
        peer_str = f"{username}@{ip}:{port}"

        clean_table.append([file_name, progress_str, peer_str])

    print_table(clean_table, ["File Name", "Progress", "Peer"], 50)
