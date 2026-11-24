"""Command-line interface for the Hotel Reservation Management System."""

from pathlib import Path

from hotel import HotelService, HotelError
from models import ValidationError
from storage import StorageError


DATA_DIRECTORY = Path(__file__).parent / "data"


def print_line() -> None:
    print("-" * 72)


def show_rooms(service: HotelService) -> None:
    print("\nROOM DIRECTORY")
    print_line()
    print(f"{'Room No.':<12}{'Type':<16}{'Base/night':>15}{'Amenities/night':>20}")
    print_line()
    for room in service.list_rooms():
        print(
            f"{room.room_number:<12}{room.room_type:<16}"
            f"{room.price_per_night:>15.2f}{room.amenities_fee_per_night:>20.2f}"
        )
    print_line()
    print("Note: Charges are displayed in INR (₹).")


def search_rooms(service: HotelService) -> None:
    room_type = input("Room type (Standard / Deluxe / Suite): ")
    check_in = input("Check-in date (YYYY-MM-DD): ")
    check_out = input("Check-out date (YYYY-MM-DD): ")
    rooms = service.search_available_rooms(room_type, check_in, check_out)
    if not rooms:
        print("No rooms of that type are available for those dates.")
        return
    print("\nAvailable rooms:")
    for room in rooms:
        print(
            f"Room {room.room_number} | {room.room_type} | "
            f"Base rate: ₹{room.price_per_night:.2f}/night | "
            f"Amenities: ₹{room.amenities_fee_per_night:.2f}/night"
        )


def register_customer(service: HotelService) -> None:
    print("\nCUSTOMER REGISTRATION")
    name = input("Full name: ")
    phone = input("Phone number (digits only): ")
    email = input("Email (optional): ")
    customer = service.register_customer(name, phone, email)
    print(f"Customer registered. Customer ID: {customer.customer_id}")


def create_booking(service: HotelService) -> None:
    print("\nCREATE RESERVATION")
    customer_id = input("Customer ID: ")
    room_number = input("Room number: ")
    check_in = input("Check-in date (YYYY-MM-DD): ")
    check_out = input("Check-out date (YYYY-MM-DD): ")
    reservation = service.create_reservation(
        customer_id, room_number, check_in, check_out
    )
    room = service.get_room(reservation.room_number)
    print("\nRESERVATION CONFIRMED")
    print_line()
    print(f"Reservation ID : {reservation.reservation_id}")
    print(f"Customer ID    : {reservation.customer_id}")
    print(f"Room           : {room.room_number} ({room.room_type})")
    print(f"Stay           : {reservation.check_in} to {reservation.check_out}")
    print(f"Nights         : {reservation.nights}")
    print(f"Total charge   : ₹{reservation.total_charge:,.2f}")
    print_line()


def cancel_booking(service: HotelService) -> None:
    reservation_id = input("Reservation ID to cancel: ")
    reservation = service.cancel_reservation(reservation_id)
    print(f"Reservation {reservation.reservation_id} has been cancelled.")


def show_reservations(service: HotelService) -> None:
    reservations = service.list_reservations()
    if not reservations:
        print("No reservations have been recorded.")
        return
    print("\nRESERVATION RECORDS")
    print_line()
    for reservation in reservations:
        customer = service.get_customer(reservation.customer_id)
        room = service.get_room(reservation.room_number)
        print(f"ID: {reservation.reservation_id} | Status: {reservation.status}")
        print(f"Customer: {customer.full_name} ({customer.customer_id})")
        print(f"Room: {room.room_number} - {room.room_type}")
        print(
            f"Dates: {reservation.check_in} to {reservation.check_out} | "
            f"Nights: {reservation.nights} | "
            f"Total: ₹{reservation.total_charge:,.2f}"
        )
        print_line()


def search_customer(service: HotelService) -> None:
    query = input("Enter all or part of the customer's name: ")
    customers = service.search_customers(query)
    if not customers:
        print("No matching customers found.")
        return
    for customer in customers:
        print(
            f"{customer.customer_id} | {customer.full_name} | "
            f"{customer.phone} | {customer.email or 'No email'}"
        )


def main() -> None:
    try:
        service = HotelService(DATA_DIRECTORY)
    except (StorageError, ValidationError) as exc:
        print(f"Could not start the application: {exc}")
        return

    actions = {
        "1": ("View all rooms", lambda: show_rooms(service)),
        "2": ("Search available rooms", lambda: search_rooms(service)),
        "3": ("Register customer", lambda: register_customer(service)),
        "4": ("Create reservation", lambda: create_booking(service)),
        "5": ("Cancel reservation", lambda: cancel_booking(service)),
        "6": ("View reservations", lambda: show_reservations(service)),
        "7": ("Search customers", lambda: search_customer(service)),
    }

    while True:
        print("\n" + "=" * 72)
        print("             HOTEL RESERVATION MANAGEMENT SYSTEM")
        print("=" * 72)
        for key, (label, _) in actions.items():
            print(f"{key}. {label}")
        print("8. Exit")
        choice = input("Select an option (1-8): ").strip()

        if choice == "8":
            print("Thank you. Application closed.")
            break
        if choice not in actions:
            print("Invalid menu choice. Enter a number from 1 to 8.")
            continue

        try:
            actions[choice][1]()
        except (HotelError, ValidationError, StorageError) as exc:
            print(f"Error: {exc}")
        except (ValueError, TypeError) as exc:
            print(f"Invalid input: {exc}")
        except KeyboardInterrupt:
            print("\nOperation interrupted. Returning to the main menu.")


if __name__ == "__main__":
    main()
