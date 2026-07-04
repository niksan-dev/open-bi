from dataclasses import dataclass, field
import pandas as pd

from openbi.core.base import BaseEntity
from openbi.model.column import Column
from openbi.metadata.profiler import MetadataProfiler


@dataclass
class Table(BaseEntity):

    name: str = ""

    dataframe: pd.DataFrame = field(default_factory=pd.DataFrame)

    columns: list[Column] = field(default_factory=list)

    description: str = ""

    @classmethod
    def from_dataframe(cls, name: str, dataframe: pd.DataFrame):

        table = cls(
            name=name,
            dataframe=dataframe
        )

        profiler = MetadataProfiler()

        metadata = profiler.profile(dataframe)

        for col in dataframe.columns:

            column = Column(
                name=col,
                datatype=str(dataframe[col].dtype),
                metadata=metadata[col]
            )

            table.columns.append(column)

        return table

    @property
    def row_count(self):
        return len(self.dataframe)

    @property
    def column_count(self):
        return len(self.columns)