from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Dict, Any, Optional
from src.app.data.mocks import BIKES
from src.app.data.schema import Bike

class BikesDataSource:
    
    def __init__(self, db=AsyncSession):
        self.db = db

    async def get_all_bikes(self) -> List[Bike]:
        """Retrieve all bikes."""
        result = await self.db.execute(select(Bike))
        return result.scalars().all()

    async def get_bike(self, bike_id: int) -> Optional[Bike]:
        """Retrieve a single bike by ID."""
        result = await self.db.execute(select(Bike).where(Bike.id == bike_id))
        bike = result.scalars_one_or_none()
        return bike

    async def create_bike(self, bike_data: Dict[str, Any]) -> Bike:
        """Create a new bike and auto-increment the ID."""
        # simple logic to find max ID + 1
        new_id = 1
        if BIKES:
            new_id = max(bike["id"] for bike in BIKES) + 1
        
        # Add ID to the new data
        new_bike = {**bike_data, "id": new_id}
        BIKES.append(new_bike)
        return new_bike

    async def update_bike(self, bike_id: int, update_data: Dict[str, Any]) -> Optional[Bike]:
        """Update a bike. Returns the updated bike or None if not found."""
        bike = await self.get_bike(bike_id)
        if bike:
            for key, value in update_data.items():
                setattr(bike, key, value)
            await self.db.commit()
            await self.db.refresh(bike)
            return bike
        return None

    async def delete_bike(self, bike_id: int) -> bool:
        """Delete a bike. Returns True if deleted, False if not found."""
        bike = await self.get_bike(bike_id)
        if bike:
            await self.db.delete(bike)
            await self.db.commit()
            return True
        return False

def get_bike_datasource() -> BikesDataSource:
    """Factory function to get a BikesDataSource instance."""
    return BikesDataSource()