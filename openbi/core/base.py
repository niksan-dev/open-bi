from dataclasses import dataclass, field
from datetime import datetime
import uuid


@dataclass
class BaseEntity:
    """
    Base class for all OpenBI objects.
    """

    id: str = field(default_factory=lambda: str(uuid.uuid4()))

    created_at: datetime = field(default_factory=datetime.now)

    modified_at: datetime = field(default_factory=datetime.now)

    def touch(self):

        self.modified_at = datetime.now()