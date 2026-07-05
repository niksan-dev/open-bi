import time
import pandas as pd
import gspread

from google.oauth2.service_account import Credentials

from openbi.datasource.datasource import DataSource
from openbi.datasource.datasource_result import DataSourceResult

from openbi.model.dataset import Dataset
from openbi.model.table import Table

from openbi.metadata.profiler import MetadataProfiler
from openbi.pipeline.pipeline_builder import DefaultPipeline


class GoogleSheetConnector(DataSource):
    """
    Loads a Google Spreadsheet into an OpenBI Dataset.
    """

    SCOPES = [
        "https://www.googleapis.com/auth/spreadsheets.readonly"
    ]

    def __init__(
        self,
        spreadsheet_id: str,
        credentials_file: str,
        worksheet=None,
        dataset_name=None
    ):

        super().__init__(spreadsheet_id)

        self.credentials_file = credentials_file

        self.spreadsheet_id = spreadsheet_id

        self.worksheet = worksheet

        self.dataset_name = dataset_name

        self.client = None

    @property
    def name(self):

        return "Google Sheet Connector"

    def connect(self):

        credentials = Credentials.from_service_account_file(

            self.credentials_file,

            scopes=self.SCOPES

        )

        self.client = gspread.authorize(credentials)

        return True

    def disconnect(self):

        self.client = None

        return True

    def load(self):

        start = time.perf_counter()

        self.connect()

        spreadsheet = self.client.open_by_key(

            self.spreadsheet_id

        )

        dataset = Dataset(

            self.dataset_name

            or spreadsheet.title

        )

        # -----------------------------
        # Load all worksheets
        # -----------------------------

        if self.worksheet is None:

            worksheets = spreadsheet.worksheets()

        else:

            worksheets = [

                spreadsheet.worksheet(

                    self.worksheet

                )

            ]

        for ws in worksheets:

            values = ws.get_all_records()

            df = pd.DataFrame(values)

            pipeline = DefaultPipeline.create()

            pipeline_result = pipeline.execute(df)

            table = Table.from_dataframe(

                name=ws.title,

                dataframe=pipeline_result.dataframe

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