import pandas as pd

from openbi.metadata.column_metadata import ColumnMetadata
from openbi.profiler.statistics_profiler import StatisticsProfiler
from openbi.profiler.datatype_detector import DataTypeDetector
from openbi.profiler.key_detector import KeyDetector


class MetadataProfiler:
    """
    Profiles an entire DataFrame and returns metadata for each column.
    """

    def profile(self, dataframe: pd.DataFrame) -> dict[str, ColumnMetadata]:

        metadata_map: dict[str, ColumnMetadata] = {}

        for column_name in dataframe.columns:

            series = dataframe[column_name]

            # Create metadata object
            metadata = ColumnMetadata()

            # -----------------------------------
            # Detect Data Type
            # -----------------------------------
            metadata.dtype = DataTypeDetector.detect(series)

            # -----------------------------------
            # Compute Statistics
            # -----------------------------------
            stats = StatisticsProfiler.profile(series)

            metadata.null_count = stats["null_count"]
            metadata.distinct_count = stats["distinct_count"]
            metadata.is_unique = stats["is_unique"]
            metadata.sample_values = stats["sample_values"]

            metadata.min_value = stats["min"]
            metadata.max_value = stats["max"]
            metadata.mean = stats["mean"]

            metadata.nullable = metadata.null_count > 0

            # -----------------------------------
            # Detect Primary Key
            # -----------------------------------
            metadata.primary_key_candidate = KeyDetector.detect(
                column_name,
                metadata
            )

            # -----------------------------------
            # Future Modules
            # -----------------------------------
            #
            # metadata.pattern = PatternDetector.detect(series)
            #
            # metadata.data_quality =
            #       QualityProfiler.profile(series)
            #
            # metadata.foreign_key_candidate =
            #       RelationshipDetector.detect(...)
            #

            metadata_map[column_name] = metadata

        return metadata_map