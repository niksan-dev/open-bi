import pandas as pd

from openbi.pipeline.pipeline_step import PipelineStep


class StringCleaner(PipelineStep):

    @property
    def name(self) -> str:
        return "String Cleaner"

    def process(self, dataframe: pd.DataFrame) -> pd.DataFrame:

        df = dataframe.copy()

        object_columns = df.select_dtypes(
            include=["object", "string"]
        ).columns

        for column in object_columns:

            df[column] = (
                df[column]
                .astype("string")
                .str.strip()                    # Remove leading/trailing spaces
                .str.replace(r"\s+", " ", regex=True)  # Multiple spaces -> single
            )

        return df