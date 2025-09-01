<<<<<<< HEAD
CREATE DATABASE IF NOT EXISTS food_sharing;
USE food_sharing;
CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    role ENUM('donor','recipient') NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
INSERT INTO users (name, email, password, role) VALUES
('Alice Donor', 'alice@example.com', 'password123', 'donor'),
('Bob Recipient', 'bob@example.com', 'password123', 'recipient'),
('Carol Donor', 'carol@example.com', 'password123', 'donor'),
('David Recipient', 'david@example.com', 'password123', 'recipient'),
('Eve Donor', 'eve@example.com', 'password123', 'donor');

CREATE TABLE food_posts (
    id INT AUTO_INCREMENT PRIMARY KEY,
    donor_id INT NOT NULL,
    food_name VARCHAR(100) NOT NULL,
    description TEXT,
    quantity INT NOT NULL,
    expiry_date DATE NOT NULL,
    location VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (donor_id) REFERENCES users(id)
);
INSERT INTO food_posts (donor_id, food_name, description, quantity, expiry_date, location) VALUES
(1, 'Rice', '5kg bag of rice, well packed', 1, '2025-09-15', 'Nairobi'),
(3, 'Milk', 'Fresh 2 liters of milk', 2, '2025-09-05', 'Mombasa'),
(5, 'Bread', 'Whole wheat bread loafs', 10, '2025-09-02', 'Kisumu'),
(1, 'Beans', 'Dry beans, 3kg', 1, '2025-09-20', 'Nakuru'),
(3, 'Vegetables', 'Fresh assorted vegetables', 5, '2025-09-01', 'Thika');

CREATE TABLE claims (
    id INT AUTO_INCREMENT PRIMARY KEY,
    food_post_id INT NOT NULL,
    recipient_id INT NOT NULL,
    status ENUM('pending', 'approved', 'rejected') DEFAULT 'pending',
    claimed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (food_post_id) REFERENCES food_posts(id),
    FOREIGN KEY (recipient_id) REFERENCES users(id)
);
INSERT INTO claims (food_post_id, recipient_id, status) VALUES
(1, 2, 'pending'),    -- Recipient claims Rice from donor
(2, 4, 'approved'),   -- Recipient claims Milk from donor
(3, 2, 'rejected'),   -- Recipient claims Bread but rejected
(4, 4, 'approved'),   -- Recipient claims Beans
(5, 2, 'pending');    -- Recipient claims Vegetables




=======
CREATE DATABASE IF NOT EXISTS food_sharing;
USE food_sharing;
CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    role ENUM('donor','recipient') NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
INSERT INTO users (name, email, password, role) VALUES
('Alice Donor', 'alice@example.com', 'password123', 'donor'),
('Bob Recipient', 'bob@example.com', 'password123', 'recipient'),
('Carol Donor', 'carol@example.com', 'password123', 'donor'),
('David Recipient', 'david@example.com', 'password123', 'recipient'),
('Eve Donor', 'eve@example.com', 'password123', 'donor');

CREATE TABLE food_posts (
    id INT AUTO_INCREMENT PRIMARY KEY,
    donor_id INT NOT NULL,
    food_name VARCHAR(100) NOT NULL,
    description TEXT,
    quantity INT NOT NULL,
    expiry_date DATE NOT NULL,
    location VARCHAR(255) NOT NULL,
    image_url VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (donor_id) REFERENCES users(id)
);
INSERT INTO food_posts (donor_id, food_name, description, quantity, expiry_date, location) VALUES
(1, 'Rice', '5kg bag of rice, well packed', 1, '2025-09-15', 'Nairobi'),
(3, 'Milk', 'Fresh 2 liters of milk', 2, '2025-09-05', 'Mombasa'),
(5, 'Bread', 'Whole wheat bread loafs', 10, '2025-09-02', 'Kisumu'),
(1, 'Beans', 'Dry beans, 3kg', 1, '2025-09-20', 'Nakuru'),
(3, 'Vegetables', 'Fresh assorted vegetables', 5, '2025-09-01', 'Thika');

CREATE TABLE claims (
    id INT AUTO_INCREMENT PRIMARY KEY,
    food_post_id INT NOT NULL,
    recipient_id INT NOT NULL,
    status ENUM('pending', 'approved', 'rejected') DEFAULT 'pending',
    claimed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (food_post_id) REFERENCES food_posts(id),
    FOREIGN KEY (recipient_id) REFERENCES users(id)
);
INSERT INTO claims (food_post_id, recipient_id, status) VALUES
(1, 2, 'pending'),    -- Recipient claims Rice from donor
(2, 4, 'approved'),   -- Recipient claims Milk from donor
(3, 2, 'rejected'),   -- Recipient claims Bread but rejected
(4, 4, 'approved'),   -- Recipient claims Beans
(5, 2, 'pending');    -- Recipient claims Vegetables




>>>>>>> f7d95ff (FoodShare)
