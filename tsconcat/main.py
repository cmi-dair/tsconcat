from os import PathLike
import pathlib as pl
from typing import Iterable, Union
import pandas as pd
import numpy as np
import nibabel as nib
from hashlib import sha1

from .concat import concat_nifti1_4d
from .b2t import b2t_cpac


from contextlib import contextmanager
import time
import datetime
import argparse


@contextmanager
def timeprint(title: str):
    print(f'Start: {title}')
    start = time.perf_counter()
    yield
    duration = time.perf_counter()-start
    print(f'Done: {title} - {datetime.timedelta(seconds=duration)}')
    


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-i", "--input",
        type=pl.Path,
        help="Path to BIDS dataset",
        required=True
    )
    parser.add_argument(
        "-o", "--output",
        type=pl.Path,
        help="Path to output directory",
        required=True
    )

    parser.add_argument(
        "-g", "--group_by",
        type=str,
        help="Group by",
        default="sub"
    )

    args = parser.parse_args()

    input_dir = args.input
    output_dir = args.output
    group_label = args.group_by


    if group_label not in ['sub']:#['dataset','sub','ses','run']:
        raise Exception('Unknown group label.')

    output_dir.mkdir(parents=True, exist_ok=True)

    df = b2t_cpac(
        bids_dir=input_dir, 
        parquet_cache_dir=output_dir / f'temp_{sha1(str(input_dir).encode("utf-8")).hexdigest()}'
    )

    def fun(df: pd.DataFrame):

        with timeprint(f'Processing: {df.name}'):

            df_bold = df.query("datatype == 'func' and ext == '.nii.gz' and suffix == 'bold' and desc == 'preproc' and space == 'MNI152NLin6ASym'")

            first_row = df_bold.iloc[0]

            first_row['ses'] = None  # todo

            import bids2table.helpers
            out_path: pl.Path = output_dir / 'out' / bids2table.helpers.join_bids_path(first_row)
            out_path.parent.mkdir(parents=True, exist_ok=True)

            concat_nifti1_4d(
                paths=df_bold.file_path.values,
                out_path=out_path
            )
        
        return df

    df.sort_values(by=['dataset','sub','ses','run']).groupby([group_label]).apply(fun)


if __name__ == '__main__':
    main()