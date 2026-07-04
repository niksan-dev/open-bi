from dataclasses import dataclass
from openbi.pipeline.pipeline_context import PipelineContext
import pandas as pd

@dataclass
class PipelineResult:

    dataframe: pd.DataFrame

    context: PipelineContext

    @property
    def statistics(self):

        return self.context.statistics