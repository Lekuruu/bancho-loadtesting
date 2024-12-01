
from __future__ import annotations
from config import Config, User
from osu import Game, TcpGame
from typing import List
import actions

def create_collection(config: Config) -> List[Game]:
    return [
        create_game(user, config)
        for user in config.Users
    ]

def create_chunk(config: Config, worker_index: int) -> List[Game]:
    chunk_size = len(config.Users) // min(config.Connection.Workers, len(config.Users))

    if chunk_size <= 0 and worker_index < len(config.Users) - 1:
        return []

    start = worker_index * chunk_size
    end = max(start + chunk_size, len(config.Users))

    return [
        create_game(user, config)
        for user in config.Users[start:end]
    ]

def create_tcp_game(user: User, config: Config) -> TcpGame:
    return TcpGame(
        user.Username,
        user.Password,
        config.Connection.Domain,
        config.Connection.TCP.Version,
        config.Connection.TCP.ExecutableHash,
        config.Connection.TCP.IP,
        config.Connection.TCP.Port,
    )

def create_http_game(user: User, config: Config) -> Game:
    return Game(
        user.Username,
        user.Password,
        config.Connection.Domain,
    )

def create_game(user: User, config: Config) -> Game:
    game_function = (
        create_http_game
        if not config.Connection.TCP.Enabled
        else create_tcp_game
    )

    game = game_function(user, config)
    actions.add_actions(game, config)
    return game
