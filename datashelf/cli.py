import argparse
import sys

from datashelf import init, save, checkout, ls, show, load
from datashelf.core.display import print_success, print_error, print_message, print_table, print_entry_detail
from datashelf.load import AmbiguousLookupError


def init_command(args):
    """Initialize a datashelf directory in the current working directory or a specified path.

    Args:
        args (_type_): The arguments passed from the command line. It should contain the following attributes:
            - path (str, optional): An optional path to initialize the datashelf directory.
            If not provided, the datashelf directory will be initialized in the current working directory.

    Returns:
        int: 0 if the datashelf directory was initialized successfully, 1 otherwise.
    """
    try:
        initialized, datashelf_path = init(custom_path = args.path) # If no args.path, will default to args.path = None
    except Exception as e:
        print_error(msg = f"Error initializing Datashelf directory: {e}")
        return 1 
    
    if initialized:
        print_success(msg = f"Initialized Datashelf at {str(datashelf_path)}")
    else:
        print_message(msg = f"Datashelf already initialized at {str(datashelf_path)}")
    
    return 0


def save_file_command(args):
    """Save a file to the datashelf.

    Args:
        args (_type_): The arguments passed from the command line. It should contain the following attributes:
            - file_path (str): The path to the file to be saved.
            - name (str): The name to save the file as in the datashelf.
            - message (str, optional): An optional message describing the file being saved.
            - tag (str, optional): An optional tag to associate with the saved file.
            - on_duplicate(Literal['skip', 'error', 'update'], optional): An optional tag to define what to do 
            if file is a duplicate. Defaults to skip.

    Returns:
        int: 0 if the file was saved successfully, 1 otherwise.
    """

    name = args.name.strip() if args.name else ""
    message = args.message.strip() if args.message else ""
    tag = args.tag.strip() if args.tag else ""
    
    try:
        save(data = args.file_path, name = name, message = message, tag = tag, on_duplicate = args.on_duplicate)
        print_success(f"save() was successful for {name}.")
        return 0
    
    except Exception as e:
        print_error(msg = f"Error saving file: {e}")
        return 1

def load_command(args):
    """Load a file from the datashelf.

    Args:
        args: The arguments passed from the command line. It should contain:
            - lookup_key (str): Dataset name, full hash, or unique hash prefix.
            - to_df (bool, optional): If True, load and display the artifact as a DataFrame.
              If False, print the resolved stored path.

    Returns:
        int: 0 if the file was loaded successfully, 1 otherwise.
    """
    try:
        result = load(lookup_key=args.lookup_key, to_df=args.to_df)
        
        if args.to_df:
            print(str(result))
        else:
            print_success(msg = "Successfully retrieved file path:")
            print_message(msg = f"{result}")
          
        return 0
    
    except AmbiguousLookupError as e:
        print_error(f"Multiple matches found for '{e.lookup_key}':")
        print_table(e.matches)
        print_message("Rerun with a more specific lookup key.")
        return 1
    
    except Exception as e:
        print_error(str(e))
        return 1


def ls_command(args):
    """Return all dataset entries currently registered in .datashelf.

    Optionally filters entries by one or more tags. If tag enforcement is enabled
    in config, filter tags are validated against the allowed tags list before filtering.

    Args:
        filter_tag (list[str] | str | None, optional): Tag or list of tags to filter 
            entries by. If None, all entries are returned. Defaults to None.

    Raises:
        ValueError: If tag enforcement is enabled and a provided filter tag is not
            in the allowed tags list.

    Returns:
        list[FileEntry]: All matching entries, or an empty list if none are found.
    """
    try:
        entries = ls(filter_tag=args.filter_tag)
        
        if not entries: 
            print_message(msg = "No matching entries found.")
            return 0

        print_table(entries = entries)
        return 0

    except Exception as e:
        print_error(f"Error listing files: {e}")
        return 1


def show_command(args):
    """Return metadata entries for a dataset identified by the lookup key.

    Resolves the lookup key against stored metadata by checking dataset name first,
    then hash prefix, then exact hash. Returns all matches found at the first
    successful match level — if name matches exist they are returned without
    checking hash matches.

    Args:
        lookup_key (str): Dataset name, full hash, or unique hash prefix to look up 
            in the metadata.

    Raises:
        ValueError: If no matching dataset is found for the lookup key.
        RuntimeError: If an unexpected state is encountered during resolution.

    Returns:
        list[FileEntry]: One or more matching metadata entries.
    """
    try:
        entries = show(lookup_key=args.lookup_key)
        print_entry_detail(entries = entries)
        return 0

    except ValueError as e:
        print_error(str(e))
        return 1
    
    except Exception as e:
        print_error(f"Unexpected error: {e}")
        return 1


