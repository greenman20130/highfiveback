"""
Точка входа.
"""

from fastapi import FastAPI

from src.chat.router import router as router_chat
from src.result.router import router as router_result

from starlette.middleware.cors import CORSMiddleware
from starlette_exporter import handle_metrics
from starlette_exporter import PrometheusMiddleware

from src.config import ALLOWED_ORIGINS

app = FastAPI()

# app.mount("/static", StaticFiles(directory=os.path.join("src", "public")))

origins = ALLOWED_ORIGINS.split(';')
app.add_middleware(CORSMiddleware, allow_origins=['*'], allow_methods=['*'],
                   allow_headers=['*'], allow_credentials=True)


app.include_router(router_chat)
app.include_router(router_result)
app.add_middleware(PrometheusMiddleware)
app.add_route("/metrics", handle_metrics)

@app.get("/")
async def root():
    return {"message": "Hello!"}


@app.get("/ping", include_in_schema=False)
async def health():
    return {"msg": "mxnzEgBjbUQSNE9i8dfk"}
