import pandas as pd

from openbi.datasource.datasource import DataSource


class CSVConnector(DataSource):

    @property
    def name(self):

        return "CSV Connector"

    def connect(self):

        self.validate()

    def disconnect(self):

        pass

    def read(self):

        return {

            self.source_name:

            pd.read_csv(self.source)

        }