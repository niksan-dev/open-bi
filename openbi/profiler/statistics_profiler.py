import pandas as pd


class StatisticsProfiler:

    @staticmethod
    def profile(series: pd.Series):

        stats = {}

        stats["null_count"] = int(series.isna().sum())

        stats["distinct_count"] = int(series.nunique())

        stats["is_unique"] = bool(series.is_unique)

        stats["sample_values"] = (
            series.dropna()
                  .head(5)
                  .tolist()
        )

        if pd.api.types.is_numeric_dtype(series):

            stats["min"] = float(series.min())

            stats["max"] = float(series.max())

            stats["mean"] = float(series.mean())

        else:

            stats["min"] = None
            stats["max"] = None
            stats["mean"] = None

        return stats