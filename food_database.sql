create database fooddeliver_db;
use fooddeliver_db;


DROP DATABASE IF EXISTS food_delivery_db;
CREATE DATABASE food_delivery_db;
USE food_delivery_db;

-- ============================================================================
-- TABLE 1: CUSTOMERS
-- ============================================================================
DROP TABLE IF EXISTS customers;
CREATE TABLE customers (
    Customer_ID VARCHAR(20) PRIMARY KEY,
    Customer_Age INT,
    Customer_Gender VARCHAR(10),
    Age_Group VARCHAR(20),
    Created_Date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ============================================================================
-- TABLE 2: RESTAURANTS
-- ============================================================================
DROP TABLE IF EXISTS restaurants;
CREATE TABLE restaurants (
    Restaurant_ID VARCHAR(20) PRIMARY KEY,
    Restaurant_Name VARCHAR(100),
    Cuisine_Type VARCHAR(50),
    Average_Rating DECIMAL(3,2),
    Total_Orders INT DEFAULT 0,
    Created_Date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ============================================================================
-- TABLE 3: DELIVERY PARTNERS
-- ============================================================================
DROP TABLE IF EXISTS delivery_partners;
CREATE TABLE delivery_partners (
    Delivery_Partner_ID VARCHAR(20) PRIMARY KEY,
    Average_Rating DECIMAL(3,2),
    Total_Deliveries INT DEFAULT 0,
    Created_Date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ============================================================================
-- TABLE 4: ORDERS (Main Fact Table)
-- ============================================================================
DROP TABLE IF EXISTS orders;
CREATE TABLE orders (
    Order_ID VARCHAR(20) PRIMARY KEY,
    Customer_ID VARCHAR(20),
    Restaurant_ID VARCHAR(20),
    Delivery_Partner_ID VARCHAR(20),
    
    -- Order Details
    Order_Date DATE,
    Order_Time TIME,
    Order_Day VARCHAR(10),
    Order_Day_Type VARCHAR(10),
    
    -- Location Details
    City VARCHAR(50),
    Area VARCHAR(50),
    Distance_km DECIMAL(10,2),
    
    -- Financial Details
    Order_Value DECIMAL(10,2),
    Discount_Applied DECIMAL(10,2),
    Final_Amount DECIMAL(10,2),
    Profit_Margin DECIMAL(5,4),
    Profit_Margin_Percent DECIMAL(8,2),
    
    -- Delivery Details
    Delivery_Time_Min INT,
    Delivery_Performance VARCHAR(30),
    Delivery_Rating INT,
    
    -- Order Status
    Order_Status VARCHAR(20),
    Cancellation_Reason VARCHAR(100),
    
    -- Additional Attributes
    Payment_Mode VARCHAR(20),
    Cuisine_Type VARCHAR(50),
    Restaurant_Rating DECIMAL(3,2),
    Peak_Hour BOOLEAN,
    Is_Delayed BOOLEAN,
    Is_High_Value BOOLEAN,
    
    -- Timestamp
    Created_Date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    -- Foreign Keys
    FOREIGN KEY (Customer_ID) REFERENCES customers(Customer_ID),
    FOREIGN KEY (Restaurant_ID) REFERENCES restaurants(Restaurant_ID),
    FOREIGN KEY (Delivery_Partner_ID) REFERENCES delivery_partners(Delivery_Partner_ID),
    
    -- Indexes for performance
    INDEX idx_order_date (Order_Date),
    INDEX idx_city (City),
    INDEX idx_order_status (Order_Status),
    INDEX idx_customer (Customer_ID),
    INDEX idx_restaurant (Restaurant_ID)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ============================================================================
-- TABLE 5: ORDER_ANALYTICS (Derived Metrics)
-- ============================================================================
DROP TABLE IF EXISTS order_analytics;
CREATE TABLE order_analytics (
    Analytics_ID INT AUTO_INCREMENT PRIMARY KEY,
    Order_ID VARCHAR(20),
    
    -- Time-based Analysis
    Year INT,
    Month INT,
    Month_Name VARCHAR(20),
    Week INT,
    Day INT,
    Day_Of_Week VARCHAR(20),
    
    -- Categorizations
    Order_Value_Category VARCHAR(30),
    Distance_Category VARCHAR(30),
    Age_Group VARCHAR(20),
    
    -- Calculated Metrics
    Revenue_Per_KM DECIMAL(10,2),
    Discount_Percentage DECIMAL(5,2),
    Time_Per_KM DECIMAL(10,2),
    
    -- Flags
    Is_Weekend BOOLEAN,
    Is_Peak_Hour BOOLEAN,
    Is_Premium_Order BOOLEAN,
    
    Created_Date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (Order_ID) REFERENCES orders(Order_ID),
    INDEX idx_year_month (Year, Month)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ============================================================================
-- TABLE 6: DAILY_SUMMARY (Aggregated Daily Metrics)
-- ============================================================================
DROP TABLE IF EXISTS daily_summary;
CREATE TABLE daily_summary (
    Summary_ID INT AUTO_INCREMENT PRIMARY KEY,
    Summary_Date DATE UNIQUE,
    
    -- Order Metrics
    Total_Orders INT,
    Delivered_Orders INT,
    Cancelled_Orders INT,
    Cancellation_Rate DECIMAL(5,2),
    
    -- Financial Metrics
    Total_Revenue DECIMAL(15,2),
    Total_Order_Value DECIMAL(15,2),
    Total_Discount DECIMAL(15,2),
    Average_Order_Value DECIMAL(10,2),
    Total_Profit DECIMAL(15,2),
    Average_Profit_Margin DECIMAL(5,2),
    
    -- Operational Metrics
    Average_Delivery_Time DECIMAL(10,2),
    Average_Distance DECIMAL(10,2),
    Average_Delivery_Rating DECIMAL(3,2),
    Average_Restaurant_Rating DECIMAL(3,2),
    
    Created_Date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    INDEX idx_summary_date (Summary_Date)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ============================================================================
-- TABLE 7: RESTAURANT_PERFORMANCE (Aggregated Restaurant Metrics)
-- ============================================================================
DROP TABLE IF EXISTS restaurant_performance;
CREATE TABLE restaurant_performance (
    Performance_ID INT AUTO_INCREMENT PRIMARY KEY,
    Restaurant_ID VARCHAR(20),
    
    -- Performance Period
    Year INT,
    Month INT,
    
    -- Order Metrics
    Total_Orders INT,
    Delivered_Orders INT,
    Cancelled_Orders INT,
    Cancellation_Rate DECIMAL(5,2),
    
    -- Financial Metrics
    Total_Revenue DECIMAL(15,2),
    Average_Order_Value DECIMAL(10,2),
    Total_Profit DECIMAL(15,2),
    
    -- Quality Metrics
    Average_Rating DECIMAL(3,2),
    Average_Delivery_Time DECIMAL(10,2),
    
    Created_Date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (Restaurant_ID) REFERENCES restaurants(Restaurant_ID),
    INDEX idx_restaurant_period (Restaurant_ID, Year, Month)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ============================================================================
-- TABLE 8: CITY_PERFORMANCE (Aggregated City Metrics)
-- ============================================================================
DROP TABLE IF EXISTS city_performance;
CREATE TABLE city_performance (
    Performance_ID INT AUTO_INCREMENT PRIMARY KEY,
    City VARCHAR(50),
    
    -- Performance Period
    Year INT,
    Month INT,
    
    -- Order Metrics
    Total_Orders INT,
    Total_Customers INT,
    Total_Restaurants INT,
    
    -- Financial Metrics
    Total_Revenue DECIMAL(15,2),
    Average_Order_Value DECIMAL(10,2),
    
    -- Operational Metrics
    Average_Delivery_Time DECIMAL(10,2),
    Average_Distance DECIMAL(10,2),
    
    Created_Date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    INDEX idx_city_period (City, Year, Month)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ============================================================================
-- INDEXES FOR OPTIMIZATION
-- ============================================================================

-- Additional indexes for better query performance
CREATE INDEX idx_orders_customer_date ON orders(Customer_ID, Order_Date);
CREATE INDEX idx_orders_restaurant_date ON orders(Restaurant_ID, Order_Date);
CREATE INDEX idx_orders_city_date ON orders(City, Order_Date);
CREATE INDEX idx_orders_status_date ON orders(Order_Status, Order_Date);

-- ============================================================================
-- VIEWS FOR COMMON QUERIES
-- ============================================================================

-- View 1: Order Details with Full Information
CREATE OR REPLACE VIEW vw_order_details AS
SELECT 
    o.Order_ID,
    o.Order_Date,
    o.Order_Day_Type,
    c.Customer_ID,
    c.Customer_Age,
    c.Customer_Gender,
    c.Age_Group,
    r.Restaurant_ID,
    r.Restaurant_Name,
    r.Cuisine_Type,
    o.City,
    o.Area,
    o.Distance_km,
    o.Order_Value,
    o.Discount_Applied,
    o.Final_Amount,
    o.Profit_Margin_Percent,
    o.Delivery_Time_Min,
    o.Delivery_Performance,
    o.Delivery_Rating,
    o.Restaurant_Rating,
    o.Order_Status,
    o.Cancellation_Reason,
    o.Payment_Mode,
    o.Peak_Hour
FROM orders o
LEFT JOIN customers c ON o.Customer_ID = c.Customer_ID
LEFT JOIN restaurants r ON o.Restaurant_ID = r.Restaurant_ID;

-- View 2: Daily KPIs
CREATE OR REPLACE VIEW vw_daily_kpis AS
SELECT 
    Order_Date,
    COUNT(*) as Total_Orders,
    SUM(CASE WHEN Order_Status = 'Delivered' THEN 1 ELSE 0 END) as Delivered_Orders,
    SUM(CASE WHEN Order_Status = 'Cancelled' THEN 1 ELSE 0 END) as Cancelled_Orders,
    ROUND(SUM(CASE WHEN Order_Status = 'Cancelled' THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) as Cancellation_Rate,
    ROUND(SUM(Final_Amount), 2) as Total_Revenue,
    ROUND(AVG(Order_Value), 2) as Avg_Order_Value,
    ROUND(AVG(Delivery_Time_Min), 2) as Avg_Delivery_Time,
    ROUND(AVG(Delivery_Rating), 2) as Avg_Delivery_Rating
FROM orders
GROUP BY Order_Date;

-- View 3: Restaurant Performance Summary
CREATE OR REPLACE VIEW vw_restaurant_summary AS
SELECT 
    r.Restaurant_ID,
    r.Restaurant_Name,
    r.Cuisine_Type,
    COUNT(o.Order_ID) as Total_Orders,
    SUM(CASE WHEN o.Order_Status = 'Delivered' THEN 1 ELSE 0 END) as Delivered_Orders,
    SUM(CASE WHEN o.Order_Status = 'Cancelled' THEN 1 ELSE 0 END) as Cancelled_Orders,
    ROUND(SUM(CASE WHEN o.Order_Status = 'Cancelled' THEN 1 ELSE 0 END) * 100.0 / COUNT(o.Order_ID), 2) as Cancellation_Rate,
    ROUND(SUM(o.Final_Amount), 2) as Total_Revenue,
    ROUND(AVG(o.Order_Value), 2) as Avg_Order_Value,
    ROUND(AVG(o.Restaurant_Rating), 2) as Avg_Rating
FROM restaurants r
LEFT JOIN orders o ON r.Restaurant_ID = o.Restaurant_ID
GROUP BY r.Restaurant_ID, r.Restaurant_Name, r.Cuisine_Type;

-- View 4: City Performance Summary
CREATE OR REPLACE VIEW vw_city_summary AS
SELECT 
    City,
    COUNT(*) as Total_Orders,
    COUNT(DISTINCT Customer_ID) as Unique_Customers,
    COUNT(DISTINCT Restaurant_ID) as Unique_Restaurants,
    ROUND(SUM(Final_Amount), 2) as Total_Revenue,
    ROUND(AVG(Order_Value), 2) as Avg_Order_Value,
    ROUND(AVG(Delivery_Time_Min), 2) as Avg_Delivery_Time,
    ROUND(AVG(Distance_km), 2) as Avg_Distance
FROM orders
GROUP BY City;

-- View 5: Customer Segmentation
CREATE OR REPLACE VIEW vw_customer_segments AS
SELECT 
    c.Customer_ID,
    c.Customer_Age,
    c.Customer_Gender,
    c.Age_Group,
    COUNT(o.Order_ID) as Total_Orders,
    ROUND(SUM(o.Final_Amount), 2) as Total_Spent,
    ROUND(AVG(o.Order_Value), 2) as Avg_Order_Value,
    ROUND(AVG(o.Delivery_Rating), 2) as Avg_Delivery_Rating,
    MAX(o.Order_Date) as Last_Order_Date
FROM customers c
LEFT JOIN orders o ON c.Customer_ID = o.Customer_ID
GROUP BY c.Customer_ID, c.Customer_Age, c.Customer_Gender, c.Age_Group;



-- Query 1: Identify Top 10 Spending Customers
SELECT 
    c.Customer_ID,
    c.Customer_Age,
    c.Customer_Gender,
    c.Age_Group,
    COUNT(o.Order_ID) as Total_Orders,
    ROUND(SUM(o.Final_Amount), 2) as Total_Spent,
    ROUND(AVG(o.Order_Value), 2) as Avg_Order_Value,
    ROUND(AVG(o.Delivery_Rating), 2) as Avg_Delivery_Rating
FROM onine_food_delivery_analysis
JOIN orders o ON c.Customer_ID = o.Customer_ID
WHERE o.Order_Status = 'Delivered'
GROUP BY c.Customer_ID, c.Customer_Age, c.Customer_Gender, c.Age_Group
ORDER BY Total_Spent DESC
LIMIT 10;

