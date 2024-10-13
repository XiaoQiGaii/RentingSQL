DROP DATABASE IF EXISTS RentSys;
CREATE DATABASE RentSys;
USE RentSys;

-- Table for Reservations
CREATE TABLE Reservations (
    id INT AUTO_INCREMENT PRIMARY KEY,
    RName VARCHAR(100) NOT NULL,
    Cartype VARCHAR(50) NOT NULL,
    StartDate DATETIME NOT NULL,
    EndDate DATETIME NOT NULL,
    Price DECIMAL(10, 2) NOT NULL,
    Extend BOOLEAN DEFAULT FALSE
);

-- Table for Pricing
CREATE TABLE Pricing (
    Cartype VARCHAR(50) PRIMARY KEY,
    DailyRate DECIMAL(10, 2)
);

-- Insert sample pricing for different vehicle types
INSERT INTO Pricing (Cartype, DailyRate) VALUES
('sedan', 30),
('SUV', 50),
('pickup', 35),
('van', 45);

-- Check the created tables
SHOW TABLES;
