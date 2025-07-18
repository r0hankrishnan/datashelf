import os
import hashlib
import pickle
import datetime
import json

def init():
    # Create datashelf folder
    ...

def save():
    # Take in a pd.DataFrame, save it as a pickle or csv (not sure which yet, maybe based on size) and store file name + metadata in log file
    ...

def ls():
    # List collection's log file
    ...

def load():
    # Load in a particular file from .datashelf folder by name
    ...
