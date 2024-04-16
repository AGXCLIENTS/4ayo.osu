from __future__ import annotations

from typing import Any
from typing import cast
from typing import Generic
from typing import Literal
from typing import TypeVar

from pydantic import BaseModel

from app.api.v2.common import json


T = TypeVar("T")


class Success(BaseModel, Generic[T]):
    status: Literal["success"]
    data: T
    meta: dict[str, Any]


def success(
    content: T,
    status_code: int = 200,
    headers: dict[str, Any] | None = None,
    meta: dict[str, Any] | None = None,
) -> Success[T]:
    if meta is None:
        meta = {}
    data = {"status": "success", "data": content, "meta": meta}
    # XXX:HACK to make typing work
    return cast(Success[T], json.ORJSONResponse(data, status_code, headers))


class Failure(BaseModel):
    status: Literal["error"]
    error: str


def failure(
    # TODO: error code
    message: str,
    status_code: int = 400,
    headers: dict[str, Any] | None = None,
) -> Failure:
    data = {"status": "error", "error": message}
    # XXX:HACK to make typing work
    return cast(Failure, json.ORJSONResponse(data, status_code, headers))
