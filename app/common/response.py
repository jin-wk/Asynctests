from typing import Any, Optional
from pydantic import BaseModel
from starlette.responses import JSONResponse
from fastapi.encoders import jsonable_encoder


class Response(BaseModel):
    detail: str
    data: Optional[Any]


class CustomResponse:
    def __call__(
        self, status_code: int = 200, detail: str = "Ok", data: Optional[Any] = None
    ) -> JSONResponse:
        if data is not None:
            data = jsonable_encoder(data)
        return JSONResponse(
            status_code=status_code,
            content=dict(detail=detail, data=data),
        )


response = CustomResponse()
