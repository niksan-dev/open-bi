from enum import Enum

class NullStrategy(Enum):
    KEEP = "keep"
    DROP_ROWS = "drop_rows"
    DROP_COLUMNS = "drop_columns"
    FILL = "fill"