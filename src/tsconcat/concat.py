import pathlib as pl
from os import PathLike
from typing import Iterable, List, Union

import nibabel as nib
import numpy as np


def concat_nifti1_4d(
    paths: Iterable[Union[str, PathLike]], out_path: Union[str, PathLike]
) -> None:
    """
    Concat 4D Nifti files.

    Args:
        paths: Paths to 4D Nifti files.
        out_path: Path to output 4D Nifti file.

    Raises:
        Exception: If affines are not equal.
        Exception: If path list is empty.
    """
    paths = [pl.Path(p) for p in paths]

    if len(paths) == 0:
        raise Exception("Empty path list.")

    img_handles: List[nib.nifti1.Nifti1Image] = [nib.nifti1.Nifti1Image.load(p) for p in paths]  # type: ignore

    img_affines: List[np.ndarray] = [img.affine for img in img_handles]

    affs = np.asarray(img_affines)
    if not np.all(affs == affs[0, :, :]):
        raise Exception("Affines must be equal.")

    img_arrays = [img.get_fdata() for img in img_handles]

    concat = np.concatenate(img_arrays, axis=3)

    concat_n1 = nib.nifti1.Nifti1Image(concat, img_affines[0])
    nib.nifti1.save(concat_n1, out_path)
