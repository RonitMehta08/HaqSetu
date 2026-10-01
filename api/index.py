"""Vercel serverless entrypoint for the HaqSetu API.

Vercel's Python runtime detects the module-level ASGI ``app`` and serves it.
The FastAPI application itself is unchanged and still runs identically under
Docker (see ``Dockerfile``), so this file only fixes up the import path.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

# The function bundle mirrors the repository layout, but the repository root is
# not guaranteed to be on sys.path, so "backend" would not be importable.
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from backend.main import app as fastapi_app  # noqa: E402


async def app(scope, receive, send):
    """Diagnostic wrapper — logs the raw ASGI scope path on /__debug."""
    if scope["type"] == "http" and scope.get("path") == "/__debug":
        body = json.dumps({
            "path": scope.get("path"),
            "raw_path": scope.get("raw_path", b"").decode("utf-8", errors="replace"),
            "root_path": scope.get("root_path", ""),
            "query_string": scope.get("query_string", b"").decode("utf-8", errors="replace"),
            "headers": {
                k.decode(): v.decode()
                for k, v in scope.get("headers", [])
                if k.decode() in ("host", "x-forwarded-for", "x-vercel-forwarded-for", "x-real-url", "x-matched-path", "x-vercel-id")
            },
        }).encode()
        await send({
            "type": "http.response.start",
            "status": 200,
            "headers": [[b"content-type", b"application/json"]],
        })
        await send({"type": "http.response.body", "body": body})
        return
    await fastapi_app(scope, receive, send)

