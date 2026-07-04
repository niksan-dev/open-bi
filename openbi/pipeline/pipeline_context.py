from dataclasses import dataclass, field
from openbi.pipeline.pipeline_statistics import PipelineStatistics
@dataclass
class PipelineContext:

    current_step: str = ""

    warnings: list[str] = field(default_factory=list)

    errors: list[str] = field(default_factory=list)

    statistics: PipelineStatistics = field(
        default_factory=PipelineStatistics
    )