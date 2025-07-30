#!/usr/bin/env python3
"""
Command-line interface for datashelf
"""
import argparse
import sys
from pathlib import Path
import questionary

# Import your existing functions
from datashelf.core import init, create_collection, checkout
from datashelf.core.display import _multiselect_ls, _get_collection_list
from datashelf.core.save import _save_from_file
from datashelf.core.config import get_allowed_tags


def init_command(args):
    #Run init() when user types datashelf init
    try:
        if args.path:
            init(set_dir=args.path)
        else:
            init()
        return 0
    except Exception as e:
        print(f"Error initializing datashelf directory: {e}", file=sys.stderr)
        return 1

def create_command(args):
    # Run create_collection() when user types datashelf create-collection name
    try:
        create_collection(collection_name=args.name)
        return 0
    except Exception as e:
        print(f"Error creating collection: {e}", file=sys.stderr)
        return 1
    
def multiselect_ls_command(args):
    # Run multiselect_ls() when user types datashelf ls to_display
    try:
        _multiselect_ls(to_display=args.to_display)
        return 0
    except Exception as e:
        print(f"Error displaying data: {e}", file = sys.stderr)
        return 1
    
def save_from_file_command(args):
    # Run save_from_file() when user types datashelf save <args>
    
    # Prompt interactively for missing arguments
    if not args.file_path:
        args.file_path = input("Enter the path to the file: ").strip().replace('"', '').replace("'","")

    if not args.collection_name:
        collection_choices = _get_collection_list()
        answer = questionary.select(
            message = "Select a collection to add file to: ",
            choices = collection_choices
        ).ask()
        if not answer:
            sys.exit(1)
        args.collection_name = answer.strip()

    if not args.name:
        args.name = input("Enter a name for the file: ").strip()

    if not args.tag:
        tag_options = get_allowed_tags()
        answer = questionary.select(
            message="Select a tag for the file: ",
            choices=tag_options
        ).ask()
        if not answer:
            sys.exit(1)
        args.tag = answer.strip()

    if not args.message:
        args.message = input("Enter a commit message for the save: ").strip()

    # Validate file existence
    file_path_obj = Path(args.file_path)
    if not file_path_obj.exists():
        print(f"Error: File {args.file_path} does not exist.", file=sys.stderr)
        return 1

    # Validate file type
    if file_path_obj.suffix not in [".csv", ".parquet"]:
        print("Error: Only .csv and .parquet files are supported.", file=sys.stderr)
        return 1

    if not args.name.strip():
        print("Error: Name cannot be empty.", file=sys.stderr)
        return 1
    
    try:
        _save_from_file(
            file_path=args.file_path,
            collection_name=args.collection_name,
            name=args.name,
            tag=args.tag,
            message=args.message,
            duplicate=args.duplicate
        )
        return 0
        
    except Exception as e:
        print(f"Error saving file: {e}", file = sys.stderr)
        return 1
        
    
def checkout_command(args):
    # Run checkout() when user types datashelf checkout name hash_value
    try:
        checkout(collection_name=args.collection_name, hash_value=args.hash)
        return 0
    except Exception as e:
        print(f"Error displaying data: {e}", file = sys.stderr)
        return 1

def main():
    # Define CLI entry point
    parser = argparse.ArgumentParser(
        prog='datashelf',
        description='A simple git-like version control system for datasets'
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Init command
    init_parser = subparsers.add_parser('init', help='Initialize a new datashelf directory')
    init_parser.add_argument('--path', help='Directory to initialize datashelf in (default: current directory)')
    init_parser.set_defaults(func=init_command)
    
    # Create collection command
    create_parser = subparsers.add_parser('create-collection', help='Create a new collection in .datashelf/')
    create_parser.add_argument('name', help='Name of the collection to create')
    create_parser.set_defaults(func=create_command)
    
    # ls command
    ls_parser = subparsers.add_parser('ls', help = 'Display metadata of .datashelf/ or specific collections')
    ls_parser.add_argument('to_display', help=('Please select one of the following based on what you want to display:\n'
                                                          '\tdatashelf_metadata.yaml "metadata": ds-md'
                                                          '\n\tdatashelf_metadata.yaml "collections": ds-coll'
                                                          '\n\t{collection_name}_metadata.yaml "metadata": coll-md'
                                                          '\n\t{collection_name}_metadata.yaml "files": coll-files'))
    ls_parser.set_defaults(func=multiselect_ls_command)
    
    # save command
    save_parser = subparsers.add_parser('save', help = 'Save a file to a collection in .datashelf/')
    save_parser.add_argument('--file_path', help = "Path of the file you want to save")
    save_parser.add_argument('--collection_name', help = "Name of collection you want to save file into")
    save_parser.add_argument('--name', help = "Name for the file")
    save_parser.add_argument('--tag', help = "Tag for the file")
    save_parser.add_argument('--message', help = "Commit message describing the file")
    save_parser.add_argument('--duplicate','-d', action="store_true", help = "Include if you want file to be duplicated to .datashelf/ instead of moved.")
    save_parser.set_defaults(func=save_from_file_command)

    # checkout command
    checkout_parser = subparsers.add_parser('checkout', help = 'Checkout a dataset from your collection. Data set will be copied to the same directory that .datashelf/ is in.')
    checkout_parser.add_argument('collection_name', help = "Select the collection to checkout from.")
    checkout_parser.add_argument('hash', help = "Enter the hash of the dataset you want to checkout")
    checkout_parser.set_defaults(func=checkout_command)
    
    # Parse arguments
    args = parser.parse_args()
    
    # If no command is provided, show help
    if not args.command:
        parser.print_help()
        return 1
    
    # Execute the command
    return args.func(args)


if __name__ == '__main__':
    sys.exit(main())