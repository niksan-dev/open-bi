import pandas as pd
from openbi.enums.data_type import DataType

DATE_FORMATS = [
    "%d-%m-%Y",
    "%Y-%m-%d",
    "%d/%m/%Y",
    "%m/%d/%Y",
    "%d.%m.%Y",
]


class DataTypeDetector:

    @staticmethod
    def detect(series: pd.Series):

        if pd.api.types.is_integer_dtype(series):
            return DataType.INTEGER

        if pd.api.types.is_float_dtype(series):
            return DataType.FLOAT

        if pd.api.types.is_datetime64_any_dtype(series):
            return DataType.DATETIME

        if pd.api.types.is_bool_dtype(series):
            return DataType.BOOLEAN

        if pd.api.types.is_object_dtype(series) or pd.api.types.is_string_dtype(series):

            values = series.dropna().astype(str)

            # Normalize separators
            values = (
                values
                .str.replace("/", "-", regex=False)
                .str.replace(".", "-", regex=False)
            )

            try:
                pd.to_datetime(
                    values,
                    format="%d-%m-%Y",
                    errors="raise"
                )
                return DataType.DATETIME

            except Exception:
                pass

        return DataType.STRING