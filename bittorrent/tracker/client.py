import requests
import random
import string
from bittorrent import models


class Client:

    def __init__(self, announce: str):
        self.announce = announce
        self.peer_id = self._peer_id()

    def _peer_id(self):
        return "pybt" + ''.join(
            random.choices(string.ascii_letters + string.digits, k=16)
        )

    def get(
        self,
        info_hash: bytes,
        ip: str = None,
        port: int = 6881,
        uploaded: int = 0,
        downloaded: int = 0,
        left: int = 0,
        event: str = None,
        compact: bool = True
    ) -> models.TrackerAnnounce:
        response = requests.get(self.announce, params={
            "info_hash": info_hash,
            "peer_id": self.peer_id,
            "ip": ip,
            "port": port,
            "uploaded": uploaded,
            "downloaded": downloaded,
            "left": left,
            "event": event,
            "compact": 1 if compact else None
        })
        response.raise_for_status()
        return models.TrackerAnnounce.from_bytes(response.content)
