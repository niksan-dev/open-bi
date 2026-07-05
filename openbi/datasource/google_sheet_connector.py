import time

import gspread
import pandas as pd

from google.oauth2.service_account import Credentials

from openbi.datasource.datasource import DataSource
from openbi.datasource.datasource_result import DataSourceResult


class GoogleSheetConnector(DataSource):

    SCOPES = [

        "https://www.googleapis.com/auth/spreadsheets.readonly"

    ]

    def __init__(

        self,

        spreadsheet_id,

        credentials_file,

        worksheet=None,

        dataset_name=None

    ):

        super().__init__(spreadsheet_id)

        self.spreadsheet_id = spreadsheet_id

        self.credentials_file = credentials_file

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

        dataset = self.create_dataset(

            self.dataset_name

            or spreadsheet.title

        )

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

            table = self.create_table(

                ws.title,

                df

            )

            dataset.model.add_table(table)

        self.statistics.table_count = len(

            dataset.model.tables

        )

        end = time.perf_counter()

        self.statistics.execution_time_ms = (

            end - start

        ) * 1000

        self.disconnect()

        return DataSourceResult(

            dataset=dataset,

            statistics=self.statistics

        )