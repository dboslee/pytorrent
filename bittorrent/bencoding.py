from typing import (
    Dict,
    List,
    Union
)


class BencodeCodec:

    def __init__(self):
        self.encode_func = {
            dict: self.encode_dict,
            list: self.encode_list,
            int: self.encode_int,
            str: self.encode_str,
        }
        self.decode_func = {
            b"d": self.decode_dict,
            b"l": self.decode_list,
            b"i": self.decode_int,
            b"0": self.decode_str,
            b"1": self.decode_str,
            b"2": self.decode_str,
            b"3": self.decode_str,
            b"4": self.decode_str,
            b"5": self.decode_str,
            b"6": self.decode_str,
            b"7": self.decode_str,
            b"8": self.decode_str,
            b"9": self.decode_str,
        }

    def encode(self, data: Union[Dict, List, int, str]) -> bytes:
        """Encode data to bencoding byte format."""
        encode_func = self.encode_func.get(type(data))
        if not encode_func:
            raise ValueError(f"Unable to encode unsupported type {type(data)}")

        return encode_func(data)

    def decode(self, data: bytes):
        """Decode data fro bencoding byte format."""
        decoded_data, offset = self._decode(data)
        if offset != len(data):
            raise Exception
        return decoded_data

    def _decode(self, data: bytes, offset: int = 0) -> Union[Dict, List, str]:
        """Checks the offset and uses the correct decode function."""
        decode_type = data[offset:offset+1]
        decode_func = self.decode_func.get(decode_type)
        if not decode_func:
            raise Exception(f"Invalid bencoding at offset {offset}")

        decoded_data, offset = decode_func(data, offset)
        return decoded_data, offset

    def encode_str(self, data: str) -> bytes:
        """Encode a string."""
        return f"{len(data)}:{data}".encode()

    def encode_int(self, value: int) -> bytes:
        """Encode an integer."""
        return f"i{value}e".encode()

    def encode_dict(self, data: Dict) -> bytes:
        """Encode a dictionary."""
        encoding = b"d"
        for key, value in sorted(data.items()):
            if not isinstance(key, str):
                raise ValueError("All keys must be of type str")
            encoding += self.encode_str(key) + self.encode(value)

        return encoding + b"e"

    def encode_list(self, data: List) -> bytes:
        """Encode a list."""
        encoding = b"l"
        for value in data:
            encoding += self.encode(value)
        return encoding + b"e"

    def decode_str(self, data: bytes, offset: int = 0) -> str:
        """Decode a string from a given offset."""
        colon_index = data.index(b":", offset)
        length = int(data[offset:colon_index])
        start_index = colon_index + 1
        str_value = data[start_index:start_index + length].decode()

        return str_value, start_index + length

    def decode_int(self, data: bytes, offset: int = 0) -> int:
        end_index = data.index(b"e", offset)
        decoded_int = int(data[offset + 1:end_index])

        return decoded_int, end_index + 1

    def decode_dict(self, data: bytes, offset: int = 0) -> Dict:
        offset += 1
        decoded_dict = {}
        while data[offset:offset+1] != b"e":
            key, offset = self._decode(data, offset)
            if not isinstance(key, str):
                raise Exception

            value, offset = self._decode(data, offset)
            decoded_dict[key] = value

        return decoded_dict, offset + 1

    def decode_list(self, data: bytes, offset: int = 0) -> List:
        offset += 1
        decoded_list = []
        while data[offset:offset+1] != b"e":
            value, offset = self._decode(data, offset)
            decoded_list.append(value)

        return decoded_list, offset + 1
