import pydantic
from typing import List
from .base import BaseModel
from .peer import Peer


class TrackerAnnounce(BaseModel):

    interval: int = None
    peers: List[Peer] = None
    failure_reason: str = None

    @pydantic.root_validator
    def mutually_exclusive_attrs(cls, values):
        failure_reason = values.get("failure_reason")
        if failure_reason is None:
            assert values.get("interval") is not None,\
                "Missing required value interval"
            assert values.get("peers") is not None,\
                "Missing required value peers"

        return values

    @pydantic.validator("peers", pre=True)
    def decode_peers(cls, value):
        if isinstance(value, bytes):
            value = cls._peers_frombytes(value)

        return value

    @classmethod
    def _peers_frombytes(self, p: bytes) -> List[Peer]:
        peers = []
        for chunk in range(0, len(p), 6):
            ip_bytes = p[chunk:chunk+4]
            port_bytes = p[chunk+4:chunk+6]
            ip = ".".join([str(octet) for octet in ip_bytes])
            port = int(port_bytes.hex(), 16)

            peer = Peer(ip=ip, port=port)
            peers.append(peer)

        return peers
