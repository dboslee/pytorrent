import pydantic
from bittorrent.bencode import bencode


class BaseModel(pydantic.BaseModel):

    @classmethod
    def from_bytes(cls, data):
        return load_model_from_bytes(data, cls)

    def to_dict(self) -> dict:
        return self.dict(by_alias=True, exclude_none=True)

    def to_bytes(self) -> bytes:
        data = self.to_dict()
        return bencode.encode(data)


def load_model_from_bytes(data: bytes, model: pydantic.BaseModel):
    decoded_data = bencode.decode(data)
    return model(**decoded_data)
