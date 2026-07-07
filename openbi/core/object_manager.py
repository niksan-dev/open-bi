from abc import ABC
from typing import Dict, Generic, TypeVar

T = TypeVar("T")


class ObjectManager(ABC, Generic[T]):
    """
    Generic manager for OpenBI semantic objects.
    """

    def __init__(self):

        self._items: Dict[str, T] = {}

    # -----------------------------------------

    def add(self, item: T):

        self._items[item.name] = item

    # -----------------------------------------

    def remove(self, name: str):

        self._items.pop(name, None)

    # -----------------------------------------

    def get(self, name: str):

        return self._items.get(name)

    # -----------------------------------------

    def exists(self, name: str):

        return name in self._items

    # -----------------------------------------

    def clear(self):

        self._items.clear()

    # -----------------------------------------

    @property
    def count(self):

        return len(self._items)

    # -----------------------------------------

    def values(self):

        return self._items.values()

    # -----------------------------------------

    def items(self):

        return self._items.items()

    # -----------------------------------------

    def keys(self):

        return self._items.keys()

    # -----------------------------------------

    def to_list(self):

        return list(self._items.values())

    # -----------------------------------------

    def __iter__(self):

        return iter(self._items.values())

    # -----------------------------------------

    def __len__(self):

        return len(self._items)