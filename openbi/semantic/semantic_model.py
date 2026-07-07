from dataclasses import dataclass, field

from openbi.model.table import Table
from openbi.relationship.relationship import Relationship
from openbi.relationship.relationship_manager import RelationshipManager

@dataclass
class SemanticModel:

    tables: dict[str, Table] = field(default_factory=dict)

    relationships: list[Relationship] = field(default_factory=list)

    #relationships = RelationshipManager()

    measures: dict = field(default_factory=dict)

    hierarchies: dict = field(default_factory=dict)

    perspectives: dict = field(default_factory=dict)

    roles: dict = field(default_factory=dict)

    kpis: dict = field(default_factory=dict)

    # ------------------------------------

    def add_table(self, table: Table):

        self.tables[table.name] = table

    # ------------------------------------

    def get_table(self, name: str):

        return self.tables.get(name)

    # ------------------------------------

    def remove_table(self, name: str):

        self.tables.pop(name, None)

    # ------------------------------------

    @property
    def table_count(self):

        return len(self.tables)

    # ------------------------------------

    def add_relationship(self, relationship):

        self.relationships.append(relationship)