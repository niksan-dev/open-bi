from dataclasses import dataclass

from openbi.connector_options.connector_options import ConnectorOptions


@dataclass
class CSVOptions(ConnectorOptions):

    delimiter: str = ","

    encoding: str = "utf-8"

    header: int = 0

    skip_rows: int = 0

    quotechar: str = '"'