import sqlite3
import time

from openbi.datasource.database_datasource import DatabaseDataSource
from openbi.datasource.datasource_result import DataSourceResult


class SQLiteConnector(DatabaseDataSource):

    @property
    def name(self):
        return "SQLite Connector"

    def connect(self):

        self.connection = sqlite3.connect(
            self.connection_string
        )

        return True

    def load(self, table_name):

        start = time.perf_counter()

        self.connect()

        df = self.load_table(table_name)

        dataset = self.create_dataset(
            self.database
            or "SQLite"
        )

        table = self.create_table(
            table_name,
            df
        )

        dataset.model.add_table(table)

        self.statistics.table_count = 1

        self.disconnect()

        self.statistics.execution_time_ms = (
            time.perf_counter() - start
        ) * 1000

        return DataSourceResult(
            dataset=dataset,
            statistics=self.statistics
        )