from typing import Union

from fastapi import Depends
from typing_extensions import Annotated


class CommonQueryParams:
    def __init__(self, q: Union[str, None] = None, offset: int = 0, limit: int = 100):
        self.q = q
        self.offset = offset
        self.limit = limit


CommonQuery = Annotated[CommonQueryParams, Depends()]
