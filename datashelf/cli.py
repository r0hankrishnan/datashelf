#!/usr/bin/env python3
"""
Command-line interface for datashelf
"""
import argparse
import sys

# Import your existing functions
from datashelf.core import init, create_collection, ls, checkout


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

def ls_command(args):
    # Run ls() when user types datashelf ls to_display
    try:
        ls(to_display=args.to_display)
        return 0
    except Exception as e:
        print(f"Error displaying data: {e}", file = sys.stderr)
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
    ls_parser.add_argument('to_display', help='Choose from [ds-md, ds-coll, coll-md, coll-files]')
    ls_parser.set_defaults(func=ls_command)
    
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