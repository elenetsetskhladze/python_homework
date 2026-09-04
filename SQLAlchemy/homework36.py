from datetime import date, timedelta

from sqlalchemy import create_engine, ForeignKey, String, Integer, Float, Date, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship, Session


engine = create_engine("sqlite:///hotel.db")


class Base(DeclarativeBase):
    pass


class Hotel(Base):
    __tablename__ = "hotels"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    country: Mapped[str] = mapped_column(String(50))
    city: Mapped[str] = mapped_column(String(50))
    stars: Mapped[int] = mapped_column(Integer)

    rooms: Mapped[list["Room"]] = relationship(back_populates="hotel")


class Room(Base):
    __tablename__ = "rooms"

    id: Mapped[int] = mapped_column(primary_key=True)
    room_number: Mapped[int] = mapped_column(Integer)
    floor: Mapped[int] = mapped_column(Integer)
    price_per_night: Mapped[float] = mapped_column(Float)
    hotel_id: Mapped[int] = mapped_column(ForeignKey("hotels.id"))

    hotel: Mapped["Hotel"] = relationship(back_populates="rooms")
    bookings: Mapped[list["Booking"]] = relationship(back_populates="room")


class Guest(Base):
    __tablename__ = "guests"

    id: Mapped[int] = mapped_column(primary_key=True)
    first_name: Mapped[str] = mapped_column(String(50))
    last_name: Mapped[str] = mapped_column(String(50))
    email: Mapped[str] = mapped_column(String(100))
    phone: Mapped[str] = mapped_column(String(30))

    bookings: Mapped[list["Booking"]] = relationship(back_populates="guest")


class Booking(Base):
    __tablename__ = "bookings"

    id: Mapped[int] = mapped_column(primary_key=True)
    guest_id: Mapped[int] = mapped_column(ForeignKey("guests.id"))
    room_id: Mapped[int] = mapped_column(ForeignKey("rooms.id"))
    check_in: Mapped[date] = mapped_column(Date)
    check_out: Mapped[date] = mapped_column(Date)

    guest: Mapped["Guest"] = relationship(back_populates="bookings")
    room: Mapped["Room"] = relationship(back_populates="bookings")


Base.metadata.create_all(engine)

session = Session(engine)


def add_hotel(name, country, city, stars):
    hotel = Hotel(
        name=name,
        country=country,
        city=city,
        stars=stars
    )

    session.add(hotel)
    session.commit()

    print("Hotel created successfully.")
    return hotel


def add_room(room_number, floor, price, hotel_id):
    hotel = session.get(Hotel, hotel_id)

    if not hotel:
        print("Hotel not found.")
        return None

    room = Room(
        room_number=room_number,
        floor=floor,
        price_per_night=price,
        hotel=hotel
    )

    session.add(room)
    session.commit()

    print("Room created successfully.")
    return room


def add_guest(first_name, last_name, email, phone):
    guest = Guest(
        first_name=first_name,
        last_name=last_name,
        email=email,
        phone=phone
    )

    session.add(guest)
    session.commit()

    print("Guest created successfully.")
    return guest


def add_booking(guest_id, room_id, check_in, check_out):
    guest = session.get(Guest, guest_id)
    room = session.get(Room, room_id)

    if not guest or not room:
        print("Guest or room not found.")
        return None

    booking = Booking(
        guest=guest,
        room=room,
        check_in=check_in,
        check_out=check_out
    )

    session.add(booking)
    session.commit()

    print("Booking created successfully.")
    return booking


def get_all_hotels():
    hotels = session.query(Hotel).all()

    for hotel in hotels:
        print(
            hotel.id,
            hotel.name,
            hotel.city,
            hotel.stars
        )

    return hotels


def get_hotel_by_id(hotel_id):
    hotel = session.get(Hotel, hotel_id)

    if hotel:
        print(
            hotel.name,
            hotel.city,
            hotel.stars
        )
    else:
        print("Hotel not found.")

    return hotel


def get_all_rooms():
    rooms = session.query(Room).all()

    for room in rooms:
        print(
            room.id,
            room.room_number,
            room.floor,
            room.price_per_night
        )

    return rooms


def get_guest_by_email(email):
    guest = session.query(Guest).filter(
        Guest.email == email
    ).first()

    if guest:
        print(
            guest.first_name,
            guest.last_name,
            guest.email
        )
    else:
        print("Guest not found.")

    return guest


def update_room_price(room_id, new_price):
    room = session.get(Room, room_id)

    if room:
        room.price_per_night = new_price
        session.commit()

        print("Room price updated successfully.")
    else:
        print("Room not found.")


def delete_guest(guest_id):
    guest = session.get(Guest, guest_id)

    if guest:
        session.delete(guest)
        session.commit()

        print("Guest deleted successfully.")
    else:
        print("Guest not found.")


def delete_room(room_id):
    room = session.get(Room, room_id)

    if room:
        session.delete(room)
        session.commit()

        print("Room deleted successfully.")
    else:
        print("Room not found.")


hotel1 = add_hotel(
    "Grand Hotel",
    "Georgia",
    "Tbilisi",
    5
)

