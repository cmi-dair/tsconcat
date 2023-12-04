"""CLI for tsconcat."""

import json
import pathlib as pl
from collections.abc import Callable
from typing import List, Optional

import bids2table.helpers
import elbow.dtypes  # noqa  makes pandas load json types as dicts from parquet
import elbow.utils
import pandas as pd

from .concat import concat_nifti1_4d
from .pretreeprint import pretreeprint
from .utils import (
    build_bidsapp_group_parser,
    file_path_from_b2table_row,
    file_paths_from_b2table,
    sidecar_path_from_b2table_row,
)

elbow.utils.setup_logging("ERROR")

REDUCE_COLUMNS = ["dataset", "sub", "ses", "run"]
REDUCE_COLUMNS_SET = set(REDUCE_COLUMNS)


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

    df.sort_values(by=REDUCE_COLUMNS, inplace=True)

    grouped = df.groupby(by=list(REDUCE_COLUMNS_SET - group_by_set), dropna=False)

    def _func_reduce(df_group: pd.DataFrame) -> Optional[pd.Series]:
        if df_group.shape[0] == 0:
            print("empty group")
            return None

        first_row: pd.Series = df_group.iloc[0]

        for group_label in group_by:
            first_row[group_label] = None  # todo does vectorized work here?

        if group_callback is not None:
            group_callback(df_group)

        return first_row

    df_reduced = grouped.apply(func=_func_reduce)

    return df_reduced


def _read_if_parquet(p: pl.Path, *args, **kwargs) -> Optional[pd.DataFrame]:  # noqa
    try:
        return pd.read_parquet(p, *args, **kwargs)
    except:  # noqa
        return None


def main() -> None:
    """Concatenate MRI timeseries."""
    parser = build_bidsapp_group_parser(prog="ba-tsconcat", description="Concatenate MRI timeseries.")

    parser.add_argument(
        "-c",
        "--concat",
        type=str,
        help=f"Concat across. Can be any combination of {', '.join(REDUCE_COLUMNS)} separated by spaces. "
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

    args = parser.parse_args()

    input_dir: pl.Path = args.bids_dir
    output_dir: pl.Path = args.output_dir
    concat_labels: List[str] = args.concat.split(" ")
    dry_run: bool = args.dry_run
    fake: bool = args.fake
    dry_run = dry_run or fake

    if not input_dir.exists():
        raise Exception("Input directory does not exist.")

    if dry_run and (df := _read_if_parquet(input_dir)) is not None:
        df = bids2table.helpers.flat_to_multi_columns(df)
    else:
        df = bids2table.bids2table(input_dir)

        if df.shape[0] == 0:
            raise Exception("Empty BIDS dataset")

    if not dry_run:
        output_dir.mkdir(parents=True, exist_ok=True)

    # We dont care about these
    df = df.droplevel(0, axis="columns")

    df_bold = df.query(
        "datatype == 'func' and "
        "ext == '.nii.gz' and "
        "suffix == 'bold' and "
        "desc == 'preproc' and "
        "space == 'MNI152NLin6ASym'"
    )

    def _process_group(df_group: pd.DataFrame) -> None:
        group_identifiers = df_group.iloc[0][list(REDUCE_COLUMNS_SET - set(concat_labels))].to_dict()
        print(f"Process group: {group_identifiers}")

        first_row: pd.Series = df_group.iloc[0]

        for group_label in concat_labels:
            first_row[group_label] = None  # todo does vectorized work here?

        # Generate file

        file_path = output_dir / file_path_from_b2table_row(first_row)

        file_path.parent.mkdir(parents=True, exist_ok=True)
        concat_nifti1_4d(paths=df_group.file_path.values, out_path=file_path)

        # Generate sidecar

        sidecar_path = output_dir / sidecar_path_from_b2table_row(first_row)
        sidecar_contents = first_row["sidecar"]  # TODO: Maybe add list of files that were concatenated?
        with open(sidecar_path, "w", encoding="utf-8") as fp:
            json.dump(sidecar_contents, fp)

    df_reduced_bold = _reduce_op(
        df_bold,
        group_by=concat_labels,
        group_callback=None if dry_run else _process_group,
    )

    if fake:
        df_reduced_bold = df_reduced_bold.astype(
            {"sidecar": "json", "dataset_description": "json", "extra_entities": "json"}
        )
        df_reduced_bold.to_parquet(output_dir)

    filepaths = file_paths_from_b2table(df_reduced_bold, include_sidecars=True)
    pretreeprint(filepaths)


if __name__ == "__main__":
    main()
