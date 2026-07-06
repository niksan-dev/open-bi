from dataclasses import dataclass

from openbi.connector_options.connector_options import ConnectorOptions


@dataclass
class ExcelOptions(ConnectorOptions):

    sheet_name=None

    header=0

    skip_rows=0