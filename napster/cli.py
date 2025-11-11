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
    command_input = input("> ").split(" ")
    command = command_input[0]

    match command:
        case "lr" | "leechers":
            pass
        case "clear" | "cls":
            clear()
        case "sdl" | "shared_list":
            check_sharing()
        case "dl" | "download":
            pass
        case "dls" | "downloads":
            pass
        case "help":
            pass
        case "exit":
            break
        case _:
            print("Unknown command")



