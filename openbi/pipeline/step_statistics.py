from dataclasses import dataclass, field
import pandas as pd


@dataclass
class StepStatistics:

    step_name: str = ""

    rows_before: int = 0
    rows_after: int = 0

    columns_before: int = 0
    columns_after: int = 0

    rows_removed: int = 0
    rows_added: int = 0

    columns_removed: int = 0
    columns_added: int = 0
    columns_changed: int = 0

    values_changed: int = 0

    execution_time_ms: float = 0.0

    warnings: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)

    def capture_before(self, df: pd.DataFrame):

        self.rows_before = len(df)
        self.columns_before = len(df.columns)

    def capture_after(self, df: pd.DataFrame):

        self.rows_after = len(df)
        self.columns_after = len(df.columns)