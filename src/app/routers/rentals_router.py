
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from src.app.data.database import get_db
from ..models.rental import RentalProcessing, RentalOutcome
from src.app.data.schema import Rental, Bike
from sqlalchemy import select
import datetime

router = APIRouter()

@router.post("/rentals", response_model=RentalOutcome)
async def create_rental(
    rental: RentalProcessing,
    db: AsyncSession = Depends(get_db)
):
    # Buscar la bicicleta
    result = await db.execute(select(Bike).where(Bike.battery >= 20))
    bike = result.scalars().first()
    if not bike:
        raise ValueError("No enough bikes with sufficient battery.")

    # Crear el rental
    new_rental = Rental(
        user_id=rental.user_id,
        bike_id=bike.id,
        start_time=str(datetime.datetime.now()),
        end_time=None
    )
    db.add(new_rental)
    await db.commit()
    await db.refresh(new_rental)

    # Actualizar batería de la bici (ejemplo: restar 10%)
    bike.battery -= 10
    await db.commit()
    await db.refresh(bike)

    return RentalOutcome(
        bike_id=bike.id,
        user_id=rental.user_id,
        battery_level=bike.battery
    )

