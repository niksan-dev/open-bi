import time
import requests
import pandas as pd

from openbi.datasource.datasource import DataSource
from openbi.datasource.datasource_result import DataSourceResult


class RESTConnector(DataSource):
    """
    Generic REST API connector.
    """

    def __init__(
        self,
        url: str,
        dataset_name: str = None,
        headers: dict | None = None,
        params: dict | None = None,
        auth=None,
        timeout: int = 30
    ):

        super().__init__(url)

        self.url = url

        self.dataset_name = dataset_name

        self.headers = headers or {}

        self.params = params or {}

        self.auth = auth

        self.timeout = timeout

    @property
    def name(self):

        return "REST Connector"

    def connect(self):

        return True

    def disconnect(self):

        return True

    def load(self):

        start = time.perf_counter()

        response = requests.get(

            self.url,

            headers=self.headers,

            params=self.params,

            auth=self.auth,

            timeout=self.timeout

        )

        response.raise_for_status()

        data = response.json()

        dataset = self.create_dataset(

            self.dataset_name
            or "REST API"

        )

        # ---------------------------------
        # JSON Array
        # ---------------------------------

        if isinstance(data, list):

            df = pd.DataFrame(data)

            table = self.create_table(

                "Data",

                df

            )

            dataset.model.add_table(table)

        # ---------------------------------
        # JSON Object
        # ---------------------------------

        elif isinstance(data, dict):

            created = False

            for key, value in data.items():

                if isinstance(value, list):

                    df = pd.DataFrame(value)

                    table = self.create_table(

                        key,

                        df

                    )

                    dataset.model.add_table(table)

                    created = True

            if not created:

                df = pd.json_normalize(data)

                table = self.create_table(

                    "Data",

                    df

                )

                dataset.model.add_table(table)

        else:

            raise ValueError(

                "Unsupported API response."

            )

        self.statistics.table_count = len(

            dataset.model.tables

        )

        self.statistics.execution_time_ms = (

            time.perf_counter() - start

        ) * 1000

        return DataSourceResult(

            dataset=dataset,

            statistics=self.statistics

        )