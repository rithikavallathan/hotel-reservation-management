"""Domain models for the Hotel Reservation Management System."""

from dataclasses import dataclass, asdict
from typing import Any, Dict, Type


class ValidationError(ValueError):
    """Raised when a model receives invalid user or record data."""


class Room:
    """Base room class. Subclasses override calculate_charge()."""

    room_type = "Room"

    def __init__(self, room_number: int, price_per_night: float,
                 amenities_fee_per_night: float = 0.0) -> None:
        if int(room_number) <= 0:
            raise ValidationError("Room number must be a positive integer.")
        if float(price_per_night) <= 0:
            raise ValidationError("Price per night must be greater than zero.")
        if float(amenities_fee_per_night) < 0:
            raise ValidationError("Amenities fee cannot be negative.")

        self.room_number = int(room_number)
        self.price_per_night = float(price_per_night)
        self.amenities_fee_per_night = float(amenities_fee_per_night)

    def calculate_charge(self, nights: int) -> float:
        """Default billing behaviour for a generic room."""
        if nights <= 0:
            raise ValidationError("Number of nights must be greater than zero.")
        return round(self.price_per_night * nights, 2)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "room_number": self.room_number,
            "room_type": self.room_type,
            "price_per_night": self.price_per_night,
            "amenities_fee_per_night": self.amenities_fee_per_night,
        }

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> "Room":
        room_classes: Dict[str, Type[Room]] = {
            "Standard": StandardRoom,
            "Deluxe": DeluxeRoom,
            "Suite": Suite,
        }
        room_type = str(data.get("room_type", "")).strip()
        room_class = room_classes.get(room_type)
        if room_class is None:
            raise ValidationError(f"Unknown room type in data file: {room_type!r}.")
        return room_class(
            room_number=int(data["room_number"]),
            price_per_night=float(data["price_per_night"]),
            amenities_fee_per_night=float(data.get("amenities_fee_per_night", 0.0)),
        )


class StandardRoom(Room):
    """Standard rooms charge only their listed nightly rate."""

    room_type = "Standard"

    def calculate_charge(self, nights: int) -> float:
        if nights <= 0:
            raise ValidationError("Number of nights must be greater than zero.")
        return round(self.price_per_night * nights, 2)


class DeluxeRoom(Room):
    """Deluxe rooms include an additional per-night amenities fee."""

    room_type = "Deluxe"

    def calculate_charge(self, nights: int) -> float:
        if nights <= 0:
            raise ValidationError("Number of nights must be greater than zero.")
        nightly_total = self.price_per_night + self.amenities_fee_per_night
        return round(nightly_total * nights, 2)


class Suite(Room):
    """Suites include a per-night premium amenities fee."""

    room_type = "Suite"

    def calculate_charge(self, nights: int) -> float:
        if nights <= 0:
            raise ValidationError("Number of nights must be greater than zero.")
        nightly_total = self.price_per_night + self.amenities_fee_per_night
        return round(nightly_total * nights, 2)


@dataclass
class Customer:
    customer_id: str
    full_name: str
    phone: str
    email: str = ""

    def to_dict(self) -> Dict[str, str]:
        return asdict(self)

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> "Customer":
        return Customer(
            customer_id=str(data["customer_id"]),
            full_name=str(data["full_name"]),
            phone=str(data["phone"]),
            email=str(data.get("email", "")),
        )


@dataclass
class Reservation:
    reservation_id: str
    customer_id: str
    room_number: int
    check_in: str
    check_out: str
    nights: int
    total_charge: float
    status: str = "CONFIRMED"

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> "Reservation":
        return Reservation(
            reservation_id=str(data["reservation_id"]),
            customer_id=str(data["customer_id"]),
            room_number=int(data["room_number"]),
            check_in=str(data["check_in"]),
            check_out=str(data["check_out"]),
            nights=int(data["nights"]),
            total_charge=float(data["total_charge"]),
            status=str(data.get("status", "CONFIRMED")),
        )
