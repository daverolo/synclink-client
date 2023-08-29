from fastapi import HTTPException, status
from core.node import Node


def validate_node_health(selected_ready_finalized_node: Node, detail=f"Node not initialized, having issues or no quorum yet"):
    if not selected_ready_finalized_node:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=detail)
