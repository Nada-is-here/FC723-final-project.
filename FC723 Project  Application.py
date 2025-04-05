import random
import string

#create the map of the plane so the program can have a layout it can navigate.
import random
import string


class SeatMap:
    def __init__(self):
        self.rows = 80
        self.columns = ['A', 'B', 'C', 'D', 'E', 'F']
        # Initialize seat map with all seats set as free ('F')
        self.map = self.initialize_seat_map()

    def initialize_seat_map(self):
        """
        Initialize the seat map for all rows and columns.
        For rows 77-80 and columns D, E, F, mark them as storage ('S').
        All other seats are set to 'F' to indicate they are free.
        """
        seat_map = {}
        for row in range(1, self.rows + 1):
            seat_map[row] = {}
            for col in self.columns:
                if row >= 77 and col in ['D', 'E', 'F']:
                    seat_map[row][col] = 'S'  # Storage area (non-bookable)
                else:
                    seat_map[row][col] = 'F'  # Free seat
        return seat_map

    def is_valid_seat(self, seat):
        """
        Check if the provided seat identifier (e.g., '12B') is valid.
        A valid seat must have at least two characters (row and column),
        and the row must be a number within range and the column one of the valid columns.
        """
        if len(seat) < 2:
            return False
        row_part = seat[:-1]
        col_part = seat[-1].upper()
        if col_part not in self.columns or not row_part.isdigit():
            return False
        row = int(row_part)
        return 1 <= row <= self.rows and col_part in self.columns

    def check_availability(self, seat):
        """
        Return True if the seat is valid and free ('F').
        """
        if not self.is_valid_seat(seat):
            return False
        row = int(seat[:-1])
        col = seat[-1].upper()
        return self.map[row][col] == 'F'

    def book_seat(self, seat, booking_ref):
        """
        Book a seat by replacing the free indicator ('F') with the booking reference.
        Return a message indicating the outcome.
        """
        if not self.is_valid_seat(seat):
            return "Invalid seat."
        row = int(seat[:-1])
        col = seat[-1].upper()
        if self.map[row][col] == 'F':
            self.map[row][col] = booking_ref  # Store the booking reference in place of 'R'
            return f"Seat {seat} booked successfully."
        elif self.map[row][col] != 'F':
            return f"Seat {seat} is already booked or unavailable."

    def cancel_booking(self, seat):
        """
        Cancel a booking by setting the seat status back to free ('F').
        Return a message indicating the outcome.
        """
        if not self.is_valid_seat(seat):
            return "Invalid seat."
        row = int(seat[:-1])
        col = seat[-1].upper()
        # Only booked seats (with booking references) can be canceled
        if self.map[row][col] not in ['F', 'S']:
            self.map[row][col] = 'F'
            return f"Seat {seat} is now free."
        elif self.map[row][col] == 'F':
            return f"Seat {seat} is already free."
        else:
            return f"Seat {seat} is not a bookable seat."

    def show_seat_layout(self):
        """
        Display the full seat layout.
        For each seat, display the seat number and the current status.
        For example: [12A - F] indicates seat 12A is free;
        [12A - ABC12345] indicates seat 12A is booked with booking reference ABC12345.
        """
        print("\nFull Seat Layout:")
        for row in range(1, self.rows + 1):
            row_display = f"Row {row:02}: "
            for col in self.columns:
                seat_no = f"{row}{col}"
                status = self.map[row][col]
                row_display += f"[{seat_no} - {status}] "
            print(row_display)
        print()

    def recommend_seat(self):
        """
        Recommend the first available (free) seat by scanning row by row.
        Return the seat identifier (e.g., '12B') if available; otherwise, return None.
        """
        for row in range(1, self.rows + 1):
            for col in self.columns:
                if self.map[row][col] == 'F':
                    return f"{row}{col}"
        return None  # No free seat available


