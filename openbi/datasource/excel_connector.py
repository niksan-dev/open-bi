import pandas as pd

from openbi.datasource.datasource import DataSource


class ExcelConnector(DataSource):

    @property
    def name(self):

        return "Excel Connector"

    def connect(self):

        self.validate()

    def disconnect(self):

        pass

    def read(self):

        return pd.read_excel(

            self.source,

            sheet_name=self.options.sheet_name,

            header=self.options.header,

            skiprows=self.options.skip_rows

        )