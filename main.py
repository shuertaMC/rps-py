from __future__ import annotations

from dotenv import load_dotenv

load_dotenv()

from fastapi import FastAPI

from app.router import router

app = FastAPI(title="Rock Paper Scissors API")
app.include_router(router)
