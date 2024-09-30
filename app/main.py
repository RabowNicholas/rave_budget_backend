# main.py

from fastapi import FastAPI
from app.api.user.router import user_router
from app.api.budget.router import budget_router
from app.api.dashboard.router import dashboard_router
from app.api.interest.router import interest_router


app = FastAPI()

app.include_router(user_router, prefix="/users")
app.include_router(budget_router, prefix="/budgets")
app.include_router(dashboard_router, prefix="/dashboard")
app.include_router(interest_router, prefix="/interest")
