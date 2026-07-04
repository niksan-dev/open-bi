from dataclasses import dataclass, field

@dataclass
class PipelineContext:

    current_step: str = ""

    warnings: list[str] = field(default_factory=list)

    errors: list[str] = field(default_factory=list)