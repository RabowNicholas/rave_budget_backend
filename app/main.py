# main.py

from fastapi import FastAPI
from app.api.user.router import user_router
from app.api.budget.router import budget_router


app = FastAPI()

app.include_router(user_router, prefix="/users")
app.include_router(budget_router, prefix="/budgets")
