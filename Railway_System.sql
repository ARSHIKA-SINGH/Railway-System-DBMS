CREATE DATABASE railwaydb;
USE railwaydb;

CREATE TABLE Passenger (
  passenger_id INT PRIMARY KEY,
  name VARCHAR(50),
  age INT,
  gender VARCHAR(10),
  phone VARCHAR(15)
);

CREATE TABLE Train (
  train_id INT PRIMARY KEY,
  train_name VARCHAR(50),
  train_type VARCHAR(20)
);

CREATE TABLE Station (
  station_id INT PRIMARY KEY,
  station_name VARCHAR(50),
  city VARCHAR(50)
);

CREATE TABLE Route (
  route_id INT PRIMARY KEY,
  train_id INT,
  station_id INT,
  arrival_time TIME,
  departure_time TIME,
  stop_number INT,
  FOREIGN KEY (train_id) REFERENCES Train(train_id),
  FOREIGN KEY (station_id) REFERENCES Station(station_id)
);

CREATE TABLE Booking (
  booking_id INT PRIMARY KEY,
  passenger_id INT,
  train_id INT,
  booking_date DATE,
  status VARCHAR(20),
  FOREIGN KEY (passenger_id) REFERENCES Passenger(passenger_id),
  FOREIGN KEY (train_id) REFERENCES Train(train_id)
);

CREATE TABLE Ticket (
  ticket_id INT PRIMARY KEY,
  booking_id INT,
  seat_number VARCHAR(10),
  coach_number VARCHAR(10),
  fare FLOAT,
  FOREIGN KEY (booking_id) REFERENCES Booking(booking_id)
);

INSERT INTO Passenger VALUES
(1, 'Rahul Sharma', 25, 'Male', '9876543210'),
(2, 'Priya Singh', 22, 'Female', '9123456780'),
(3, 'Amit Kumar', 30, 'Male', '9988776655'),
(4, 'Sneha Reddy', 27, 'Female', '9012345678');

INSERT INTO Train VALUES
(101, 'Rajdhani Express', 'AC'),
(102, 'Shatabdi Express', 'AC'),
(103, 'Passenger Train', 'Non-AC');

INSERT INTO Station VALUES
(201, 'New Delhi', 'Delhi'),
(202, 'Bhopal', 'Bhopal'),
(203, 'Mumbai CST', 'Mumbai'),
(204, 'Hyderabad', 'Hyderabad');

INSERT INTO Route VALUES
(1, 101, 201, '08:00:00', '08:10:00', 1),
(2, 101, 202, '12:00:00', '12:10:00', 2),
(3, 102, 203, '09:00:00', '09:15:00', 1),
(4, 103, 204, '10:00:00', '10:20:00', 1);

INSERT INTO Booking VALUES
(301, 1, 101, '2026-04-01', 'Booked'),
(302, 2, 102, '2026-04-02', 'Booked'),
(303, 3, 101, '2026-04-03', 'Cancelled'),
(304, 4, 103, '2026-04-04', 'Booked');

INSERT INTO Ticket VALUES
(401, 301, 'A1-23', 'A1', 1500),
(402, 302, 'B2-10', 'B2', 1200),
(403, 303, 'C1-05', 'C1', 800),
(404, 304, 'D1-01', 'D1', 500);

-- Check Passenger Table
SELECT * FROM Passenger;

-- Check Train Table
SELECT * FROM Train;

-- Check Station Table
SELECT * FROM Station;

-- Check Route Table
SELECT * FROM Route;

-- Check Booking Table
SELECT * FROM Booking;

-- Check Ticket Table
SELECT * FROM Ticket;

-- 1. Display all passenger details
SELECT * FROM Passenger;

-- 2. Display passenger name and booking status (JOIN)
SELECT p.name, b.status
FROM Passenger p
JOIN Booking b ON p.passenger_id = b.passenger_id;

-- 3. Display passenger name and train name (JOIN)
SELECT p.name, t.train_name
FROM Passenger p
JOIN Booking b ON p.passenger_id = b.passenger_id
JOIN Train t ON b.train_id = t.train_id;

-- 4. Display ticket details with passenger name (JOIN)
SELECT p.name, tk.seat_number, tk.fare
FROM Passenger p
JOIN Booking b ON p.passenger_id = b.passenger_id
JOIN Ticket tk ON b.booking_id = tk.booking_id;

-- 5. Count total number of bookings (AGGREGATE)
SELECT COUNT(*) AS total_bookings FROM Booking;

-- 6. Calculate average ticket fare (AGGREGATE)
SELECT AVG(fare) AS average_fare FROM Ticket;

-- 7. Find maximum ticket fare (AGGREGATE)
SELECT MAX(fare) AS highest_fare FROM Ticket;

-- 8. Find total fare collected (AGGREGATE)
SELECT SUM(fare) AS total_fare FROM Ticket;

-- 9. Display passengers who booked Rajdhani Express (SUBQUERY)
SELECT name FROM Passenger
WHERE passenger_id IN (
    SELECT passenger_id FROM Booking
    WHERE train_id = (
        SELECT train_id FROM Train
        WHERE train_name = 'Rajdhani Express'
    )
);

-- 10. Display train-wise number of bookings (GROUP BY)
SELECT train_id, COUNT(*) AS total_bookings
FROM Booking
GROUP BY train_id;

-- View 1: Booking Details
CREATE VIEW Booking_Details AS
SELECT p.name, t.train_name, b.booking_date, b.status
FROM Passenger p
JOIN Booking b ON p.passenger_id = b.passenger_id
JOIN Train t ON b.train_id = t.train_id;

-- View 2: Ticket Information
CREATE VIEW Ticket_Info AS
SELECT b.booking_id, t.train_name, tk.seat_number, tk.coach_number, tk.fare
FROM Booking b
JOIN Train t ON b.train_id = t.train_id
JOIN Ticket tk ON b.booking_id = tk.booking_id;

-- View 3: Route Details
CREATE VIEW Route_Details AS
SELECT tr.train_name, s.station_name, r.arrival_time, r.departure_time
FROM Route r
JOIN Train tr ON r.train_id = tr.train_id
JOIN Station s ON r.station_id = s.station_id;

SELECT * FROM Booking_Details;
SELECT * FROM Ticket_Info;
SELECT * FROM Route_Details;