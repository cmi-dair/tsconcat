import argparse
import datetime
import pathlib as pl
import time
from contextlib import contextmanager
from typing import List

import bids2table.helpers
import pandas as pd


@contextmanager
def timeprint(title: str):
    """
    Context manager to print the time elapsed between entering and exiting the
    context.

    Args:
        title: Title to be printed before and after the context.
    """
    print(f"Start: {title}")
    start = time.perf_counter()
    yield
    duration = time.perf_counter() - start
    print(f"Done: {title} - {datetime.timedelta(seconds=duration)}")


def build_bidsapp_group_parser(*args, **kwargs):
    """
    Build a parser skeleton for the BIDS App group level.

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
    parser.add_argument(
        "analysis_level", choices=["group"], help='Processing stage, must be "group".'
    )
    return parser


def file_paths_from_b2table(df: pd.DataFrame, inplace=False) -> List[pl.Path]:
    """Generate list of filepaths from bids2table dataframe."""

    # b2t crashes if sidecar is not None
    if not inplace:
        df = df.copy()
    df['sidecar'] = None

    paths_series: pd.Series = df.apply(
        func=lambda row: bids2table.helpers.join_bids_path(row),
        axis=1
    )
    return list(paths_series.values)


def file_path_from_b2table_row(row: pd.Series, inplace=False, sidecar=False) -> pl.Path:
    """Generate list of filepaths from bids2table dataframe."""

    # b2t crashes if sidecar is not None
    if not inplace:
        row = row.copy()
    row['sidecar'] = None

    if sidecar:
        row = {**row, "ext": ".json"}

    return bids2table.helpers.join_bids_path(row)


def sidecar_path_from_b2table_row(row: pd.Series, inplace=False) -> pl.Path:
    """Generate list of filepaths from bids2table dataframe."""

    # b2t crashes if sidecar is not None
    if not inplace:
        row = row.copy()
    row['sidecar'] = None

    return bids2table.helpers.join_bids_path({**row, "ext": ".json"})
