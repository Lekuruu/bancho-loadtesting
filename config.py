
from dataclasses import dataclass, field

import json
import os

@dataclass
class TcpSettings:
    Ip: str = "127.0.0.1"
    Port: int = 13381

@dataclass
class HttpSettings:
    Domain: str | None = None

@dataclass
class WebSocketSettings:
    Url: str | None = None
    Path: str = "/"
    Secure: bool = True
    Headers: dict[str, str] = field(default_factory=dict)
    OpenTimeout: float | None = 10
    PingInterval: float | None = 20
    PingTimeout: float | None = 20
    CloseTimeout: float | None = 10

@dataclass
class ConnectorSettings:
    Type: str
    Http: HttpSettings = field(default_factory=HttpSettings)
    Tcp: TcpSettings = field(default_factory=TcpSettings)
    WebSocket: WebSocketSettings = field(default_factory=WebSocketSettings)

@dataclass
class Connection:
    Domain: str
    Workers: int
    Version: int
    ExecutableHash: str
    Connector: ConnectorSettings

@dataclass
class Flags:
    EnableMessages: bool
    EnableStatusUpdates: bool
    EnableSpectating: bool
    EnableLeaderboardRequests: bool

@dataclass
class User:
    Username: str
    Password: str
    Messages: list
    SpectatorTargetId: int
    MessageTargetChannel: str

@dataclass
class Leaderboard:
    BeatmapFilename: str
    BeatmapHash: str
    BeatmapsetId: int
    RequestIntervalMs: int

@dataclass
class Config:
    Connection: Connection
    Flags: Flags
    Users: list[User]
    Leaderboard: Leaderboard

def load(path: str = "config.json") -> Config:
    if not os.path.exists(path):
        raise FileNotFoundError(f"Configuration file not found: '{path}'")

    with open(path, "r") as f:
        data = json.load(f)

    connection_data = data["Connection"]
    connector_data = connection_data["Connector"]
    connector_type = connector_data["Type"].lower()

    # support both "ws" and "websocket"
    connector_type = "websocket" if connector_type == "ws" else connector_type

    if connector_type not in {"http", "tcp", "websocket"}:
        raise ValueError(
            f"Unsupported connector type: '{connector_type}'. "
            "Expected one of: http, tcp, websocket"
        )

    connector = ConnectorSettings(
        Type=connector_type,
        Http=HttpSettings(**connector_data.get("Http", {})),
        Tcp=TcpSettings(**connector_data.get("Tcp", {})),
        WebSocket=WebSocketSettings(**connector_data.get("WebSocket", {})),
    )
    connection_data = {
        **connection_data,
        "Connector": connector,
    }

    return Config(
        Connection=Connection(**connection_data), # type: ignore
        Flags=Flags(**data["Flags"]),
        Users=[User(**user) for user in data["Users"]],
        Leaderboard=Leaderboard(**data["Leaderboard"]),
    )
