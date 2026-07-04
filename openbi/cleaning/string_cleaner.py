import pandas as pd

from openbi.pipeline.pipeline_step import PipelineStep
from openbi.pipeline.step_result import StepResult
from openbi.pipeline.step_statistics import StepStatistics


class StringCleaner(PipelineStep):
    """
    Cleans string values.

    - Removes extra spaces
    - Removes tabs/newlines
    - Collapses multiple spaces
    """

    @property
    def name(self) -> str:
        return "String Cleaner"

    def process(self, dataframe: pd.DataFrame) -> StepResult:

        df = dataframe.copy()

        stats = StepStatistics()
        stats.step_name = self.name

        stats.capture_before(df)

        values_changed = 0

        object_columns = df.select_dtypes(
            include=["object", "string"]
        ).columns

        for column in object_columns:

            original = df[column].copy()

            cleaned = (
                original
                .astype("string")
                .str.replace(r"[\r\n\t]+", " ", regex=True)
                .str.replace(r"\s{2,}", " ", regex=True)
            )

            changed = (
                original.astype("string")
                != cleaned
            )

            values_changed += int(
                changed.fillna(False).sum()
            )

            df[column] = cleaned

        stats.capture_after(df)

        stats.values_changed = values_changed

        return StepResult(
            dataframe=df,
            statistics=stats
        )