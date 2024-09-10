# main.py
from fastapi import FastAPI, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.models import User
from app.database import Base, engine, get_db

app = FastAPI()


# Create tables in the database (run once)
@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


@app.post("/users/", response_model=User)
async def create_user(name: str, email: str, db=Depends(get_db)):
    user = User(name=name, email=email)
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user
