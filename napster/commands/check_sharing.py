from napster.commands.print_table import print_table
from napster.core.singleton import SingletonManager

def check_sharing():
    data_table = SingletonManager.DBManager_instance.select_all_shared_table()
    clean_table = []
    for row in data_table:
        clean_table.append([row[0], row[2], row[4]])

    print_table(clean_table, 50)
