import os
from datashelf.utils.tools import _find_datashelf_root, _get_collection_files
from datashelf.utils.shelf import _make_datashelf_metadata_structure, \
    _update_datashelf_metadata_with_added_collection, _update_datashelf_metadata_with_added_file_in_collection
from datashelf.utils.collection import _make_collection_metadata_structure, \
    _add_file_to_collection_metadata, _update_config_metadata
from datashelf.utils.hashing import _hash_pandas_df
from datashelf.utils.logging import setup_logger
import pandas as pd

logger = setup_logger(__name__)

def load():
    ...
    
def checkout():
    ...