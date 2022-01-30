# Standards

# Third part
from pydantic import BaseModel


class Filter(BaseModel):
    page: int = 2
    page_size: int = 1
