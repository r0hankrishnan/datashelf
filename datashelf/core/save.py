import pandas as pd
from pathlib import Path
import shutil
from datashelf.utils.tools import _find_datashelf_root, _get_collection_files
from datashelf.core.metadata import (
    _get_next_version_number,
    _add_file_to_collection_metadata,
    _update_collection_metadata_info,
    _update_datashelf_metadata_collection_files,
)
from datashelf.utils.hashing import _hash_pandas_df
from datashelf.utils.logging import setup_logger
from datashelf.core.config import check_tag_enforcement, get_allowed_tags

logger = setup_logger(__name__)


def save(df: pd.DataFrame, collection_name: str, name: str, tag: str, message: str):
    """User-facing function to save a data frame to a collection folder

    Args:
        df (pd.DataFrame): DataFrame (pandas class) to save
        collection_name (str): Name of collection to save to
        name (str): Name of data
        tag (str): Tag for data
        message (str): Message for data

    Raises:
        ValueError: Invalid tag.
        ValueError: Trying to use Polars Data Frame before implemented.
        ValueError: Trying to use some other data type that's unsupported.

    Returns:
        _type_: _description_
    """

    # Tag checking
    tags_enforced = check_tag_enforcement()
    allowed_tags = get_allowed_tags()

    if tags_enforced and tag not in allowed_tags:
        err_msg = (
            f"{tag} is not a valid tag."
            f"Tag enforcement is currently set to {tags_enforced}."
            f"You cannot change enforcement as of this version of DataShelf."
            f'Please use one of the following allowed tags {", ".join(allowed_tags)}'
        )
        logger.error(err_msg)
        raise ValueError(err_msg)

    # Run pandas process if passed a pandas df
    if isinstance(df, pd.DataFrame):
        _pandas_save_df(df, collection_name, name, tag, message)
        return 0

    # Return err msg for polars
    elif isinstance(df, pl.DataFrame):
        err_msg = "Polars not currently supported, sorry!"
        logger.error(err_msg)
        raise ValueError(err_msg)

    # Return err for all other types
    else:
        err_msg = "Unsupported data type. DataShelf only supports pandas DataFrames at the moment."
        logger.error(err_msg)
        raise ValueError(err_msg)


################################################################################
# Helper functions for parsing and saving pandas data frames
################################################################################


def _pandas_save_df(
    df: pd.DataFrame, collection_name: str, name: str, tag: str, message: str
):

    hashed_df = _hash_pandas_df(df)
    collection_files = _get_collection_files(collection_name=collection_name)
    file_name = f'{name.lower().replace(" ", "_")}_{tag}'
    collection_path = _find_datashelf_root(
        return_datashelf_path=True
    ) / collection_name.lower().replace(" ", "_")
    file_path_base = collection_path / file_name

    version_number = _get_next_version_number(
        collection_name=collection_name, collection_path=collection_path
    )

    if version_number == 1:
        file_type = _pandas_assign_smart_save(df=df)
        file_path = str(file_path_base) + file_type

        _save_and_register_df(
            df=df,
            file_type=file_type,
            collection_name=collection_name,
            file_name=name,
            tag=tag,
            message=message,
            df_hash=hashed_df,
            version=version_number,
            file_path=file_path,
            collection_path=collection_path,
        )

        logger.info(f"{name} added to {collection_name}")
        return 0

    elif len(collection_files) > 1:
        for _, file in enumerate(collection_files):
            if file["hash"] == hashed_df:
                logger.info(
                    f"{name}'s hash matches a dataframe that is already saved in datashelf: {file['name']}."
                )
                return 1
            else:
                pass

        file_type = _pandas_assign_smart_save(df=df)
        file_path = str(file_path_base) + file_type

        _save_and_register_df(
            df=df,
            file_type=file_type,
            collection_name=collection_name,
            file_name=name,
            tag=tag,
            message=message,
            df_hash=hashed_df,
            version=version_number,
            file_path=file_path,
            collection_path=collection_path,
        )

        logger.info(f"{name} added to {collection_name}")
        return 0

    else:
        err_msg = (
            f"There are 0 files in {collection_name}'s metadata file. "
            "Something went wrong with it's initialization. "
            "Please try recreating the collection or raise an issue on GitHub!"
        )
        logger.error(err_msg)
        raise ValueError(err_msg)


def _pandas_assign_smart_save(df: pd.DataFrame):

    df_size = df.memory_usage(deep=True).sum()

    threshold = 10 * 1024 * 1024  # 10MB

    if df_size < threshold:
        logger.info(f"Save as CSV ({df_size / 1e6:.2f} MB)")
        return ".csv"
    else:
        logger.info(f"Save as Parquet ({df_size / 1e6:.2f} MB)")
        return ".parquet"


################################################################################
# Helper functions for saving and parsing Polars data frames
################################################################################


def _save_polars_data_frame(
    df: pd.DataFrame, collection_name: str, name: str, tag: str, message: str
): ...


def _polars_assign_smart_save(df: pd.DataFrame): ...


