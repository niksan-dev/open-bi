import time
import pandas as pd

from openbi.datasource.datasource import DataSource


class CSVConnector(DataSource):

    def __init__(
        self,
        source: str,
        dataset_name: str = None,
        table_name: str = None
    ):

        super().__init__(source)

        self.dataset_name = dataset_name
        self.table_name = table_name

    @property
    def name(self):

        return "CSV Connector"

    def connect(self):

        self.validate()

    def disconnect(self):

        pass

    def load(self):

        start = time.perf_counter()

        self.connect()

        df = pd.read_csv(self.source)

        dataset = self.create_dataset(

            self.dataset_name
            or self.source_name

        )

        self.add_table(

            dataset,

            self.table_name
            or self.source_name,

            df

        )

        self.statistics.execution_time_ms = (

            time.perf_counter() - start

        ) * 1000

        self.disconnect()

        return self.create_result(dataset)