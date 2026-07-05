import json
import time
import pandas as pd

from openbi.datasource.datasource import DataSource
from openbi.datasource.datasource_result import DataSourceResult

from openbi.model.dataset import Dataset
from openbi.model.table import Table

from openbi.metadata.profiler import MetadataProfiler
from openbi.pipeline.pipeline_builder import DefaultPipeline


class JSONConnector(DataSource):
    """
    Loads JSON files into an OpenBI Dataset.
    """

    def __init__(
        self,
        source: str,
        dataset_name: str | None = None,
        table_name: str | None = None,
        orient: str = "records"
    ):

        super().__init__(source)

        self.dataset_name = dataset_name
        self.table_name = table_name
        self.orient = orient

    @property
    def name(self) -> str:
        return "JSON Connector"

    def connect(self):

        self.validate()

        return True

    def disconnect(self):

        return True

    def load(self) -> DataSourceResult:

        start = time.perf_counter()

        self.connect()

        # ------------------------------------
        # Load JSON
        # ------------------------------------

        with open(
            self.source,
            "r",
            encoding="utf-8"
        ) as f:

            data = json.load(f)

        # ------------------------------------
        # Convert JSON to DataFrame
        # ------------------------------------

        if isinstance(data, list):

            df = pd.DataFrame(data)

        elif isinstance(data, dict):

            # Nested JSON
            try:

                df = pd.json_normalize(data)

            except Exception:

                df = pd.DataFrame([data])

        else:

            raise ValueError(
                "Unsupported JSON format."
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

            self.dataset_name
            or self.source_name

        )

        # ------------------------------------
        # Create Table
        # ------------------------------------

        table = Table.from_dataframe(

            name=self.table_name
            or self.source_name.replace(".json", ""),

            dataframe=clean_df

        )

        MetadataProfiler.profile(table)

        dataset.model.add_table(table)

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