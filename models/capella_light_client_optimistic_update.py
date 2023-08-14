# coding: utf-8

from __future__ import annotations
from datetime import date, datetime  # noqa: F401

import re  # noqa: F401
from typing import Any, Dict, List, Optional  # noqa: F401

from pydantic import AnyUrl, BaseModel, EmailStr, Field, validator  # noqa: F401
from models.get_light_client_bootstrap_response_data_one_of1_header import GetLightClientBootstrapResponseDataOneOf1Header
from models.publish_blinded_block_request_one_of1_message_all_of_body_sync_aggregate import PublishBlindedBlockRequestOneOf1MessageAllOfBodySyncAggregate


class CapellaLightClientOptimisticUpdate(BaseModel):
    """NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).

    Do not edit the class manually.

    CapellaLightClientOptimisticUpdate - a model defined in OpenAPI

        attested_header: The attested_header of this CapellaLightClientOptimisticUpdate [Optional].
        sync_aggregate: The sync_aggregate of this CapellaLightClientOptimisticUpdate [Optional].
        signature_slot: The signature_slot of this CapellaLightClientOptimisticUpdate [Optional].
    """

    attested_header: Optional[GetLightClientBootstrapResponseDataOneOf1Header] = Field(alias="attested_header", default=None)
    sync_aggregate: Optional[PublishBlindedBlockRequestOneOf1MessageAllOfBodySyncAggregate] = Field(alias="sync_aggregate", default=None)
    signature_slot: Optional[str] = Field(alias="signature_slot", default=None)

CapellaLightClientOptimisticUpdate.update_forward_refs()
