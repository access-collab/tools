from fastapi import FastAPI
from fastapi.responses import JSONResponse

from app.database import init_db
from app.routers import health
from app.routers import vlopse
app = FastAPI(title="DSA40 Application Helper")

init_db()

app.include_router(health.router)
app.include_router(vlopse.router)
@app.get("/")
def index_fallback() -> JSONResponse:
    return JSONResponse({"message": "Hello World!"})

