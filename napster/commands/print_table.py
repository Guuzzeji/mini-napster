def __format_cell(text, column_width=15):
    return str(text)[:column_width].ljust(column_width)

def print_table(table, headers=None, column_width=15):
    if headers:
        # Format and join headers with a space
        header_line = ' '.join([__format_cell(header, column_width) for header in headers])
        print(header_line)

        # Print separator line
        separator = ' '.join(['-' * column_width for _ in range(len(headers))])
        print(separator)

    for row in table:
        # Format and join row cells with a space
        row_line = ' '.join([__format_cell(cell, column_width) for cell in row])
        print(row_line)