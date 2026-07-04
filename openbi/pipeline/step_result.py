from dataclasses import dataclass

import pandas as pd

from openbi.pipeline.step_statistics import StepStatistics


@dataclass
class StepResult:

    dataframe: pd.DataFrame

    statistics: StepStatistics