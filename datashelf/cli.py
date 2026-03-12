import argparse
import sys
from pathlib import Path

from datashelf import init, save, checkout, ls, show, load


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
        if args.path:
            init(custom_path=args.path)
        else:
            init()
        return 0
    except Exception as e:
        print(f"Error initializing datashelf directory: {e}", file=sys.stderr)
        return 1


def save_file_command(args):
    """Save a file to the datashelf.

    Args:
        args (_type_): The arguments passed from the command line. It should contain the following attributes:
            - file_path (str): The path to the file to be saved.
            - name (str): The name to save the file as in the datashelf.
            - message (str, optional): An optional message describing the file being saved.
            - tag (str, optional): An optional tag to associate with the saved file.

    Returns:
        int: 0 if the file was saved successfully, 1 otherwise.
    """

    filepath_obj = Path(args.file_path)
    if not filepath_obj.exists():
        print(f"Error: File {args.file_path} does not exist.", file=sys.stderr)
        return 1

    name = args.name.strip() if args.name else ""
    if not name:
        print("Error: Name cannot be empty.", file=sys.stderr)
        return 1

    message = args.message.strip() if args.message else ""
    tag = args.tag.strip() if args.tag else ""

    try:
        save(data=args.file_path, name=name, message=message, tag=tag)
        return 0

    except Exception as e:
        print(f"Error saving file: {e}", file=sys.stderr)
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
        print(result)

        return 0

    except Exception as e:
        print(f"Error loading file: {e}", file=sys.stderr)
        return 1


def ls_command(args):
    """List files currently registered in the datashelf.

    Args:
        args: The arguments passed from the command line. It should contain:
            - filter_tag (list[str] | str | None, optional): Optional tag or tags used to
              filter displayed metadata entries.

    Returns:
        int: 0 if the list command completed successfully, 1 otherwise.
    """
    try:
        ls(filter_tag=args.filter_tag)
        return 0

    except Exception as e:
        print(f"Error listing files: {e}", file=sys.stderr)
        return 1


def show_command(args):
    """Show metadata for a specific datashelf entry.

    Args:
        args: The arguments passed from the command line. It should contain:
            - lookup_key (str): Dataset name, full hash, or hash prefix to inspect.

    Returns:
        int: 0 if matching metadata was displayed successfully, 1 otherwise.
    """
    try:
        show(lookup_key=args.lookup_key)
        return 0

    except Exception as e:
        print(f"Error showing metadata: {e}", file=sys.stderr)
        return 1


def checkout_command(args):
    """Copy a stored artifact from the datashelf to a user-specified destination.

    Args:
        args: The arguments passed from the command line. It should contain:
            - lookup_key (str): Dataset name, full hash, or unique hash prefix.
            - dest (str): Destination file path to copy the artifact to.

    Returns:
        int: 0 if the checkout completed successfully, 1 otherwise.
    """
    try:
        checkout(lookup_key=args.lookup_key, dest=args.dest)
        return 0

    except Exception as e:
        print(f"Error checking out file: {e}", file=sys.stderr)
        return 1


def main():
    parser = argparse.ArgumentParser(description="Datashelf CLI")
    subparsers = parser.add_subparsers(title="Commands", dest="command")

    # Init command
    init_parser = subparsers.add_parser(
        "init", help="Initialize a datashelf directory."
    )
    init_parser.add_argument(
        "--path",
        type=str,
        help="Optional path to initialize the datashelf directory. If not provided, the datashelf directory will be initialized in the current working directory.",
    )
    init_parser.set_defaults(func=init_command)

    # Save command
    save_parser = subparsers.add_parser("save", help="Save a file to the datashelf.")
    save_parser.add_argument(
        "file_path", type=str, help="The path to the file to be saved."
    )
    save_parser.add_argument(
        "name", type=str, help="The name to save the file as in the datashelf."
    )
    save_parser.add_argument(
        "--message",
        type=str,
        help="An optional message describing the file being saved.",
    )
    save_parser.add_argument(
        "--tag", type=str, help="An optional tag to associate with the saved file."
    )
    save_parser.set_defaults(func=save_file_command)

    # Load command
    load_parser = subparsers.add_parser("load", help="Load a file from the datashelf.")
    load_parser.add_argument(
        "lookup_key", type=str, help="Dataset name, full hash, or unique hash prefix."
    )
    load_parser.add_argument(
        "--df",
        action="store_true",
        dest="to_df",
        help="If set, load and display the artifact as a DataFrame.",
    )
    load_parser.set_defaults(func=load_command)

    # List command
    ls_parser = subparsers.add_parser(
        "list", help="List files currently registered in the datashelf."
    )
    ls_parser.add_argument(
        "--filter_tag",
        type=str,
        nargs="+",
        help="Optional tag or tags used to filter displayed metadata entries.",
    )
    ls_parser.set_defaults(func=ls_command)

    # Show command
    show_parser = subparsers.add_parser(
        "show", help="Show metadata for a specific datashelf entry."
    )
    show_parser.add_argument(
        "lookup_key",
        type=str,
        help="Dataset name, full hash, or hash prefix to inspect.",
    )
    show_parser.set_defaults(func=show_command)

    # Checkout command
    checkout_parser = subparsers.add_parser(
        "checkout",
        help="Copy a stored artifact from the datashelf to a user-specified destination.",
    )
    checkout_parser.add_argument(
        "lookup_key", type=str, help="Dataset name, full hash, or unique hash prefix."
    )
    checkout_parser.add_argument(
        "dest", type=str, help="Destination file path to copy the artifact to."
    )
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
