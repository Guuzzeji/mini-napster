import sys

from pyfiglet import Figlet

from napster.commands.help import help_command
from napster.commands.search_files import search_file
from napster.core.singleton import SingletonManager
from napster.core.constants import USERNAME, UDP_IP, UDP_PORT
from napster.core.server import NapsterServer
from napster.commands.check_sharing import check_sharing
from napster.commands.clear import clear
from napster.commands.download import download_command
from napster.commands.downloads import downloads
from napster.commands.leachers import leachers  

f = Figlet(font='doom')
print(f.renderText('MINI/NAPSTER'))

USERNAME = sys.argv[1] if len(sys.argv) > 1 else USERNAME
IP = sys.argv[2] if len(sys.argv) > 2 else UDP_IP
PORT = sys.argv[3] if len(sys.argv) > 3 else UDP_PORT
print(f"== Welcome {USERNAME} | IP: {IP} | Port: {PORT} ==\n")

# Run server
server = NapsterServer(IP, int(PORT), USERNAME, SingletonManager.SharingFilesManager_instance)

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
        case "sf" | "search-file":
            artist = command_input[1] if len(command_input) > 1 else ''
            song = command_input[2] if len(command_input) > 2 else ''
            search_file(artist, song)
        case "lr" | "leachers":
            leachers()
        case "clear" | "cls":
            clear()
        case "sl" | "shared-list":
            check_sharing()
        case "dl" | "download":
            download_command(command_input, download_clients, USERNAME)
        case "dls" | "downloads":
            downloads()
        case "help":
            help_command()
        case "exit":
            break
        case _:
            print("Unknown command")
            print("Type 'help' to see available commands")
