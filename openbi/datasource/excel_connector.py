import pandas as pd

from openbi.datasource.datasource import DataSource


class ExcelConnector(DataSource):

    def __init__(
        self,
        source: str,
        dataset_name: str = None
    ):

        super().__init__(source)

        self.dataset_name = dataset_name

    @property
    def name(self):

        return "Excel Connector"

    def connect(self):

        self.validate()

    def disconnect(self):

        pass

    def load(self):

        self.connect()

        workbook = pd.read_excel(

            self.source,

            sheet_name=None

        )

        dataset = self.create_dataset(

            self.dataset_name
            or self.source_name

        )

        for sheet_name, dataframe in workbook.items():

            self.add_table(

                dataset,

                sheet_name,

                dataframe

            )

        self.disconnect()

        return self.create_result(dataset)