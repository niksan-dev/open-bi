from dataclasses import dataclass

from openbi.core.base import BaseEntity


@dataclass
class Relationship(BaseEntity):

    from_table: str = ""

    from_column: str = ""

    to_table: str = ""

    to_column: str = ""

    cardinality: str = "OneToMany"

    cross_filter: str = "Single"

    active: bool = True