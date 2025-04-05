class SeatMap:
    def __init__(self):
        # this function here is used to set the number of rows and seat layout
        self.rows = 80
        self.columns = ['A', 'B', 'C', 'X', 'D', 'E', 'F']
        self.map = self.initialize_seat_map()

    def initialize_seat_map(self):
        # this function creates the full seat layout with aisles and storage
        seat_map = {}
        for row in range(1, self.rows + 1):
            seat_map[row] = {}
            for col in self.columns:
                if col == 'X':
                    seat_map[row][col] = 'X'  # aisle
                elif row >= 77 and col in ['D', 'E', 'F']:
                    seat_map[row][col] = 'S'  # storage at the back
                else:
                    seat_map[row][col] = 'F'  # free
        return seat_map

    def is_valid_seat(self, seat):
        # this one checks if the seat is real and bookable
        if len(seat) < 2 or not seat[:-1].isdigit():
            return False
        row = int(seat[:-1])
        col = seat[-1].upper()
        return row in self.map and col in self.map[row]

    def check_availability(self, seat):
        # this one returns True if seat is free and valid
        if not self.is_valid_seat(seat):
            return False
        row = int(seat[:-1])
        col = seat[-1].upper()
        return self.map[row][col] == 'F'

    def book_seat(self, seat):
        # this one is used to reserve a seat if it's free
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
        # this one cancels a booking if it's already reserved

        # check if the seat is valid before doing anything
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
        # this one prints the full map of all seats and their current status
        print("\nBooking Status:")
        for row in range(1, self.rows + 1):
            row_display = f"Row {row:02}: "
            for col in self.columns:
                row_display += self.map[row][col] + " "
            print(row_display)
        print()


class BookingApp:
    def __init__(self):
        # this line here is used to make the seat map work by calling the class we made for it above
        self.seat_map = SeatMap()

        # this is a list to keep track of the seats this user books in the session
        self.user_bookings = []

    # this function here is just to show the menu options to the user
    def display_menu(self):
        print("\n--- Apache Airlines Booking Menu ---")
        print("1. Check availability of seat")
        print("2. Book a seat")
        print("3. Cancel a booking")  # changed wording here
        print("4. Show your booking status")
        print("5. Exit program")

    # this is the main function that keeps the app running until user wants to exit
    def run(self):
        while True:
            # call the menu so the user can pick what they want
            self.display_menu()
            # take the user's choice and remove spaces
            choice = input("Enter your choice (1-5): ").strip()

            # this one checks if a seat is available
            if choice == '1':
                seat = input("Enter seat (e.g., 12B): ").strip()
                if self.seat_map.check_availability(seat):
                    print(f"Seat {seat} is available.")
                else:
                    print(f"Seat {seat} is not available or invalid.")

            # this one lets the user book a seat
            elif choice == '2':
                seat = input("Enter seat to book: ").strip()
                result = self.seat_map.book_seat(seat)
                print(result)
                # if booking is successful, we add that seat to our list
                if "booked successfully" in result:
                    self.user_bookings.append(seat.upper())

            # this option is now for canceling a booking instead of freeing a seat
            elif choice == '3':
                seat = input("Enter seat to cancel: ").strip()
                result = self.seat_map.cancel_booking(seat)
                print(result)
                # if cancel works, remove from user booking list
                if "now free" in result and seat.upper() in self.user_bookings:
                    self.user_bookings.remove(seat.upper())

            # this one shows only the seats booked by the user during this session
            elif choice == '4':
                if self.user_bookings:
                    print("\nYour booked seats:")
                    for seat in self.user_bookings:
                        print(f" - {seat}")
                else:
                    print("You have not booked any seats.")

            # this one is to close the app
            elif choice == '5':
                print("Exiting program. Goodbye!")
                break

            # if they enter anything other than 1-5
            else:
                print("Invalid choice. Please try again.")

if __name__ == "__main__":
    app = BookingApp()
    app.run()