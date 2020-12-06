import unittest
from common import read_file_bytes
from bittorrent.models import MetaInfo

TEST_FILE = "test/files/ubuntu-20.10-desktop-amd64.iso.torrent"


class TestMetaInfo(unittest.TestCase):

    def test_dottorrent_from_bytes(self):
        data = read_file_bytes(TEST_FILE)
        t1 = MetaInfo.from_bytes(data)
        assert t1.info
        assert t1.info.name
        assert t1.info.pieces

        # Convert to bytes and back
        t2 = MetaInfo.from_bytes(t1.to_bytes())

        assert t1.announce == t2.announce
        assert t1.info.name == t2.info.name
        assert t1.info.piece_length == t2.info.piece_length
        assert t1.info.pieces == t2.info.pieces
        assert t1.info.length == t2.info.length

    def test_info_hash(self):
        data = read_file_bytes(TEST_FILE)
        torrent_file = MetaInfo.from_bytes(data)
        info_hash = torrent_file.info_hash()
        assert info_hash.hex() == "5fff0e1c8ac414860310bcc1cb76ac28e960efbe"
