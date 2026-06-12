from __future__ import annotations

import os
from pathlib import Path
from typing import Any

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

from .config import load_config
from .dashboard import build_dashboard, merge_note_progress
from .parser import parse_all_notes
from .progress import ProgressStore


VAULT_ROOT = Path(__file__).resolve().parents[2]
FRONTEND_ROOT = VAULT_ROOT / "trainer" / "frontend"
CONFIG = load_config(VAULT_ROOT)
PROGRESS_PATH = Path(os.environ.get("TRAINER_PROGRESS_PATH", str(VAULT_ROOT / CONFIG["progress_path"])))

app = FastAPI(title=CONFIG["app_title"])
progress_store = ProgressStore(PROGRESS_PATH)

app.mount("/static", StaticFiles(directory=FRONTEND_ROOT), name="static")
if (VAULT_ROOT / "assets").exists():
    app.mount("/assets", StaticFiles(directory=VAULT_ROOT / "assets"), name="assets")


class RatingPayload(BaseModel):
    rating: int = Field(ge=1, le=5)
    note: str | None = None


@app.get("/")
def index() -> FileResponse:
    return FileResponse(FRONTEND_ROOT / "index.html")


@app.get("/api/config")
def config() -> dict[str, Any]:
    return CONFIG


@app.get("/api/health")
def health() -> dict[str, Any]:
    notes = parse_all_notes(VAULT_ROOT, CONFIG)
    return {"status": "ok", "questions": len(notes)}


@app.get("/api/questions")
def questions() -> list[dict[str, Any]]:
    notes = parse_all_notes(VAULT_ROOT, CONFIG)
    progress = progress_store.read()
    return [merge_note_progress(note, progress) for note in notes]


@app.get("/api/questions/{number}")
def question(number: int) -> dict[str, Any]:
    note = find_note(number)
    progress = progress_store.read()
    data = note.full()
    data["progress"] = progress.get("questions", {}).get(str(number), {})
    return data


@app.post("/api/questions/{number}/rating")
def save_rating(number: int, payload: RatingPayload) -> dict[str, Any]:
    find_note(number)
    updated = progress_store.update_rating(number, payload.rating, payload.note)
    return {"number": number, "progress": updated}


@app.get("/api/dashboard")
def dashboard() -> dict[str, Any]:
    notes = parse_all_notes(VAULT_ROOT, CONFIG)
    progress = progress_store.read()
    return build_dashboard(notes, progress)


def find_note(number: int):
    for note in parse_all_notes(VAULT_ROOT, CONFIG):
        if note.number == number:
            return note
    raise HTTPException(status_code=404, detail=f"Question {number} not found")
