from abc import abstractmethod

import pandas as pd

from openbi.datasource.datasource import DataSource


class DatabaseDataSource(DataSource):

    def __init__(
        self,
        connection_string,
        database=None
    ):

        super().__init__(connection_string)

        self.connection_string = connection_string
        self.database = database

        self.connection = None

    @abstractmethod
    def connect(self):
        pass

    def disconnect(self):

        if self.connection:

            self.connection.close()

            self.connection = None

    def execute_query(self, query):

        return pd.read_sql(
            query,
            self.connection
        )

    def load_table(self, table_name):

        query = f"SELECT * FROM {table_name}"

        return self.execute_query(query)