from hashlib import sha256


def hashed(s: str):
    return sha256(s.encode('UTF-8')).digest()
