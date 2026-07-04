from dataclasses import dataclass, field

from openbi.pipeline.step_statistics import StepStatistics


@dataclass
class PipelineStatistics:

    total_execution_time_ms: float = 0.0

    rows_before: int = 0

    rows_after: int = 0

    columns_before: int = 0

    columns_after: int = 0

    steps: list[StepStatistics] = field(default_factory=list)

    warnings: list[str] = field(default_factory=list)

    errors: list[str] = field(default_factory=list)

    @property
    def rows_removed(self):

        return self.rows_before - self.rows_after