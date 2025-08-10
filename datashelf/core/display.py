from typing import Literal
import yaml
from datashelf.utils.logging import setup_logger
from datashelf.utils.tools import _find_datashelf_root
import questionary
import textwrap
from rich.table import Table
from rich.console import Console


logger = setup_logger(__name__)


def ls(
    to_display: Literal["ds-md", "ds-coll", "coll-md", "coll-files"],
    collection_name: str = None,
):
    """User-facing function to display tables of either:
            - datashelf metadata
            - datashelf collections
            - collection metadata
            - collection files

    Args:
        to_display (Literal[&quot;ds): Choice of which the four above options to display
        collection_name (str, optional): Collection name. Only required if to_display is "coll-md" or "coll-files".
        If not supplied but needed, user will be prompted in the console for a collection name. Defaults to None.

    Raises:
        ValueError: Thrown if user inputs an invalid choice for to_display
    """

    if to_display not in ["ds-md", "ds-coll", "coll-md", "coll-files"]:
        err_msg = (
            f"{to_display} is not a valid value for to_display."
            "Please select one of the following based on what you want to display:\n"
            '\tdatashelf_metadata.yaml "metadata": "ds-md"'
            '\n\tdatashelf_metadata.yaml "collections": "ds-coll"'
            '\n\t{collection_name}_metadata.yaml "metadata": "coll-md"'
            '\n\t{collection_name}_metadata.yaml "files": "coll-files"'
        )
        logger.error(err_msg)
        raise ValueError(err_msg)

    else:

        if to_display == "ds-md":
            _display_datashelf_metadata(field="metadata")

        elif to_display == "ds-coll":
            _display_datashelf_metadata(field="collections")

        elif to_display == "coll-md":
            if not collection_name:
                collection_name = _collection_input()
                _display_collection_metadata(
                    collection_name=collection_name, field="metadata"
                )
            else:
                _display_collection_metadata(
                    collection_name=collection_name, field="metadata"
                )

        else:
            if not collection_name:
                collection_name = _collection_input()
                _display_collection_metadata(
                    collection_name=collection_name, field="files"
                )
            else:
                _display_collection_metadata(
                    collection_name=collection_name, field="files"
                )


def _collection_input():
    collection_names = _get_collection_list()

    input_msg = f"Select a collection to display: {', '.join(collection_names)}"

    return input(input_msg)


def _multiselect_ls(
    to_display: Literal["ds-md", "ds-coll", "coll-md", "coll-files"],
    collection_name: str = None,
):
    """CLI version of ls function. Has support for questionary-based arg selection

    Args:
        to_display (Literal[&quot;ds): Choice of which the four above options to display
        collection_name (str, optional): Collection name. Only required if to_display is "coll-md" or "coll-files".
        If not supplied but needed, user will be prompted in the console for a collection name. Defaults to None.

    Raises:
        ValueError: Thrown if user inputs an invalid choice for to_display
    """

    if to_display in ["ds-md", "ds-coll", "coll-md", "coll-files"]:

        if to_display == "ds-md":
            _display_datashelf_metadata(field="metadata")

        elif to_display == "ds-coll":
            _display_datashelf_metadata(field="collections")

        elif to_display == "coll-md":
            if not collection_name:
                collection_choices = _get_collection_list()
                collection_name = questionary.select(
                    message="Select a collection to display", choices=collection_choices
                ).ask()
                # collection_name = input("Collection name? ")
                _display_collection_metadata(
                    collection_name=collection_name, field="metadata", terminal=True
                )
            else:
                _display_collection_metadata(
                    collection_name=collection_name, field="metadata", terminal=True
                )

        else:
            if not collection_name:
                collection_choices = _get_collection_list()
                collection_name = questionary.select(
                    message="Select a collection to display", choices=collection_choices
                ).ask()
                # collection_name = input("Collection name? ")
                _display_collection_metadata(
                    collection_name=collection_name, field="files", terminal=True
                )
            else:
                _display_collection_metadata(
                    collection_name=collection_name, field="files", terminal=True
                )

    else:
        err_msg = (
            f"{to_display} is not a valid value for to_display."
            "Please select one of the following based on what you want to display:\n"
            '\tdatashelf_metadata.yaml "metadata": "ds-md"'
            '\n\tdatashelf_metadata.yaml "collections": "ds-coll"'
            '\n\t{collection_name}_metadata.yaml "metadata": "coll-md"'
            '\n\t{collection_name}_metadata.yaml "files": "coll-files"'
        )
        logger.error(err_msg)
        raise ValueError(err_msg)


