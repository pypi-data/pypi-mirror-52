import bisect
from typing import List


class UtempidGenerator(object):
    """
    Unique temporary id generator class:
    Can be used to create small temporary id's and track the amount of current tempids in use
    Always returns the smallest currently available id starting from 0
    """
    def __init__(self) -> None:
        super(UtempidGenerator, self).__init__()
        self.max_id: int = 0
        self.idle_ids: List[int] = []

    def get_id(self) -> int:
        if len(self.idle_ids) == 0:
            _id, self.max_id = self.max_id, self.max_id + 1
        else:
            _id = self.idle_ids.pop(0)
        return _id

    def return_id(self, _id: int) -> None:
        if _id < 0:
            raise ValueError("Returned id must be positive")
        if _id in self.idle_ids or _id >= self.max_id:
            raise ValueError("Returned id is not currently in use")
        bisect.insort(self.idle_ids, _id)
        while len(self.idle_ids) > 0 and self.idle_ids[-1] == self.max_id - 1:
            self.max_id = self.idle_ids.pop()

    @property
    def active_count(self) -> int:
        return self.max_id - len(self.idle_ids)

    def __repr__(self) -> str:
        return "UtempidGenerator(idle_ids: {}, max_id: {})".format(
            self.idle_ids, self.max_id)

    def __str__(self) -> str:
        return repr(self)