import pandas as pd

from openbi.pipeline.pipeline_step import PipelineStep
from openbi.pipeline.step_result import StepResult
from openbi.pipeline.step_statistics import StepStatistics


class WhitespaceCleaner(PipelineStep):
    """
    Removes leading/trailing whitespace from string columns.
    """

    @property
    def name(self) -> str:
        return "Whitespace Cleaner"

    def process(self, dataframe: pd.DataFrame) -> StepResult:

        df = dataframe.copy()

        stats = StepStatistics()
        stats.step_name = self.name

        stats.rows_before = len(df)
        stats.columns_before = len(df.columns)

        values_changed = 0

        object_columns = df.select_dtypes(
            include=["object", "string"]
        ).columns

        for column in object_columns:

            original = df[column].copy()

            cleaned = (
                original
                .astype("string")
                .str.strip()
            )

            changed = (
                original.astype("string")
                != cleaned
            )

            values_changed += int(changed.fillna(False).sum())

            df[column] = cleaned

        stats.rows_after = len(df)
        stats.columns_after = len(df.columns)
        stats.values_changed = values_changed

        return StepResult(
            dataframe=df,
            statistics=stats
        )