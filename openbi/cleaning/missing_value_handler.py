import pandas as pd

from openbi.pipeline.pipeline_step import PipelineStep
from openbi.pipeline.step_result import StepResult
from openbi.pipeline.step_statistics import StepStatistics


class MissingValueHandler(PipelineStep):
    """
    Standardizes different representations of missing values.

    Example

        NULL
        null
        N/A
        ""
        --
        None

    become

        <NA>
    """

    DEFAULT_MISSING_VALUES = {
        "",
        " ",
        "NULL",
        "null",
        "Null",
        "N/A",
        "n/a",
        "NA",
        "na",
        "NaN",
        "nan",
        "None",
        "none",
        "-",
        "--"
    }

    def __init__(self, missing_values=None):

        self.missing_values = (
            set(missing_values)
            if missing_values
            else self.DEFAULT_MISSING_VALUES
        )

    @property
    def name(self) -> str:
        return "Missing Value Handler"

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

            series = df[column].astype("string")

            original = series.copy()

            cleaned = series.str.strip()

            cleaned = cleaned.replace(
                list(self.missing_values),
                pd.NA
            )

            changed = (
                original.fillna("<NA>")
                != cleaned.fillna("<NA>")
            )

            values_changed += int(
                changed.sum()
            )

            df[column] = cleaned

        stats.capture_after(df)

        stats.values_changed = values_changed

        return StepResult(
            dataframe=df,
            statistics=stats
        )