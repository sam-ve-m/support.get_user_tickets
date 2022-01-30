# Standards

# Third part
from pydantic import BaseModel


class Filter(BaseModel):
    page: int = 0
    page_size: int = 15
