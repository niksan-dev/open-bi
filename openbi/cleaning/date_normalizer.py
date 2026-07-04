import pandas as pd

from openbi.pipeline.pipeline_step import PipelineStep


class DateNormalizer(PipelineStep):
    """
    Normalize date columns to a standard format (dd-MM-yyyy).
    """

    @property
    def name(self) -> str:
        return "Date Normalizer"

    def process(self, dataframe: pd.DataFrame) -> pd.DataFrame:

        df = dataframe.copy()

        object_columns = df.select_dtypes(
            include=["object", "string"]
        ).columns

        for column in object_columns:

            series = df[column]

            # Skip empty columns
            if series.dropna().empty:
                continue

            # Normalize separators
            values = (
                series.astype("string")
                      .str.strip()
                      .str.replace("/", "-", regex=False)
                      .str.replace(".", "-", regex=False)
            )

            # Parse dates
            parsed = pd.to_datetime(
                values,
                format="%d-%m-%Y",
                errors="coerce"
            )

            # If most values are valid dates, treat the column as a date column
            valid_ratio = parsed.notna().sum() / len(values)

            if valid_ratio >= 0.8:
                mask = parsed.notna()

                df.loc[mask, column] = (
                    parsed.loc[mask]
                          .dt.strftime("%d-%m-%Y")
                )

        return df