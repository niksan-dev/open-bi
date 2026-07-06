from abc import ABC, abstractmethod
from pathlib import Path
import time
import pandas as pd

from openbi.datasource.datasource_statistics import DataSourceStatistics
from openbi.datasource.datasource_result import DataSourceResult

from openbi.model.dataset import Dataset
from openbi.model.table import Table

from openbi.pipeline.pipeline_builder import DefaultPipeline
from openbi.metadata.profiler import MetadataProfiler
from openbi.connector_options.connector_options import ConnectorOptions

class DataSource(ABC):

    def __init__(
        self,
        source: str,
        dataset_name: str = None,
        options: ConnectorOptions = None
    ):

        self.source = source
        self.dataset_name = dataset_name
        self.options = options

        self.statistics = DataSourceStatistics()

    # ---------------------------------------------------
    # Properties
    # ---------------------------------------------------

    @property
    @abstractmethod
    def name(self):
        pass

    @property
    def source_name(self):

        return Path(self.source).stem

    @property
    def exists(self):

        return Path(self.source).exists()

    # ---------------------------------------------------
    # Connection
    # ---------------------------------------------------

    @abstractmethod
    def connect(self):
        pass

    @abstractmethod
    def disconnect(self):
        pass

    # ---------------------------------------------------
    # Read
    # ---------------------------------------------------

    @abstractmethod
    def read(self) -> dict[str, pd.DataFrame]:
        """
        Returns

        {
            "Orders": dataframe,
            "Customers": dataframe
        }
        """
        pass

    # ---------------------------------------------------
    # Validation
    # ---------------------------------------------------

    def validate(self):

        if not self.exists:

            raise FileNotFoundError(self.source)

    # ---------------------------------------------------
    # Dataset
    # ---------------------------------------------------

    def create_dataset(self):

        return Dataset(

            self.dataset_name
            or self.source_name

        )

    # ---------------------------------------------------
    # Table
    # ---------------------------------------------------

    def create_table(
        self,
        name,
        dataframe
    ):

        pipeline = DefaultPipeline.create()

        result = pipeline.execute(dataframe)

        table = Table.from_dataframe(

            name,

            result.dataframe

        )

        MetadataProfiler.profile(table)

        self.statistics.row_count += table.row_count

        self.statistics.column_count += table.column_count

        return table

    # ---------------------------------------------------

    def add_table(
        self,
        dataset,
        name,
        dataframe
    ):

        table = self.create_table(

            name,

            dataframe

        )

        dataset.model.add_table(table)

        self.statistics.table_count += 1

    # ---------------------------------------------------

    def create_result(
        self,
        dataset
    ):

        return DataSourceResult(

            dataset=dataset,

            statistics=self.statistics

        )

    # ---------------------------------------------------
    # Template Method
    # ---------------------------------------------------

    def load(self):

        start = time.perf_counter()

        self.connect()

        tables = self.read()

        dataset = self.create_dataset()

        for name, dataframe in tables.items():

            self.add_table(

                dataset,

                name,

                dataframe

            )

        self.statistics.execution_time_ms = (

            time.perf_counter() - start

        ) * 1000

        self.disconnect()

        return self.create_result(dataset)