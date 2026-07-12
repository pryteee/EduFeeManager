CREATE DATABASE fee_structure_management;

USE fee_structure_management;


CREATE TABLE admin (
    admin_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(50),
    username VARCHAR(50) UNIQUE NOT NULL,
    password VARCHAR(50),
    email_id VARCHAR(60),
    contact VARCHAR(10),
    create_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


CREATE TABLE counselor (
    counselor_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100),
    email VARCHAR(100),
    contact VARCHAR(15),
    username VARCHAR(50) UNIQUE NOT NULL,
    password VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


CREATE TABLE student (
    student_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100),
    email VARCHAR(100),
    contact VARCHAR(15),
    course VARCHAR(100),
    academic_year VARCHAR(20),
    username VARCHAR(50) UNIQUE NOT NULL,
    password VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    total_fee DECIMAL(10,2) NOT NULL DEFAULT 0.00
);


CREATE TABLE fee (
    fee_id INT AUTO_INCREMENT PRIMARY KEY,
    student_id INT UNIQUE,
    course_fee DECIMAL(10,2) DEFAULT 0.00,
    paid_amount DECIMAL(10,2) DEFAULT 0.00,
    pending_amount DECIMAL(10,2) DEFAULT 0.00,
    status VARCHAR(30) DEFAULT 'Pending',

    FOREIGN KEY (student_id) REFERENCES student(student_id)
);