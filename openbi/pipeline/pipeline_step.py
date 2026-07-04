from abc import ABC, abstractmethod
import pandas as pd


class PipelineStep(ABC):

    @property
    def name(self) -> str:
        return self.__class__.__name__

    @abstractmethod
    def process(self, dataframe: pd.DataFrame) -> pd.DataFrame:
        pass