from distutils import core
from typing import Union
from loguru import logger

import core.synclink
from fastapi import APIRouter, Header, Query, Response, Request
from fastapi.responses import JSONResponse, StreamingResponse
from models.get_block_root_response import GetBlockRootResponse
from models.get_block_v2_response import GetBlockV2Response
from models.get_deposit_contract_response import GetDepositContractResponse
from models.get_fork_schedule_response import GetForkScheduleResponse
from models.get_genesis_response import GetGenesisResponse
from models.get_peer_count_response import GetPeerCountResponse
from models.get_peers_response import GetPeersResponse
from models.get_spec_response import GetSpecResponse
from models.get_state_finality_checkpoints_response import \
    GetStateFinalityCheckpointsResponse
from models.get_state_v2_response import GetStateV2Response
from models.get_syncing_status_response import GetSyncingStatusResponse
from models.get_version_response import GetVersionResponse
from services.eth2api import ETH2API
from validators.content_type import (ContentTypeJSON, ContentTypeSSZ,
                                     validate_content_type)
from validators.node_health import validate_node_health
from validators.response import validate_response

eth_router = APIRouter()

synclink_client = core.synclink.client


@eth_router.get("/v1/beacon/genesis", tags=["Beacon"], response_model=GetGenesisResponse)
async def handle_eth_v1_beacon_genesis(request: Request, content_type: str = Header(default=ContentTypeJSON)):
    validate_content_type(content_type, [ContentTypeJSON])
    validate_node_health(synclink_client.selected_ready_finalized_node)

    r = await synclink_client.selected_ready_finalized_node.api.beacon.genesis()
    validate_response(r,request,synclink_client.selected_ready_finalized_node)

    return r


@eth_router.get("/v1/beacon/blocks/{block_id}/root", tags=["Beacon"], response_model=GetBlockRootResponse)
async def handle_eth_v1_beacon_blocks_root(block_id, request: Request, content_type: str = Header(default=ContentTypeJSON)):
    validate_content_type(content_type, [ContentTypeJSON])
    validate_node_health(synclink_client.selected_ready_finalized_node)

    r = await synclink_client.selected_ready_finalized_node.api.beacon.block_root(block_id)
    validate_response(r,request,synclink_client.selected_ready_finalized_node)

    return r


@eth_router.get("/v1/beacon/states/{state_id}/finality_checkpoints", tags=["Beacon"], response_model=GetStateFinalityCheckpointsResponse)
async def handle_eth_v1_beacon_blocks_root(state_id, request: Request, content_type: str = Header(default=ContentTypeJSON)):
    validate_content_type(content_type, [ContentTypeJSON])
    validate_node_health(synclink_client.selected_ready_finalized_node)

    r = await synclink_client.selected_ready_finalized_node.api.beacon.state_finality_checkpoints(state_id)
    validate_response(r,request,synclink_client.selected_ready_finalized_node)

    return r


@eth_router.get("/v2/beacon/blocks/{block_id}", tags=["Beacon"], response_model=GetBlockV2Response)
async def handle_eth_v2_beacon_block(block_id, request: Request, accept: str = Header(default=ContentTypeJSON)):
    validate_node_health(synclink_client.selected_ready_finalized_node)

    api = synclink_client.selected_ready_finalized_node.api

    if (ContentTypeSSZ in accept):
        return StreamingResponse(api.beacon.block_ssz(block_id=block_id), headers={"Content-Type": "application/octet-stream"})

    r = await api.beacon.block(block_id)
    validate_response(r,request,synclink_client.selected_ready_finalized_node)

    return r


@eth_router.get("/v1/config/spec", tags=["Config"], response_model=GetSpecResponse)
async def handle_eth_v1_config_spec(content_type: str = Header(default=ContentTypeJSON)):
    validate_content_type(content_type, [ContentTypeJSON])
    validate_node_health(synclink_client.selected_ready_finalized_node)

    spec = synclink_client.selected_ready_finalized_node.config.spec

    return GetSpecResponse(data=spec)


@eth_router.get("/v1/config/deposit_contract", tags=["Config"], response_model=GetDepositContractResponse)
async def handle_eth_v1_config_deposit_contract(content_type: str = Header(default=ContentTypeJSON)):
    validate_content_type(content_type, [ContentTypeJSON])
    validate_node_health(synclink_client.selected_ready_finalized_node)

    deposit_contract = synclink_client.selected_ready_finalized_node.config.deposit_contract

    return GetDepositContractResponse(data=deposit_contract)


