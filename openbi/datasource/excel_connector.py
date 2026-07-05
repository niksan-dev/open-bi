import time
import pandas as pd

from openbi.datasource.datasource import DataSource
from openbi.datasource.datasource_result import DataSourceResult
from openbi.model.dataset import Dataset
from openbi.model.table import Table
from openbi.metadata.profiler import MetadataProfiler
from openbi.pipeline.pipeline_builder import DefaultPipeline


class ExcelConnector(DataSource):
    """
    Loads Excel workbooks into an OpenBI Dataset.
    """

    def __init__(
        self,
        source: str,
        sheet_name=0,
        dataset_name=None
    ):

        super().__init__(source)

        self.sheet_name = sheet_name
        self.dataset_name = dataset_name

    @property
    def name(self):

        return "Excel Connector"

    def connect(self):

        self.validate()

        return True

    def disconnect(self):

        return True

    def load(self) -> DataSourceResult:

        start = time.perf_counter()

        self.connect()

        workbook = pd.read_excel(
            self.source,
            sheet_name=self.sheet_name
        )

        dataset = Dataset(

            name=self.dataset_name
            or self.source_name

        )

        # -------------------------------------
        # Multiple sheets
        # -------------------------------------

        if isinstance(workbook, dict):

            for sheet_name, df in workbook.items():

                pipeline = DefaultPipeline.create()

                result = pipeline.execute(df)

                table = Table.from_dataframe(

                    name=sheet_name,

                    dataframe=result.dataframe

                )

                MetadataProfiler.profile(table)

                dataset.model.add_table(table)

        # -------------------------------------
        # Single sheet
        # -------------------------------------

        else:

            pipeline = DefaultPipeline.create()

            result = pipeline.execute(workbook)

            table = Table.from_dataframe(

                name=str(self.sheet_name),

                dataframe=result.dataframe

            )

            MetadataProfiler.profile(table)

            dataset.model.add_table(table)

        end = time.perf_counter()

        self.statistics.execution_time_ms = (

            end - start

        ) * 1000

        self.statistics.table_count = len(
            dataset.model.tables
        )

        self.disconnect()

        return DataSourceResult(

            dataset=dataset,

            statistics=self.statistics
        )