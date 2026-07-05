
import time
import pandas as pd

from openbi.datasource.datasource import DataSource
from openbi.datasource.datasource_result import DataSourceResult

from openbi.model.dataset import Dataset
from openbi.model.table import Table

from openbi.metadata.profiler import MetadataProfiler
from openbi.pipeline.pipeline_builder import DefaultPipeline


class CSVConnector(DataSource):
    """
    Loads a CSV file into an OpenBI Dataset.
    """

    def __init__(
        self,
        source: str,
        dataset_name: str | None = None,
        table_name: str | None = None,
        encoding: str = "utf-8",
        delimiter: str = ",",
        header: int = 0
    ):

        super().__init__(source)

        self.dataset_name = dataset_name
        self.table_name = table_name
        self.encoding = encoding
        self.delimiter = delimiter
        self.header = header

    @property
    def name(self) -> str:
        return "CSV Connector"

    def connect(self):
        self.validate()
        return True

    def disconnect(self):
        return True

    def load(self) -> DataSourceResult:

        start = time.perf_counter()

        self.connect()

        # ------------------------------------
        # Read CSV
        # ------------------------------------

        df = pd.read_csv(
            self.source,
            encoding=self.encoding,
            sep=self.delimiter,
            header=self.header
        )

        # ------------------------------------
        # Execute Pipeline
        # ------------------------------------

        pipeline = DefaultPipeline.create()

        pipeline_result = pipeline.execute(df)

        clean_df = pipeline_result.dataframe

        # ------------------------------------
        # Create Dataset
        # ------------------------------------

        dataset = Dataset(

            name=self.dataset_name
            or self.source_name

        )

        # ------------------------------------
        # Create Table
        # ------------------------------------

        table = Table.from_dataframe(

            name=self.table_name
            or self.source_name.split(".")[0],

            dataframe=clean_df

        )

        # ------------------------------------
        # Metadata
        # ------------------------------------

        MetadataProfiler.profile(table)

        dataset.model.add_table(table)

        # ------------------------------------
        # Statistics
        # ------------------------------------

        end = time.perf_counter()

        self.statistics.execution_time_ms = (

            end - start

        ) * 1000

        self.statistics.table_count = 1

        self.statistics.row_count = table.row_count

        self.statistics.column_count = table.column_count

        self.disconnect()

        return DataSourceResult(

            dataset=dataset,

            statistics=self.statistics
        )