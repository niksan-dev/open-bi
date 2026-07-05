import pyodbc

from openbi.datasource.database_datasource import DatabaseDataSource


class SQLServerConnector(DatabaseDataSource):

    @property
    def name(self):
        return "SQL Server Connector"

    def connect(self):

        self.connection = pyodbc.connect(

            self.connection_string

        )

        return True