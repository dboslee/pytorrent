import pydantic
import ipaddress


class Peer(pydantic.BaseModel):

    ip: ipaddress.IPv4Address
    port: int
    peer_id: str = None

    @pydantic.validator("ip", pre=True)
    def convert_ip(cls, value):
        if isinstance(value, bytes):
            value = value.decode()

        return value

    def to_dict(self):
        data = super().to_dict()
        data["ip"] = str(self.ip)
        return data
