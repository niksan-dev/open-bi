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

    def read(self):

        workbook = self.client.open_by_key(

            self.spreadsheet_id

        )

        tables = {}

        for sheet in workbook.worksheets():

            tables[sheet.title] = pd.DataFrame(

                sheet.get_all_records()

            )

        return tables