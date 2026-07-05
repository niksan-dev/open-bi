import pandas as pd

from openbi.metadata.column_metadata import ColumnMetadata
from openbi.metadata.detector import KeyDetector


class MetadataProfiler:

    @staticmethod
    def profile(table):

        dataframe = table.dataframe

        for column in table.columns:

            series = dataframe[column.name]

            metadata = ColumnMetadata()

            metadata.dtype = str(series.dtype)

            metadata.null_count = int(series.isna().sum())

            metadata.nullable = metadata.null_count > 0

            metadata.distinct_count = int(series.nunique(dropna=True))

            metadata.is_unique = series.is_unique

            metadata.primary_key_candidate = (
                KeyDetector.is_primary_key_candidate(
                    column.name,
                    metadata
                )
            )

            metadata.foreign_key_candidate = (
                KeyDetector.is_foreign_key_candidate(
                    column.name,
                    metadata
                )
            )

            metadata.sample_values = (
                series.dropna()
                .head(5)
                .tolist()
            )

            if pd.api.types.is_numeric_dtype(series):

                metadata.min_value = float(series.min())

                metadata.max_value = float(series.max())

                metadata.mean = float(series.mean())

            column.metadata = metadata

        return table