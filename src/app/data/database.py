# Configuración de AsyncEngine para SQLite usando aiosqlite
from sqlalchemy.ext.asyncio import create_async_engine, AsyncEngine, AsyncSession
from sqlalchemy.orm import sessionmaker
from typing import AsyncGenerator

DATABASE_URL = "sqlite+aiosqlite:///./ecomute.db"

engine: AsyncEngine = create_async_engine(DATABASE_URL, echo=True)

# Generador de dependencia para obtener una sesión asíncrona

async_session = sessionmaker(
	engine, class_=AsyncSession, expire_on_commit=False
)

async def get_db() -> AsyncGenerator[AsyncSession, None]:
	async with async_session() as session:
		yield session
