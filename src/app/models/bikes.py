from pydantic import BaseModel, Field
from typing import Optional, Literal

class BikeBase(BaseModel):
    model: str
    battery: float = Field(..., le=100, ge=0)
    status: Literal['available', 'rented', 'maintenance']
    station_id: Optional[int] = None

class BikeCreate(BikeBase):
    id: int    

class BikeResponse(BikeBase):
    id: int

class BikeUpdate(BaseModel):
    model: Optional[str] = None
    battery: Optional[float] = Field(None, le=100, ge=0)
    status: Optional[Literal['available', 'rented', 'maintenance']] = None
    station_id: Optional[int] = None

