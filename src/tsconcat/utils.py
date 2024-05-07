"""Utility functions for tsconcat."""

import argparse
import datetime
import pathlib as pl
import time
from contextlib import contextmanager
from typing import Generator, List

import bids2table.table
import pandas as pd

from tsconcat.b2t_columns import B2tColumn


@contextmanager
def timeprint(title: str) -> Generator[None, None, None]:
    """Context manager to print the time elapsed between entering and exiting the context.

    Args:
        title: Title to be printed before and after the context.
    """
    print(f"Start: {title}")
    start = time.perf_counter()
    yield
    duration = time.perf_counter() - start
    print(f"Done: {title} - {datetime.timedelta(seconds=duration)}")


def build_bidsapp_group_parser(*args, **kwargs) -> argparse.ArgumentParser:  # noqa
    """Build a parser skeleton for the BIDS App group level.

    Args:
        args: Positional arguments to be passed to ArgumentParser costructor.
        kwargs: Keyword arguments to be passed to ArgumentParser costructor.
    """
    parser = argparse.ArgumentParser(*args, **kwargs)
    parser.add_argument(
        "bids_dir",
        action="store",
        type=pl.Path,
        help="Input BIDS folder path.",
    )
    parser.add_argument(
        "output_dir",
        action="store",
        type=pl.Path,
        help="Output BIDS folder path.",
    )
    parser.add_argument("analysis_level", default="group", choices=["group"], help='Processing stage, must be "group".')
    return parser


def file_paths_from_b2table(df: pd.DataFrame, include_sidecars: bool = False, inplace: bool = False) -> List[pl.Path]:
    """Generate list of filepaths from bids2table dataframe."""
    # b2t crashes if sidecar is not None
    if not inplace:
        df = df.copy()
    df[B2tColumn.MetaJson] = None

    paths = list(df.apply(func=lambda row: bids2table.table.join_bids_path(row), axis=1).values)

    if include_sidecars:
        sidecar_paths = list(
            df.apply(
                func=lambda row: bids2table.table.join_bids_path({**row, B2tColumn.FileExtension: ".json"}),
                axis=1,
            ).values
        )
        return paths + sidecar_paths

    return paths


def file_path_from_b2table_row(row: pd.Series, inplace: bool = False, sidecar: bool = False) -> pl.Path:
    """Generate list of filepaths from bids2table dataframe."""
    # b2t crashes if sidecar is not None
    if not inplace:
        row = row.copy()
    row[B2tColumn.MetaJson] = None

    if sidecar:
        row = {**row, B2tColumn.FileExtension: ".json"}

    return bids2table.table.join_bids_path(row)


def sidecar_path_from_b2table_row(row: pd.Series, inplace: bool = False) -> pl.Path:
    """Generate list of filepaths from bids2table dataframe."""
    # b2t crashes if sidecar is not None
    if not inplace:
        row = row.copy()
    row[B2tColumn.MetaJson] = None

    return bids2table.table.join_bids_path({**row, B2tColumn.FileExtension: ".json"})
