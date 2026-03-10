from __future__ import annotations

from pydantic import BaseModel


class Game(BaseModel):
    id: str
    player1_move: str | None = None
    player2_move: str | None = None
    status: str = "waiting"
    winner: str | None = None
    created_at: str


class MakeMoveRequest(BaseModel):
    player: int
    choice: str
