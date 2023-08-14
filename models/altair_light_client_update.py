# coding: utf-8

from __future__ import annotations
from datetime import date, datetime  # noqa: F401

import re  # noqa: F401
from typing import Any, Dict, List, Optional  # noqa: F401

from pydantic import AnyUrl, BaseModel, EmailStr, Field, validator  # noqa: F401
from models.get_light_client_bootstrap_response_data_one_of_current_sync_committee import GetLightClientBootstrapResponseDataOneOfCurrentSyncCommittee
from models.get_light_client_bootstrap_response_data_one_of_header import GetLightClientBootstrapResponseDataOneOfHeader
from models.publish_blinded_block_request_one_of1_message_all_of_body_sync_aggregate import PublishBlindedBlockRequestOneOf1MessageAllOfBodySyncAggregate


class AltairLightClientUpdate(BaseModel):
    """NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).

    Do not edit the class manually.

    AltairLightClientUpdate - a model defined in OpenAPI

        attested_header: The attested_header of this AltairLightClientUpdate [Optional].
        next_sync_committee: The next_sync_committee of this AltairLightClientUpdate [Optional].
        next_sync_committee_branch: The next_sync_committee_branch of this AltairLightClientUpdate [Optional].
        finalized_header: The finalized_header of this AltairLightClientUpdate [Optional].
        finality_branch: The finality_branch of this AltairLightClientUpdate [Optional].
        sync_aggregate: The sync_aggregate of this AltairLightClientUpdate [Optional].
        signature_slot: The signature_slot of this AltairLightClientUpdate [Optional].
    """

    attested_header: Optional[GetLightClientBootstrapResponseDataOneOfHeader] = Field(alias="attested_header", default=None)
    next_sync_committee: Optional[GetLightClientBootstrapResponseDataOneOfCurrentSyncCommittee] = Field(alias="next_sync_committee", default=None)
    next_sync_committee_branch: Optional[List[str]] = Field(alias="next_sync_committee_branch", default=None)
    finalized_header: Optional[GetLightClientBootstrapResponseDataOneOfHeader] = Field(alias="finalized_header", default=None)
    finality_branch: Optional[List[str]] = Field(alias="finality_branch", default=None)
    sync_aggregate: Optional[PublishBlindedBlockRequestOneOf1MessageAllOfBodySyncAggregate] = Field(alias="sync_aggregate", default=None)
    signature_slot: Optional[str] = Field(alias="signature_slot", default=None)

AltairLightClientUpdate.update_forward_refs()
