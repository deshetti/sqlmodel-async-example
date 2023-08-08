from contextlib import asynccontextmanager
from typing import Optional

from fastapi import FastAPI
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlmodel import Field, SQLModel

# Initialize FastAPI application
app = FastAPI()


# Define User model for SQLModel
class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    age: int


# Define UserCreate model for Pydantic validation
# For id field to not show up on the OpenAPI spec
class UserCreate(BaseModel):
    name: str
    age: int


# Database connection string
DATABASE_URL = "postgresql+asyncpg://postgres:postgres@localhost/sampledb"

# Create an asynchronous engine for the database
engine = create_async_engine(
    DATABASE_URL,
    echo=True,
    future=True,
    pool_size=20,
    max_overflow=20,
    pool_recycle=3600,
)


# Ayschronous Context manager for handling database sessions
@asynccontextmanager
async def get_session() -> AsyncSession:
    async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    async with async_session() as session:
        yield session


# Function to create a new user in the database
async def create_user(user: User) -> User:
    async with get_session() as session:
        session.add(user)
        await session.commit()
        await session.refresh(user)
    return user


# Event handler for startup event of FastAPI application
@app.on_event("startup")
async def on_startup():
    async with engine.begin() as conn:
        # For SQLModel, this will create the tables (but won't drop existing ones)
        await conn.run_sync(SQLModel.metadata.create_all)


# Endpoint to create a new user
@app.post("/users/", response_model=User)
async def create_user_endpoint(user: UserCreate):
    db_user = User(**user.dict())
    result = await create_user(db_user)
    return result


# Main entry point of the application
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
