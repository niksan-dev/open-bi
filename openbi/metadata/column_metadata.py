from dataclasses import dataclass, field
from typing import Any


@dataclass
class ColumnMetadata:

    dtype: str = ""

    null_count: int = 0

    distinct_count: int = 0

    is_unique: bool = False

    nullable: bool = True

    min_value: Any = None

    max_value: Any = None

    mean: Any = None

    sample_values: list = field(default_factory=list)

    primary_key_candidate: bool = False

    foreign_key_candidate: bool = False