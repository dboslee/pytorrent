import unittest
import os
from bittorrent import bencoding

curr_dir = os.path.abspath(os.path.dirname(__file__))


class TestBencoding(unittest.TestCase):

    def setUp(self):
        self.codec = bencoding.BencodeCodec()

    def test_encode_string(self):
        data = "test"
        encoded_data = b"4:test"
        result = self.codec.encode_str(data)
        assert result == encoded_data

        result = self.codec.encode("test")
        assert result == encoded_data

    def test_decode_string(self):
        data = b"4:test"
        decoded_data = "test"

        result, offset = self.codec.decode_str(data)
        assert result == decoded_data
        assert offset == len(data)

        result = self.codec.decode(data)
        assert result == decoded_data

    def test_encode_integer(self):
        data = 123
        encoded_data = b"i123e"

        result = self.codec.encode_int(data)
        assert result == encoded_data

        result = self.codec.encode(data)
        assert result == encoded_data

    def test_decode_integer(self):
        data = b"i123e"
        decoded_data = 123

        result, offset = self.codec.decode_int(data)
        assert result == decoded_data
        assert offset == len(data)

        result = self.codec.decode(data)
        assert result == decoded_data

    def test_encode_list(self):
        data = [1, 2, "3"]
        encoded_data = b"li1ei2e1:3e"

        result = self.codec.encode_list(data)
        assert result == encoded_data

        result = self.codec.encode(data)
        assert result == encoded_data

    def test_decode_list(self):
        data = b"li1ei2e1:3e"
        decoded_data = [1, 2, "3"]

        result, offset = self.codec.decode_list(data)
        assert result == decoded_data
        assert offset == len(data)

        result = self.codec.decode(data)
        assert result == decoded_data

    def test_encode_dict(self):
        data = {"key": 1}
        encoded_data = b"d3:keyi1ee"

        result = self.codec.encode_dict(data)
        assert result == encoded_data

        result = self.codec.encode(data)
        assert result == encoded_data

    def test_decode_dict(self):
        data = b"d3:keyi1ee"
        decoded_data = {"key": 1}

        result, offset = self.codec.decode_dict(data)
        assert result == decoded_data
        assert offset == len(data)

        result = self.codec.decode(data)
        assert result == decoded_data

    def test_decode_file(self):
        data = b""
        with open(f"{curr_dir}/test1.torrent", "rb") as f:
            byte = f.read(1)
            while byte:
                data += byte
                byte = f.read(1)

        result = self.codec.decode(data)
        assert result is not None
