from colorama import Fore, Style, init

init(autoreset=True)

def help_command():
    """Display help information for all available commands"""
    
    print(f"\n{Fore.CYAN}=== MINI/NAPSTER - Available Commands ==={Style.RESET_ALL}\n")
    
    print(f"{Fore.GREEN}sf | search-file {Fore.YELLOW}<artist> <song>{Style.RESET_ALL}")
    print(f"  Search for files by artist and/or song name")
    print(f"  {Fore.MAGENTA}Example: sf Beatles Yesterday{Style.RESET_ALL}\n")
    
    print(f"{Fore.GREEN}lr | leachers{Style.RESET_ALL}")
    print(f"  Display all users currently downloading from you\n")
    
    print(f"{Fore.GREEN}sl | shared-list{Style.RESET_ALL}")
    print(f"  Display list of files you are currently sharing\n")
    
    print(f"{Fore.GREEN}dl | download {Fore.YELLOW}<file-id>{Style.RESET_ALL}")
    print(f"  Download a file using its ID from search results")
    print(f"  {Fore.MAGENTA}Example: dl abc-123{Style.RESET_ALL}\n")
    
    print(f"{Fore.GREEN}dls | downloads{Style.RESET_ALL}")
    print(f"  Show progress of all active downloads\n")
    
    print(f"{Fore.GREEN}clear | cls{Style.RESET_ALL}")
    print(f"  Clear the terminal screen\n")
    
    print(f"{Fore.GREEN}help{Style.RESET_ALL}")
    print(f"  Display this help message\n")
    
    print(f"{Fore.GREEN}exit{Style.RESET_ALL}")
    print(f"  Exit the application\n")