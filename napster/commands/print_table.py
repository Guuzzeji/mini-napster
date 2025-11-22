def __format_cell(text, column_width):
    return str(text)[:column_width]

def print_table(table, column_width=15):
    for row in table:
        # Format and join row cells with a space
        row_line = ' | '.join([__format_cell(cell, column_width) for cell in row])
        print(row_line)