# Standards

# Third part
from pydantic import BaseModel, StrictInt


class Filter(BaseModel):
    page: StrictInt = 0
    page_size: StrictInt = 15
