"""
Validator class for specific config types.
FIXME: for whetever reason validators fail on macOS with errors like:
AttributeError: module 'validators' has no attribute 'ip_address'
"""
from typing import List
import validators

class validate:

    @staticmethod
    def addr(cls, addr: str) -> str:
        # if addr != "localhost" and not validators.domain(addr) and not validators.ip_address.ipv4(addr) and not validators.ip_address.ipv6(addr):
        #     raise ValueError(f"'addr' must be a valid domain or IP, got: {addr}")
        return addr

    @staticmethod
    def port(cls, port: int) -> int:
        if port < 1024:
            raise ValueError(f"'port' must be non-privileged, got: {port}")
        return port

    @staticmethod
    def nodes(cls, nodes: List[str]) -> List[str]:
        # for i in nodes:
        #     if not validators.url(i):
        #         raise ValueError(f"'nodes' address must be a valid url, got: {i}")
        return nodes

    @staticmethod
    def quorum_percent(cls, quorum_percent: int) -> int:
        if quorum_percent < 0:
            raise ValueError(f"'quorum_percent' must not lower 0, got: {quorum_percent}")
        if quorum_percent > 100:
            raise ValueError(f"'quorum_percent' must not higher 100, got: {quorum_percent}")
        return quorum_percent