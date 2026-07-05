

from dataclasses import dataclass


@dataclass
class DataSourceStatistics:

    execution_time_ms: float = 0

    table_count: int = 0

    row_count: int = 0

    column_count: int = 0