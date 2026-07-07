from dataclasses import dataclass, field

from openbi.semantic.semantic_model import SemanticModel


@dataclass
class Dataset:

    name: str

    model: SemanticModel = field(

        default_factory=SemanticModel

    )

    description: str = ""

    #source: DataSourceInfo