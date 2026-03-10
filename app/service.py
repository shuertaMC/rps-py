from __future__ import annotations

import json
import os
import secrets
from datetime import datetime, timezone
from pathlib import Path

from .models import Game

_STORAGE_PATH = Path(__file__).parent.parent / "var" / "data" / "games.json"

_VALID_CHOICES = {"rock", "paper", "scissors"}

_BEATS: dict[str, set[str]] = {
    "rock": {"scissors"},
    "scissors": {"paper"},
    "paper": {"rock"},
}


def _load_games() -> dict[str, dict]:
    if not _STORAGE_PATH.exists():
        return {}
    with open(_STORAGE_PATH) as f:
        return json.load(f)


def _save_games(games: dict[str, dict]) -> None:
    _STORAGE_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(_STORAGE_PATH, "w") as f:
        json.dump(games, f, indent=4)


def _hydrate(data: dict) -> Game:
    return Game(**data)


def _determine_winner(p1: str, p2: str) -> str:
    if p1 == p2:
        return "draw"
    return "player1" if p2 in _BEATS[p1] else "player2"


def create_game() -> Game:
    game = Game(
        id=secrets.token_hex(8),
        created_at=datetime.now(timezone.utc).isoformat(),
    )
    games = _load_games()
    games[game.id] = game.model_dump()
    _save_games(games)
    return game


def make_move(game_id: str, player: int, choice: str) -> Game:
    if player not in (1, 2):
        raise ValueError("Player must be 1 or 2")
    if choice not in _VALID_CHOICES:
        raise ValueError(f"Choice must be one of: {', '.join(sorted(_VALID_CHOICES))}")

    games = _load_games()
    if game_id not in games:
        raise KeyError(f"Game {game_id!r} not found")

    game = _hydrate(games[game_id])

    if game.status == "complete":
        raise ValueError("Game is already complete")

    move_field = f"player{player}_move"
    if getattr(game, move_field) is not None:
        raise ValueError(f"Player {player} has already made a move")

    setattr(game, move_field, choice)

    if game.player1_move is not None and game.player2_move is not None:
        game.winner = _determine_winner(game.player1_move, game.player2_move)
        game.status = "complete"

    games[game_id] = game.model_dump()
    _save_games(games)
    return game
