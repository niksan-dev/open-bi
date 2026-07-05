import json
import pandas as pd

from openbi.datasource.datasource import DataSource


class JSONConnector(DataSource):

    @property
    def name(self):

        return "JSON Connector"

    def connect(self):

        self.validate()

    def disconnect(self):

        pass

    def read(self):

        with open(

            self.source,

            encoding="utf-8"

        ) as file:

            data = json.load(file)

        if isinstance(data, list):

            return {

                self.source_name:

                pd.DataFrame(data)

            }

        if isinstance(data, dict):

            tables = {}

            for key, value in data.items():

                if isinstance(value, list):

                    tables[key] = pd.DataFrame(value)

            if tables:

                return tables

            return {

                self.source_name:

                pd.json_normalize(data)

            }

        raise ValueError(

            "Unsupported JSON."

        )