import pathlib as pl
from os import PathLike, environ
from typing import Union

import bids2table
import elbow.dtypes  # noqa  makes pandas load json types as dicts from parquet
import elbow.utils
import pandas as pd


def _remove_cpac_provenance(df: pd.DataFrame) -> pd.DataFrame:
    def _remove_cprov(x):
        x.pop('CpacProvenance', None)
        return x

    df['sidecar'] = df['sidecar'].apply(_remove_cprov)
    return df


def b2t_cpac(bids_dir: Union[str, PathLike], parquet_cache_dir: Union[str, PathLike]) -> pd.DataFrame:
    parquet_cache_dir = pl.Path(parquet_cache_dir)
    if not parquet_cache_dir.exists():
        elbow.utils.setup_logging("ERROR")
        print('Executing b2t...')
        cores = int(environ.get('SLURM_CPUS_ON_NODE', 8))
        print(f'Using {cores} workers.')
        _ = bids2table.load_bids_parquet(bids_dir, parquet_cache_dir, workers=cores)  # type: ignore
    else:
        print('Loading cached b2t...')

    df = pd.read_parquet(parquet_cache_dir)
    df = _remove_cpac_provenance(df)
    return df
