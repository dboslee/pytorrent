import hashlib
import pydantic
from typing import (
    List,
    Optional
)

from .base import BaseModel


class TorrentFileInfo(BaseModel):

    length: int
    path: List[str]


class TorrentInfo(BaseModel):

    name: Optional[str]
    pieces: List[bytes]
    piece_length: int = pydantic.Field(alias="piece length")
    length: Optional[int]
    files: Optional[List[TorrentFileInfo]]

    @pydantic.root_validator
    def mutally_exclusive_attrs(cls, values):
        assert (values.get("length") is None) ^ (values.get("files") is None),\
            "Mutually exclusive attrs length and files"
        return values

    @pydantic.validator("pieces", pre=True)
    def decode_pieces(cls, value):
        if isinstance(value, bytes):
            return [
                value[chunk:chunk+20]
                for chunk in range(0, len(value), 20)
            ]

        return value

    def to_dict(self):
        data = super().to_dict()
        data["pieces"] = b"".join(data["pieces"])
        if data.get("files"):
            data["files"] = [file.to_dict() for file in data["files"]]

        return data


class MetaInfo(BaseModel):

    info: TorrentInfo
    announce: Optional[pydantic.HttpUrl]

    def info_hash(self):
        info_bytes = self.info.to_bytes()
        hash_object = hashlib.sha1(info_bytes)
        return bytes.fromhex(hash_object.hexdigest())

    def to_dict(self):
        data = super().to_dict()
        data["info"] = self.info.to_dict()
        if data.get("announce"):
            data["announce"] = data["announce"].encode()

        return data
