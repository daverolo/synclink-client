# coding: utf-8

from __future__ import annotations
from datetime import date, datetime  # noqa: F401

import re  # noqa: F401
from typing import Any, Dict, List, Optional  # noqa: F401

from pydantic import AnyUrl, BaseModel, EmailStr, Field, validator  # noqa: F401
from models.get_state_finality_checkpoints_response_data_previous_justified import GetStateFinalityCheckpointsResponseDataPreviousJustified


class AttestationData(BaseModel):
    """NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).

    Do not edit the class manually.

    AttestationData - a model defined in OpenAPI

        slot: The slot of this AttestationData [Optional].
        index: The index of this AttestationData [Optional].
        beacon_block_root: The beacon_block_root of this AttestationData [Optional].
        source: The source of this AttestationData [Optional].
        target: The target of this AttestationData [Optional].
    """

    slot: Optional[str] = Field(alias="slot", default=None)
    index: Optional[str] = Field(alias="index", default=None)
    beacon_block_root: Optional[str] = Field(alias="beacon_block_root", default=None)
    source: Optional[GetStateFinalityCheckpointsResponseDataPreviousJustified] = Field(alias="source", default=None)
    target: Optional[GetStateFinalityCheckpointsResponseDataPreviousJustified] = Field(alias="target", default=None)

AttestationData.update_forward_refs()
