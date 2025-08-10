import pandas as pd
import numpy as np
import hashlib


def _hash_pandas_df(df: pd.DataFrame) -> str:
    df_hash_series = pd.util.hash_pandas_object(df)
    # Perform XOR on all hashes in series to get one, row-order-independent hash
    # The reduce functions is taking the binary version of each hash and performing XOR with the next hash
    # XOR returns 1 if 1 XOR 0 or 0 XOR 1, and 0 if 0 XOR 0 or 1 XOR 1
    reduced_hash = np.bitwise_xor.reduce(
        df_hash_series
    )  # applies row by row and combines output iteratively
    final_hash = hashlib.sha256(str(reduced_hash).encode()).hexdigest()

    return final_hash


def _hash_polars_df(df): ...
