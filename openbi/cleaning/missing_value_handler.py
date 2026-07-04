import pandas as pd

from openbi.pipeline.pipeline_step import PipelineStep


class MissingValueHandler(PipelineStep):

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

    def process(self, dataframe: pd.DataFrame) -> pd.DataFrame:

        df = dataframe.copy()

        object_columns = df.select_dtypes(
            include=["object", "string"]
        ).columns

        for column in object_columns:

            df[column] = (
                df[column]
                .astype("string")
                .str.strip()
            )

            df[column] = df[column].replace(
                list(self.missing_values),
                pd.NA
            )

        return df