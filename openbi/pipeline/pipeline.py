import pandas as pd
import time
from openbi.pipeline.pipeline_context import PipelineContext
from openbi.pipeline.pipeline_result import PipelineResult
class DataPipeline:

    def __init__(self):

        self.steps = []

    def add(self, step):

        self.steps.append(step)

        return self

    def execute(self, dataframe: pd.DataFrame):

        context = PipelineContext()

        df = dataframe.copy()

        for step in self.steps:

            start = time.perf_counter()

            context.current_step = step.name

            df = step.process(df)

            elapsed = time.perf_counter() - start

            print(f"[{step.name}] {elapsed:.3f}s")

        return PipelineResult(df, context)