def checkout_command(args):
    """Copy a stored artifact from the datashelf to a user-specified destination.

    Resolves the lookup key against stored metadata and copies the matching artifact
    to the specified destination path. Renders a Rich table of matches if the lookup
    key is ambiguous, and a success message with the destination path on completion.

    Args:
        args: The arguments passed from the command line. It should contain:
            - lookup_key (str): Dataset name, full hash, or unique hash prefix.
            - dest_path (str): Destination file path to copy the artifact to.
                Must have a .parquet suffix and must not already exist.

    Raises:
        AmbiguousLookupError: If multiple matching datasets are found for the lookup
            key. Handled internally — renders a table of matches and returns 1.
        TypeError: If the destination path does not have a .parquet suffix.
            Handled internally — prints error and returns 1.
        FileExistsError: If a file already exists at the destination path.
            Handled internally — prints error and returns 1.

    Returns:
        int: 0 if the checkout completed successfully, 1 otherwise.
    """
    try:
        dest_path = checkout(lookup_key = args.lookup_key, dest_path = args.dest_path)
        print_success(msg = f"Checked out artifact to {dest_path}")
        return 0
    
    except AmbiguousLookupError as e:
        print_error(str(e))
        print_table(e.matches)
        print_message("Rerun with a more specific lookup key.")
        return 1
    
    except Exception as e:
        print_error(str(e))
        return 1

def main():
    parser = argparse.ArgumentParser(description="Datashelf CLI")
    subparsers = parser.add_subparsers(title="Commands", dest="command")

    # Init command
    init_parser = subparsers.add_parser("init", help="Initialize a Datashelf directory.")
    init_help_msg = (
        "Optional path to initialize the Datashelf directory. " 
        "If not provided, the Datashelf directory will be initialized in the current working directory.")
    init_parser.add_argument("-p", "--path", type = str, help = init_help_msg)
    init_parser.set_defaults(func=init_command)

    # Save command
    save_parser = subparsers.add_parser("save", help="Save a file to the Datashelf.")
    
    save_parser.add_argument("file_path", type=str, help="The path to the file to be saved.")
    save_parser.add_argument("name", type=str, help="The name to save the file as in the datashelf.")
    save_parser.add_argument("-m", "--message", type=str, help="An optional message describing the file being saved.")
    save_parser.add_argument("-t", "--tag", type=str, help="An optional tag to associate with the saved file.")
    save_parser.add_argument("--on-duplicate", type=str, choices=["skip", "error", "update"], default="skip", dest="on_duplicate",
                             help="How to handle duplicate data. One of 'skip', 'error', or 'update'. Defaults to 'skip'.")
    
    save_parser.set_defaults(func=save_file_command)

    # Load command
    load_parser = subparsers.add_parser("load", help = "Load a file from the datashelf.")
    load_parser.add_argument("lookup_key", type=str, help="Dataset name, full hash, or unique hash prefix.")
    load_parser.add_argument("-df", "--dataframe", action="store_true", dest="to_df", 
                             help="If set, load and display the artifact as a DataFrame.")
    load_parser.set_defaults(func = load_command)

    # List command
    ls_parser = subparsers.add_parser("list", help="List files currently registered in the datashelf.")
    ls_parser.add_argument("--filter_tag", type=str, nargs="+", 
                           help="Optional tag or tags used to filter displayed metadata entries.")
    ls_parser.set_defaults(func=ls_command)

    # Show command
    show_parser = subparsers.add_parser("show", help="Show metadata for a specific datashelf entry.")
    show_parser.add_argument("lookup_key", type=str, help="Dataset name, full hash, or hash prefix to inspect.")
    show_parser.set_defaults(func=show_command)

    # Checkout command
    checkout_parser = subparsers.add_parser("checkout", 
                                            help="Copy a stored artifact from the datashelf to a user-specified destination.")
    checkout_parser.add_argument("lookup_key", type=str, help="Dataset name, full hash, or unique hash prefix.")
    checkout_parser.add_argument("dest_path", type=str, 
                                 help="Destination file path to copy the artifact to. Should include file name and suffix.")
    checkout_parser.set_defaults(func=checkout_command)

    args = parser.parse_args()
    
    if hasattr(args, "func"):
        exit_code = args.func(args)
        sys.exit(exit_code)

    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
