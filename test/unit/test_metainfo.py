import unittest
from common import read_file_bytes
from bittorrent import metainfo


class TestMetaInfo(unittest.TestCase):

    def test_dottorrent_from_bytes(self):
        data = read_file_bytes("test/files/test1.torrent")
        t1 = metainfo.DotTorrent.from_bytes(data)
        assert t1.info
        assert t1.info.name
        assert t1.info.pieces

        # Convert to bytes and back
        t2 = metainfo.DotTorrent.from_bytes(t1.to_bytes())

        assert t1.announce == t2.announce
        assert t1.info.name == t2.info.name
        assert t1.info.piece_length == t2.info.piece_length
        assert t1.info.pieces == t2.info.pieces
        assert t1.info.length == t2.info.length
