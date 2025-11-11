import sys

from pyfiglet import Figlet

from napster.core.singleton import UDP_IP, UDP_PORT, SingletonManager
from napster.core.server import NapsterServer

from napster.commands.check_sharing import check_sharing
from napster.commands.clear import clear

f = Figlet(font='slant')
print(f.renderText('Mini Napster'))

username = sys.argv[1] if len(sys.argv) > 1 else "Anonymous"
ip = sys.argv[2] if len(sys.argv) > 2 else UDP_IP
port = sys.argv[3] if len(sys.argv) > 3 else UDP_PORT
print(f"== Welcome {username} | IP: {ip} | Port: {port} ==\n")

# Run server
server = NapsterServer(ip, int(port), username, SingletonManager.SharingFilesManager_instance)

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
            # TODO: implement download command, so people can download a file base on specified id, ip, and port
            # i.e download <ip> <port> <file-id>
            pass
        case "dls" | "downloads":
            # TODO: implement downloads command, so people can see all the files they are currently downloading
            # NOTE: This should put into a thread pool for downloading multiple files
            pass
        case "help":
            # TODO: implement help command, just list all the commands available
            pass
        case "exit":
            break
        case _:
            print("Unknown command")



