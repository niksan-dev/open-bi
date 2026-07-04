
from openbi.pipeline.pipeline_step import PipelineStep


class DuplicateRemover(PipelineStep):

    @property
    def name(self) -> str:
        return "Duplicate Remover"

    def process(self, dataframe):

        return dataframe.drop_duplicates()