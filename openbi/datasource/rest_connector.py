import time
import requests
import pandas as pd

from openbi.datasource.datasource import DataSource
from openbi.datasource.datasource_result import DataSourceResult


class RESTConnector(DataSource):

    @property
    def name(self):
        return "REST Connector"

    def connect(self):
        pass

    def disconnect(self):
        pass

    def read(self):

        response = requests.get(

            self.source,

            headers=self.options.headers,

            params=self.options.params,

            timeout=self.options.timeout,

            auth=self.options.auth

        )

        response.raise_for_status()

        data = response.json()

        if isinstance(data, list):

            return {
                "Data": pd.DataFrame(data)
            }

        if isinstance(data, dict):

            return {
                "Data": pd.json_normalize(data)
            }

        raise ValueError("Unsupported response.")