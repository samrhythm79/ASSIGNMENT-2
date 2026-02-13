# Online Food Delivery Analysis - Complete Data Analytics Project

## 📊 Project Overview

This project analyzes **100,000 online food delivery orders** to extract actionable business insights for optimizing delivery operations, restaurant performance, customer satisfaction, and revenue growth.

### Business Objectives
- Understand customer ordering behavior and preferences
- Identify operational inefficiencies in delivery
- Evaluate restaurant performance metrics
- Track revenue, profit margins, and order cancellations
- Provide data-driven insights for business decision-making

---

## 🗂️ Project Structure

```
food-delivery-analysis/
│
├── data/
│   ├── raw/
│   │   └── ONINE_FOOD_DELIVERY_ANALYSIS.csv (100,000 records)
│   └── cleaned/
│       └── food_delivery_cleaned.csv (processed data)
│
├── scripts/
│   ├── food_delivery_analysis.py      (Data cleaning & EDA)
│   ├── mysql_integration.py           (Database integration)
│   └── visualization_script.py        (Optional: Matplotlib/Seaborn)
│
├── sql/
│   ├── sql_schema.sql                 (Database schema)
│   └── sql_analytical_queries.sql     (30+ analytical queries)
│
├── reports/
│   ├── data_summary_report.txt
│   └── eda_insights.md
│
├── dashboards/
│   └── food_delivery_dashboard.pbix   (streamlit)
│
└── README.md
```

---

## 📋 Dataset Information

### Dataset Specifications
- **Total Records**: 100,000 orders
- **Features**: 25 columns
- **Date Range**: January 2024 - December 2024
- **Format**: CSV file

### Data Dictionary

| Column Name | Data Type | Description |
|------------|-----------|-------------|
| Order_ID | String | Unique order identifier |
| Customer_ID | String | Unique customer identifier |
| Customer_Age | Integer | Age of customer |
| Customer_Gender | String | Gender (Male/Female/Other) |
| City | String | Delivery city |
| Area | String | Delivery area within city |
| Restaurant_ID | String | Unique restaurant identifier |
| Restaurant_Name | String | Name of restaurant |
| Cuisine_Type | String | Type of cuisine (Chinese, Italian, etc.) |
| Order_Date | Date | Date of order placement |
| Order_Time | Time | Time of order placement |
| Delivery_Time_Min | Integer | Delivery time in minutes |
| Distance_km | Float | Delivery distance in kilometers |
| Order_Value | Float | Original order amount |
| Discount_Applied | Float | Discount amount |
| Final_Amount | Float | Final payment amount |
| Payment_Mode | String | Payment method (COD/UPI/Card/Wallet) |
| Order_Status | String | Status (Delivered/Cancelled) |
| Cancellation_Reason | String | Reason if cancelled |
| Delivery_Partner_ID | String | Unique delivery partner ID |
| Delivery_Rating | Integer | Rating for delivery (1-5) |
| Restaurant_Rating | Float | Rating for restaurant (1-5) |
| Order_Day | String | Weekday/Weekend |
| Peak_Hour | Boolean | Peak hour indicator |
| Profit_Margin | Float | Profit margin ratio |

---

## 🔧 Technical Stack

### Technologies Used
- **Python 3.8+**
  - pandas (Data manipulation)
  - numpy (Numerical operations)
  - matplotlib & seaborn (Visualization)
  - sqlalchemy (Database connectivity)
  - pymysql (MySQL driver)

- **Database**
  - MySQL 8.0+

- **Business Intelligence**
  - streamlit db

- **Tools**
  - Jupyter Notebook (Optional)
  - VS Code / PyCharm
  - MySQL Workbench

---

## 🚀 Installation & Setup

### Prerequisites
```bash
# Python packages
pip install pandas numpy matplotlib seaborn sqlalchemy pymysql

# MySQL Server
# Download and install from: https://dev.mysql.com/downloads/
```

### Step 1: Clone or Download Project Files
```bash
# Create project directory
mkdir food-delivery-analysis
cd food-delivery-analysis
```

### Step 2: Set Up MySQL Database
```bash
# Login to MySQL
mysql -u root -p

# Run schema creation script
mysql -u root -p < sql/sql_schema.sql
```

### Step 3: Configure Database Connection
Edit `mysql_integration.py` and update credentials:
```python
DB_CONFIG = {
    'host': 'localhost',
    'port': 3306,
    'user': 'your_username',
    'password': 'your_password',
    'database': 'food_delivery_db'
}
```

---

## 📊 Execution Steps

### Phase 1: Data Cleaning & Preprocessing

```bash
python scripts/food_delivery_analysis.py
```

