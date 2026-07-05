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

    def read(self):

        response = requests.get(

            self.url

        )

        response.raise_for_status()

        return {

            "Data":

            pd.DataFrame(

                response.json()

            )

        }