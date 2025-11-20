import sys
import logging

from pyfiglet import Figlet

from napster.core.singleton import UDP_IP, UDP_PORT, SingletonManager
from napster.core.server import NapsterServer

# Configure logging
# Set to DEBUG to see all logs, INFO for important events, WARNING for issues only
logging.basicConfig(
    level=logging.INFO,  # Change to DEBUG for verbose output
    format='%(asctime)s [%(levelname)s] %(name)s: %(message)s',
    datefmt='%H:%M:%S'
)

from napster.commands.check_sharing import check_sharing
from napster.commands.clear import clear
from napster.commands.download import download
from napster.commands.downloads import downloads

f = Figlet(font='slant')
print(f.renderText('Mini Napster'))

username = sys.argv[1] if len(sys.argv) > 1 else "Anonymous"
ip = sys.argv[2] if len(sys.argv) > 2 else UDP_IP
port = sys.argv[3] if len(sys.argv) > 3 else UDP_PORT
print(f"== Welcome {username} | IP: {ip} | Port: {port} ==\n")

# Run server
server = NapsterServer(ip, int(port), username, SingletonManager.SharingFilesManager_instance)

# Store active download clients per peer (ip, port)
# This allows reusing the same client for multiple downloads from the same peer
download_clients = {}

while True:
    """
    NOTE: All commands are store in the commands folder, please add your own commands there
    """
    command_input = input("> ").split(" ") # split commands by spaces to get different input
    command = command_input[0]

    match command:
        case "lr" | "leechers":
            # TODO: implement leechers, get the usernames and files people are downloading, print it as a table
            pass
        case "clear" | "cls":
            clear()
        case "sdl" | "shared_list":
            check_sharing()
        case "dl" | "download":
            # Usage: download <ip> <port> <file-id> <filename> 
            if len(command_input) < 4:
                print("Usage: download <ip> <port> <file-id> <filename>")
                print("Example: download 127.0.0.1 5005 abc-123 song.mp3")
            else:
                target_ip = command_input[1]
                target_port = int(command_input[2])
                file_id = command_input[3]
                file_name = command_input[4]

                peer_key = (target_ip, target_port)

                # Reuse existing client for this peer, or create a new one
                if peer_key not in download_clients:
                    client = download(username, target_ip, target_port, file_id, file_name)
                    if client:
                        download_clients[peer_key] = client
                        print(f"Created new connection to peer {target_ip}:{target_port}")
                else:
                    # Reuse existing client connection
                    client = download_clients[peer_key]
                    client.download_file(file_name=file_name, file_id=file_id, checksum="")
                    print(f"Reusing existing connection to peer {target_ip}:{target_port}")
                    print(f"Download started for {file_name}")
                    print(f"Check download progress with 'dls' command")
        case "dls" | "downloads":
            downloads()
        case "help":
            # TODO: implement help command, just list all the commands available
            pass
        case "exit":
            break
        case _:
            print("Unknown command")



