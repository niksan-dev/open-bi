from abc import ABC, abstractmethod
from pathlib import Path

import pandas as pd

from openbi.datasource.datasource_result import DataSourceResult
from openbi.datasource.datasource_statistics import DataSourceStatistics

from openbi.model.dataset import Dataset
from openbi.model.table import Table

from openbi.pipeline.pipeline_builder import DefaultPipeline
from openbi.metadata.profiler import MetadataProfiler


class DataSource(ABC):
    """
    Base class for all OpenBI data sources.

    Examples
    --------
    CSVConnector
    ExcelConnector
    JSONConnector
    GoogleSheetConnector
    SQLiteConnector
    SQLServerConnector
    PostgreSQLConnector
    MySQLConnector
    RESTConnector
    """

    def __init__(self, source: str):

        self.source = source

        self.statistics = DataSourceStatistics()

    # ============================================================
    # Properties
    # ============================================================

    @property
    @abstractmethod
    def name(self) -> str:
        pass

    @property
    def source_name(self) -> str:

        return Path(self.source).stem

    @property
    def source_path(self) -> str:

        return str(Path(self.source).resolve())

    @property
    def exists(self) -> bool:

        return Path(self.source).exists()

    # ============================================================
    # Connection
    # ============================================================

    @abstractmethod
    def connect(self):
        """
        Open the data source.
        """
        pass

    @abstractmethod
    def disconnect(self):
        """
        Close the data source.
        """
        pass

    @abstractmethod
    def load(self) -> DataSourceResult:
        """
        Load data into OpenBI.
        """
        pass

    # ============================================================
    # Validation
    # ============================================================

    def validate(self):

        if not self.exists:

            raise FileNotFoundError(

                f"Data source not found:\n{self.source}"

            )

        return True

    # ============================================================
    # Dataset Helper
    # ============================================================

    def create_dataset(
        self,
        dataset_name: str
    ) -> Dataset:

        return Dataset(
            name=dataset_name
        )

    # ============================================================
    # Table Helper
    # ============================================================

    def create_table(
        self,
        name: str,
        dataframe: pd.DataFrame
    ) -> Table:
        """
        DataFrame
              ↓
        Pipeline
              ↓
        Table
              ↓
        Metadata
        """

        pipeline = DefaultPipeline.create()

        pipeline_result = pipeline.execute(dataframe)

        clean_df = pipeline_result.dataframe

        table = Table.from_dataframe(

            name=name,

            dataframe=clean_df

        )

        MetadataProfiler.profile(table)

        self.statistics.row_count += table.row_count

        self.statistics.column_count += table.column_count

        return table

    # ============================================================
    # Dataset Helper
    # ============================================================

    def add_table(
        self,
        dataset: Dataset,
        name: str,
        dataframe: pd.DataFrame
    ) -> Table:

        table = self.create_table(

            name,

            dataframe

        )

        dataset.model.add_table(table)

        self.statistics.table_count += 1

        return table

    # ============================================================
    # Result Helper
    # ============================================================

    def create_result(
        self,
        dataset: Dataset
    ) -> DataSourceResult:

        return DataSourceResult(

            dataset=dataset,

            statistics=self.statistics

        )