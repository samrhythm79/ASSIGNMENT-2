import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
from sqlalchemy import create_engine

import warnings
warnings.filterwarnings('ignore')

st.set_page_config(layout="wide")
st.title("🍔 Online Food Delivery Analytics Dashboard")
@st.cache_data
def load_data():
    return pd.read_csv("C:/Users/SARVIN/Downloads/cleaned_food_delivery_dataset.csv")

df = load_data()

st.write("Shape:", df.shape)
st.write("Data Types:")
st.write(df.dtypes)




# Load dataset
df = pd.read_csv("C:/Users/SARVIN/Downloads/ONINE_FOOD_DELIVERY_ANALYSIS.csv")

# Check dataset size
df.shape
#Step 2: Data Understanding
df.info()

df.head()

#data cleaning and preprocessing
#check missing values
df.isnull().sum()



#data cleaning and preprocessing
#Prevents KeyError issues.


#  Check Missing Values
missing_data = pd.DataFrame({
    'Column': df.columns,
    'Missing_Count': df.isnull().sum(),
    'Missing_Percentage': (df.isnull().sum() / len(df) * 100).round(2)
})

missing_data = missing_data[missing_data['Missing_Count'] > 0] \
                .sort_values('Missing_Count', ascending=False)

print(missing_data)

# Handle Missing Values
#Numerical → Median
#Categorical → Mode

df['Delivery_Time_Min'].fillna(df['Delivery_Time_Min'].median(), inplace=True)
df['Order_Value'].fillna(df['Order_Value'].median(), inplace=True)

df['Cancellation_Reason'].fillna('Not Cancelled', inplace=True)




# Outlier Treatment (IQR Method)

#Example: order_value & delivery_time

def cap_outliers(column):
    Q1 = df[column].quantile(0.25)
    Q3 = df[column].quantile(0.75)
    IQR = Q3 - Q1
    
    lower = Q1 - 1.5 * IQR
    upper = Q3 + 1.5 * IQR
    
    df[column] = df[column].clip(lower, upper)

# Apply to important columns
cap_outliers('Order_Value')
cap_outliers('Delivery_Time_Min')

# Correct Invalid Values(ratings > 5, negative profit margin)
# Ratings must be between 0 and 5
df['Restaurant_Rating'] = df['Restaurant_Rating'].clip(0, 5)
df['Profit_Margin'] = df['Profit_Margin'].clip(lower=0)


# Profit margin should not be negative
if 'Profit_Margin' in df.columns:
    df.loc[df['Profit_Margin'] < 0, 'Profit_Margin'] = 0

#  Standardize Categorical Values
df['City'] = df['City'].str.title()
df['Order_Status'] = df['Order_Status'].str.strip().str.lower()


#  Ensure Logical Consistency

#Example: Cancelled orders should vs ratings

df.loc[df['Order_Status'] == 'cancelled', 'restaurant_rating'] = None


#  Convert Data Types
if 'order_date' in df.columns:
    df['order_date'] = pd.to_datetime(df['order_date'], errors='coerce')

if 'order_time' in df.columns:
    df['order_time'] = pd.to_datetime(df['order_time'], errors='coerce')

df.info()

#EDA Analysis & Code
#1️⃣ Distribution of Order Value & Delivery Time
df['Order_Value'].describe()
df[ 'Delivery_Time_Min'].describe()


#2️⃣ City-wise Order Analysis
df.groupby('City')['Order_ID'].count().sort_values(ascending=False)

#3️⃣ Cuisine-wise Demand
df.groupby('Cuisine_Type')['Order_ID'].count().sort_values(ascending=False)

#4️⃣ Weekend vs Weekday Demand
df.groupby('Order_Day')['Order_ID'].count()

#5️⃣ Distance vs Delivery Delay
df[['Distance_km', 'Delivery_Time_Min']].corr()

#6️⃣ Cancellation Reasons Analysis
df[df['Order_Status'] == 'Cancelled']['Cancellation_Reason'].value_counts()

#7️⃣ Correlation Analysis (Numeric Features)
df.corr(numeric_only=True)

import pandas as pd
#Step 5: Feature Engineering

#1️⃣ Order Day Type (Weekday / Weekend)


# Convert to datetime
df['Order_Date'] = pd.to_datetime(df['Order_Date'], errors='coerce')

# Create weekday/weekend column
df['Order_Day'] = df['Order_Date'].dt.dayofweek.apply(
    lambda x: 'Weekend' if x >= 5 else 'Weekday'
)


#2️⃣ Peak Hour Indicator
# Extract hour
df['order_hour'] = pd.to_datetime(df['Order_Time'], errors='coerce').dt.hour



# Create peak hour flag (1 = Peak, 0 = Non-peak)
df['peak_hour'] = df['order_hour'].apply(
    lambda x: 1 if (12 <= x <= 14) or (19 <= x <= 22) else 0
)


#3️⃣ Profit Margin Percentage
df['Profit_Margin_pct'] = (
    (df['Profit_Margin'] / df['Order_Value']) * 100
).round(2)


