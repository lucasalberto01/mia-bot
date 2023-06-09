from dataclasses import dataclass


@dataclass
class IUser:
    user_id: int
    user_nome: str
    user_username: str


@dataclass
class IChannel:
    """
    Chat: Container in chat typing message
    Server: Set of Chat
    """
    chat_id: int | None
    chat_name: str | None
    serve_id: int
    serve_nome: str
    is_private: bool = False
