# CMI-DAIR Template Python Repository

This is a template repository. Below is a checklist of things you should do to use it:

- [ ] Rewrite this `README` file, updating the badges as needed.
- [ ] Update the pre-commit versions in `.pre-commit-config.yaml`.
- [ ] Install the `pre-commit` hooks.
- [ ] Update the `LICENSE` file to your desired license and set the year.
- [ ] Replace "ENTER_YOUR_EMAIL_ADDRESS" in `CODE_OF_CONDUCT.md`
- [ ] Remove the placeholder src and test files, these are there merely to show how the CI works.
- [ ] Update `pyproject.toml`
- [ ] Update the name of `src/APP_NAME`
- [ ] Grant third-party app permissions (e.g. Codecov) [here](https://github.com/organizations/cmi-dair/settings/installations), if necessary.
- [ ] Either generate a `CODECOV_TOKEN` secret [here](https://github.com/cmi-dair/flowdump/blob/main/.github/workflows/python_tests.yaml) (if its a private repository) or remove the line `token: ${{ secrets.CODECOV_TOKEN }}`


# grag-tsconcat

[![Build](https://github.com/cmi-dair/tsconcat/actions/workflows/test.yaml/badge.svg?branch=main)](https://github.com/cmi-dair/tsconcat/actions/workflows/test.yaml?query=branch%3Amain)
[![codecov](https://codecov.io/gh/cmi-dair/tsconcat/branch/main/graph/badge.svg?token=22HWWFWPW5)](https://codecov.io/gh/cmi-dair/tsconcat)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![L-GPL License](https://img.shields.io/badge/license-L--GPL-blue.svg)](LICENSE)
[![pages](https://img.shields.io/badge/api-docs-blue)](https://cmi-dair.github.io/tsconcat)


What problem does this tool solve?

## Features

- A few
- Cool
- Things

## Installation

Install this package via :

```sh
pip install tsconcat
```

Or get the newest development version via:

```sh
pip install git+https://github.com/cmi-dair/tsconcat
```

## Quick start

```sh
python -m tsconcat.main -i /path/to/input/bids -o /path/to/output
```

```
tree /path/to/input/bids -L 3

/path/to/input/bids
└── pipeline_default-afni
    ├── sub-0025431
    │   ├── ses-1
    │   ├── ses-10
    │   ├── ses-2
    │   ├── ses-3
    │   ├── ses-4
    │   ├── ses-5
    │   ├── ses-6
    │   ├── ses-7
    │   ├── ses-8
    │   └── ses-9
    ├── sub-0025435
    │   ├── ses-1
    │   ├── ses-10
    │   ├── ses-2
    │   ├── ses-3
    │   ├── ses-4
    │   ├── ses-5
    │   ├── ses-6
    │   ├── ses-7
    │   ├── ses-8
    │   └── ses-9
    ├── sub-0025441
    │   ├── ses-10
    │   ├── ses-2
    │   ├── ses-7
    │   └── ses-9
    ├── sub-0025453
    │   ├── ses-1
    │   ├── ses-10
    │   ├── ses-2
    │   ├── ses-3
    │   ├── ses-4
    │   ├── ses-5
    │   ├── ses-6
    │   ├── ses-7
    │   ├── ses-8
    │   └── ses-9
    └── sub-0025455
        ├── ses-1
        ├── ses-10
        ├── ses-2
        ├── ses-3
        ├── ses-4
        ├── ses-5
        ├── ses-6
        ├── ses-7
        ├── ses-8
        └── ses-9
```

```
tree /path/to/output

b2t_test1/
├── out
│   ├── sub-0025431
│   │   └── func
│   │       └── sub-0025431_task-rest_run-1.0_space-MNI152NLin6ASym_desc-preproc_bold.nii.gz
│   ├── sub-0025435
│   │   └── func
│   │       └── sub-0025435_task-rest_run-1.0_space-MNI152NLin6ASym_desc-preproc_bold.nii.gz
│   ├── sub-0025441
│   │   └── func
│   │       └── sub-0025441_task-rest_run-1.0_space-MNI152NLin6ASym_desc-preproc_bold.nii.gz
│   ├── sub-0025453
│   │   └── func
│   │       └── sub-0025453_task-rest_run-1.0_space-MNI152NLin6ASym_desc-preproc_bold.nii.gz
│   └── sub-0025455
│       └── func
│           └── sub-0025455_task-rest_run-1.0_space-MNI152NLin6ASym_desc-preproc_bold.nii.gz
└── temp_cde199d696958c4182c6afe8d6795c7ae772dc94
    ├── part-20230517165220-0000
    ├── part-20230517165220-0001
    ├── part-20230517165220-0002
    ├── part-20230517165220-0003
    ├── part-20230517165220-0004
    ├── part-20230517165220-0005
    ├── part-20230517165220-0006
    ├── part-20230517165220-0007
    ├── part-20230517165220-0008
    └── part-20230517165220-0009
```

## Links or References

- [https://www.wikipedia.de](https://www.wikipedia.de)
