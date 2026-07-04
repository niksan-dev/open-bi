import pandas as pd

from openbi.pipeline.pipeline_step import PipelineStep
from openbi.pipeline.step_result import StepResult
from openbi.pipeline.step_statistics import StepStatistics
from openbi.enums.null_strategy import NullStrategy


class NullHandler(PipelineStep):
    """
    Handles null values according to the selected strategy.
    """

    def __init__(
        self,
        strategy: NullStrategy = NullStrategy.KEEP,
        fill_value=None
    ):
        self.strategy = strategy
        self.fill_value = fill_value

    @property
    def name(self) -> str:
        return "Null Handler"

    def process(self, dataframe: pd.DataFrame) -> StepResult:

        df = dataframe.copy()

        stats = StepStatistics()
        stats.step_name = self.name
        stats.capture_before(df)

        null_count_before = int(df.isna().sum().sum())

        # --------------------------------------------------
        # KEEP
        # --------------------------------------------------

        if self.strategy == NullStrategy.KEEP:

            pass

        # --------------------------------------------------
        # DROP ROWS
        # --------------------------------------------------

        elif self.strategy == NullStrategy.DROP_ROWS:

            before = len(df)

            df = df.dropna()

            stats.rows_removed = before - len(df)

        # --------------------------------------------------
        # DROP COLUMNS
        # --------------------------------------------------

        elif self.strategy == NullStrategy.DROP_COLUMNS:

            before = len(df.columns)

            df = df.dropna(axis=1)

            stats.columns_removed = before - len(df.columns)

        # --------------------------------------------------
        # FILL
        # --------------------------------------------------

        elif self.strategy == NullStrategy.FILL:

            df = df.fillna(self.fill_value)

        else:

            raise ValueError(
                f"Unknown NullStrategy: {self.strategy}"
            )

        null_count_after = int(df.isna().sum().sum())

        stats.capture_after(df)

        stats.values_changed = null_count_before - null_count_after

        return StepResult(
            dataframe=df,
            statistics=stats
        )