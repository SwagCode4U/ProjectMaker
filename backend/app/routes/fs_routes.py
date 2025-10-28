# backend/app/routes/fs_routes.py
from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel
from typing import Optional
from pathlib import Path

router = APIRouter(prefix="/api/fs", tags=["Filesystem"])

# Compute project root as repository root (three levels up from this file)
PROJECT_ROOT = Path(__file__).resolve().parents[3]
ROOT_NAME = PROJECT_ROOT.name

class CreatePayload(BaseModel):
    currentDir: str = "."
    input: str


def _safe_join(rel: str) -> Path:
    rel = (rel or "").strip()
    rel = rel.replace("\\", "/")
    if rel in ("", "."):
        return PROJECT_ROOT
    rel = rel.lstrip("/")
    # Strip leading project root name if present
    parts = [p for p in rel.split('/') if p]
    if parts and parts[0] == ROOT_NAME:
        parts = parts[1:]
    rel = '/'.join(parts)
    p = (PROJECT_ROOT / rel).resolve()
    if PROJECT_ROOT == p or PROJECT_ROOT in p.parents:
        return p
    raise HTTPException(status_code=400, detail="Path escapes project root")


def _looks_like_file(name: str) -> bool:
    return "." in Path(name).name


@router.get("/list")
def list_dir(dir: Optional[str] = Query(default=".")):
    try:
        base = _safe_join(dir)
        if not base.exists():
            base.mkdir(parents=True, exist_ok=True)
        items = []
        for entry in base.iterdir():
            items.append({
                "name": entry.name,
                "type": "dir" if entry.is_dir() else "file"
            })
        items.sort(key=lambda x: (x["type"], x["name"]))
        rel = str(base.relative_to(PROJECT_ROOT)) if base != PROJECT_ROOT else "."
        return {"ok": True, "dir": rel, "items": items}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/create")
def create_item(payload: CreatePayload):
    try:
        trimmed = (payload.input or "").strip()
        if not trimmed:
            raise HTTPException(status_code=400, detail="Empty input")

        base = _safe_join(payload.currentDir)

        # Decide file vs dir based on input convention
        if trimmed.startswith("/"):
            name = trimmed.lstrip("/")
            kind = "dir"
        else:
            name = trimmed
            kind = "file" if _looks_like_file(name) else "dir"

        safe_name = str(Path(name))
        target = _safe_join(str((base.relative_to(PROJECT_ROOT) / safe_name).as_posix()))

        if kind == "dir":
            target.mkdir(parents=True, exist_ok=True)
        else:
            target.parent.mkdir(parents=True, exist_ok=True)
            with open(target, "x") as f:
                f.write("")

        return {"ok": True, "kind": kind, "path": str(target.relative_to(PROJECT_ROOT))}
    except FileExistsError:
        raise HTTPException(status_code=400, detail="File already exists")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
