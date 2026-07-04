import pandas as pd

from openbi.pipeline.pipeline_step import PipelineStep
from openbi.pipeline.step_result import StepResult
from openbi.pipeline.step_statistics import StepStatistics


class DateNormalizer(PipelineStep):
    """
    Normalizes date columns to a standard format.

    Example:

        03-07-2026
        03/07/2027
        03.07.2028

    becomes

        03-07-2026
        03-07-2027
        03-07-2028
    """

    DATE_FORMATS = [
        "%d-%m-%Y",
        "%d/%m/%Y",
        "%d.%m.%Y",
        "%Y-%m-%d",
        "%m/%d/%Y",
    ]

    OUTPUT_FORMAT = "%d-%m-%Y"

    CONFIDENCE_THRESHOLD = 0.80

    @property
    def name(self) -> str:
        return "Date Normalizer"

    def process(self, dataframe: pd.DataFrame) -> StepResult:

        df = dataframe.copy()

        stats = StepStatistics()
        stats.step_name = self.name
        stats.capture_before(df)

        normalized_count = 0

        object_columns = df.select_dtypes(
            include=["object", "string"]
        ).columns

        for column in object_columns:

            original_series = df[column]

            if original_series.dropna().empty:
                continue

            normalized_values = []
            parsed_count = 0

            for value in original_series:

                if pd.isna(value):
                    normalized_values.append(value)
                    continue

                text = str(value).strip()

                parsed = None

                for fmt in self.DATE_FORMATS:

                    try:
                        parsed = pd.to_datetime(
                            text,
                            format=fmt,
                            errors="raise"
                        )
                        break

                    except Exception:
                        pass

                if parsed is not None:

                    normalized = parsed.strftime(
                        self.OUTPUT_FORMAT
                    )

                    normalized_values.append(normalized)

                    if normalized != text:
                        normalized_count += 1

                    parsed_count += 1

                else:

                    normalized_values.append(value)

            total_values = original_series.notna().sum()

            if total_values == 0:
                continue

            confidence = parsed_count / total_values

            if confidence >= self.CONFIDENCE_THRESHOLD:

                df[column] = normalized_values

        stats.capture_after(df)

        stats.values_changed = normalized_count

        return StepResult(
            dataframe=df,
            statistics=stats
        )