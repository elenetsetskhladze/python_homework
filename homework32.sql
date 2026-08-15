DROP TABLE IF EXISTS cars;

CREATE TABLE cars (
	car_id SERIAL PRIMARY KEY,
	car_brand VARCHAR(50) NOT NULL,
	car_model VARCHAR(50) NOT NULL,
	release_year INT NOT NULL,
	vin_code VARCHAR(17) UNIQUE,
	created_at DATE DEFAULT CURRENT_DATE,
	engine_volume NUMERIC CHECK (engine_volume > 0.5),
	mileage INT,
	customs_cleared BOOLEAN DEFAULT TRUE,
	price DECIMAL(10, 2),
	bio TEXT,
	sold_out BOOLEAN
);

INSERT INTO cars (car_brand, car_model, release_year) VALUES 
	 ('Toyota', 'Supra', 1978),
	 ('BMW', '3 series', 1975),
	 ('Mercedes-Benz', 'C-class', 1993),
	 ('Audi', 'A4', 1994),
	 ('Ford', 'Mustang', 1964),
	 ('Honda', 'Civic', 1972),
	 ('Volkswagen', 'Golf', 1974),
	 ('Porsche', '991', 1964),
	 ('Chevrolet', 'Camaro', 1966),
	 ('Nissan', ' GT-R', 2007);

SELECT * FROM cars;
SELECT car_brand, car_model, release_year, price FROM cars;
SELECT * FROM cars WHERE car_brand = 'Mercedes-Benz'




	