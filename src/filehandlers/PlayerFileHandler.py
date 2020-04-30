from src.common.Constants import PLAYER_STORAGE
from src.logic.Player import Player
import pickle
from typing import List


def load_players() -> List[Player]:
    try:
        with open(PLAYER_STORAGE, mode='rb') as players_file:
            return pickle.load(players_file)
    except FileNotFoundError:
        return []


def save_players(players: List[Player]) -> None:
    with open(PLAYER_STORAGE, mode='wb+') as players_file:
        pickle.dump(players, players_file)
