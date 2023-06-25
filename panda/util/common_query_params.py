from typing import Union

from fastapi import Depends
from typing_extensions import Annotated


class CommonQueryParams:
    def __init__(self, query: Union[str, None] = None, offset: int = 0, limit: int = 100):
        self.query = query
        self.offset = offset
        self.limit = limit


CommonQuery = Annotated[CommonQueryParams, Depends()]
