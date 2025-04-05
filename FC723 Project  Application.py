class SeatMap:
    def __init__(self):
        self.rows = 80
        self.columns = ['A', 'B', 'C', 'D', 'E', 'F']
        self.map = self.initialize_seat_map()

    def initialize_seat_map(self):
        seat_map = {}
        for row in range(1, self.rows + 1):
            seat_map[row] = {}
            for col in self.columns:
                if col == 'X':
                    seat_map[row][col] = 'X'  # aisle
                elif row >= 77 and col in ['D', 'E', 'F']:
                    seat_map[row][col] = 'S'  # storage at the back
                else:
                    seat_map[row][col] = f"{row}{col}"  # show seat number as row and column
        return seat_map

    def is_valid_seat(self, seat):
        if len(seat) < 2:
            return False
        row = seat[:-1]
        col = seat[-1].upper()
        if col not in self.columns or not row.isdigit():
            return False
        row = int(row)
        return 1 <= row <= self.rows and col != 'X'

    def check_availability(self, seat):
        if not self.is_valid_seat(seat):
            return False
        row = int(seat[:-1])
        col = seat[-1].upper()
        return self.map[row][col] == 'F'

    def book_seat(self, seat):
        if not self.is_valid_seat(seat):
            return "Invalid seat."
        row = int(seat[:-1])
        col = seat[-1].upper()
        if self.map[row][col] == 'F':
            self.map[row][col] = 'R'
            return f"Seat {seat} booked successfully."
        elif self.map[row][col] == 'R':
            return f"Seat {seat} is already booked."
        else:
            return f"Seat {seat} cannot be booked (unavailable area)."

    def cancel_booking(self, seat):
        if not self.is_valid_seat(seat):
            return "Invalid seat."
        row = int(seat[:-1])
        col = seat[-1].upper()
        if self.map[row][col] == 'R':
            self.map[row][col] = 'F'
            return f"Seat {seat} is now free."
        elif self.map[row][col] == 'F':
            return f"Seat {seat} is already free."
        else:
            return f"Seat {seat} is not a bookable seat."

    def show_booking_status(self):
        print("\nBooking Status:")
        for row in range(1, self.rows + 1):
            row_display = f"Row {row:02}: "
            for col in self.columns:
                row_display += self.map[row][col] + " "
            print(row_display)
        print()

    def show_seat_layout(self):
        print("\nFull Seat Layout:")
        for row in range(1, self.rows + 1):
            row_display = f"Row {row:02}: "
            for col in self.columns:
                # Display seat number instead of F or R
                row_display += f"[{self.map[row][col]}] "
            print(row_display)
        print()

    def recommend_seat(self):
        for row in range(1, self.rows + 1):
            for col in self.columns:
                if self.map[row][col] == 'F':  # Check if the seat is free
                    return f"{row}{col}"  # Recommend the first free seat
        return None  # If no seat is free

class BookingApp:
    def __init__(self):
        self.seat_map = SeatMap()
        self.user_bookings = []

    def display_menu(self):
        print("\n--- Apache Airlines Booking Menu ---")
        print("1. Check availability of seat")
        print("2. Book a seat")
        print("3. Cancel a booking")
        print("4. Show your booking status")
        print("5. Show all seats layout")
        print("6. Exit program")

    def run(self):
        while True:
            self.display_menu()
            choice = input("Enter your choice (1-6): ").strip()

            if choice == '1':
                seat = input("Enter seat (e.g., 12B): ").strip()
                if self.seat_map.check_availability(seat):
                    print(f"Seat {seat} is available.")
                else:
                    print(f"Seat {seat} is not available or invalid.")

            elif choice == '2':
                # Recommend a seat first
                recommended_seat = self.seat_map.recommend_seat()
                if recommended_seat:
                    print(f"Recommended seat: {recommended_seat}")
                    book_choice = input(f"Would you like to book seat {recommended_seat}? (yes/no): ").strip().lower()
                    if book_choice == 'yes':
                        result = self.seat_map.book_seat(recommended_seat)
                        print(result)
                        if "booked successfully" in result:
                            self.user_bookings.append(recommended_seat.upper())
                    else:
                        seat = input("Enter your preferred seat to book (e.g., 12B): ").strip()
                        result = self.seat_map.book_seat(seat)
                        print(result)
                        if "booked successfully" in result:
                            self.user_bookings.append(seat.upper())
                else:
                    print("No available seats.")

            elif choice == '3':
                seat = input("Enter seat to cancel: ").strip()
                result = self.seat_map.cancel_booking(seat)
                print(result)
                if "now free" in result and seat.upper() in self.user_bookings:
                    self.user_bookings.remove(seat.upper())

            elif choice == '4':
                if self.user_bookings:
                    print("\nYour booked seats:")
                    for seat in self.user_bookings:
                        print(f" - {seat}")
                else:
                    print("You have not booked any seats.")

            elif choice == '5':
                self.seat_map.show_seat_layout()

            elif choice == '6':
                print("Exiting program. Goodbye!")
                break

            else:
                print("Invalid choice. Please try again.")

# Running the booking app
app = BookingApp()
app.run()
