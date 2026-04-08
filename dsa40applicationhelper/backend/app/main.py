from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.routing import APIRoute

from app.database import init_db
from app.routers import health
from app.routers import form
from app.routers import vlopse


def custom_generate_unique_id(route: APIRoute) -> str:
    return f"{route.path}-{route.name}"


app = FastAPI(
    title="DSA40 Application Helper",
    generate_unique_id_function=custom_generate_unique_id,
)

init_db()

app.include_router(health.router)
app.include_router(vlopse.router)
@app.get("/")
def index_fallback() -> JSONResponse:
    return JSONResponse({"message": "Hello World!"})

