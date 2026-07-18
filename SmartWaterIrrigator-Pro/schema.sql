-- Smart Water Irrigator - MySQL Database Schema




-- Users Table (Handles both regular users and admins)
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    role ENUM('farmer', 'admin') DEFAULT 'farmer',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Crops Table
CREATE TABLE IF NOT EXISTS crops (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(100) NOT NULL,
    min_temp FLOAT NOT NULL,
    max_temp FLOAT NOT NULL,
    min_humidity FLOAT NOT NULL,
    max_humidity FLOAT NOT NULL,
    min_rainfall FLOAT DEFAULT 0,
    max_rainfall FLOAT DEFAULT 1000,
    base_water_req FLOAT NOT NULL, -- Liters per sq meter or standard unit
    season VARCHAR(50) DEFAULT 'All',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Calculations History Table (Farmer History)
CREATE TABLE IF NOT EXISTS calculations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INT NOT NULL,
    city VARCHAR(100) NOT NULL,
    farm_size FLOAT NOT NULL,
    crop_id INT,
    temperature FLOAT,
    humidity FLOAT,
    wind_speed FLOAT,
    rain_probability FLOAT,
    soil_moisture FLOAT, -- manual input from user
    water_required FLOAT NOT NULL,
    calculation_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (crop_id) REFERENCES crops(id) ON DELETE SET NULL
);

-- Contact Messages Table
CREATE TABLE IF NOT EXISTS contact_messages (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL,
    subject VARCHAR(200),
    message TEXT NOT NULL,
    status ENUM('unread', 'read', 'resolved') DEFAULT 'unread',
    submitted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Insert some default crops for recommendation testing
INSERT INTO crops (name, min_temp, max_temp, min_humidity, max_humidity, base_water_req, season) VALUES
('Wheat', 10, 25, 40, 70, 400, 'Winter'),
('Rice', 20, 35, 60, 90, 900, 'Monsoon'),
('Cotton', 21, 30, 50, 80, 700, 'Summer'),
('Sugarcane', 20, 35, 70, 95, 1500, 'All'),
('Maize', 18, 27, 50, 75, 500, 'Monsoon');
