from dataclasses import dataclass, field

from openbi.connector_options.connector_options import ConnectorOptions


@dataclass
class RESTOptions(ConnectorOptions):

    headers: dict = field(default_factory=dict)

    params: dict = field(default_factory=dict)

    timeout: int = 30

    auth: object = None