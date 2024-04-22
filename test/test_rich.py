from rich import print
from rich.table import Table
out_table = Table()
out_table.add_column('1')
out_table.add_column('2')

grid = Table.grid(expand=True, pad_edge=True)
grid.add_column('1.1')
grid.add_column('1.2', justify="right")
grid.add_row("Raising shields", "[bold magenta]COMPLETED [green]:heavy_check_mark:")

out_table.add_row('a', grid)
print(out_table)