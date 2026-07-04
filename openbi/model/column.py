from dataclasses import dataclass, field

from openbi.core.base import BaseEntity
from openbi.metadata.column_metadata import ColumnMetadata


@dataclass
class Column(BaseEntity):

    name: str = ""

    datatype: str = ""

    metadata: ColumnMetadata = field(default_factory=ColumnMetadata)

    description: str = ""