def print_table(table, headers=None, column_width=15):
    # Define a fixed column width

    # Helper function for formatting a cell
    def format_cell(text):
        # Truncate and left-align the text within the column width
        return str(text)[:column_width].ljust(column_width)

    if headers:
        # Format and join headers with a space
        header_line = ' '.join([format_cell(header) for header in headers])
        print(header_line)

        # Print separator line
        separator = ' '.join(['-' * column_width for _ in range(len(headers))])
        print(separator)

    for row in table:
        # Format and join row cells with a space
        row_line = ' '.join([format_cell(cell) for cell in row])
        print(row_line)