class BookingApp:
    def __init__(self):
        self.seat_map = SeatMap()
        # Simulated "database table" for customer details.
        # Keys: booking reference; Values: dictionary with customer details.
        self.booking_database = {}
        # Set to store used booking references to avoid duplicates.
        self.used_references = set()

    def generate_booking_reference(self):
        """
        Generate a unique 8-character alphanumeric booking reference.

        Implementation Logic:
        - Use random.choices to select 8 characters from uppercase letters and digits.
        - Check the generated reference against the 'used_references' set to ensure uniqueness.
        - Repeat the process until a unique reference is found.
        - Add the new reference to the set and return it.
        """
        while True:
            reference = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
            if reference not in self.used_references:
                self.used_references.add(reference)
                return reference

    def book_seat_with_customer_data(self, seat, passport, first_name, last_name):
        """
        Book a seat while capturing traveler details.
        - Generates a booking reference.
        - Calls SeatMap.book_seat to update the seat map with the booking reference.
        - Stores the customer details in the simulated booking database.
        Returns a message including the booking reference if successful.
        """
        if not self.seat_map.check_availability(seat):
            return f"Seat {seat} is not available or invalid."

        booking_ref = self.generate_booking_reference()
        result = self.seat_map.book_seat(seat, booking_ref)
        if "booked successfully" in result:
            # Store traveler details in the database
            row = seat[:-1]
            col = seat[-1].upper()
            self.booking_database[booking_ref] = {
                'passport': passport,
                'first_name': first_name,
                'last_name': last_name,
                'seat_row': row,
                'seat_column': col
            }
            return f"{result} Your booking reference is: {booking_ref}"
        return result

    def cancel_booking_with_data(self, seat):
        """
        Cancel a booking and remove the associated customer data from the database.
        - Finds the booking reference stored in the seat.
        - Cancels the booking in the seat map.
        - Removes the booking details from the booking database.
        """
        if not self.seat_map.is_valid_seat(seat):
            return "Invalid seat."
        row = int(seat[:-1])
        col = seat[-1].upper()
        booking_ref = self.seat_map.map[row][col]
        result = self.seat_map.cancel_booking(seat)
        if "now free" in result and booking_ref in self.booking_database:
            del self.booking_database[booking_ref]
            return f"{result} Booking reference {booking_ref} removed."
        return result

    def display_menu(self):
        print("\n--- Apache Airlines Booking Menu ---")
        print("1. Check availability of seat")
        print("2. Book a seat")
        print("3. Cancel a booking")
        print("4. Show full seat layout")
        print("5. Exit program")

    def run(self):
        while True:
            self.display_menu()
            choice = input("Enter your choice (1-5): ").strip()

            if choice == '1':
                seat = input("Enter seat (e.g., 12B): ").strip()
                if self.seat_map.check_availability(seat):
                    print(f"Seat {seat} is available.")
                else:
                    print(f"Seat {seat} is not available or invalid.")

            elif choice == '2':
                # Integrated recommend-seat option in booking process
                recommended_seat = self.seat_map.recommend_seat()
                if recommended_seat:
                    print(f"Recommended seat: {recommended_seat}")
                    book_choice = input(f"Would you like to book seat {recommended_seat}? (yes/no): ").strip().lower()
                    if book_choice == 'yes':
                        seat_to_book = recommended_seat
                    else:
                        seat_to_book = input("Enter your preferred seat to book (e.g., 12B): ").strip()
                else:
                    print("No available seats.")
                    continue

                # Get traveler details from the user
                passport = input("Enter your passport number: ").strip()
                first_name = input("Enter your first name: ").strip()
                last_name = input("Enter your last name: ").strip()

                result = self.book_seat_with_customer_data(seat_to_book, passport, first_name, last_name)
                print(result)

            elif choice == '3':
                seat = input("Enter seat to cancel (e.g., 12B): ").strip()
                result = self.cancel_booking_with_data(seat)
                print(result)

            elif choice == '4':
                self.seat_map.show_seat_layout()

            elif choice == '5':
                print("Exiting program. Goodbye!")
                break

            else:
                print("Invalid choice. Please try again.")


# Running the booking app
app = BookingApp()
app.run()

