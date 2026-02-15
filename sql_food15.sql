use food_delivery_db;
SELECT Customer_ID, SUM(Order_Value) AS total_spent
FROM cleaned_food_delivery_dataset
GROUP BY Customer_ID
ORDER BY total_spent DESC
LIMIT 10;
#2️⃣	Age Group vs Average Order Value
SELECT Customer_Age_Group, AVG(Order_Value) AS avg_order_value
FROM cleaned_food_delivery_dataset
GROUP BY Customer_Age_Group;

#weekend vs Weekday Order Patterns
SELECT Order_Day, COUNT(*) AS total_orders
FROM cleaned_food_delivery_dataset
GROUP BY Order_Day;

#REVENUE & PROFIT ANALYSIS
#Monthly Revenue Trend
SELECT DATE_FORMAT(Order_Date,'%Y-%m') AS month,
       SUM(Order_Value) AS revenue
FROM cleaned_food_delivery_dataset
GROUP BY month
ORDER BY month;

#Impact of Discounts on Profit
SELECT Discount_Applied, AVG(Profit_Margin) AS avg_profit
FROM cleaned_food_delivery_dataset
GROUP BY Discount_Applied;

#High Revenue Cities
SELECT City, SUM(Order_Value) AS total_revenue
FROM cleaned_food_delivery_dataset
GROUP BY City
ORDER BY total_revenue DESC;

#High Revenue Cuisines
SELECT Cuisine_Type, SUM(Order_Value) AS total_revenue
FROM cleaned_food_delivery_dataset
GROUP BY Cuisine_Type
ORDER BY total_revenue DESC;

#DELIVERY PERFORMANCE
#Average Delivery Time by City
SELECT City, AVG(Delivery_Time_Min) AS avg_delivery_time
FROM cleaned_food_delivery_dataset
GROUP BY City;

#Distance vs Delivery Delay Data
SELECT Distance_km, Delivery_Time_Min
FROM cleaned_food_delivery_dataset;




#Delivery Rating vs Delivery Time
SELECT Restaurant_Rating, AVG(Delivery_Time_Min) AS avg_time
FROM cleaned_food_delivery_dataset
GROUP BY Restaurant_Rating;

#RESTAURANT PERFORMANCE
#Top Rated Restaurants
SELECT Restaurant_Name, AVG(Restaurant_Rating) AS avg_rating
FROM cleaned_food_delivery_dataset
GROUP BY Restaurant_Name
ORDER BY avg_rating DESC
LIMIT 10;

#Cancellation Rate by Restaurant
SELECT Restaurant_Name,
       COUNT(CASE WHEN Order_Status='cancelled' THEN 1 END) * 100.0 / COUNT(*) AS cancel_rate
FROM cleaned_food_delivery_dataset
GROUP BY Restaurant_Name;

#Cuisine-wise Performance (Revenue + Rating)
SELECT Cuisine_Type,
       SUM(Order_Value) AS revenue,
       AVG(Restaurant_Rating) AS avg_rating
FROM cleaned_food_delivery_dataset
GROUP BY Cuisine_Type;

#OPERATIONAL INSIGHTS
#Peak Hour Demand Analysis
SELECT Peak_Hour, COUNT(*) AS total_orders
FROM cleaned_food_delivery_dataset
GROUP BY Peak_Hour;

#Payment Mode Preferences
SELECT Payment_Mode, COUNT(*) AS usage_count
FROM cleaned_food_delivery_dataset
GROUP BY Payment_Mode
ORDER BY usage_count DESC;



-- 15. Cancellation Reason Analysis

SELECT 
    Cancellation_Reason,
    COUNT(*) AS Total_Cancellations,
    ROUND(COUNT(*) * 100.0 / 
        (SELECT COUNT(*) 
         FROM cleaned_food_delivery_dataset 
         WHERE Order_Status = 'Cancelled'), 2
    ) AS Percentage
FROM cleaned_food_delivery_dataset
WHERE Order_Status = 'Cancelled'
GROUP BY Cancellation_Reason
ORDER BY Total_Cancellations DESC;




