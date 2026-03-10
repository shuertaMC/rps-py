from __future__ import annotations

from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse

from . import service
from .models import Game, MakeMoveRequest

router = APIRouter()


@router.post("/games", status_code=201)
async def create_game() -> Game:
    return service.create_game()


@router.post("/games/{game_id}/moves")
async def make_move(game_id: str, body: MakeMoveRequest) -> Game:
    try:
        return service.make_move(game_id, body.player, body.choice)
    except KeyError:
        raise HTTPException(status_code=404, detail="Game not found")
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))
    except Exception:
        raise HTTPException(status_code=500, detail="An unexpected error occurred")
