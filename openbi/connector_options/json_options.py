from dataclasses import dataclass

from openbi.connector_options.connector_options import ConnectorOptions


@dataclass
class JSONOptions(ConnectorOptions):

    encoding="utf-8"

    normalize=True

    table_name: str | None = None