**What it does:**
- ✅ Loads raw CSV data
- ✅ Handles missing values (median/mode imputation)
- ✅ Removes outliers using percentile capping
- ✅ Corrects invalid values (ratings, negative amounts)
- ✅ Converts data types
- ✅ Creates derived features (age groups, delivery performance, etc.)
- ✅ Performs comprehensive EDA
- ✅ Saves cleaned data to outputs folder

**Output Files:**
- `food_delivery_cleaned.csv`
- `data_summary_report.txt`

### Phase 2: Database Integration

```bash
python scripts/mysql_integration.py
```

**What it does:**
- ✅ Creates database connection
- ✅ Populates dimension tables (customers, restaurants, delivery_partners)
- ✅ Populates fact table (orders)
- ✅ Creates analytical tables (order_analytics)
- ✅ Generates aggregated summaries (daily_summary, restaurant_performance, city_performance)
- ✅ Runs verification queries

**Database Tables Created:**
1. `customers` - Customer master data
2. `restaurants` - Restaurant master data
3. `delivery_partners` - Delivery partner master data
4. `orders` - Main fact table with all order details
5. `order_analytics` - Derived metrics and categorizations
6. `daily_summary` - Daily aggregated KPIs
7. `restaurant_performance` - Monthly restaurant metrics
8. `city_performance` - City-level performance metrics

### Phase 3: Run Analytical Queries

```bash
# From MySQL Workbench or command line
mysql -u root -p food_delivery_db < sql/sql_analytical_queries.sql
```

**30+ Analytical Queries covering:**
1. **Customer Analysis** (5 queries)
2. **Revenue & Profit Analysis** (5 queries)
3. **Delivery Performance** (5 queries)
4. **Restaurant Performance** (5 queries)
5. **Operational Insights** (5 queries)
6. **Advanced Analytics** (5 queries)



---

## 📈 Key Features Created

### Derived Features

1. **Date Features**
   - Year, Month, Month_Name
   - Day, Day_Of_Week, Week
   
2. **Customer Segmentation**
   - Age_Group (18-25, 26-35, 36-45, 46-55, 56+)
   
3. **Order Categorization**
   - Order_Value_Category (Low, Medium, High, Very High)
   - Distance_Category (Near, Medium, Far, Very Far)
   - Delivery_Performance (Fast, Normal, Slow, Very Slow)
   
4. **Business Metrics**
   - Profit_Margin_Percent
   - Is_Delayed (Boolean)
   - Is_High_Value (Boolean)
   - Revenue_Per_KM
   - Discount_Percentage
   - Time_Per_KM

---

## 📊 Key Performance Indicators (KPIs)

### Dashboard KPIs to Track

1. **Order Metrics**
   - Total Orders
   - Delivered Orders
   - Cancelled Orders
   - Cancellation Rate (%)

2. **Financial Metrics**
   - Total Revenue
   - Average Order Value
   - Total Discounts
   - Profit Margin (%)

3. **Operational Metrics**
   - Average Delivery Time
   - Average Distance
   - On-Time Delivery Rate
   - Peak Hour Order %

4. **Quality Metrics**
   - Average Delivery Rating
   - Average Restaurant Rating
   - Customer Satisfaction Score

---

## 🎯 Sample Analytical Insights

### Customer Insights
- **Top spending customers** contribute to 25-30% of revenue
- **Age group 26-35** has highest average order value
- **Weekend orders** are 15% higher than weekdays
- **Peak hours** (12-2 PM, 7-9 PM) account for 45% of orders

### Revenue Insights
- **Total Revenue**: ₹XXX Million
- **High discount orders** have lower profit margins
- **Top 3 cities** generate 60% of total revenue
- **Chinese cuisine** is most popular with 35% order share

### Delivery Performance
- **Average delivery time**: 78 minutes
- **Distance-delay correlation**: +0.72 (strong positive)
- **<30 min deliveries** get 4.5+ ratings
- **Peak hours** increase delivery time by 20%

### Restaurant Performance
- **Top 10 restaurants** account for 18% of orders
- **Cancellation rate**: 8-12% varies by restaurant
- **Italian cuisine** has highest average ratings (4.3/5)
- **Underperforming restaurants**: 15% have >15% cancellation rate

---

## 🗄️ Database Schema

### Star Schema Design

**Fact Table**: `orders`
- Contains transactional data
- Foreign keys to dimension tables

**Dimension Tables**:
- `customers` (Customer master)
- `restaurants` (Restaurant master)
- `delivery_partners` (Partner master)

**Aggregate Tables**:
- `order_analytics` (Derived metrics)
- `daily_summary` (Daily KPIs)
- `restaurant_performance` (Monthly restaurant metrics)
- `city_performance` (City-level metrics)

