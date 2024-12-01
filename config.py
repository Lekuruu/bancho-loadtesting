
from dataclasses import dataclass
from typing import List

import json
import os

@dataclass
class TcpSettings:
    Enabled: bool
    IP: str
    Port: int

@dataclass
class Connection:
    Domain: str
    Workers: int
    Version: int
    ExecutableHash: str
    TCP: TcpSettings

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
    Users: List[User]
    Leaderboard: Leaderboard

def load(path: str = "config.json") -> Config:
    if not os.path.exists(path):
        raise FileNotFoundError(f"Configuration file not found: '{path}'")

    with open(path, "r") as f:
        data = json.load(f)
        data["Connection"]["TCP"] = TcpSettings(**data["Connection"]["TCP"])

    return Config(
        Connection=Connection(**data["Connection"]),
        Flags=Flags(**data["Flags"]),
        Users=[User(**user) for user in data["Users"]],
        Leaderboard=Leaderboard(**data["Leaderboard"])
    )
