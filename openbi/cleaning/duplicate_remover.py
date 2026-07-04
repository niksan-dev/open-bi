import pandas as pd

from openbi.pipeline.pipeline_step import PipelineStep
from openbi.pipeline.step_result import StepResult
from openbi.pipeline.step_statistics import StepStatistics


class DuplicateRemover(PipelineStep):
    """
    Removes duplicate rows from the DataFrame.
    """

    @property
    def name(self) -> str:
        return "Duplicate Remover"

    def process(self, dataframe: pd.DataFrame) -> StepResult:

        df = dataframe.copy()

        stats = StepStatistics()
        stats.step_name = self.name

        # Capture initial state
        stats.capture_before(df)

        before_rows = len(df)

        df = df.drop_duplicates(ignore_index=True)

        after_rows = len(df)

        stats.capture_after(df)

        stats.rows_removed = before_rows - after_rows

        # Optional
        stats.values_changed = before_rows - after_rows

        return StepResult(
            dataframe=df,
            statistics=stats
        )