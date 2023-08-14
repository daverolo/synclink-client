# coding: utf-8

from __future__ import annotations
from datetime import date, datetime  # noqa: F401

import re  # noqa: F401
from typing import Any, Dict, List, Optional  # noqa: F401

from pydantic import AnyUrl, BaseModel, EmailStr, Field, validator  # noqa: F401


class GetForkChoiceResponseForkChoiceNodesInner(BaseModel):
    """NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).

    Do not edit the class manually.

    GetForkChoiceResponseForkChoiceNodesInner - a model defined in OpenAPI

        slot: The slot of this GetForkChoiceResponseForkChoiceNodesInner [Optional].
        block_root: The block_root of this GetForkChoiceResponseForkChoiceNodesInner [Optional].
        parent_root: The parent_root of this GetForkChoiceResponseForkChoiceNodesInner [Optional].
        justified_epoch: The justified_epoch of this GetForkChoiceResponseForkChoiceNodesInner [Optional].
        finalized_epoch: The finalized_epoch of this GetForkChoiceResponseForkChoiceNodesInner [Optional].
        weight: The weight of this GetForkChoiceResponseForkChoiceNodesInner [Optional].
        validity: The validity of this GetForkChoiceResponseForkChoiceNodesInner [Optional].
        execution_block_hash: The execution_block_hash of this GetForkChoiceResponseForkChoiceNodesInner [Optional].
        extra_data: The extra_data of this GetForkChoiceResponseForkChoiceNodesInner [Optional].
    """

    slot: Optional[str] = Field(alias="slot", default=None)
    block_root: Optional[str] = Field(alias="block_root", default=None)
    parent_root: Optional[str] = Field(alias="parent_root", default=None)
    justified_epoch: Optional[str] = Field(alias="justified_epoch", default=None)
    finalized_epoch: Optional[str] = Field(alias="finalized_epoch", default=None)
    weight: Optional[str] = Field(alias="weight", default=None)
    validity: Optional[str] = Field(alias="validity", default=None)
    execution_block_hash: Optional[str] = Field(alias="execution_block_hash", default=None)
    extra_data: Optional[Dict[str, Any]] = Field(alias="extra_data", default=None)

GetForkChoiceResponseForkChoiceNodesInner.update_forward_refs()
