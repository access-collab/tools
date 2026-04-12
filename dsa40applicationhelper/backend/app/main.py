import sqlite3
from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.routing import APIRoute
from fastapi.staticfiles import StaticFiles
from sqlalchemy.exc import IntegrityError

from app.database import init_db
from app.routers import form, health, questions, vlopse


def custom_generate_unique_id(route: APIRoute) -> str:
    return f"{route.path}-{route.name}"


app = FastAPI(
    title="DSA40 Application Helper",
    generate_unique_id_function=custom_generate_unique_id,
)


@app.exception_handler(IntegrityError)
async def http_exception_handler(request, exc: IntegrityError):
    orig = exc.orig
    if isinstance(orig, sqlite3.IntegrityError):
        if "UNIQUE constraint failed: vlopse_question.id" in orig.args:
            return JSONResponse(
                status_code=409,
                content={"message": "Duplicate VLOPSE question id"},
            )
        elif "UNIQUE constraint failed: dsa_question.id" in orig.args:
            return JSONResponse(
                status_code=409,
                content={"message": "Duplicate DSA40 question id"},
            )
    return JSONResponse(status_code=500, content={"message": "Unknown integrity error"})


init_db()

app.include_router(health.router)
app.include_router(form.router)
app.include_router(vlopse.router)
app.include_router(questions.router)

STATIC_DIR = Path(__file__).parent / "static"


if STATIC_DIR.exists() and any(STATIC_DIR.iterdir()):
    app.mount("/", StaticFiles(directory=STATIC_DIR, html=True), name="static")
else:

    @app.get("/")
    def index_fallback() -> JSONResponse:
        return JSONResponse({"message": "Hello World!"})
