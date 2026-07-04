import pandas as pd

from openbi.pipeline.pipeline_step import PipelineStep
from openbi.pipeline.step_result import StepResult
from openbi.pipeline.step_statistics import StepStatistics
from openbi.profiler.datatype_detector import DataTypeDetector
from openbi.enums.data_type import DataType


class TypeConverter(PipelineStep):
    """
    Converts DataFrame columns to the most appropriate pandas dtype.
    """

    @property
    def name(self) -> str:
        return "Type Converter"

    def process(self, dataframe: pd.DataFrame) -> StepResult:

        df = dataframe.copy()

        stats = StepStatistics()
        stats.step_name = self.name
        stats.capture_before(df)

        converted_columns = 0

        for column in df.columns:

            original_dtype = str(df[column].dtype)

            detected_type = DataTypeDetector.detect(df[column])

            try:

                # ----------------------------------------
                # Integer
                # ----------------------------------------

                if detected_type == DataType.INTEGER:

                    df[column] = pd.to_numeric(
                        df[column],
                        errors="coerce"
                    ).astype("Int64")

                # ----------------------------------------
                # Float
                # ----------------------------------------

                elif detected_type == DataType.FLOAT:

                    df[column] = pd.to_numeric(
                        df[column],
                        errors="coerce"
                    )

                # ----------------------------------------
                # Boolean
                # ----------------------------------------

                elif detected_type == DataType.BOOLEAN:

                    df[column] = (
                        df[column]
                        .astype("boolean")
                    )

                # ----------------------------------------
                # Date
                # ----------------------------------------

                elif detected_type == DataType.DATETIME:

                    df[column] = pd.to_datetime(
                        df[column],
                        format="%d-%m-%Y",
                        errors="coerce"
                    )

                # ----------------------------------------
                # String
                # ----------------------------------------

                else:

                    df[column] = df[column].astype("string")

            except Exception as ex:

                stats.warnings.append(
                    f"{column}: {str(ex)}"
                )

                continue

            if original_dtype != str(df[column].dtype):
                converted_columns += 1

        stats.capture_after(df)

        stats.columns_changed = converted_columns

        return StepResult(
            dataframe=df,
            statistics=stats
        )