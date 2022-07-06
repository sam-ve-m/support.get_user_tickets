# Third party
from pydantic import BaseModel, validator


class TicketFilters(BaseModel):
    page: str = 0
    page_size: str = 15

    @validator('*')
    def is_numeric(cls, params):
        if params.isnumeric():
            params = int(params)
            return params
        raise ValueError('Invalid type')
