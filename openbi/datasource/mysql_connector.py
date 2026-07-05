import pymysql

from openbi.datasource.database_datasource import DatabaseDataSource


class MySQLConnector(DatabaseDataSource):

    @property
    def name(self):
        return "MySQL Connector"

    def connect(self):

        self.connection = pymysql.connect(

            host=self.connection_string["host"],

            user=self.connection_string["user"],

            password=self.connection_string["password"],

            database=self.connection_string["database"]

        )

        return True