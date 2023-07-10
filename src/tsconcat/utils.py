import argparse
import datetime
import pathlib as pl
import time
from contextlib import contextmanager


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
