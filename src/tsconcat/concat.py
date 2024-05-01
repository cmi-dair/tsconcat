"""Concatenate 4D Nifti files."""

import pathlib as pl
from os import PathLike
from typing import Iterable, List, Union

import nibabel as nib
import numpy as np


def concat_nifti1_4d(paths: Iterable[Union[str, PathLike]], out_path: Union[str, PathLike]) -> None:
    """Concat 4D Nifti files.

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

    img_shapes: List[tuple] = [img.shape for img in img_handles]

    # All 4D
    if not np.all([len(shape) == 4 for shape in img_shapes]):
        raise Exception("Images must be 4D.")

    # First 3 dimensions must be equal
    if not np.all([img_shapes[0][:-1] == shape[:-1] for shape in img_shapes]):
        raise Exception("Spatial shapes must be equal.")

    img_affines: List[np.ndarray] = [img.affine for img in img_handles]

    affs = np.asarray(img_affines)
    if not np.all(affs == affs[0, :, :]):
        raise Exception("Affines must be equal.")

    # Should this use the _dataobj to preserve integer types?
    img_arrays = [img.get_fdata() for img in img_handles]

    concat = np.concatenate(img_arrays, axis=3)

    concat_n1 = nib.nifti1.Nifti1Image(concat, img_affines[0])
    nib.nifti1.save(concat_n1, out_path)
