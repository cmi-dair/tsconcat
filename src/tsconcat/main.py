import argparse
import json
import pathlib as pl
from hashlib import sha1

import bids2table.helpers
import pandas as pd

from tsconcat.utils import timeprint
from .b2t import b2t_cpac
from .concat import concat_nifti1_4d


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

    input_dir: pl.Path = args.input
    output_dir: pl.Path = args.output
    group_label: str = args.group_by

    if group_label not in ['sub']:  # ['dataset','sub','ses','run']:
        raise Exception('Unknown group label.')

    output_dir.mkdir(parents=True, exist_ok=True)

    df = b2t_cpac(
        bids_dir=input_dir,
        parquet_cache_dir=output_dir / f'temp_{sha1(str(input_dir).encode("utf-8")).hexdigest()}'
    )

    def fun(df: pd.DataFrame):
        with timeprint(f'Processing: {df.name}'):
            df_bold = df.query(
                "datatype == 'func' and "
                "ext == '.nii.gz' and "
                "suffix == 'bold' and "
                "desc == 'preproc' and "
                "space == 'MNI152NLin6ASym'")

            first_row = df_bold.iloc[0]

            first_row['ses'] = None  # todo

            out_path = output_dir / 'out' / bids2table.helpers.join_bids_path(first_row)
            out_path.parent.mkdir(parents=True, exist_ok=True)

            concat_nifti1_4d(
                paths=df_bold.file_path.values,
                out_path=out_path
            )

            sidecar_path = output_dir / 'out' / bids2table.helpers.join_bids_path({**first_row, "ext": ".json"})
            with open(sidecar_path, 'w', encoding='utf-8') as fp:
                json.dump(first_row['sidecar'], fp)

        return df

    df.sort_values(by=['dataset', 'sub', 'ses', 'run']).groupby([group_label]).apply(fun)


if __name__ == '__main__':
    main()