#4️⃣ Delivery Performance Categories
def delivery_category(time):
    if time <= 30:
        return 'Fast'
    elif time <= 45:
        return 'On-Time'
    else:
        return 'Delayed'

df['delivery_performance'] = df['Delivery_Time_Min'].apply(delivery_category)



#5️⃣ Customer Age Groups
def age_group(age):
    if age < 25:
        return 'Youth'
    elif age < 40:
        return 'Adult'
    else:
        return 'Senior'

df['customer_age_group'] = df['Customer_Age'].apply(age_group)

# EDA VISUALIZATIONS
    # =============================
st.subheader("📊 Exploratory Data Analysis")

col1, col2 = st.columns(2)

    # Distribution plots
with col1:
        st.write("Order Value Distribution")
        fig, ax = plt.subplots()
        sns.histplot(df['Order_Value'], kde=True, ax=ax)
        st.pyplot(fig)

with col2:
        st.write("Delivery Time Distribution")
        fig, ax = plt.subplots()
        sns.histplot(df['Delivery_Time_Min'], kde=True, ax=ax)
        st.pyplot(fig)

    # City Orders
        st.subheader("City-wise Orders")
        st.bar_chart(df['City'].value_counts())

    # Cuisine Orders
        st.subheader("Cuisine-wise Orders")
        st.bar_chart(df['Cuisine_Type'].value_counts())

    # Distance vs Delivery
        st.subheader("Distance vs Delivery Time")
        fig, ax = plt.subplots()
        sns.scatterplot(x='Distance_km', y='Delivery_Time_Min', data=df, ax=ax)
        st.pyplot(fig)

    # Cancellation Reasons
        st.subheader("Cancellation Reasons")
        fig, ax = plt.subplots()
        sns.countplot(y='Cancellation_Reason', data=df,
                  order=df['Cancellation_Reason'].value_counts().index, ax=ax)
        st.pyplot(fig)

    # Correlation Heatmap
        st.subheader("Correlation Heatmap")
        fig, ax = plt.subplots(figsize=(10,6))
        sns.heatmap(df.corr(numeric_only=True), annot=True, cmap="coolwarm", ax=ax)
        st.pyplot(fig)


# Save cleaned dataset
df.to_csv("cleaned_food_delivery_dataset.csv")

print("food_delivery_dataset!")



#load data
df_1=pd.read_csv("cleaned_food_delivery_data.csv")

#1️⃣ Distribution of Order Value & Delivery Time




import matplotlib.pyplot as plt

# Order Value Distribution
plt.figure()
plt.hist(df['Order_Value'], bins=30)
plt.title("Distribution of Order Value")
plt.xlabel("Order Value")
plt.ylabel("Frequency")
plt.show()

# Delivery Time Distribution
plt.figure()
plt.hist(df['Delivery_Time_Min'], bins=30)
plt.title("Distribution of Delivery Time")
plt.xlabel("Delivery Time (minutes)")
plt.ylabel("Frequency")
plt.show()




#2️⃣ City-wise Order Analysis



city_orders = df['City'].value_counts()

plt.figure()
city_orders.plot(kind='bar')
plt.title("City-wise Order Count")
plt.xlabel("City")
plt.ylabel("Number of Orders")
plt.show()




# 3️⃣ Cuisine-wise Order Analysis
cuisine_orders = df['Cuisine_Type'].value_counts()

plt.figure()
cuisine_orders.plot(kind='bar')
plt.title("Cuisine-wise Order Count")
plt.xlabel("Cuisine Type")
plt.ylabel("Number of Orders")
plt.show()




# 4️⃣ Weekend vs Weekday Demand




day_orders = df['Order_Day'].value_counts()

plt.figure()
day_orders.plot(kind='bar')
plt.title("Weekend vs Weekday Orders")
plt.xlabel("Day Type")
plt.ylabel("Number of Orders")
plt.show()




# 5️⃣ Distance vs Delivery Delay Relationship


plt.figure()
plt.scatter(df['Distance_km'], df['Delivery_Time_Min'])
plt.title("Distance vs Delivery Time")
plt.xlabel("Distance (km)")
plt.ylabel("Delivery Time (minutes)")
plt.show()



# 6️⃣ Cancellation Reasons Analysis
cancel_data = df[df['Order_Status'] == 'cancelled']

cancel_counts = cancel_data['Cancellation_Reason'].value_counts()

plt.figure()
cancel_counts.plot(kind='bar')
plt.title("Cancellation Reasons")
plt.xlabel("Reason")
plt.ylabel("Count")
plt.show()




# 7️⃣ Correlation Analysis (Numeric Features)
correlation_matrix = df.corr(numeric_only=True)

plt.figure()
plt.imshow(correlation_matrix)
plt.title("Correlation Matrix")
plt.colorbar()
plt.xticks(range(len(correlation_matrix.columns)), correlation_matrix.columns, rotation=90)
plt.yticks(range(len(correlation_matrix.columns)), correlation_matrix.columns)
plt.show()



# Summary
print("Rows:", df.shape[0])
print("Columns:", df.shape[1])
print(df.head())


