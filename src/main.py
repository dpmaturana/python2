
from fastapi import FastAPI
from contextlib import asynccontextmanager
from src.app.routers.rentals_router import router as rentals_router
from src.app.routers.bikes_router import router as bikes_router
from src.app.routers.users_router import router as users_router
from src.app.routers.admin_router import router as admin_router
from src.app.data.database import engine
from src.app.data.schema import Base

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Crear tablas en la base de datos al iniciar la app
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    await engine.dispose()

app = FastAPI(lifespan=lifespan)
app.include_router(rentals_router)
app.include_router(bikes_router)
app.include_router(users_router)
app.include_router(admin_router)

@app.get("/")
async def get_root():
    return {"message": "Hello Class"}















































