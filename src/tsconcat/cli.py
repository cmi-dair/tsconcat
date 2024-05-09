"""CLI for tsconcat."""

import argparse
import json
import logging
import pathlib as pl
from collections.abc import Callable
from dataclasses import dataclass
from typing import Any, List, Optional

import bids2table.table
import elbow.dtypes  # noqa  makes pandas load json types as dicts from parquet
import pandas as pd

from tsconcat.b2t_columns import B2tColumn

from .concat import concat_nifti1_4d
from .pretreeprint import pretreeprint
from .utils import (
    build_bidsapp_group_parser,
    file_path_from_b2table_row,
    file_paths_from_b2table,
    sidecar_path_from_b2table_row,
)

# Set bids2table logger to error
logging.getLogger("bids2table").setLevel(logging.ERROR)

REDUCE_COLUMNS = [
    B2tColumn.Dataset,
    B2tColumn.Subject,
    B2tColumn.Session,
    B2tColumn.Run,
    B2tColumn.Description,
    B2tColumn.Space,
]
REDUCE_COLUMNS_SET = set(REDUCE_COLUMNS)
REDUCE_COLUMNS_ALIAS = {
    "dataset": B2tColumn.Dataset,
    "sub": B2tColumn.Subject,
    "subject": B2tColumn.Subject,
    "ses": B2tColumn.Session,
    "session": B2tColumn.Session,
    "run": B2tColumn.Run,
}


def _reduce_op(
    df: pd.DataFrame,
    group_by: List[str],
    inplace: bool = False,
    group_callback: Optional[Callable[[pd.DataFrame], None]] = None,
) -> pd.DataFrame:
    """Reduce dataframe to one row per group."""
    if not inplace:
        df = df.copy()

    group_by_set = set(group_by)

    unknown_cols = list(group_by_set - REDUCE_COLUMNS_SET)
    if len(unknown_cols) > 0:
        raise Exception(f"Unknown columns: {unknown_cols}")
    del unknown_cols

    df = df.sort_values(by=REDUCE_COLUMNS)

    group_by_columns = list(REDUCE_COLUMNS_SET - group_by_set)
    # Duplicate group_by columns in df to retain them
    # This used to be the default behavior of groupby.apply, but it was deprecated in pandas 2.2
    for col in group_by_columns:
        df[f"temp_copy_{col}"] = df[col]
    grouped = df.groupby(by=group_by_columns, dropna=False)

    def _func_reduce(df_group: pd.DataFrame) -> Optional[pd.Series]:
        if df_group.shape[0] == 0:
            print("empty group")
            return None

        # Name them back to normal
        df_group = df_group.rename(columns={f"temp_copy_{col}": col for col in group_by_columns})

        first_row: pd.Series = df_group.iloc[0]

        for group_label in group_by:
            first_row = first_row.copy()
            first_row[group_label] = None  # todo does vectorized work here?

        if group_callback is not None:
            group_callback(df_group)

        return first_row

    df_reduced = grouped.apply(func=_func_reduce, include_groups=False)
    df_reduced = df_reduced.reset_index(drop=True)

    return df_reduced


def _read_if_parquet(p: pl.Path, *args, **kwargs) -> Optional[pd.DataFrame]:  # noqa
    try:
        return pd.read_parquet(p, *args, **kwargs)
    except:  # noqa
        return None


def build_parser_tsconcat_bids_app() -> argparse.ArgumentParser:
    """Build parser for tsconcat BIDS app."""
    parser = build_bidsapp_group_parser(prog="ba-tsconcat", description="Concatenate MRI timeseries.")

    parser.add_argument(
        "-c",
        "--concat",
        type=str,
        help=f"Concat across. Can be any combination of {', '.join(REDUCE_COLUMNS_ALIAS.keys())} separated by spaces. "
        f"Output data will be grouped by the set difference.",
        default="ses",
    )

    parser.add_argument(
        "-d",
        "--dry_run",
        action="store_true",
        help="Dry run. Print output directory structure instead of actually doing something. "
        "If this is enabled 'bids_dir' may be a path to a bids2table parquet directory.",
        default=False,
    )

    parser.add_argument(
        "-f",
        "--fake",
        action="store_true",
        help="Fake output. Output a bids2table parquet directory instead of actually doing something.",
        default=False,
    )

    # workers
    parser.add_argument(
        "-w",
        "--workers",
        type=int,
        help="Number of workers for bids2table. Default is 1.",
        default=1,
    )

    return parser


