

from dataclasses import dataclass

from openbi.model.dataset import Dataset
from openbi.datasource.datasource_statistics import DataSourceStatistics

@dataclass
class DataSourceResult:

    dataset: Dataset

    statistics: DataSourceStatistics