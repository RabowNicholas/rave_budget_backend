# main.py

from fastapi import FastAPI
from app.api.user.router import user_router


app = FastAPI()

app.include_router(user_router, prefix="/users")
