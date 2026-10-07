from fastapi import FastAPI

from apps.api.files import router

app = FastAPI()

app.include_router(router)