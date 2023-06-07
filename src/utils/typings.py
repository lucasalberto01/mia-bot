from dataclasses import dataclass


@dataclass
class IUser:
    user_id: int
    user_nome: str
    user_username: str


@dataclass
class IServer:
    serve_id: int
    serve_nome: str
