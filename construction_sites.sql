CREATE TABLE construction_sites (
    site_id INT PRIMARY KEY AUTO_INCREMENT,
    site_name VARCHAR(100),
    site_address VARCHAR(255),
    site_manager VARCHAR(100),
    safety_status VARCHAR(50)
);

CREATE TABLE employees (
    employee_id INT PRIMARY KEY AUTO_INCREMENT,
    employee_name VARCHAR(100),
    gender VARCHAR(10),
    work_site_id INT,
    join_date DATE
);
