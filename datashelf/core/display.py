from rich.console import Console
from rich.table import Table
from datashelf.core.metadata import FileEntry

# Create console objects to be used across modules
_console = Console(color_system = "auto")
_error_console = Console(stderr = True, style = "bold red")

def print_error(msg: str):
    _error_console.print(msg)
    
def print_success(msg: str):
    _console.print(f"[bold green]{msg}")
    
def print_message(msg: str):
    _console.print(msg)
    
def print_entry_detail(entries: list[FileEntry]):
    if len(entries) == 1:
        title = f"Displaying {1} matching entry"
    else:
        title = f"Displaying {len(entries)} matching entries"
        
    detail_table = Table(title = title)  
    
    headers = [key for key, value in entries[0].items()]
    for header in headers:
        detail_table.add_column(header = header)
        
    for entry in entries:
        detail_table.add_row(entry["file_hash"], entry["name"], entry["tag"], entry["message"], entry["stored_path"], entry["datetime_added"])

    _console.print(detail_table)
    
def print_table(entries: list[FileEntry]):
    if len(entries) == 1:
        title = f"Displaying {1} entry"
    else:
        title = f"Displaying all {len(entries)} entries"
        
    table = Table(title = title)
    
    headers = ["file_hash", "name", "tag", "message"]

    for header in headers:
        table.add_column(header = header)
    
    for entry in entries:
        table.add_row(entry["file_hash"], entry["name"], entry["tag"], entry["message"])
        
    _console.print(table)
    
