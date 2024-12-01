
from osu.bancho.constants import StatusAction
from config import Leaderboard, Config
from osu import Game

import random

def send_message(game: Game, user_messages: list):
    if not game.bancho.connected:
        return

    if not user_messages:
        return

    channel = game.bancho.channels.get("#osu")

    if not channel:
        return

    message = random.choice(user_messages)
    channel.send_message(message)
    user_messages.remove(message)

def spectate(game: Game, spectator_id: int):
    if not game.bancho.connected:
        return

    if not game.bancho.player:
        return

    if game.bancho.spectating:
        return

    if not (target := game.bancho.players.by_id(spectator_id)):
        return

    game.bancho.start_spectating(target)

def request_leaderboard(game: Game, config: Leaderboard):
    if not game.bancho.connected:
        return

    game.api.get_scores(
        config.BeatmapHash,
        config.BeatmapFilename,
        config.BeatmapsetId,
    )

def change_status(game: Game):
    if not game.bancho.connected:
        return
    
    if not game.bancho.player:
        return
    
    game.bancho.player.status.action = random.choice([
        StatusAction.Idle,
        StatusAction.Afk,
        StatusAction.Playing,
        StatusAction.Editing,
        StatusAction.Modding,
        StatusAction.Paused,
        StatusAction.Lobby,
        StatusAction.OsuDirect
    ])

    game.bancho.update_status()

def add_actions(game: Game, config: Config):
    if config.Flags.EnableSpectating:
        game.tasks.register(seconds=5)(
            lambda: spectate(game, config.SpectatorId)
        )

    if config.Flags.EnableMessages:
        game.tasks.register(seconds=5, loop=True)(
            lambda: send_message(game, config.Messages)
        )

    if config.Flags.EnableStatusUpdates:
        game.tasks.register(seconds=5, loop=True)(
            lambda: change_status(game)
        )

    if config.Flags.EnableLeaderboardRequests:
        game.tasks.register(seconds=config.Leaderboard.RequestIntervalMs / 1000, loop=True)(
            lambda: request_leaderboard(game, config.Leaderboard)
        )