**Views**:
- `vw_order_details` - Complete order information
- `vw_daily_kpis` - Daily performance metrics
- `vw_restaurant_summary` - Restaurant performance
- `vw_city_summary` - City-level summary
- `vw_customer_segments` - Customer segmentation

---


---

## 📊 streamlit Dashboard Components

### Page 1: Executive Summary
- Total Orders Card
- Total Revenue Card
- Avg Order Value Card
- Cancellation Rate Gauge
- Revenue Trend (Line Chart)
- Orders by City (Map)
- Top Cuisines (Bar Chart)

### Page 2: Customer Analytics
- Customer Segmentation (Pie Chart)
- Age Group Analysis (Column Chart)
- Payment Mode Distribution (Donut Chart)
- Weekend vs Weekday (Clustered Bar)
- Customer Lifetime Value (Table)

### Page 3: Delivery Performance
- Avg Delivery Time by City (Bar Chart)
- Distance vs Time Scatter Plot
- Delivery Rating Distribution (Column Chart)
- Delayed Orders % (KPI)
- Performance by Hour (Heat Map)

### Page 4: Restaurant Performance
- Top 10 Restaurants (Table)
- Cuisine Popularity (Tree Map)
- Restaurant Ratings (Histogram)
- Cancellation by Restaurant (Bar Chart)

### Filters/Slicers
- Date Range Slicer
- City Multi-Select
- Order Status Filter
- Cuisine Type Filter

---

## 🎓 Key Learnings & Skills

### Data Analytics Skills
✅ Data Cleaning & Preprocessing
✅ Handling Missing Values & Outliers
✅ Feature Engineering
✅ Exploratory Data Analysis (EDA)
✅ Statistical Analysis
✅ Data Validation

### Technical Skills
✅ Python (Pandas, NumPy)
✅ SQL (MySQL)
✅ Database Design (Star Schema)
✅ SQLAlchemy (ORM)
✅ Data Visualization (Matplotlib, Seaborn)
✅ Power BI Dashboard Development

### Business Skills
✅ KPI Design
✅ Business Intelligence
✅ Data Storytelling
✅ Insight Generation
✅ Decision Support

---



**Issue 1: MySQL Connection Error**
```
Solution: 
- Verify MySQL server is running
- Check credentials in DB_CONFIG
- Ensure database exists: CREATE DATABASE food_delivery_db;
```

**Issue 2: Missing Python Packages**
```
Solution:
pip install --upgrade pandas numpy sqlalchemy pymysql
```

**Issue 3: Data Import Errors**
```
Solution:
- Check file path in scripts
- Verify CSV encoding (UTF-8)
- Ensure sufficient memory for large dataset
```

**Issue 4: Power BI MySQL Connection**
```
Solution:
- Install MySQL ODBC Driver
- Use correct connection string
- Enable Power BI to access local MySQL
```

---

## 📈 Business Recommendations

Based on analysis, here are key recommendations:

### 1. Reduce Delivery Times
- Focus on high-delay areas
- Optimize delivery routes
- Add more delivery partners in peak hours

### 2. Improve Restaurant Performance
- Work with underperforming restaurants
- Reduce cancellation rates
- Enhance quality standards

### 3. Customer Retention
- Target high-value customer segments
- Personalized promotions
- Loyalty programs for frequent customers

### 4. Revenue Optimization
- Strategic discounting
- Focus on high-margin cuisines
- Expand in high-revenue cities

### 5. Operational Efficiency
- Peak hour demand forecasting
- Dynamic pricing strategies
- Delivery partner incentives

---

## 🚀 Future Enhancements

- [ ] Implement Machine Learning models for:
  - Delivery time prediction
  - Customer churn prediction
  - Demand forecasting
- [ ] Real-time dashboard with live data
- [ ] Automated email reports
- [ ] Mobile app integration
- [ ] Sentiment analysis of customer reviews
- [ ] Geographic heat maps for delivery zones

---

## 📝 Project Evaluation Criteria

| Component | Weight | Description |
|-----------|--------|-------------|
| Data Cleaning & EDA | 35% | Quality of preprocessing and analysis |
| Data Analytics | 35% | Depth of insights and SQL queries |
| Visualization | 10% | Dashboard design and clarity |
| Documentation | 10% | Code comments and README |
| Reproducibility | 10% | Code organization and structure |

---

## 👥 Contributors

- **Project Lead**: [Your Name]
- **Data Analyst**: [Your Name]
- **Database Designer**: [Your Name]
- **BI Developer**: [Your Name]

---


---



*Happy Analyzing! 📊*
