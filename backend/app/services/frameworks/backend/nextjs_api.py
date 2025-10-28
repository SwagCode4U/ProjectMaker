# backend/app/services/frameworks/backend/nextjs_api.py
# Thin shim so the backend id `nextjs_api` resolves to the existing Next.js API module
from . import nextapi as _impl
from pathlib import Path
from typing import Dict


def normalize(v: str) -> str:
    return _impl.normalize(v)


def meta() -> Dict:
    return _impl.meta()


def preview(config: Dict) -> Dict:
    return _impl.preview(config)


def build(root: Path, config: Dict) -> Dict:
    return _impl.build(root, config)
