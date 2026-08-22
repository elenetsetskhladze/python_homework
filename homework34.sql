CREATE TABLE hotels(
	hotel_id SERIAL PRIMARY KEY,
	hotel_name VARCHAR(50) NOT NULL,
	country VARCHAR(50),
	star_numbers INT CHECK (star_numbers BETWEEN 1 AND 5)
);

CREATE TABLE rooms(
	room_id SERIAL PRIMARY KEY,
	hotel_id INT REFERENCES hotels(hotel_id) ON DELETE CASCADE,
	room_number INT NOT NULL,
	floor_number INT NOT NULL,
	one_night_price DECIMAL 
);


CREATE TABLE guests(
	guest_id SERIAL PRIMARY KEY,
	room_id INT REFERENCES rooms(room_id) ON DELETE CASCADE,
	guest_name VARCHAR(50) NOT NULL,
	guest_lname VARCHAR(50) NOT NULL,
	phone_number VARCHAR(20)
);


CREATE TABLE services(
	service_id SERIAL PRIMARY KEY,
	room_id INT REFERENCES rooms(room_id) ON DELETE CASCADE,
	price DECIMAL 
);


INSERT INTO hotels (hotel_name, country, star_numbers) VALUES
	('hotel_', 'Georgia', 5), 
	('hotel_2', 'France', 4);


INSERT INTO rooms(hotel_id, room_number, floor_number) VALUES 
	(1, 301, 5), 
	(1, 302, 5), 
	(1, 303, 5), 
	(2, 401, 6), 
	(2, 402, 6), 
	(2, 403, 6);


INSERT INTO guests(room_id, guest_name, guest_lname) VALUES 
	(1, 'g_name1', 'g_lname1'),
	(1, 'g_name2', 'g_lname2'), 
	(4, 'g_name1', 'g_lname2'), 
	(4, 'g_name2', 'g_lname2');

INSERT INTO services(room_id) VALUES 
	(1),
	(1),
	(4),
	(4);


SELECT rooms.room_number, hotels.hotel_name FROM rooms
JOIN hotels ON rooms.hotel_id = hotels.hotel_id;

SELECT guests.guest_id, rooms.room_number, hotels.hotel_name FROM guests
JOIN rooms ON guests.room_id = rooms.room_id
JOIN hotels ON rooms.hotel_id = hotels.hotel_id;

DELETE FROM rooms WHERE room_id = 2;

UPDATE rooms SET one_night_price = 150 WHERE room_id = 3;

UPDATE guests SET room_id = 5 WHERE guest_id = 1;