################################################################################
# General save and metadata updating logic
################################################################################


def _save_and_register_df(
    df,
    file_type: str,
    collection_name: str,
    file_name: str,
    tag: str,
    message: str,
    df_hash: str,
    version: int,
    file_path: str,
    collection_path: str,
):
    """Primary helper function to save df to appropriate location and update all relevant metadata

    Args:
        df (_type_): Data frame
        file_type (str): File extension type determined by helper func
        collection_name (str): Collection name
        file_name (str): File name (set by user)
        tag (str): File tag
        message (str): File message
        df_hash (str): Data frame hash calculated by helper func
        version (int): Version number
        file_path (str): Data file path
        collection_path (str): Collection folder file path

    Returns:
        int: 0 if success else error
    """

    if file_type == ".csv":
        df.to_csv(file_path, index=False)
        _add_file_to_collection_metadata(
            collection_name=collection_name,
            file_name=file_name,
            tag=tag,
            message=message,
            df_hash=df_hash,
            version=version,
            file_path=file_path,
        )
        _update_collection_metadata_info(
            collection_name=collection_name,
            saved_df_file_path=file_path,
            new_version=version,
        )
        _update_datashelf_metadata_collection_files(
            collection_name=collection_name, collection_path=collection_path
        )

        return 0

    else:
        df.to_parquet(file_path, index=False)
        _add_file_to_collection_metadata(
            collection_name=collection_name,
            file_name=file_name,
            tag=tag,
            message=message,
            df_hash=df_hash,
            version=version,
            file_path=file_path,
        )
        _update_collection_metadata_info(
            collection_name=collection_name,
            saved_df_file_path=file_path,
            new_version=version,
        )
        _update_datashelf_metadata_collection_files(
            collection_name=collection_name, collection_path=collection_path
        )

        return 0


################################################################################
# CLI save functions for files
################################################################################


def _save_from_file(
    file_path: str,
    collection_name: str,
    name: str,
    tag: str,
    message: str,
    duplicate: bool = False,
):

    path = Path(file_path)

    # Check for valid file type- only support csv and parquet for now
    if path.suffix not in [".csv", ".parquet"]:
        err_msg = f"DataShelf only supports csv and parquet files at the moment. Please convert your file to one of those two formats."
        logger.error(err_msg)
        raise TypeError(err_msg)

    # Check that filepath is valid
    if path.exists():
        pass
    else:
        err_msg = (
            f"File path {file_path} does not exist."
            " Make sure you enter a valid file path."
        )

    # Tag checking
    tags_enforced = check_tag_enforcement()
    allowed_tags = get_allowed_tags()

    if tags_enforced and tag not in allowed_tags:
        err_msg = (
            f"{tag} is not a valid tag."
            f"Tag enforcement is currently set to {tags_enforced}."
            f"You cannot change enforcement as of this version of DataShelf."
            f'Please use one of the following allowed tags {", ".join(allowed_tags)}'
        )
        logger.error(err_msg)
        raise ValueError(err_msg)

    file_type = path.suffix
    new_file_name = f'{name.lower().replace(" ", "_")}_{tag.lower()}' + file_type
    datashelf_path = _find_datashelf_root(return_datashelf_path=True)
    collection_path = datashelf_path / f'{collection_name.lower().replace(" ", "_")}'
    new_path = collection_path / new_file_name
    version_number = _get_next_version_number(
        collection_name=collection_name, collection_path=collection_path
    )

    if file_type == ".csv":
        data = pd.read_csv(filepath_or_buffer=str(path))
        hashed_df = _hash_pandas_df(data)
    else:
        data = pd.read_parquet(path=str(path))
        hashed_df = _hash_pandas_df(data)

    if duplicate:
        shutil.copy2(str(path), str(new_path))
        _add_file_to_collection_metadata(
            collection_name=collection_name,
            file_name=name,
            tag=tag,
            message=message,
            df_hash=hashed_df,
            version=version_number,
            file_path=str(new_path),
        )
        _update_collection_metadata_info(
            collection_name=collection_name,
            saved_df_file_path=str(new_path),
            new_version=version_number,
        )
        _update_datashelf_metadata_collection_files(
            collection_name=collection_name, collection_path=str(collection_path)
        )
        logger.info(
            f'File duplicated to {collection_name.lower().replace(" " , "_")} successfully.'
        )

        return 0

    else:
        shutil.move(str(path), str(new_path))
        _add_file_to_collection_metadata(
            collection_name=collection_name,
            file_name=name,
            tag=tag,
            message=message,
            df_hash=hashed_df,
            version=version_number,
            file_path=str(new_path),
        )
        _update_collection_metadata_info(
            collection_name=collection_name,
            saved_df_file_path=str(new_path),
            new_version=version_number,
        )
        _update_datashelf_metadata_collection_files(
            collection_name=collection_name, collection_path=collection_path
        )
        logger.info(
            f'File moved to {collection_name.lower().replace(" ", "_")} successfully.'
        )

        return 0
