import time

from openbi.pipeline.pipeline_context import PipelineContext
from openbi.pipeline.pipeline_result import PipelineResult


class DataPipeline:

    def __init__(self):

        self.steps = []

    def add(self, step):

        self.steps.append(step)

        return self

    def execute(self, dataframe):

        context = PipelineContext()

        stats = context.statistics

        df = dataframe.copy()

        stats.rows_before = len(df)
        stats.columns_before = len(df.columns)

        pipeline_start = time.perf_counter()

        for step in self.steps:

            context.current_step = step.name

            start = time.perf_counter()

            step_result = step.process(df)

            end = time.perf_counter()

            # Update execution time
            step_result.statistics.execution_time_ms = (
                end - start
            ) * 1000

            # Update DataFrame
            df = step_result.dataframe

            # Collect statistics
            stats.steps.append(
                step_result.statistics
            )

        pipeline_end = time.perf_counter()

        stats.total_execution_time_ms = (
            pipeline_end - pipeline_start
        ) * 1000

        stats.rows_after = len(df)
        stats.columns_after = len(df.columns)

        return PipelineResult(
            dataframe=df,
            context=context
        )