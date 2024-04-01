-- in the ER diagram do I have to add text to each link?
-- can I have foreign keys in the ER diagram
-- sql parameterized query

-- CREATE TABLES --

CREATE TABLE Aircraft (
    Aircraft_Registration_Number VARCHAR(25) PRIMARY KEY,
    Seat_Capacity INT,
    Manufacturer VARCHAR(25) NOT NULL,
    Status ENUM('Active', 'Maintenance', 'Retired') NOT NULL
);

CREATE TABLE Flight (
    Flight_Number VARCHAR (25) PRIMARY KEY,
    Aircraft_Registration_Number VARCHAR(25) FOREIGN KEY REFERENCES Aircraft(Aircraft_Registration_Number) NOT NULL,
    Departure_Airport_Code VARCHAR(25) SECONDARY KEY NOT NULL,
    Arrival_Airport_Code VARCHAR(25) NOT NULL,
    Departure_Date_Time DATETIME,
    Arrival_Date_Time DATETIME,
    Passenger_Count INT,
    Flight_Duration INT,
);

CREATE TABLE Pilot (
    Commercial_Pilot_License_Number VARCHAR(25) PRIMARY KEY,
    First_Name VARCHAR(25) NOT NULL,
    Last_Name VARCHAR(25) NOT NULL,
    License_Number VARCHAR(25) SECONDARY KEY NOT NULL,
    Contact_Number VARCHAR(25) NOT NULL,
    Pilot_Ranking ENUM('First officer', 'Captain') NOT NULL
);

CREATE TABLE Destination (
    Airport_Destination_Code INT PRIMARY KEY,
    Location VARCHAR(25) NOT NULL,
    Country VARCHAR(25) NOT NULL
);

CREATE TABLE Pilot_Flight (
    Pilot_Flight_ID INT PRIMARY KEY,
    Commercial_Pilot_License_Number VARCHAR(25) FOREIGN KEY REFERENCES Pilot(Commercial_Pilot_License_Number),
    Flight_Number VARCHAR (25) FOREIGN KEY REFERENCES Flight(Flight_Number),
    Pilot_Ranking ENUM('Pilot Cadet', 'Second officer', 'First officer', 'Captain') NOT NULL,
);

CREATE TABLE Aircraft_Destination (
    Aircraft_Destination_ID INT PRIMARY KEY,
    Aircraft_Registration_Number VARCHAR(25) FOREIGN KEY REFERENCES Aircraft(Aircraft_Registration_Number),
    Airport_Destination_Code INT FOREIGN KEY REFERENCES Destination(Airport_Destination_Code),
);

CREATE TABLE Aircraft_Flight (
    Aircraft_Flight_ID INT PRIMARY KEY,
    Aircraft_Registration_Number VARCHAR(25) FOREIGN KEY REFERENCES Aircraft(Aircraft_Registration_Number),
    Flight_Number VARCHAR (25) FOREIGN KEY REFERENCES Flight(Flight_Number),
);

-- DATA INSERTION --

INSERT INTO Aircraft (Aircraft_Registration_Number, Seat_Capacity, Manufacturer, Status)
VALUES
  ('EI-DCJ', 150, 'Boeing', 'Active'),
  ('F-WWBY', 200, 'Airbus', 'Active'),
  ('EI-HGA', 100, 'Ryanair', 'Active'),
  ('EI-DAJ', 180, 'Boeing', 'Maintenance'),
  ('F-WWAY', 250, 'Airbus', 'Retired');

INSERT INTO Flight (Flight_Number, Aircraft_Registration_Number, Departure_Airport_Code, Arrival_Airport_Code, Departure_Date_Time, Arrival_Date_Time, Passenger_Count, Flight_Duration)
VALUES
  ('B777', 'EI-DCJ', 'STD', 'EDI', '2023-10-30 08:00:00', '2023-10-30 09:30:00', 122, 1.5),
  ('F56', 'F-WWBY', 'BRI', 'MXP', '2023-11-01 14:30:00', '2023-11-01 16:30:00', 171, 2),
  ('FR2233', 'EI-HGA', 'MAD', 'BUD', '2023-11-05 10:45:00', '2023-11-05 16:45:00', 80, 3.5),
  ('B677', 'EI-DAJ', 'LIS', 'PRA', '2023-11-10 12:30:00', '2023-11-10 18:30:00', 169, 3),
  ('112', 'F-WWAY', 'BER', 'FCO', '2023-11-15 09:15:00', '2023-11-15 11:15:00', 201, 2);

INSERT INTO Pilot (Commercial_Pilot_License_Number, First_Name, Last_Name, License_Number, Contact_Number, Pilot_Ranking)
VALUES
  ('CPL001', 'John', 'Wayne', 'L12345', '123-456-7890', 'Captain'),
  ('CPL002', 'Robin', 'Gray', 'L67890', '987-654-3210', 'First officer'),
  ('CPL003', 'Felix', 'Arthur', 'L54321', '456-789-0123', 'Captain'),
  ('CPL004', 'James', 'Williams', 'L99999', '111-222-3333', 'First officer'),
  ('CPL005', 'Ben', 'Simpson', 'L11111', '444-333-2222', 'Captain'),
  ('CPL006', 'Larry', 'Wilks', 'L12345', '123-456-7890', 'First officer'),
  ('CPL007', 'Marc', 'Stewart', 'L67890', '987-654-3210', 'Captain'),
  ('CPL008', 'Shaun', 'Proctor', 'L54321', '456-789-0123', 'First officer'),
  ('CPL009', 'Ben', 'Aaron', 'L99999', '111-222-3333', 'Captain'),
  ('CPL010', 'Marc', 'Leith', 'L11111', '444-333-2222', 'First officer');

INSERT INTO Destination (Airport_Destination_Code, Location, Country)
VALUES
  (1, 'Edinburgh', 'UK'),
  (2, 'Milan', 'Italy'),
  (3, 'Budapest', 'Hungary'),
  (4, 'Prague', 'Czech Republic'),
  (10, 'Rome', 'Italy');

INSERT INTO Pilot_Flight (Pilot_Flight_ID, Commercial_Pilot_License_Number, Flight_Number, Pilot_Ranking)
VALUES
  (1, 'CPL001', 'B777', 'Captain'),
  (2, 'CPL002', 'B777', 'First officer'),
  (3, 'CPL003', 'F56', 'Captain'),
  (4, 'CPL004', 'F56', 'First officer'),
  (5, 'CPL005', 'FR2233', 'Captain'),
  (6, 'CPL006', 'FR2233', 'First officer'),
  (7, 'CPL007', 'B677', 'Captain'),
  (8, 'CPL008', 'B677', 'First officer'),
  (9, 'CPL09', '112', 'Captain'),
  (10, 'CPL010', '112', 'First officer');
-- NOTE STILL TO DO:
INSERT INTO Aircraft_Destination (Aircraft_Destination_ID, Aircraft_Registration_Number, Airport_Destination_Code)
VALUES
  (1, 'ABC123', 1),
  (2, 'DEF456', 2),
  (3, 'GHI789', 3),
  (4, 'JKL012', 4),
  (10, 'BCD890', 10);

INSERT INTO Aircraft_Flight (Aircraft_Flight_ID, Aircraft_Registration_Number, Flight_Number)
VALUES
  (1, 'ABC123', 'F123'),
  (2, 'DEF456', 'F456'),
  (3, 'GHI789', 'F789'),
  (4, 'JKL012', 'F101'),
  (10, 'BCD890', 'F178');