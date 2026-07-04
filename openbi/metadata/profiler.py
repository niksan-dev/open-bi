import pandas as pd

from openbi.metadata.column_metadata import ColumnMetadata
from openbi.metadata.detector import KeyDetector

class MetadataProfiler:

    def profile(self, dataframe: pd.DataFrame):

        result = {}

        for column in dataframe.columns:

            series = dataframe[column]

            metadata = ColumnMetadata()

            metadata.dtype = str(series.dtype)

            metadata.null_count = int(series.isna().sum())

            metadata.nullable = metadata.null_count > 0

            metadata.distinct_count = int(series.nunique())

            metadata.is_unique = series.is_unique

            metadata.primary_key_candidate = KeyDetector.is_primary_key_candidate(
                column,
                metadata
            )

            metadata.sample_values = (
                series.dropna()
                      .head(5)
                      .tolist()
            )

            # Numeric statistics

            if pd.api.types.is_numeric_dtype(series):

                metadata.min_value = float(series.min())

                metadata.max_value = float(series.max())

                metadata.mean = float(series.mean())

            result[column] = metadata

        return result