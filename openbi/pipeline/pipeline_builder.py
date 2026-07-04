
from openbi.cleaning.date_normalizer import DateNormalizer
from openbi.pipeline.pipeline import DataPipeline
from openbi.cleaning.whitespace_cleaner import WhitespaceCleaner
from openbi.cleaning.string_cleaner import StringCleaner
from openbi.cleaning.date_normalizer import DateNormalizer
from openbi.cleaning.null_handler import NullHandler
from openbi.cleaning.duplicate_remover import DuplicateRemover
from openbi.cleaning.type_converter import TypeConverter
from openbi.enums.null_strategy import NullStrategy

class DefaultPipeline:

    @staticmethod
    def create():

        return (
            DataPipeline()
            .add(WhitespaceCleaner())
            .add(StringCleaner())
             .add(DateNormalizer())
            .add(NullHandler(
                strategy=NullStrategy.DROP_ROWS
            ))
            .add(DuplicateRemover())
            .add(TypeConverter())
        )