import pathlib as pl
from os import PathLike
from typing import Iterable, Union

import nibabel as nib
import numpy as np


def concat_nifti1_4d(paths: Iterable[Union[str, PathLike]], out_path: Union[str, PathLike]) -> None:
    paths = [pl.Path(p) for p in paths]

    if len(paths) == 0:
        raise Exception("Empty path list.")

    img_handles = [nib.nifti1.Nifti1Image.load(p) for p in paths]

    img_affines = [img.affine for img in img_handles]

    affs = np.asarray(img_affines)
    if not np.all(affs == affs[0, :, :]):
        raise Exception("Affines must be equal.")

    img_arrays = [img.get_fdata() for img in img_handles]

    concat = np.concatenate(img_arrays, axis=3)

    concat_n1 = nib.nifti1.Nifti1Image(concat, img_affines[0])
    nib.nifti1.save(concat_n1, out_path)
