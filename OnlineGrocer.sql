-- drop database OnlineGrocer;
CREATE DATABASE OnlineGrocer;
USE OnlineGrocer;

CREATE TABLE Categories (
    CategoryID INT PRIMARY KEY AUTO_INCREMENT,
    CategoryName VARCHAR(50) NOT NULL
);

CREATE TABLE Suppliers (
    SupplierID INT PRIMARY KEY AUTO_INCREMENT,
    SupplierName VARCHAR(100),
    ContactName VARCHAR(100),
    ContactPhone VARCHAR(15),
    Address TEXT
);

CREATE TABLE Products (
    ProductID INT PRIMARY KEY AUTO_INCREMENT,
    ProductName VARCHAR(100) NOT NULL,
    CategoryID INT,
    SupplierID INT,
    Price DECIMAL(5,2),
    Stock INT DEFAULT 0,
    FOREIGN KEY (CategoryID) REFERENCES Categories(CategoryID),
    FOREIGN KEY (SupplierID) REFERENCES Suppliers(SupplierID)
);

CREATE TABLE Customers (
    CustomerID INT PRIMARY KEY AUTO_INCREMENT,
    FirstName VARCHAR(50),
    LastName VARCHAR(50),
    Username VARCHAR(50) UNIQUE NOT NULL,
    Phone VARCHAR(15) UNIQUE NOT NULL,
    Password VARCHAR(100) NOT NULL, -- Passwords should ideally be hashed
    Address TEXT
);

CREATE TABLE Admins (
    AdminID INT PRIMARY KEY AUTO_INCREMENT,
    Username VARCHAR(50) NOT NULL,
    Password VARCHAR(100) NOT NULL
);

CREATE TABLE Orders (
    OrderID INT PRIMARY KEY AUTO_INCREMENT,
    CustomerID INT,
    OrderDate DATETIME DEFAULT CURRENT_TIMESTAMP,
    TotalAmount DECIMAL(7,2),
    PaymentStatus VARCHAR(20) DEFAULT 'Pending',
    Status VARCHAR(20) DEFAULT 'Pending',
    FOREIGN KEY (CustomerID) REFERENCES Customers(CustomerID)
);

CREATE TABLE Order_Items (
    OrderItemID INT PRIMARY KEY AUTO_INCREMENT,
    OrderID INT,
    ProductID INT,
    Quantity INT,
    Price DECIMAL(5,2),
    FOREIGN KEY (OrderID) REFERENCES Orders(OrderID),
    FOREIGN KEY (ProductID) REFERENCES Products(ProductID)
);

-- Insert Sample Data
INSERT INTO Categories (CategoryName) VALUES ('Fruits'), ('Vegetables'), ('Dairy'), ('Bakery');

INSERT INTO Suppliers (SupplierName, ContactName, ContactPhone, Address)
VALUES ('Fresh Produce Co.', 'Alice Smith', '1234567890', '456 Maple Ave'),
       ('Supplier A', 'Alice', '123-456-7890', '123 Apple St.'),
       ('Supplier B', 'Bob', '098-765-4321', '456 Banana Rd.');

INSERT INTO Products (ProductName, CategoryID, SupplierID, Price, Stock)
VALUES ('Apple', 1, 1, 1.50, 100),
       ('Banana', 1, 1, 0.50, 150),
       ('Carrot', 2, 2, 0.20, 200),
       ('Tomato', 2, 2, 0.40, 300),
       ('Potato', 2, 2, 0.25, 250),
       ('Onion', 2, 2, 0.35, 400),
       ('Lettuce', 1, 1, 0.75, 100),
       ('Grapes', 1, 1, 1.00, 200),
       ('Orange', 1, 1, 0.60, 150);

INSERT INTO Admins (Username, Password)
VALUES ('admin', 'admin');

CREATE TABLE Carts (
    CartID INT PRIMARY KEY AUTO_INCREMENT,
    CustomerID INT,
    CreatedAt DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (CustomerID) REFERENCES Customers(CustomerID)
);

CREATE TABLE Cart_Items (
    CartItemID INT PRIMARY KEY AUTO_INCREMENT,
    CartID INT,
    ProductID INT,
    Quantity INT,
    FOREIGN KEY (CartID) REFERENCES Carts(CartID),
    FOREIGN KEY (ProductID) REFERENCES Products(ProductID)
);
