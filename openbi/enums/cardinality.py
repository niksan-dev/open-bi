from enum import Enum


class RelationshipCardinality(Enum):

    ONE_TO_ONE = "OneToOne"

    ONE_TO_MANY = "OneToMany"

    MANY_TO_ONE = "ManyToOne"

    MANY_TO_MANY = "ManyToMany"