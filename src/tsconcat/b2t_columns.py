"""bids2table column name constants."""

from abc import ABC


class B2tColumn(ABC):
    """bids2table column name constants."""

    Dataset = "ds__dataset"
    DatasetDescription = "ds__dataset_description"

    DataType = "ent__datatype"
    """i.e. 'func', 'anat', 'dwi', 'fmap'"""
    Subject = "ent__sub"
    Session = "ent__ses"
    Run = "ent__run"
    Description = "ent__desc"
    Space = "ent__space"
    ExtraEntities = "ent__extra_entities"
    FileExtension = "ent__ext"
    Suffix = "ent__suffix"

    FilePath = "finfo__file_path"

    MetaJson = "meta__json"
    """JSON sidecar contents"""
