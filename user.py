from typing import Literal, Tuple


class User:
    def __init__(self, id: int, name: str, pwd: bytes) -> None:
        self.id = id
        self.name = name
        self.pwd = pwd

    @property
    def is_authenticated(self) -> bool:
        return not self.is_anonymous

    @property
    def is_active(self) -> Literal[True]:
        return True

    @property
    def is_anonymous(self) -> bool:
        return self.name == 'anonymous'

    def get_id(self) -> str:
        return str(self.id)

    @classmethod
    def from_db(cls, fetched: Tuple[int, str, bytes]):
        return cls(*fetched)
