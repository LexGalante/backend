from fastapi import FastAPI

from .routes import index

subapp: FastAPI = FastAPI()

subapp.include_router(router=index.router, prefix="/index", tags=["index"])
