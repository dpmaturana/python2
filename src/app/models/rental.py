
from pydantic import BaseModel, field_validator, model_validator

class RentalProcessing(BaseModel):
	bike_battery: int
	user_id: int

	@model_validator(mode="after")
	def check_battery(cls, values):
		if values.bike_battery < 20:
			raise ValueError("Bike battery too low for rental.")
		return values

class RentalOutcome(BaseModel):
	bike_id: int
	user_id: int
	battery_level: float  # porcentaje de batería (0-100)

	@field_validator('battery_level')
	def min_battery(battery_level):
		if battery_level < 20:
			raise ValueError('Cannot create rental: bike battery must be at least 20%')
		return battery_level
