# `tsconcat`

[![Build](https://github.com/childmindresearch/tsconcat/actions/workflows/test.yaml/badge.svg?branch=main)](https://github.com/childmindresearch/tsconcat/actions/workflows/test.yaml?query=branch%3Amain)
[![codecov](https://codecov.io/gh/childmindresearch/tsconcat/branch/main/graph/badge.svg?token=22HWWFWPW5)](https://codecov.io/gh/childmindresearch/tsconcat)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
![stability-wip](https://img.shields.io/badge/stability-work_in_progress-lightgrey.svg)
[![L-GPL License](https://img.shields.io/badge/license-L--GPL-blue.svg)](LICENSE)
[![pages](https://img.shields.io/badge/api-docs-blue)](https://childmindresearch.github.io/tsconcat)

BIDS App and Python library for concatenating MRI time series.

Inspired by [Cho et al. 2021](https://doi.org/10.1016/j.neuroimage.2020.117549).

## Features

- Concatenate BOLD time series from multiple datasets, sessions, subjects or runs into a single file.
- Dry run mode to check what the output directory will look like.
- Fake mode to produce a [bids2table](https://github.com/childmindresearch/bids2table) compatible parquet output directory.

## Installation

<!--
Install this package via:

```sh
pip install tsconcat
```

Or -->Get the newest development version via:

```sh
pip install git+https://github.com/childmindresearch/tsconcat
```

## Quick start

```sh
ba-tsconcat /path/to/input/bids /path/to/output group --concat ses --dry_run
```

![image](https://github.com/childmindresearch/tsconcat/assets/33600480/501037b0-77c6-40fe-bc7d-a3575944b0c6)

## Usage

```sh
ba-tsconcat --help
usage: ba-tsconcat [-h] [-c CONCAT] [-d] [-f] bids_dir output_dir {group}

Concatenate MRI timeseries.

positional arguments:
  bids_dir              Input BIDS folder path.
  output_dir            Output BIDS folder path.
  {group}               Processing stage, must be "group".

options:
  -h, --help            show this help message and exit
  -c CONCAT, --concat CONCAT
                        Concat across. Can be any combination of dataset, sub, ses, run separated by spaces. Output data will be grouped by the set difference.
  -d, --dry_run         Dry run. Print output directory structure instead of actually doing something. If this is enabled 'bids_dir' may be a path to a bids2table parquet directory.
  -f, --fake            Fake output. Output a bids2table parquet directory instead of actually doing something.
```

## Links or References

- [Impact of concatenating fMRI data on reliability for functional connectomics (Cho et al. 2021)](https://doi.org/10.1016/j.neuroimage.2020.117549)
- [bids2table](https://github.com/childmindresearch/bids2table)
