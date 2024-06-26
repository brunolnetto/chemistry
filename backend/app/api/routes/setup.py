# Description: This file contains the setup routes for the FastAPI application.
from fastapi import APIRouter
import toml

from backend.app.core.config import settings

router = APIRouter()


@router.get("/ping")
async def pong():
    return {"message": "pong"}


@router.get("/health")
async def health_check():
    return dict(
        name=settings.PROJECT_NAME,
        version=settings.VERSION,
        status="OK",
        message="Visit /docs for more information.",
    )


@router.get("/info")
async def info():
    with open("pyproject.toml", "r") as f:
        config = toml.load(f)

    return {
        "name": config["tool"]["poetry"]["name"],
        "version": config["tool"]["poetry"]["version"],
        "description": config["tool"]["poetry"]["description"],
    }


@router.get("/sentry-debug")
async def trigger_error():
    division_by_zero = 1 / 0
    return division_by_zero
