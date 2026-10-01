"""Vercel serverless entrypoint for the HaqSetu API.

Vercel's Python runtime detects the module-level ASGI ``app`` and serves it.
The FastAPI application itself is unchanged and still runs identically under
Docker (see ``Dockerfile``), so this file only fixes up the import path.
"""

from __future__ import annotations

import sys
from pathlib import Path

# The function bundle mirrors the repository layout, but the repository root is
# not guaranteed to be on sys.path, so "backend" would not be importable.
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from backend.main import app  # noqa: E402  (import must follow the path fix)

__all__ = ["app"]
