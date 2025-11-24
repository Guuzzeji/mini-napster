from napster.core.singleton import SingletonManager
from napster.commands.print_table import print_table

def leachers():
    leachers_table = SingletonManager.DBManager_instance.select_all_sharing_table()

    leacher_list = []
    for leacher in leachers_table.fetchall():
        leacher_list.append([
            leacher[0],
            leacher[1],
            leacher[2],
            leacher[4],
            leacher[5]
        ])

    print_table(leacher_list, column_width=25)
