import pandas as pd

from openbi.enums.null_strategy import NullStrategy
from openbi.pipeline.pipeline_step import PipelineStep
from openbi.enums.null_strategy import NullStrategy

class NullHandler(PipelineStep):

    def __init__(
        self,
        strategy: NullStrategy = NullStrategy.KEEP,
        fill_value=None
    ):

        self.strategy = strategy
        self.fill_value = fill_value

    @property
    def name(self) -> str:
        return "Null Handler"

    def process(self, dataframe: pd.DataFrame) -> pd.DataFrame:

        df = dataframe.copy()

        if self.strategy == NullStrategy.KEEP:
            return df

        if self.strategy == NullStrategy.DROP_ROWS:
            return df.dropna()

        if self.strategy == NullStrategy.DROP_COLUMNS:
            return df.dropna(axis=1)

        if self.strategy == NullStrategy.FILL:

            return df.fillna(self.fill_value)

        raise ValueError(
            f"Unknown null handling strategy: {self.strategy}"
        )