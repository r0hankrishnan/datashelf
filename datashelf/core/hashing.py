import hashlib
import pandas as pd
from pathlib import Path
from typing import Literal

def sha256_hex(data_path: Path, chunk_size = 8192):
    """Given a file path, open the file, read its bytes in chunks of
    8192, hash each chunk with sha256, update the hash until all chunks
    have been read.

    Args:
        tmpdata (Path): Path to temporary data file
        chunk_size (int, optional): Size of chunks to read in file. Defaults to 8192.

    Returns:
        str: The sha256 hex of the file hash. 
    """
    with open(data_path, "rb") as f:
        file_hash = hashlib.sha256()
        
        while chunk := f.read(chunk_size):
            file_hash.update(chunk)
        
    return file_hash.hexdigest()

    
def make_temp_parquet(data: Path | str | pd.DataFrame, output_path: Path, engine: Literal["pyarrow", "fastparquet"]) -> Path:
    output_path.parent.mkdir(parents = True, exist_ok = True)
    
    if isinstance(data, (Path, str)):
        data_path: Path = Path(data).resolve()
    
        if not data_path.exists():
            raise FileNotFoundError(f"Could not find data file at {data_path}")
        
        suffix = data_path.suffix.lower()

        if suffix == ".csv":
            df = pd.read_csv(data_path)
    
        elif suffix == ".parquet":
            df = pd.read_parquet(data_path, engine = engine)
            
        elif suffix == ".xlsx":
            df = pd.read_excel(data_path)
            
        elif suffix == ".json":
            df = pd.read_json(data_path)
    
    else:
        if not isinstance(data, pd.DataFrame):
            raise TypeError("Instance must be a dataframe of type pd.DataFrame or a file path of type str or Path.")
        
        df = data.copy()
    
    try:
        object_cols = df.select_dtypes(include = ["object"]).columns
        if len(object_cols) > 0:
            df[object_cols] = df[object_cols].astype("string")

        df.to_parquet(output_path, engine = engine, index = False)
        
    except Exception as e:
        msg = (
            f"Something went wrong when trying to convert {data} to parquet."
            "\n\nCurrently, the loading function works best with unambigous tabluar data."
        )
        raise RuntimeError(msg) from e
        
    return output_path.resolve()