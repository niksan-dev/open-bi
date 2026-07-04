import pandas as pd

from openbi.cleaning.date_normalizer import DateNormalizer


class DataCleaner:

    @property
    def name(self):

        return "Date Cleaner"
    @staticmethod
    def clean(df: pd.DataFrame) -> pd.DataFrame:

        df = df.copy()

        for column in df.columns:
            df[column] = DateNormalizer.normalize(df[column])

        return df