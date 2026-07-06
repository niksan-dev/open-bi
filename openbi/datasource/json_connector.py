import json
import pandas as pd

from openbi.datasource.datasource import DataSource


class JSONConnector(DataSource):
    """
    JSON Connector

    Supports:
        • JSON Array
        • Nested JSON
        • Multiple Tables
    """

    @property
    def name(self) -> str:
        return "JSON Connector"

    # --------------------------------------------------
    # Connection
    # --------------------------------------------------

    def connect(self):

        self.validate()

    def disconnect(self):

        pass

    # --------------------------------------------------
    # Read
    # --------------------------------------------------

    def read(self) -> dict[str, pd.DataFrame]:

        with open(

            self.source,

            "r",

            encoding=self.options.encoding

        ) as file:

            data = json.load(file)

        # -----------------------------------------
        # JSON Array
        # -----------------------------------------

        if isinstance(data, list):

            table_name = (

                self.options.table_name
                or self.source_name

            )

            return {

                table_name:

                pd.DataFrame(data)

            }

        # -----------------------------------------
        # JSON Object
        # -----------------------------------------

        if isinstance(data, dict):

            tables = {}

            # Multiple Tables

            for key, value in data.items():

                if isinstance(value, list):

                    tables[key] = pd.DataFrame(value)

            if tables:

                return tables

            # Nested JSON

            if self.options.normalize_nested:

                dataframe = pd.json_normalize(data)

            else:

                dataframe = pd.DataFrame([data])

            table_name = (

                self.options.table_name
                or self.source_name

            )

            return {

                table_name:

                dataframe

            }

        raise ValueError(

            "Unsupported JSON format."

        )