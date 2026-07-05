import json
import pandas as pd

from openbi.datasource.datasource import DataSource


class JSONConnector(DataSource):

    def __init__(
        self,
        source: str,
        dataset_name: str = None
    ):

        super().__init__(source)

        self.dataset_name = dataset_name

    @property
    def name(self):

        return "JSON Connector"

    def connect(self):

        self.validate()

    def disconnect(self):

        pass

    def load(self):

        self.connect()

        with open(
            self.source,
            "r",
            encoding="utf-8"
        ) as file:

            data = json.load(file)

        dataset = self.create_dataset(

            self.dataset_name
            or self.source_name

        )

        # ---------------------------------
        # JSON Array
        # ---------------------------------

        if isinstance(data, list):

            self.add_table(

                dataset,

                self.source_name,

                pd.DataFrame(data)

            )

        # ---------------------------------
        # JSON Object
        # ---------------------------------

        elif isinstance(data, dict):

            created = False

            for key, value in data.items():

                if isinstance(value, list):

                    self.add_table(

                        dataset,

                        key,

                        pd.DataFrame(value)

                    )

                    created = True

            if not created:

                self.add_table(

                    dataset,

                    self.source_name,

                    pd.json_normalize(data)

                )

        else:

            raise ValueError(

                "Unsupported JSON format."

            )

        self.disconnect()

        return self.create_result(dataset)