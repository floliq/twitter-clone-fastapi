from pydantic import BaseModel


class Response(BaseModel):
    result: bool


class ResponseError(Response):
    error_type: str
    error_message: str
