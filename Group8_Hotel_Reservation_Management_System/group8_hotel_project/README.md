# Group 8 - Hotel Reservation Management System

A menu-driven Python application that manages hotel rooms, customers, reservations and billing. It is designed around the Group 8 requirements in the course project brief.

## Requirements covered

- Maintain room information and availability.
- Register customer details.
- Search available rooms by room type and dates.
- Create and cancel reservations.
- Calculate room charges.
- Persist room, customer and reservation information in JSON files.
- Handle invalid room numbers, unavailable rooms, invalid dates/input and file errors.
- Implement `Room`, `StandardRoom`, `DeluxeRoom` and `Suite` classes with inheritance and polymorphism.

## Run the application

Use Python 3.10 or later. No third-party packages are required.

From this folder, run:

```bash
python main.py
```

The application creates a `data/` directory and sample room records on first launch. Customer and reservation files are created when records are saved.

## Run the tests

```bash
python -m unittest discover -s tests -v
```

## Data files

- `data/rooms.json` - room number, room type and nightly rates.
- `data/customers.json` - registered customer details.
- `data/reservations.json` - booking dates, room, customer, status and saved charge.

The sample rooms and rates are demonstration data. They can be changed in `data/rooms.json` after the first run.

## Mapping to course outcomes

### CO3 - Room/customer/reservation data structures and string searching

- `HotelService.rooms`, `customers` and `reservations` use dictionaries for fast lookup by ID/room number.
- `list_rooms()` returns a list of Room objects.
- `search_available_rooms()` uses case-insensitive substring matching on room type.
- `search_customers()` uses case-insensitive substring matching on customer names.

### CO4 - Reservation files and exception handling

- `JsonStorage` reads and writes JSON data files.
- JSON decoding errors and operating-system file errors are converted into `StorageError`.
- `HotelService` raises specific exceptions for unavailable rooms, missing customers, missing rooms and missing reservations.
- The menu catches and displays expected errors instead of crashing for normal invalid input.

### CO5 - Room hierarchy, inheritance and polymorphism

- `Room` is the parent class.
- `StandardRoom`, `DeluxeRoom` and `Suite` inherit from `Room`.
- Each subclass overrides `calculate_charge()`.
- `create_reservation()` calls `room.calculate_charge(nights)` without needing to know the specific subclass. Python selects the correct method at runtime (polymorphism).

## Important design decisions to explain in the walkthrough

1. A room is available for a date range only when no confirmed reservation overlaps that range.
2. Check-out is treated as exclusive. A guest can check out on the same date that the next guest checks in.
3. Standard rooms charge the base nightly rate. Deluxe and Suite rooms also add the amenities fee stored in `rooms.json`. These rates/fees are sample assumptions, not figures specified by the assignment brief.
4. The reservation stores the final calculated charge so a later edit to the room's rate does not change an existing booking.
5. JSON files are used for simple local persistence; this is an educational demonstration, not a production hotel booking system.

## Suggested walkthrough order

1. Show the menu and list the room directory.
2. Search for Deluxe rooms for a valid future date range.
3. Register a customer and explain the customer dictionary and JSON file.
4. Create a reservation and explain the date-overlap check.
5. Create a second overlapping reservation for the same room and show the unavailable-room error.
6. Show the bill and explain the overridden `calculate_charge()` methods.
7. Cancel the first reservation and show that the room becomes available again.
8. Open the JSON files and explain persistence.
9. Run the unit tests and explain what each test verifies.

## Limitations

This is a local command-line college project. It does not include user login, online payments, a web interface, or concurrent multi-user booking. Do not enter real customer personal information during demonstrations.
