from itertools import islice
from typing import Iterable, List


def batched(iterable: Iterable, batch_size: int) -> Iterable[List]:
    iterator = iter(iterable)
    while batch := list(islice(iterator, batch_size)):
        yield batch
