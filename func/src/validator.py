from pydantic import BaseModel, validator


class Filter(BaseModel):
    page: str = 0
    page_size: str = 15

    @validator('*')
    def is_numeric(params):
        if params.isnumeric():
            params = int(params)
            return params
        raise ValueError('Invalid type')


