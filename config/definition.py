"""
Schema definition of the hierarchical config files and CLI arguments.
"""
from typing import List
from pydantic import validator
from pydantic.dataclasses import dataclass
from dataclasses import field
from .validate import validate

@dataclass
class Schema:
    addr: str = "0.0.0.0"
    @validator("addr")
    def check_addr(cls, addr: str) -> str:
        return validate.addr(cls,addr)
    port: int = 9000
    @validator("port")
    def check_port(cls, port: int) -> int:
        return validate.port(cls,port)
    nodes: List[str] = field(default_factory=lambda: ["http://localhost:8000"])
    @validator("nodes")
    def check_nodes(cls, nodes: List[str]) -> List[str]:
        return validate.nodes(cls,nodes)
    quorum_percent: int = 66
    @validator("quorum_percent")
    def check_quorum_percent(cls, quorum_percent: int) -> int:
        return validate.quorum_percent(cls,quorum_percent)
    config: str = "config.yaml"

cli_args = {
    'addr': {
        'args': ["-a", "--addr"],
        'type': str,
        'dest' : 'addr',
        'default' : '0.0.0.0',
        'help' : 'the ip address or domain of your synclink client api',
    },
    'port': {
        'args': ["-p", "--port"],
        'type': int,
        'dest' : 'port',
        'default' : 9000,
        'help' : 'the port of your synclink client api',
    },
    'nodes': {
        'args': ["-n", "--nodes", "--node"],
        'type': str,
        'action': 'append',
        'dest' : 'nodes',
        'default' : ["http://localhost:8000"],
        'help' : 'the http addresses of your synclink server nodes',
    },
    'quorum_percent': {
        'args': ["-q", "--quorum_percent", "--quorum"],
        'type': int,
        'dest' : 'quorum_percent',
        'default' : 66,
        'help' : 'the quorum in percent needed to accept a syncpoint',
    },
    'config': {
        'args': ["-c", "--config"],
        'type': str,
        'dest' : 'config',
        'default' : "config.yaml",
        'help' : 'path to an optional config YAML file',
    },
}