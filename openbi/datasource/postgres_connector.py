import psycopg2

from openbi.datasource.database_datasource import DatabaseDataSource


class PostgreSQLConnector(DatabaseDataSource):

    @property
    def name(self):
        return "PostgreSQL Connector"

    def connect(self):

        self.connection = psycopg2.connect(

            host=self.connection_string["host"],

            user=self.connection_string["user"],

            password=self.connection_string["password"],

            dbname=self.connection_string["database"]

        )

        return True