def read_file_bytes(filename: str) -> bytes:
    data = b""
    with open(filename, "rb") as f:
        byte = f.read(1)
        while byte:
            data += byte
            byte = f.read(1)

    return data
