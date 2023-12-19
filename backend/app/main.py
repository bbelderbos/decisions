
from fastapi import FastAPI

from app.api.router import router as api_router
from app.fastui.router import router as fastui_router

app = FastAPI()

app.include_router(fastui_router)
app.include_router(api_router)
