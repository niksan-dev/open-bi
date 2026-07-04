from abc import ABC, abstractmethod
import pandas as pd

from openbi.pipeline.step_result import StepResult


class PipelineStep(ABC):

    @property
    def name(self) -> str:
        return self.__class__.__name__

    @abstractmethod
    def process(self, dataframe: pd.DataFrame) -> StepResult:
        pass