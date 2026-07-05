import sqlite3
import time
from turtle import pd

from openbi.datasource.database_datasource import DatabaseDataSource
from openbi.datasource.datasource_result import DataSourceResult


class SQLiteConnector(DatabaseDataSource):

    @property
    def name(self):
        return "SQLite Connector"

    def read(self):

        return {

            self.table_name:

            pd.read_sql(

                f"SELECT * FROM {self.table_name}",

                self.connection

            )

        }