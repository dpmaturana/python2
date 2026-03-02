from sqlalchemy import ForeignKey, Integer
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, Relationship

class Base(DeclarativeBase):
    pass

class Bike(Base):
    __tablename__ = 'bikes'
    id: Mapped[int] = mapped_column(primary_key=True)
    model: Mapped[str] = mapped_column(nullable=False)
    battery: Mapped[float] = mapped_column(nullable=False)
    status: Mapped[str] = mapped_column(nullable=False)
    station_id: Mapped[int] = mapped_column(nullable=True)

class User(Base):
    __tablename__ = 'users'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    email: Mapped[str] = mapped_column(nullable=False, unique=True)
    password: Mapped[str] = mapped_column(nullable=False)

class Rental(Base):
    __tablename__ = 'rentals'
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(nullable=False)
    bike_id: Mapped[int] = mapped_column(Integer, ForeignKey('bikes.id'), nullable=False)
    start_time: Mapped[str] = mapped_column(nullable=False)
    end_time: Mapped[str] = mapped_column(nullable=True)
    bike: Mapped["Bike"] = Relationship("Bike", back_populates="rentals")
