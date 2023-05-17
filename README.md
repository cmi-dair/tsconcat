# `tsconcat`

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