"""
Точка входа.
"""

from fastapi import FastAPI

from src.poll.router import router as router_poll
from src.answer.router import router as router_answer
from src.template.router import router as router_template
from src.chat.router import router as router_chat
from src.user.router import router as router_user
from src.user_information.router import router as router_user_inf
from src.company.router import router as router_company
from src.result.router import router as router_result
from src.first_init import init_template
from starlette.middleware.cors import CORSMiddleware
from starlette_exporter import handle_metrics
from starlette_exporter import PrometheusMiddleware

from src.config import ALLOWED_ORIGINS

app = FastAPI()

# app.mount("/static", StaticFiles(directory=os.path.join("src", "public")))

origins = ALLOWED_ORIGINS.split(';')
app.add_middleware(CORSMiddleware, allow_origins=['*'], allow_methods=['*'],
                   allow_headers=['*'], allow_credentials=True)

# app.include_router(router_poll)
# app.include_router(router_answer)
# app.include_router(router_template)
# app.include_router(router_user)
# app.include_router(router_user_inf)
# app.include_router(router_company)

app.include_router(router_chat)
app.include_router(router_result)
app.add_middleware(PrometheusMiddleware)
app.add_route("/metrics", handle_metrics)



@app.on_event("startup")
async def setup() -> None:
    """Добавление шаблонов в реестры при необходимости."""
    await init_template.init()


@app.get("/")
async def root():
    return {"message": "Hello!"}


@app.get("/ping", include_in_schema=False)
async def health():
    return {"msg": "mxnzEgBjbUQSNE9i8dfk"}
