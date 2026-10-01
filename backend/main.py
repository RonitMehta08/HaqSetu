"""FastAPI application for the HaqSetu evidence-first demo."""

from __future__ import annotations

import json
import logging
from pathlib import Path
from typing import Any

from fastapi import FastAPI, HTTPException, Query, Request
from fastapi.encoders import jsonable_encoder
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import ValidationError

from . import __version__
from .i18n import DISCLAIMER, lang, localized
from .models import AnalyzeRequest, FeedbackRequest, HealthResponse, Profile
from .services import analyze, feedback, privacy_safe_log


ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / "data" / "schemes.json"
FRONTEND_PATH = ROOT / "frontend"


def load_schemes() -> list[dict[str, Any]]:
    with DATA_PATH.open("r", encoding="utf-8") as stream:
        data = json.load(stream)
    if not isinstance(data, list) or len(data) < 20:
        raise RuntimeError("data/schemes.json must contain at least twenty schemes")
    return data


SCHEMES = load_schemes()

DEMO_PROFILES: dict[str, dict[str, Any]] = {
    "farmer": {
        "name": "Demo Farmer",
        "state": "Madhya Pradesh",
        "age": 42,
        "occupation": "small farmer",
        "monthly_income": 12000,
        "social_category": "OBC",
        "landholding": 1.4,
        "disability": False,
        "needs": ["income support", "crop insurance", "health"],
        "language": "en",
    },
    "vendor_hi": {
        "state": "Uttar Pradesh",
        "age": 35,
        "occupation": "street vendor",
        "monthly_income": 15000,
        "social_category": "SC",
        "landholding": 0,
        "disability": False,
        "needs": ["ऋण", "स्वास्थ्य"],
        "language": "hi",
    },
    "senior": {
        "state": "Rajasthan",
        "age": 68,
        "occupation": "agricultural worker",
        "monthly_income": 8000,
        "social_category": "General",
        "landholding": 0,
        "disability": True,
        "needs": ["pension", "health"],
        "language": "en",
    },
}


logging.basicConfig(level=logging.INFO, format="%(levelname)s %(name)s %(message)s")

app = FastAPI(
    title="HaqSetu API",
    version=__version__,
    description=(
        "Evidence-first, multilingual government-benefits screening. "
        "No live government API integrations are used."
    ),
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173"],
    allow_credentials=False,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)


@app.exception_handler(ValidationError)
async def validation_exception_handler(request: Request, exc: ValidationError) -> JSONResponse:
    privacy_safe_log("validation_error", path=request.url.path, error_count=len(exc.errors()))
    return JSONResponse(status_code=422, content={"detail": jsonable_encoder(exc.errors())})


@app.get("/api/health", response_model=HealthResponse)
def health() -> HealthResponse:
    return HealthResponse(
        status="ok", service="haqsetu-backend", version=__version__,
        demo_mode=True, live_integrations=False,
    )


@app.get("/api/schemes")
def schemes(language: str = Query(default="en")) -> dict[str, Any]:
    selected_language = lang(language)
    return {
        "schemes": [
            {
                "id": scheme["id"],
                "name": localized(scheme, selected_language, "name"),
                "summary": localized(scheme, selected_language, "summary"),
                "ministry": scheme["ministry"],
                "tags": scheme.get("tags", []),
                "source": scheme["source"],
            }
            for scheme in SCHEMES
        ],
        "language": selected_language,
        "disclaimer": DISCLAIMER[selected_language],
        "live_lookup": False,
    }


def parse_profile(payload: dict[str, Any]) -> tuple[Profile, str]:
    """Accept documented envelope, bare profile, or named deterministic demo."""

    request = AnalyzeRequest.model_validate(payload)
    if request.demo:
        key = request.demo.casefold()
        if key not in DEMO_PROFILES:
            raise HTTPException(
                status_code=400,
                detail=f"Unknown demo profile. Choose: {', '.join(sorted(DEMO_PROFILES))}",
            )
        return Profile.model_validate(DEMO_PROFILES[key]), "demo"
    if request.profile is not None:
        return request.profile, "screening"
    direct = {key: value for key, value in payload.items() if key not in {"demo", "profile"}}
    try:
        return Profile.model_validate(direct), "screening"
    except ValidationError as exc:
        raise HTTPException(status_code=422, detail=exc.errors()) from exc


@app.post("/api/analyze")
def analyze_endpoint(payload: dict[str, Any]) -> dict[str, Any]:
    profile, mode = parse_profile(payload)
    return analyze(profile, SCHEMES, mode=mode)


@app.post("/v1/run")
def marketplace_run_endpoint(payload: dict[str, Any]) -> dict[str, Any]:
    """Public buyer-testing alias with a stable versioned path.

    The marketplace contract intentionally uses the same JSON body and response
    as /api/analyze, while the original route remains available for the app and
    backwards compatibility.
    """

    return analyze_endpoint(payload)


@app.post("/api/feedback")
def feedback_endpoint(payload: FeedbackRequest) -> dict[str, Any]:
    return feedback(payload.model_dump(exclude_none=True))


# Serve the judge-facing single-page demo from the same process in the
# container. API routes are declared above the mount, so /api/* remains the
# machine-readable contract while / serves the static UI.
if FRONTEND_PATH.exists():
    app.mount("/", StaticFiles(directory=FRONTEND_PATH, html=True), name="frontend")
