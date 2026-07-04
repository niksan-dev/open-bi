
from openbi.pipeline.pipeline_step import PipelineStep


class WhitespaceCleaner(PipelineStep):

    @property
    def name(self) -> str:
        return "Whitespace Cleaner"

    def process(self, dataframe):

        df = dataframe.copy()

        for col in df.select_dtypes(include="object"):

            df[col] = df[col].astype(str).str.strip()

        return df