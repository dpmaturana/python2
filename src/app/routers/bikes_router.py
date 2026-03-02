# bikes_router.py
from fastapi import APIRouter, HTTPException, Query, Depends
from typing import List, Optional, Literal
from src.app.models.bikes import BikeResponse, BikeCreate, BikeUpdate
from src.app.data.datasources.bikes_data_source import get_bike_datasource, BikesDataSource
from sqlalchemy.ext.asyncio import AsyncSession
from src.app.data.database import get_db

router = APIRouter()

def get_bike_datasource(db: AsyncSession = Depends(get_db)) -> BikesDataSource:
    return BikesDataSource(db)

@router.get("/", response_model=List[BikeResponse])
async def read_bikes(
    status: Optional[Literal['available', 'rented', 'maintenance']] = Query(None, description="Bike status to filter"),
    datasource: BikesDataSource = Depends(get_bike_datasource),
):
    all_bikes = await datasource.get_all_bikes()
    if status:
        return [bike for bike in all_bikes if bike.get("status") == status]
    return all_bikes

@router.get("/{bike_id}", response_model=BikeResponse)
def read_bike(bike_id: int, datasource: BikesDataSource = Depends(get_bike_datasource)):
    bike = datasource.get_bike(bike_id)
    if not bike:
        raise HTTPException(status_code=404, detail="Bike not found")
    return bike

@router.post("/", response_model=BikeResponse, status_code=201)
def create_bike(bike: BikeCreate, datasource: BikesDataSource = Depends(get_bike_datasource)):
    new_bike = datasource.create_bike(bike())
    return new_bike

@router.put("/{bike_id}", response_model=BikeResponse)
def update_bike(bike_id: int, bike: BikeUpdate, datasource: BikesDataSource = Depends(get_bike_datasource)):
    updated = datasource.update_bike(bike_id, bike(exclude_unset=True))
    if not updated:
        raise HTTPException(status_code=404, detail="Bike not found")
    return updated

@router.delete("/{bike_id}", status_code=204)
def delete_bike(bike_id: int, datasource: BikesDataSource = Depends(get_bike_datasource)):
    deleted = datasource.delete_bike(bike_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Bike not found")