# ---------------------------
# MySQL Database Connection
# ---------------------------
DB_HOST = "localhost"
DB_USER = "root"
DB_PASS = "priyadharshini123"
DB_NAME = "food_delivery_db"

engine = create_engine(f"mysql+pymysql://{DB_USER}:{DB_PASS}@{DB_HOST}/{DB_NAME}")
#sql queries -------
query = "SELECT * FROM cleaned_food_delivery_dataset"
df = pd.read_sql(query, engine)
st.dataframe(df)
queries = {

# -----------------------------
# CUSTOMER & ORDER ANALYSIS
# -----------------------------

"top_spending_customers": """
SELECT Customer_ID, SUM(Order_Value) AS total_spent
FROM cleaned_food_delivery_dataset
GROUP BY Customer_ID
ORDER BY total_spent DESC
LIMIT 10;
""",

"age_group_vs_order_value": """
SELECT Customer_Age_Group, AVG(Order_Value) AS avg_order_value
FROM cleaned_food_delivery_dataset
GROUP BY Customer_Age_Group;
""",

"weekday_vs_weekend_orders": """
SELECT Order_Day_Type, COUNT(*) AS total_orders
FROM cleaned_food_delivery_dataset
GROUP BY Order_Day_Type;
""",


# -----------------------------
# REVENUE & PROFIT ANALYSIS
# -----------------------------

"monthly_revenue_trend": """
SELECT DATE_FORMAT(Order_Date, '%Y-%m') AS month,
       SUM(Order_Value) AS total_revenue
FROM cleaned_food_delivery_dataset
GROUP BY month
ORDER BY month;
""",

"discount_vs_profit": """
SELECT Discount_Applied,
       AVG(Profit_Margin_Percentage) AS avg_profit
FROM cleaned_food_delivery_dataset
GROUP BY Discount_Applied;
""",

"high_revenue_cities": """
SELECT City, SUM(Order_Value) AS revenue
FROM cleaned_food_delivery_dataset
GROUP BY City
ORDER BY revenue DESC;
""",


# -----------------------------
# DELIVERY PERFORMANCE
# -----------------------------

"avg_delivery_time_by_city": """
SELECT City, AVG(Delivery_Time_Minutes) AS avg_delivery_time
FROM cleaned_food_delivery_dataset
GROUP BY City;
""",

"distance_vs_delay": """
SELECT Delivery_Distance_KM,
       AVG(Delivery_Time_Minutes) AS avg_time
FROM cleaned_food_delivery_dataset
GROUP BY Delivery_Distance_KM
ORDER BY Delivery_Distance_KM;
""",

"rating_vs_delivery_time": """
SELECT Delivery_Rating,
       AVG(Delivery_Time_Minutes) AS avg_delivery_time
FROM cleaned_food_delivery_dataset
GROUP BY Delivery_Rating;
""",


# -----------------------------
# RESTAURANT PERFORMANCE
# -----------------------------

"top_rated_restaurants": """
SELECT Restaurant_Name,
       AVG(Delivery_Rating) AS avg_rating
FROM cleaned_food_delivery_dataset
GROUP BY Restaurant_Name
ORDER BY avg_rating DESC
LIMIT 10;
""",

"cancellation_rate_by_restaurant": """
SELECT Restaurant_Name,
       COUNT(*) AS total_orders,
       SUM(CASE WHEN Order_Status='Cancelled' THEN 1 ELSE 0 END) AS cancelled_orders
FROM cleaned_food_delivery_dataset
GROUP BY Restaurant_Name;
""",

"cuisine_performance": """
SELECT Cuisine_Type,
       AVG(Order_Value) AS avg_order_value,
       COUNT(*) AS total_orders
FROM cleaned_food_delivery_dataset
GROUP BY Cuisine_Type;
""",


# -----------------------------
# OPERATIONAL INSIGHTS
# -----------------------------

"peak_hour_demand": """
SELECT Peak_Hour_Indicator,
       COUNT(*) AS total_orders
FROM cleaned_food_delivery_dataset
GROUP BY Peak_Hour_Indicator;
""",

"payment_mode_preferences": """
SELECT Payment_Mode,
       COUNT(*) AS usage_count
FROM cleaned_food_delivery_dataset
GROUP BY Payment_Mode
ORDER BY usage_count DESC;
""",

"cancellation_reason_analysis": """
SELECT Cancellation_Reason,
       COUNT(*) AS total_cancellations
FROM cleaned_food_delivery_dataset
WHERE Order_Status='Cancelled'
GROUP BY Cancellation_Reason
ORDER BY total_cancellations DESC;
"""
}


# ---------------- STREAMLIT UI ----------------
st.title("food_delivery_db SQL Query Dashboard")
st.write("Select any problem statement (1–15) to run the corresponding SQL query.")

# ---------------- DROPDOWN ----------------
task = st.selectbox("Choose Task Number", list(queries.keys()))

# ---------------- RUN BUTTON ----------------
if st.button("Run Query"):
    query = queries[task]
    df = pd.read_sql(query,engine)

    st.subheader(f"Results for: {task}")
    st.dataframe(df, use_container_width=True)