@dataclass
class TSConcatSettings:
    """Settings for tsconcat."""

    input_dir: pl.Path
    output_dir: pl.Path
    concat_labels: List[str]
    dry_run: bool
    fake: bool
    workers: int

    @classmethod
    def from_args(cls, args: Any) -> "TSConcatSettings":  # noqa
        concat_labels = args.concat.split(" ")
        concat_set = set(REDUCE_COLUMNS_ALIAS.get(g, g) for g in concat_labels)

        return cls(
            input_dir=args.bids_dir,
            output_dir=args.output_dir,
            concat_labels=list(concat_set),
            dry_run=args.dry_run or args.fake,
            fake=args.fake,
            workers=args.workers,
        )


def main() -> None:
    """Concatenate MRI timeseries."""
    settings = TSConcatSettings.from_args(build_parser_tsconcat_bids_app().parse_args())

    if not settings.input_dir.exists():
        raise Exception("Input directory does not exist.")

    if settings.dry_run and (df := _read_if_parquet(settings.input_dir)) is not None:
        df = bids2table.table.flat_to_multi_columns(df)
    else:
        df = bids2table.bids2table(settings.input_dir, workers=settings.workers, with_meta=False)

        if df.shape[0] == 0:
            raise Exception("Empty BIDS dataset")

    if not settings.dry_run:
        settings.output_dir.mkdir(parents=True, exist_ok=True)

    df_bold = df.query(
        f"{B2tColumn.DataType} == 'func' and "
        f"{B2tColumn.FileExtension} == '.nii.gz' and "
        f"{B2tColumn.Suffix} == 'bold'"  # and "
        # "ent__desc == 'preproc' and "
        # "ent__space == 'MNI152NLin6ASym'"
    )  # fmt: skip

    if df_bold.shape[0] == 0:
        raise Exception("No BOLD files found")

    def _process_group(df_group: pd.DataFrame) -> None:
        group_identifiers = df_group.iloc[0][list(REDUCE_COLUMNS_SET - set(settings.concat_labels))].to_dict()
        print(f"Process group: {group_identifiers}")

        first_row: pd.Series = df_group.iloc[0]

        for group_label in settings.concat_labels:
            first_row = first_row.copy()
            first_row[group_label] = None

        # Generate file

        file_path = settings.output_dir / file_path_from_b2table_row(first_row)

        file_path.parent.mkdir(parents=True, exist_ok=True)
        try:
            concat_nifti1_4d(paths=df_group.finfo__file_path.values, out_path=file_path)
        except Exception as e:
            print(f"Warning: Could not concat group, skipping:\n{e}")
            return

        # Generate sidecar

        sidecar_path = settings.output_dir / sidecar_path_from_b2table_row(first_row)
        sidecar_contents = first_row[B2tColumn.MetaJson]  # TODO: Maybe add list of files that were concatenated?
        with open(sidecar_path, "w", encoding="utf-8") as fp:
            json.dump(sidecar_contents, fp)

    df_reduced_bold = _reduce_op(
        df_bold,
        group_by=settings.concat_labels,
        group_callback=None if settings.dry_run else _process_group,
    )

    if settings.fake:
        # You need this one, believe me
        df_reduced_bold = df_reduced_bold.astype(
            {B2tColumn.MetaJson: "json", B2tColumn.DatasetDescription: "json", B2tColumn.ExtraEntities: "json"}
        )
        df_reduced_bold.to_parquet(settings.output_dir)

    filepaths = file_paths_from_b2table(df_reduced_bold, include_sidecars=True)
    pretreeprint(filepaths)


if __name__ == "__main__":
    main()
