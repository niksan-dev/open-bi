

from openbi.pipeline.pipeline_step import PipelineStep


class TypeConverter(PipelineStep):

    @property
    def name(self) -> str:
        return "Type Converter"

    def process(self, dataframe):

        return dataframe.convert_dtypes()