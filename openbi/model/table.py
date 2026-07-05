from dataclasses import dataclass, field
import pandas as pd

from openbi.model.column import Column


@dataclass
class Table:

    name: str

    dataframe: pd.DataFrame

    columns: list[Column] = field(default_factory=list)

    description: str = ""

    def add_column(self, column: Column):

        self.columns.append(column)

    def get_column(self, name: str):

        for column in self.columns:

            if column.name == name:

                return column

        return None

    @property
    def row_count(self):

        return len(self.dataframe)

    @property
    def column_count(self):

        return len(self.columns)

    @classmethod
    def from_dataframe(cls, name: str, dataframe: pd.DataFrame):

        table = cls(
            name=name,
            dataframe=dataframe
        )

        for column_name in dataframe.columns:

            table.add_column(
                Column(
                    name=column_name,
                    datatype=str(dataframe[column_name].dtype)
                )
            )

        return table