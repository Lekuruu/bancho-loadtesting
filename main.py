
from __future__ import annotations

from multiprocessing import Pool, Process
from threading import Thread
from config import Config
from osu import TcpGame
from typing import List

import logging
import signal
import config
import game
import time
import os

def setup_logging():
    logging.basicConfig(
        level=logging.INFO,
        format='[%(asctime)s] - <%(name)s> %(levelname)s: %(message)s'
    )

def run_game_thread(client: TcpGame, delay: int = 0.15) -> Thread:
    thread = Thread(target=client.run)
    thread.start()
    time.sleep(delay)
    return thread

def run_game_process(config: Config, index: int) -> None:
    clients = game.create_chunk(config, index)

    if not clients:
        exit(0)

    threads = [
        run_game_thread(client)
        for client in clients
    ]

    def on_exit(signum, frame):
        for client in clients:
            client.bancho.exit()

        exit(0)

    signal.signal(
        signal.SIGTERM,
        on_exit
    )

    for thread in threads:
        thread.join()

def run_game_collection(config: Config) -> None:
    logging.info(f"Launching client workers... ({config.Connection.Workers})")
    processes: List[Process] = []

    with Pool(config.Connection.Workers) as pool:
        for i in range(config.Connection.Workers):
            result = pool.apply_async(run_game_process, [config, i])
            processes.append(result.get())

    signal.signal(
        signal.SIGINT,
        lambda signum, frame: on_exit(processes)
    )

    signal.signal(
        signal.SIGTERM,
        lambda signum, frame: on_exit(processes)
    )

    logging.info(
        f"Launched {len(processes * config.Connection.Workers)} clients. Press Ctrl+C to exit."
    )

    for process in processes:
        if not process:
            continue

        process.join()

def on_exit(processes: List[Process]) -> None:
    logging.info("Exiting...")

    for process in processes:
        process.terminate()
        process.kill()

    os._exit(0)

if __name__ == "__main__":
    try:
        setup_logging()
        run_game_collection(config.load())
    except KeyboardInterrupt:
        pass
