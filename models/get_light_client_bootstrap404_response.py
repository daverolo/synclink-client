# coding: utf-8

from __future__ import annotations
from datetime import date, datetime  # noqa: F401

import re  # noqa: F401
from typing import Any, Dict, List, Optional  # noqa: F401

from pydantic import AnyUrl, BaseModel, EmailStr, Field, validator  # noqa: F401


class GetLightClientBootstrap404Response(BaseModel):
    """NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).

    Do not edit the class manually.

    GetLightClientBootstrap404Response - a model defined in OpenAPI

        code: The code of this GetLightClientBootstrap404Response [Optional].
        message: The message of this GetLightClientBootstrap404Response [Optional].
        stacktraces: The stacktraces of this GetLightClientBootstrap404Response [Optional].
    """

    code: Optional[float] = Field(alias="code", default=None)
    message: Optional[str] = Field(alias="message", default=None)
    stacktraces: Optional[List[str]] = Field(alias="stacktraces", default=None)

GetLightClientBootstrap404Response.update_forward_refs()
