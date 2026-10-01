"""Pydantic request and response models for HaqSetu."""

from __future__ import annotations

from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator


class Profile(BaseModel):
    """Explicit facts used for a first-pass screening.

    Aadhaar, bank details, address, and other identifiers are intentionally
    outside this model because they are not needed for catalogue screening.
    """

    model_config = ConfigDict(extra="ignore")

    name: str | None = Field(default=None, max_length=120)
    state: str = Field(min_length=2, max_length=80)
    age: int = Field(ge=0, le=120)
    occupation: str = Field(min_length=2, max_length=120)
    monthly_income: float = Field(ge=0, le=100_000_000)
    social_category: str = Field(min_length=1, max_length=40)
    landholding: float = Field(default=0, ge=0, le=1_000_000)
    disability: bool = False
    needs: list[str] = Field(default_factory=list, max_length=20)
    language: Literal["en", "hi"] = "en"

    @field_validator("state", "occupation", "social_category", mode="before")
    @classmethod
    def trim_required_text(cls, value: Any) -> Any:
        if isinstance(value, str):
            return value.strip()
        return value

    @field_validator("name", mode="before")
    @classmethod
    def trim_name(cls, value: Any) -> Any:
        if isinstance(value, str):
            value = value.strip()
            return value or None
        return value

    @model_validator(mode="before")
    @classmethod
    def drop_blank_optionals(cls, data: Any) -> Any:
        """Treat an untouched form input as "not supplied".

        Hosted buyer-testing forms submit every declared field, sending "" for
        the ones the tester left blank. Dropping those keys lets the declared
        field defaults apply instead of failing validation.
        """

        if not isinstance(data, dict):
            return data
        optional = {"name", "landholding", "disability", "needs", "language"}
        return {
            key: value
            for key, value in data.items()
            if not (key in optional and isinstance(value, str) and not value.strip())
        }

    @field_validator("needs", mode="before")
    @classmethod
    def normalize_needs(cls, value: Any) -> Any:
        if value is None:
            return []
        if isinstance(value, str):
            # Hosted buyer-testing forms render this as a single text input, so
            # accept "income support, crop insurance" alongside a JSON array.
            value = value.split(",")
        if not isinstance(value, list):
            raise ValueError("needs must be a list of strings or a comma-separated string")
        return [item.strip() for item in value if isinstance(item, str) and item.strip()]


class AnalyzeRequest(BaseModel):
    """Request envelope, with a deterministic demo selector."""

    model_config = ConfigDict(extra="allow")

    profile: Profile | None = None
    demo: str | None = Field(default=None, max_length=40)


class FeedbackRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    analysis_id: str | None = Field(default=None, max_length=80)
    rating: int | None = Field(default=None, ge=1, le=5)
    helpful: bool | None = None
    comment: str | None = Field(default=None, max_length=500)


class HealthResponse(BaseModel):
    status: Literal["ok"]
    service: str
    version: str
    demo_mode: bool
    live_integrations: bool