hotel2 = add_hotel(
    "Tbilisi Palace",
    "Georgia",
    "Tbilisi",
    4
)

hotel3 = add_hotel(
    "Batumi Hotel",
    "Georgia",
    "Batumi",
    5
)


room1 = add_room(101, 1, 80, hotel1.id)
room2 = add_room(102, 1, 120, hotel1.id)
room3 = add_room(201, 2, 150, hotel1.id)

room4 = add_room(101, 1, 90, hotel2.id)
room5 = add_room(102, 1, 110, hotel2.id)
room6 = add_room(201, 2, 200, hotel2.id)

room7 = add_room(301, 3, 250, hotel3.id)
room8 = add_room(302, 3, 180, hotel3.id)
room9 = add_room(303, 3, 95, hotel3.id)


guest1 = add_guest(
    "Nika",
    "Beridze",
    "nika@gmail.com",
    "555111111"
)

guest2 = add_guest(
    "Ana",
    "Kiknadze",
    "ana@gmail.com",
    "555222222"
)

guest3 = add_guest(
    "Giorgi",
    "Maisuradze",
    "giorgi@gmail.com",
    "555333333"
)

guest4 = add_guest(
    "Mariam",
    "Lomidze",
    "mariam@gmail.com",
    "555444444"
)

guest5 = add_guest(
    "Luka",
    "Gelashvili",
    "luka@gmail.com",
    "555555555"
)


today = date.today()

add_booking(
    guest1.id,
    room1.id,
    today - timedelta(days=2),
    today + timedelta(days=3)
)

add_booking(
    guest1.id,
    room2.id,
    today + timedelta(days=10),
    today + timedelta(days=15)
)

add_booking(
    guest2.id,
    room3.id,
    today + timedelta(days=5),
    today + timedelta(days=8)
)

add_booking(
    guest2.id,
    room4.id,
    today + timedelta(days=20),
    today + timedelta(days=25)
)

add_booking(
    guest3.id,
    room5.id,
    today - timedelta(days=5),
    today + timedelta(days=2)
)

add_booking(
    guest4.id,
    room6.id,
    today + timedelta(days=30),
    today + timedelta(days=35)
)

add_booking(
    guest5.id,
    room7.id,
    today + timedelta(days=15),
    today + timedelta(days=20)
)


print("\n--- QUERY 1 ---")

five_star_hotels = session.query(Hotel).filter(
    Hotel.stars == 5
).all()

for hotel in five_star_hotels:
    print(hotel.name)


print("\n--- QUERY 2 ---")

tbilisi_hotels = session.query(Hotel).filter(
    Hotel.city == "Tbilisi"
).all()

for hotel in tbilisi_hotels:
    print(hotel.name)


print("\n--- QUERY 3 ---")

cheap_rooms = session.query(Room).filter(
    Room.price_per_night < 100
).all()

for room in cheap_rooms:
    print(
        room.room_number,
        room.price_per_night
    )


print("\n--- QUERY 4 ---")

hotel = session.get(Hotel, hotel1.id)

for room in hotel.rooms:
    print(
        room.room_number,
        room.price_per_night
    )


print("\n--- QUERY 5 ---")

guest = session.get(Guest, guest1.id)

for booking in guest.bookings:
    print(
        booking.id,
        booking.check_in,
        booking.check_out
    )


print("\n--- QUERY 6 ---")

future_bookings = session.query(Booking).filter(
    Booking.check_out < today
).all()

for booking in future_bookings:
    print(
        booking.id,
        booking.check_out
    )


print("\n--- QUERY 7 ---")

most_expensive_room = session.query(Room).order_by(
    Room.price_per_night.desc()
).first()

print(
    most_expensive_room.room_number,
    most_expensive_room.price_per_night
)


print("\n--- QUERY 8 ---")

room_counts = session.query(
    Hotel.name,
    func.count(Room.id)
).join(
    Room
).group_by(
    Hotel.id
).all()

for hotel_name, room_count in room_counts:
    print(
        hotel_name,
        room_count,
        "rooms"
    )


print("\n--- QUERY 9 ---")

hotels_with_three_rooms = session.query(
    Hotel.name,
    func.count(Room.id)
).join(
    Room
).group_by(
    Hotel.id
).having(
    func.count(Room.id) >= 3
).all()

for hotel_name, room_count in hotels_with_three_rooms:
    print(
        hotel_name,
        room_count,
        "rooms"
    )


print("\n--- QUERY 10 ---")

guests_with_multiple_bookings = session.query(
    Guest.first_name,
    Guest.last_name,
    func.count(Booking.id)
).join(
    Booking
).group_by(
    Guest.id
).having(
    func.count(Booking.id) > 1
).all()

for first_name, last_name, booking_count in guests_with_multiple_bookings:
    print(
        first_name,
        last_name,
        booking_count,
        "bookings"
    )


print("\n--- RELATIONSHIPS ---")

for room in hotel1.rooms:
    print(room.room_number)

for booking in guest1.bookings:
    print(booking.id)

booking = session.query(Booking).first()

print(
    booking.guest.first_name,
    booking.guest.last_name
)

print(
    booking.room.room_number,
    booking.room.price_per_night
)


session.close()