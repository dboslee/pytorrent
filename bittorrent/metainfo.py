from typing import (
    List,
    Optional
)
from .bencode import bencode


class DotTorrentKeys:

    ANNOUNCE = "announce"
    INFO = "info"
    NAME = "name"
    LENGTH = "length"
    PIECE_LENGTH = "piece length"
    PIECES = "pieces"
    FILES = "files"
    PATH = "path"


class InvalidMetaInfo(Exception):
    pass


class FileInfo:

    __slots__ = [DotTorrentKeys.PATH, DotTorrentKeys.LENGTH]

    def __init__(
        self, length: int, path: List[str]
    ):
        self.length = length
        self.path = [
            p.decode()
            if isinstance(p, bytes) else p
            for p in path
        ]
        if not path:
            raise InvalidMetaInfo("path must not me empty.")

    def __repr__(self):
        return f"<FileInfo {self.path[-1]}>"

    @classmethod
    def from_dict(cls, data: dict) -> "TorrentInfo":
        """Load torrent info from dictionary."""
        data = decode_keys(data)
        return cls(
            data[DotTorrentKeys.LENGTH],
            data[DotTorrentKeys.PATH]
        )

    @classmethod
    def from_bytes(cls, data: bytes) -> "TorrentInfo":
        """Load torrent info from bytes."""
        return load_cls_from_bytes(cls, data)

    def to_dict(self) -> dict:
        """Dump torrent info to dictionary."""
        return {
            DotTorrentKeys.LENGTH: self.length,
            DotTorrentKeys.PATH: self.path,
        }

    def to_bytes(self) -> bytes:
        """Dump torrent info to bytes."""
        return bencode.encode(
            self.to_dict()
        )


class TorrentInfo:

    def __init__(
        self,
        piece_length: List[int],
        pieces: List[bytes],
        length: Optional[int] = None,
        files: Optional[List[FileInfo]] = None,
        name: Optional[str] = None,
    ):
        self.name = name.decode() if isinstance(name, bytes) else name
        self.piece_length = piece_length
        self.pieces = [
            pieces[chunk:chunk+20]
            for chunk in range(0, len(pieces), 20)
        ]
        self.length = length
        self.files = files

        if not ((self.files is not None) ^ (self.length is not None)):
            raise InvalidMetaInfo("files and length are mutually exclusive properties.")

    def __repr__(self):
        return f"<TorrentInfo {self.name}>"

    @classmethod
    def from_dict(cls, data: dict) -> "TorrentInfo":
        """Load torrent info from dictionary."""
        data = decode_keys(data)
        files = data.get(DotTorrentKeys.FILES)
        if files:
            files = [
                FileInfo.from_dict(file)
                for file in files
            ]
        return cls(
            piece_length=data[DotTorrentKeys.PIECE_LENGTH],
            pieces=data[DotTorrentKeys.PIECES],
            length=data.get(DotTorrentKeys.LENGTH),
            files=files,
            name=data.get(DotTorrentKeys.NAME),
        )

    @classmethod
    def from_bytes(cls, data: bytes) -> "TorrentInfo":
        """Load torrent info from bytes."""
        return load_cls_from_bytes(cls, data)

    def to_dict(self) -> dict:
        """Dump torrent info to dictionary."""
        files = None
        if self.files is not None:
            files = [
                file.to_dict()
                for file in self.files
            ]

        data = {
            DotTorrentKeys.NAME: self.name,
            DotTorrentKeys.PIECE_LENGTH: self.piece_length,
            DotTorrentKeys.PIECES: b"".join(self.pieces),
            DotTorrentKeys.LENGTH: self.length,
            DotTorrentKeys.FILES: files,
        }

        return remove_none(data)

    def to_bytes(self) -> bytes:
        """Dump torrent info to bytes."""
        return bencode.encode(
            self.to_dict()
        )


class DotTorrent:

    def __init__(
        self, info: TorrentInfo, announce: str,
    ):
        """Represents a .torrent file."""
        self.info = info
        self.announce = announce

        if isinstance(self.announce, bytes):
            self.announce = self.announce.decode()

    def __repr__(self):
        return f"<DotTorrent {self.info}>"

    @classmethod
    def from_dict(cls, data: dict) -> "DotTorrent":
        """Load .torrent file from dictionary."""
        data = decode_keys(data)
        announce = data.get(DotTorrentKeys.ANNOUNCE)

        info = TorrentInfo.from_dict(
            data[DotTorrentKeys.INFO]
        )
        return cls(info=info, announce=announce)

    @classmethod
    def from_bytes(cls, data: bytes) -> "DotTorrent":
        """ Load .torrent file from bytes."""
        return load_cls_from_bytes(cls, data)

    def to_dict(self) -> dict:
        data = {
            DotTorrentKeys.INFO: self.info.to_dict(),
            DotTorrentKeys.ANNOUNCE: self.announce,
        }
        return remove_none(data)

    def to_bytes(self) -> bytes:
        return bencode.encode(
            self.to_dict()
        )


def load_cls_from_bytes(cls, data: bytes):
    data_dict = bencode.decode(data)
    return cls.from_dict(data_dict)


def decode_keys(data: dict):
    return {
        (key.decode() if isinstance(key, bytes) else key): value
        for key, value in data.items()
    }


def remove_none(data: dict):
    return {
        key: value
        for key, value in data.items()
        if value is not None
    }
