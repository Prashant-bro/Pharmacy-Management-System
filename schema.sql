CREATE DATABASE IF NOT EXISTS project;

USE project;

CREATE TABLE IF NOT EXISTS medicine (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    expiry_date DATE NOT NULL,
    batch_number VARCHAR(100),
    price DECIMAL(10, 2),
    quantity INT,
    section VARCHAR(100)
);
