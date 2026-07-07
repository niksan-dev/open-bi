from dataclasses import dataclass

#from openbi.relationship.relationship_cardinality import RelationshipCardinality
from openbi.relationship.filter_direction import FilterDirection
from openbi.relationship.relationship_type import RelationshipType


@dataclass
class Relationship:

    name: str

    from_table: str

    from_column: str

    to_table: str

    to_column: str

   # cardinality: RelationshipCardinality

    filter_direction: FilterDirection

    relationship_type: RelationshipType

    description: str = ""