
from config import Config, User
from osu import (
    WebsocketBanchoConnector,
    HttpBanchoConnector,
    TcpBanchoConnector,
    BanchoConnector,
    Game,
)
import actions

def create_collection(config: Config) -> list[Game]:
    return [create_game(user, config) for user in config.Users]

def create_chunk(config: Config, worker_index: int) -> list[Game]:
    chunk_size = len(config.Users) // min(config.Connection.Workers, len(config.Users))

    if chunk_size <= 0 and worker_index < len(config.Users) - 1:
        return []

    start = worker_index * chunk_size
    end = max(start + chunk_size, len(config.Users))

    return [create_game(user, config) for user in config.Users[start:end]]

def create_base_game(user: User, config: Config) -> Game:
    return Game(
        user.Username,
        user.Password,
        config.Connection.Domain,
        "stable40",
        config.Connection.Version,
        config.Connection.ExecutableHash,
    )

def create_connector(config: Config) -> BanchoConnector:
    settings = config.Connection.Connector

    if settings.Type == "http":
        return HttpBanchoConnector(settings.Http.Domain)

    if settings.Type == "tcp":
        return TcpBanchoConnector(
            settings.Tcp.Ip,
            settings.Tcp.Port,
        )

    if settings.Type == "websocket":
        return WebsocketBanchoConnector(
            settings.WebSocket.Url,
            path=settings.WebSocket.Path,
            secure=settings.WebSocket.Secure,
            headers=settings.WebSocket.Headers,
            open_timeout=settings.WebSocket.OpenTimeout,
            ping_interval=settings.WebSocket.PingInterval,
            ping_timeout=settings.WebSocket.PingTimeout,
            close_timeout=settings.WebSocket.CloseTimeout,
        )

    raise ValueError(f"Unsupported connector type: '{settings.Type}'")

def create_game(user: User, config: Config) -> Game:
    game = create_base_game(user, config)
    game.bancho.set_connector(create_connector(config))
    actions.add_actions(game, user, config)
    return game
