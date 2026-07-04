import pandas as pd

from openbi.model.dataset import Dataset
from openbi.model.table import Table

dataset = Dataset(name="Retail Sales")

df = pd.read_excel("examples/sales.xlsx", sheet_name="Orders")

orders = Table.from_dataframe(
    name="Orders",
    dataframe=df
)

dataset.model.add_table(orders)

print(orders.row_count)
print(orders.column_count)