def _display_datashelf_metadata(
    field=Literal["metadata", "collections"], terminal: bool = False
):

    if field not in ["metadata", "collections"]:
        err_msg = (
            f'field must be either "metadata" or "collections". {field} is invalid.'
        )
        logger.error(err_msg)
        raise ValueError(err_msg)
    try:
        datashelf_path = _find_datashelf_root(return_datashelf_path=True)
        datashelf_metadata_path = datashelf_path / "datashelf_metadata.yaml"
    except Exception as e:
        err_msg = f"An error occured. Make sure you are in the same directory as your .datashelf folder."
        logger.error(err_msg)
        raise ValueError(e)

    with open(datashelf_metadata_path, "r") as f:
        data = yaml.safe_load(f)

    if field == "metadata" and terminal:
        console = Console(force_terminal=True)
        table = _render_rich_datashelf_table(data=data, field="metadata")

        console.print(table)

    elif field == "metadata" and not terminal:
        console = Console(width=200, force_terminal=True)
        table = _render_rich_datashelf_table(data=data, field="metadata")

        console.print(table)

    elif field == "collections" and terminal:
        console = Console(force_terminal=True)
        table = _render_rich_datashelf_table(data=data, field="collections")

        console.print(table)

    else:
        console = Console(width=200, force_terminal=True)
        table = _render_rich_datashelf_table(data=data, field="collections")

        console.print(table)


def _display_collection_metadata(
    collection_name: str, field=Literal["metadata", "files"], terminal: bool = False
):
    if field not in ["metadata", "files"]:
        err_msg = f'field must be either "metadata" or "files". {field} is invalid.'
        logger.error(err_msg)
        raise ValueError(err_msg)

    try:
        datashelf_path = _find_datashelf_root(return_datashelf_path=True)
        collection_path = datashelf_path / collection_name.lower().replace(" ", "_")
        collection_metadata_path = (
            collection_path
            / f'{collection_name.strip().lower().replace(" ", "_")}_metadata.yaml'
        )
    except Exception as e:
        err_msg = f"An error occured. Make sure you are in the same directory as your .datashelf folder."
        logger.error(err_msg)
        raise ValueError(e)

    with open(collection_metadata_path, "r") as f:
        data = yaml.safe_load(f)

    if field == "metadata" and terminal:
        console = Console(force_terminal=True)
        table = _render_rich_collection_table(data=data, field="metadata")

        console.print(table)

    elif field == "metadata" and not terminal:
        console = Console(width=200, force_terminal=True)
        table = _render_rich_collection_table(data=data, field="metadata")

        console.print(table)

    elif field == "files" and terminal:
        console = Console(force_terminal=True)
        table = _render_rich_collection_table(data=data, field="files")

        console.print(table)

    else:
        console = Console(width=200, force_terminal=True)
        table = _render_rich_collection_table(data=data, field="files")

        console.print(table)


def _render_rich_datashelf_table(data: dict, field: Literal["metadata, collections"]):
    if field == "metadata":
        console = Console()

        data_row = data["metadata"]

        table = Table(show_header=True, header_style="bold #A5B4FC", show_lines=True)

        for key in data_row.keys():
            table.add_column(key)

        row_values = []
        for _, v in data_row.items():
            row_values.append("" if v is None else str(v))

        table.add_row(*row_values)

        return table

    elif field == "collections":

        table = Table(show_header=True, header_style="bold #A5B4FC", show_lines=True)

        for key in data["collections"][0].keys():
            table.add_column(key)

        for row in data["collections"]:
            new_row = []
            for _, v in row.items():
                new_row.append("" if v is None else str(v))
            table.add_row(*new_row)

        return table

    else:
        err_msg = f'{field} is not a valid value for to_display arg. Should be either "metadata" or "files"'
        logger.error(err_msg)
        raise ValueError(err_msg)


def _render_rich_collection_table(data: dict, field: Literal["metadata", "files"]):
    if field == "metadata":

        def wrap_text(text, width):
            if text is None:
                return ""
            return "\n".join(textwrap.wrap(str(text), width=width))

        data_row = data["metadata"]

        table = Table(show_header=True, header_style="bold #A5B4FC", show_lines=True)

        for key in data_row.keys():
            # For fields like hash, disable wrapping to show full value
            table.add_column(key)

        row_values = []
        for k, v in data_row.items():
            row_values.append("" if v is None else str(v))

        table.add_row(*row_values)

        return table

    elif field == "files":

        def wrap_text(text, width):
            if text is None:
                return ""
            elif " " in text:
                # has spaces, just wrap normally
                return "\n".join(textwrap.wrap(text, width=width))

            return "\n".join(text[i : i + width] for i in range(0, len(text), width))

        table = Table(show_header=True, header_style="bold #A5B4FC", show_lines=True)

        for key in data["files"][0].keys():
            if key == "hash":
                # Show full hash, no wrapping, no truncation
                table.add_column(key, min_width=15, max_width=40, overflow="fold")
            elif key in ("file_path", "message"):
                table.add_column(key, min_width=15, max_width=40, overflow="fold")
            else:
                table.add_column(key, min_width=15, max_width=40, overflow="fold")

        for row in data["files"]:
            new_row = []
            for _, v in row.items():
                new_row.append("" if v is None else str(v))
            table.add_row(*new_row)

        return table

    else:
        err_msg = f'{field} is not a valid value for to_display arg. Should be either "metadata" or "files"'
        logger.error(err_msg)
        raise ValueError(err_msg)


def _get_collection_list():
    datashelf_path = _find_datashelf_root(return_datashelf_path=True)
    datashelf_metadata_path = datashelf_path / "datashelf_metadata.yaml"

    with open(datashelf_metadata_path, "r") as f:
        data = yaml.safe_load(f)

    collection_choices = data["metadata"]["collections"]

    return collection_choices