@eth_router.get("/v1/config/fork_schedule", tags=["Config"], response_model=GetForkScheduleResponse)
async def handle_eth_v1_config_fork_schedule(content_type: str = Header(default=ContentTypeJSON)):
    validate_content_type(content_type, [ContentTypeJSON])
    validate_node_health(synclink_client.selected_ready_finalized_node)

    fork_epochs = synclink_client.selected_ready_finalized_node.config.fork_epochs

    return GetForkScheduleResponse(data=fork_epochs)


@eth_router.get("/v1/node/health", tags=["Node"], responses={
    200: {"description": "Node is ready", "content": None},
    206: {"description": "Node is syncing but can serve incomplete data", "content": None},
    400: {"description": "Invalid syncing status code", "content": None},
    503: {"description": "Node not initialized, having issues or no quorum yet", "content": None }
})
async def handle_eth_v1_node_health(request: Request):
    if not synclink_client.selected_ready_finalized_node:
        return Response(status_code=503)
    
    r = await synclink_client.selected_ready_finalized_node.api.node.health()
    if not r:
        logger.warning(f"Response from request {synclink_client.selected_ready_finalized_node.url + request.scope['path']} was '{r}'")
        return Response(status_code=503)

    return Response(status_code=r.status_code)


@eth_router.get("/v1/node/syncing", tags=["Node"], response_model=GetSyncingStatusResponse)
async def handle_eth_v1_node_syncing(request: Request, content_type: str = Header(default=ContentTypeJSON)):
    validate_content_type(content_type, [ContentTypeJSON])
    validate_node_health(synclink_client.selected_ready_finalized_node)

    r = await synclink_client.selected_ready_finalized_node.api.node.syncing()
    validate_response(r,request,synclink_client.selected_ready_finalized_node)

    return r

@eth_router.get("/v1/node/version", tags=["Node"], response_model=GetVersionResponse)
async def handle_eth_v1_node_version(request: Request, content_type: str = Header(default=ContentTypeJSON)):
    validate_content_type(content_type, [ContentTypeJSON])
    validate_node_health(synclink_client.selected_ready_finalized_node)

    r = await synclink_client.selected_ready_finalized_node.api.node.version()
    validate_response(r,request,synclink_client.selected_ready_finalized_node)

    return r


@eth_router.get("/v1/node/peers", tags=["Node"], response_model=GetPeersResponse)
async def handle_eth_v1_node_peers(request: Request, content_type: str = Header(default=ContentTypeJSON)):
    validate_content_type(content_type, [ContentTypeJSON])
    validate_node_health(synclink_client.selected_ready_finalized_node)

    r = await synclink_client.selected_ready_finalized_node.api.node.peers()
    validate_response(r,request,synclink_client.selected_ready_finalized_node)

    return r


@eth_router.get("/v1/node/peer_count", tags=["Node"], response_model=GetPeerCountResponse)
async def handle_eth_v1_node_peer_count(request: Request, content_type: str = Header(default=ContentTypeJSON)):
    validate_content_type(content_type, [ContentTypeJSON])
    validate_node_health(synclink_client.selected_ready_finalized_node)

    r = await synclink_client.selected_ready_finalized_node.api.node.peer_count()
    validate_response(r,request,synclink_client.selected_ready_finalized_node)

    return r


@eth_router.get("/v2/debug/beacon/states/{state_id}", tags=["Debug"], response_model=GetStateV2Response)
async def handle_eth_v2_debug_beacon_state(state_id, accept: str = Header(default=ContentTypeSSZ)):
    validate_node_health(synclink_client.selected_ready_finalized_node)

    if (ContentTypeSSZ in accept):
        return StreamingResponse(synclink_client.selected_ready_finalized_node.api.debug.bacon_state(state_id=state_id), headers={"Content-Type": "application/octet-stream"})
    
    #return StreamingResponse(synclink_client.selected_ready_finalized_node.api.debug.bacon_state(state_id=state_id), headers={"Content-Type": "application/json"})
    return Response(status_code=415) # if we dont support json in the client then respond a proper error header instead