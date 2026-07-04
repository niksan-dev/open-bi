from dataclasses import dataclass, field

from openbi.model.datamodel import DataModel


@dataclass
class Dataset:

    name: str

    model: DataModel = field(default_factory=DataModel)

    source: str = ""