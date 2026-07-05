import pandas as pd


class KeyDetector:

    PRIMARY_KEY_KEYWORDS = {
        "id",
        "_id",
        "code",
        "number",
        "key"
    }

    @staticmethod
    def is_primary_key_candidate(
        column_name: str,
        series: pd.Series
    ) -> bool:

        # Must not contain NULLs
        if series.isna().any():
            return False

        # Must be unique
        if not series.is_unique:
            return False

        name = column_name.lower()

        return any(
            keyword in name
            for keyword in KeyDetector.PRIMARY_KEY_KEYWORDS
        )

    @staticmethod
    def is_foreign_key_candidate(
        column_name: str
    ) -> bool:

        name = column_name.lower()

        return (
            name.endswith("id")
            or name.endswith("_id")
        )