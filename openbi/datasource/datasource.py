from abc import ABC, abstractmethod
from pathlib import Path

from openbi.datasource.datasource_result import DataSourceResult
from openbi.datasource.datasource_statistics import DataSourceStatistics


class DataSource(ABC):
    """
    Base class for all OpenBI data source connectors.

    Examples:
        - ExcelConnector
        - CSVConnector
        - SQLiteConnector
        - SQLServerConnector
        - PostgreSQLConnector
        - RESTConnector
    """

    def __init__(self, source: str):

        self.source = source

        self.statistics = DataSourceStatistics()

    @property
    @abstractmethod
    def name(self) -> str:
        """
        Friendly connector name.
        """

        pass

    @property
    def source_name(self) -> str:

        return Path(self.source).name

    @property
    def source_path(self) -> str:

        return str(Path(self.source).resolve())

    @property
    def exists(self) -> bool:

        return Path(self.source).exists()

    @abstractmethod
    def connect(self):
        """
        Establish connection if required.

        File connectors can simply return True.
        Database connectors open a connection.
        """

        pass

    @abstractmethod
    def disconnect(self):
        """
        Close any active connection.
        """

        pass

    @abstractmethod
    def load(self) -> DataSourceResult:
        """
        Load the data source.

        Returns
        -------
        DataSourceResult
        """

        pass

    def validate(self):

        if not self.exists:

            raise FileNotFoundError(

                f"Data source not found:\n{self.source}"

            )

        return True