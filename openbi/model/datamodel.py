from dataclasses import dataclass, field

from openbi.model.table import Table
from openbi.model.relationship import Relationship


@dataclass
class DataModel:

    tables: dict[str, Table] = field(default_factory=dict)

    relationships: list[Relationship] = field(default_factory=list)

    def add_table(self, table: Table):

        self.tables[table.name] = table

    def add_relationship(self, relationship: Relationship):

        self.relationships.append(relationship)

    def get_table(self, name):

        return self.tables.get(name)