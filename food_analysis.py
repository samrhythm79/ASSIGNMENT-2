"""
Online Food Delivery Analysis - Streamlit Dashboard
Interactive web dashboard for business insights
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

# ============================================================================
# PAGE CONFIGURATION
# ============================================================================
st.set_page_config(
    page_title="Food Delivery Analytics Dashboard",
    page_icon="🍔",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================================
# CUSTOM CSS STYLING
# ============================================================================
st.markdown("""
    <style>
    .main {
        padding: 0rem 1rem;
    }
    .stMetric {
        background-color: #f0f2f6;
        padding: 15px;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .stMetric:hover {
        box-shadow: 0 4px 8px rgba(0,0,0,0.15);
        transform: translateY(-2px);
        transition: all 0.3s ease;
    }
    h1 {
        color: #1E2761;
        font-weight: 700;
    }
    h2 {
        color: #028090;
        font-weight: 600;
    }
    h3 {
        color: #00A896;
        font-weight: 600;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 24px;
    }
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        padding-left: 20px;
        padding-right: 20px;
        background-color: #f0f2f6;
        border-radius: 10px 10px 0px 0px;
    }
    .stTabs [aria-selected="true"] {
        background-color: #028090;
        color: white;
    }
    div[data-testid="stExpander"] {
        background-color: #f8f9fa;
        border-radius: 10px;
        border: 1px solid #e0e0e0;
    }
    </style>
    """, unsafe_allow_html=True)

# ============================================================================
# DATA LOADING FUNCTION
# ============================================================================
@st.cache_data
def load_data():
    """Load and cache the cleaned dataset"""
    try:
        # Try to load from outputs first
        df = pd.read_csv('cleaned_food_delivery_data.csv')
    except:
        try:
            # Fall back to uploads
            df = pd.read_csv('/mnt/user-data/uploads/ONINE_FOOD_DELIVERY_ANALYSIS.csv')
            st.warning("Loading raw data. For best results, run data cleaning script first.")
        except Exception as e:
            st.error(f"Error loading data: {e}")
            return None
    
    # Convert date column
    if 'Order_Date' in df.columns:
        df['Order_Date'] = pd.to_datetime(df['Order_Date'], errors='coerce')
    
    return df

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================
def format_currency(value):
    """Format number as Indian Rupees"""
    return f"₹{value:,.0f}"

def format_percentage(value):
    """Format number as percentage"""
    return f"{value:.1f}%"

def create_metric_card(col, label, value, delta=None, delta_color="normal"):
    """Create a styled metric card"""
    with col:
        st.metric(label=label, value=value, delta=delta, delta_color=delta_color)

# ============================================================================
# LOAD DATA
# ============================================================================
df = load_data()

if df is None:
    st.stop()

# ============================================================================
# SIDEBAR - FILTERS
# ============================================================================
st.sidebar.image("https://img.icons8.com/color/96/000000/food-delivery.png", width=80)
st.sidebar.title("🍔 Food Delivery Analytics")
st.sidebar.markdown("---")

st.sidebar.header("📊 Filters")

# Date Range Filter
if 'Order_Date' in df.columns and df['Order_Date'].notna().any():
    date_range = st.sidebar.date_input(
        "Select Date Range",
        value=(df['Order_Date'].min(), df['Order_Date'].max()),
        min_value=df['Order_Date'].min(),
        max_value=df['Order_Date'].max()
    )
    
    # Filter data by date
    if len(date_range) == 2:
        mask = (df['Order_Date'] >= pd.to_datetime(date_range[0])) & \
               (df['Order_Date'] <= pd.to_datetime(date_range[1]))
        filtered_df = df[mask].copy()
    else:
        filtered_df = df.copy()
else:
    filtered_df = df.copy()

# City Filter
if 'City' in filtered_df.columns:
    cities = ['All'] + sorted(filtered_df['City'].dropna().unique().tolist())
    selected_city = st.sidebar.selectbox("Select City", cities)
    
    if selected_city != 'All':
        filtered_df = filtered_df[filtered_df['City'] == selected_city]

# Order Status Filter
if 'Order_Status' in filtered_df.columns:
    status_options = ['All'] + sorted(filtered_df['Order_Status'].dropna().unique().tolist())
    selected_status = st.sidebar.selectbox("Order Status", status_options)
    
    if selected_status != 'All':
        filtered_df = filtered_df[filtered_df['Order_Status'] == selected_status]

# Cuisine Filter
if 'Cuisine_Type' in filtered_df.columns:
    cuisines = ['All'] + sorted(filtered_df['Cuisine_Type'].dropna().unique().tolist())
    selected_cuisine = st.sidebar.multiselect(
        "Select Cuisine Type(s)", 
        cuisines,
        default=['All']
    )
    
    if 'All' not in selected_cuisine:
        filtered_df = filtered_df[filtered_df['Cuisine_Type'].isin(selected_cuisine)]

st.sidebar.markdown("---")
st.sidebar.info(f"**Showing {len(filtered_df):,} of {len(df):,} orders**")

# ============================================================================
# MAIN DASHBOARD
# ============================================================================

# Header
st.title("🍔 Online Food Delivery Analytics Dashboard")
st.markdown("### Real-time Business Intelligence & Insights")
st.markdown("---")

# ============================================================================
# KEY METRICS ROW
# ============================================================================
col1, col2, col3, col4, col5,col6,col7 = st.columns(7)
cols = st.columns(7)

#one by one metrics with formatting and deltas where applicable
current_orders = df.shape[0]
previous_orders = 95000   # example last month value

delta_orders = current_orders - previous_orders

st.metric(
    label="📦 Total Orders",
    value=f"{current_orders:,}",
    delta=f"{delta_orders:,}"
)




# Total Orders
total_orders = len(filtered_df)
create_metric_card(col1, "📦 Total Orders", f"{total_orders:,}")

# Total Revenue
if 'Final_Amount' in filtered_df.columns:
    total_revenue = filtered_df['Final_Amount'].sum()
    create_metric_card(col2, "💰 Total Revenue", format_currency(total_revenue))

# Average Order Value
if 'Order_Value' in filtered_df.columns:
    avg_order_value = filtered_df['Order_Value'].mean()
    create_metric_card(col3, "🛒 Avg Order Value", format_currency(avg_order_value))

# Cancellation Rate
if 'Order_Status' in filtered_df.columns:
    cancelled = len(filtered_df[filtered_df['Order_Status'] == 'Cancelled'])
    cancellation_rate = (cancelled / total_orders * 100) if total_orders > 0 else 0
    create_metric_card(col4, "❌ Cancellation Rate", format_percentage(cancellation_rate))

# Average Delivery Time
if 'Delivery_Time_Min' in filtered_df.columns:
    avg_delivery_time = filtered_df['Delivery_Time_Min'].mean()
    create_metric_card(col5, "🚚 Avg Delivery Time", f"{avg_delivery_time:.0f} min")

#average delivery rating
if 'Delivery_Rating' in filtered_df.columns:
    avg_delivery_rating = filtered_df['Delivery_Rating'].mean()
    create_metric_card(col6, "⭐ Avg Delivery Rating", f"{avg_delivery_rating:.2f}/5")

#average profit margin
if 'Profit_Margin' in filtered_df.columns:
    avg_profit_margin = filtered_df['Profit_Margin'].mean()
    create_metric_card(col7, "📈 Avg Profit Margin", f"{avg_profit_margin:.2f}%")


st.markdown("---")

# ============================================================================
# TABS FOR DIFFERENT SECTIONS
# ============================================================================
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📊 Executive Summary", 
    "👥 Customer Analytics", 
    "🚚 Delivery Performance",
    "🍽️ Restaurant Insights",
    "💡 Advanced Analytics"
])

# ============================================================================
# TAB 1: EXECUTIVE SUMMARY
# ============================================================================
with tab1:
    st.header("Executive Summary")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📈 Revenue Trend Over Time")
        if 'Order_Date' in filtered_df.columns and 'Final_Amount' in filtered_df.columns:
            # Monthly revenue trend
            filtered_df['YearMonth'] = filtered_df['Order_Date'].dt.to_period('M').astype(str)
            monthly_revenue = filtered_df.groupby('YearMonth')['Final_Amount'].sum().reset_index()
            
            fig = px.line(
                monthly_revenue, 
                x='YearMonth', 
                y='Final_Amount',
                title='Monthly Revenue Trend',
                labels={'YearMonth': 'Month', 'Final_Amount': 'Revenue (₹)'}
            )
            fig.update_traces(line_color='#028090', line_width=3)
            fig.update_layout(height=350, hovermode='x unified')
            st.plotly_chart(fig, use_container_width=True)
        
        st.subheader("🏙️ Orders by City")
        if 'City' in filtered_df.columns:
            city_orders = filtered_df['City'].value_counts().reset_index()
            city_orders.columns = ['City', 'Orders']
            
            fig = px.bar(
                city_orders.head(10),
                x='Orders',
                y='City',
                orientation='h',
                title='Top 10 Cities by Order Count',
                color='Orders',
                color_continuous_scale='Teal'
            )
            fig.update_layout(height=350, showlegend=False)
            st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("📦 Order Status Distribution")
        if 'Order_Status' in filtered_df.columns:
            status_counts = filtered_df['Order_Status'].value_counts().reset_index()
            status_counts.columns = ['Status', 'Count']
            
            fig = px.pie(
                status_counts,
                values='Count',
                names='Status',
                title='Order Status Breakdown',
                color_discrete_sequence=['#028090', '#FF6B6B', '#4ECDC4']
            )
            fig.update_traces(textposition='inside', textinfo='percent+label')
            fig.update_layout(height=350)
            st.plotly_chart(fig, use_container_width=True)
        
        st.subheader("🍜 Cuisine Popularity")
        if 'Cuisine_Type' in filtered_df.columns:
            cuisine_orders = filtered_df['Cuisine_Type'].value_counts().head(8).reset_index()
            cuisine_orders.columns = ['Cuisine', 'Orders']
            
            fig = px.bar(
                cuisine_orders,
                x='Cuisine',
                y='Orders',
                title='Top Cuisines by Order Count',
                color='Orders',
                color_continuous_scale='Teal'
            )
            fig.update_layout(height=350, showlegend=False)
            st.plotly_chart(fig, use_container_width=True)
    
    # Payment Mode Analysis
    st.subheader("💳 Payment Mode Preferences")
    col1, col2, col3 = st.columns(3)
    
    if 'Payment_Mode' in filtered_df.columns:
        payment_dist = filtered_df['Payment_Mode'].value_counts()
        
        for idx, (mode, count) in enumerate(payment_dist.items()):
            col = [col1, col2, col3][idx % 3]
            with col:
                percentage = (count / len(filtered_df) * 100)
                st.metric(
                    label=f"{mode}",
                    value=f"{count:,} orders",
                    delta=f"{percentage:.1f}%"
                )

# ============================================================================
# TAB 2: CUSTOMER ANALYTICS
# ============================================================================
with tab2:
    st.header("Customer Analytics")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("👤 Customer Demographics")
        
        # Age Group Analysis
        if 'Age_Group' in filtered_df.columns and 'Order_Value' in filtered_df.columns:
            age_analysis = filtered_df.groupby('Age_Group').agg({
                'Order_ID': 'count',
                'Order_Value': 'mean',
                'Final_Amount': 'sum'
            }).reset_index()
            age_analysis.columns = ['Age Group', 'Orders', 'Avg Order Value', 'Total Revenue']
            
            fig = make_subplots(specs=[[{"secondary_y": True}]])
            
            fig.add_trace(
                go.Bar(name='Orders', x=age_analysis['Age Group'], y=age_analysis['Orders'],
                       marker_color='#028090'),
                secondary_y=False,
            )
            
            fig.add_trace(
                go.Scatter(name='Avg Order Value', x=age_analysis['Age Group'], 
                          y=age_analysis['Avg Order Value'], mode='lines+markers',
                          marker_color='#FF6B6B', line=dict(width=3)),
                secondary_y=True,
            )
            
            fig.update_xaxes(title_text="Age Group")
            fig.update_yaxes(title_text="Number of Orders", secondary_y=False)
            fig.update_yaxes(title_text="Average Order Value (₹)", secondary_y=True)
            fig.update_layout(title="Orders and Average Value by Age Group", height=400)
            
            st.plotly_chart(fig, use_container_width=True)
        
        # Gender Distribution
        if 'Customer_Gender' in filtered_df.columns:
            st.subheader("⚧ Gender Distribution")
            gender_dist = filtered_df['Customer_Gender'].value_counts().reset_index()
            gender_dist.columns = ['Gender', 'Count']
            
            fig = px.pie(
                gender_dist,
                values='Count',
                names='Gender',
                title='Customer Gender Distribution',
                color_discrete_sequence=['#028090', '#00A896', '#02C39A']
            )
            fig.update_layout(height=300)
            st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("📅 Order Day Patterns")
        
        # Weekend vs Weekday
        if 'Order_Day' in filtered_df.columns:
            day_analysis = filtered_df.groupby('Order_Day').agg({
                'Order_ID': 'count',
                'Order_Value': 'mean',
                'Delivery_Time_Min': 'mean'
            }).reset_index()
            day_analysis.columns = ['Day Type', 'Orders', 'Avg Order Value', 'Avg Delivery Time']
            
            fig = go.Figure(data=[
                go.Bar(name='Orders', x=day_analysis['Day Type'], y=day_analysis['Orders'],
                       marker_color='#028090'),
            ])
            fig.update_layout(title="Weekend vs Weekday Orders", height=300)
            st.plotly_chart(fig, use_container_width=True)
        
        # Peak Hour Analysis
        if 'Peak_Hour' in filtered_df.columns:
            st.subheader("⏰ Peak Hour Impact")
            peak_analysis = filtered_df.groupby('Peak_Hour').agg({
                'Order_ID': 'count',
                'Order_Value': 'mean'
            }).reset_index()
            peak_analysis.columns = ['Peak Hour', 'Orders', 'Avg Order Value']
            peak_analysis['Peak Hour'] = peak_analysis['Peak Hour'].map({True: 'Peak Hours', False: 'Non-Peak'})
            
            col_a, col_b = st.columns(2)
            with col_a:
                peak_orders = peak_analysis[peak_analysis['Peak Hour'] == 'Peak Hours']['Orders'].values[0]
                st.metric("Peak Hour Orders", f"{peak_orders:,}")
            with col_b:
                if len(peak_analysis) > 1:
                    non_peak_orders = peak_analysis[peak_analysis['Peak Hour'] == 'Non-Peak']['Orders'].values[0]
                    st.metric("Non-Peak Orders", f"{non_peak_orders:,}")
        
        # Top Spending Customers
        st.subheader("💎 Top 10 Customers by Revenue")
        if 'Customer_ID' in filtered_df.columns and 'Final_Amount' in filtered_df.columns:
            top_customers = filtered_df.groupby('Customer_ID').agg({
                'Order_ID': 'count',
                'Final_Amount': 'sum'
            }).reset_index()
            top_customers.columns = ['Customer ID', 'Orders', 'Total Spent']
            top_customers = top_customers.sort_values('Total Spent', ascending=False).head(10)
            
            st.dataframe(
                top_customers.style.format({
                    'Orders': '{:,.0f}',
                    'Total Spent': '₹{:,.0f}'
                }),
                use_container_width=True
            )

# ============================================================================
# TAB 3: DELIVERY PERFORMANCE
# ============================================================================
with tab3:
    st.header("Delivery Performance Analysis")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🚚 Delivery Time Distribution")
        if 'Delivery_Time_Min' in filtered_df.columns:
            fig = px.histogram(
                filtered_df,
                x='Delivery_Time_Min',
                nbins=30,
                title='Distribution of Delivery Times',
                labels={'Delivery_Time_Min': 'Delivery Time (minutes)', 'count': 'Frequency'},
                color_discrete_sequence=['#028090']
            )
            fig.update_layout(height=350)
            st.plotly_chart(fig, use_container_width=True)
        
        st.subheader("🏙️ Delivery Time by City")
        if 'City' in filtered_df.columns and 'Delivery_Time_Min' in filtered_df.columns:
            city_delivery = filtered_df.groupby('City')['Delivery_Time_Min'].mean().sort_values(ascending=True).head(10).reset_index()
            
            fig = px.bar(
                city_delivery,
                x='Delivery_Time_Min',
                y='City',
                orientation='h',
                title='Average Delivery Time by City (Top 10)',
                labels={'Delivery_Time_Min': 'Avg Time (min)', 'City': 'City'},
                color='Delivery_Time_Min',
                color_continuous_scale='RdYlGn_r'
            )
            fig.update_layout(height=350)
            st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("📏 Distance vs Delivery Time")
        if 'Distance_km' in filtered_df.columns and 'Delivery_Time_Min' in filtered_df.columns:
            # Sample data for better visualization
            sample_df = filtered_df.dropna(subset=['Distance_km', 'Delivery_Time_Min']).sample(min(1000, len(filtered_df)))
            
            fig = px.scatter(
                sample_df,
                x='Distance_km',
                y='Delivery_Time_Min',
                title='Delivery Time vs Distance Correlation',
                labels={'Distance_km': 'Distance (km)', 'Delivery_Time_Min': 'Time (min)'},
                color='Delivery_Time_Min',
                color_continuous_scale='Viridis',
                opacity=0.6
            )
            
            # Add trend line
            from scipy import stats
            slope, intercept, r_value, p_value, std_err = stats.linregress(
                sample_df['Distance_km'].fillna(0), 
                sample_df['Delivery_Time_Min'].fillna(0)
            )
            line_x = np.array([sample_df['Distance_km'].min(), sample_df['Distance_km'].max()])
            line_y = slope * line_x + intercept
            
            fig.add_trace(go.Scatter(
                x=line_x, y=line_y,
                mode='lines',
                name=f'Trend (r²={r_value**2:.2f})',
                line=dict(color='red', width=2, dash='dash')
            ))
            
            fig.update_layout(height=350)
            st.plotly_chart(fig, use_container_width=True)
        
        st.subheader("⭐ Delivery Ratings")
        if 'Delivery_Rating' in filtered_df.columns:
            rating_dist = filtered_df['Delivery_Rating'].value_counts().sort_index().reset_index()
            rating_dist.columns = ['Rating', 'Count']
            
            fig = px.bar(
                rating_dist,
                x='Rating',
                y='Count',
                title='Distribution of Delivery Ratings',
                color='Count',
                color_continuous_scale='Teal'
            )
            fig.update_layout(height=350, showlegend=False)
            st.plotly_chart(fig, use_container_width=True)
    
    # Delivery Performance Metrics
    st.subheader("📊 Delivery Performance Metrics")
    col1, col2, col3, col4 = st.columns(4)
    
    if 'Delivery_Time_Min' in filtered_df.columns:
        with col1:
            fast_deliveries = len(filtered_df[filtered_df['Delivery_Time_Min'] < 30])
            st.metric("Fast Deliveries (<30 min)", f"{fast_deliveries:,}",
                     delta=f"{fast_deliveries/len(filtered_df)*100:.1f}%")
        
        with col2:
            normal_deliveries = len(filtered_df[(filtered_df['Delivery_Time_Min'] >= 30) & 
                                                (filtered_df['Delivery_Time_Min'] <= 60)])
            st.metric("Normal Deliveries (30-60 min)", f"{normal_deliveries:,}",
                     delta=f"{normal_deliveries/len(filtered_df)*100:.1f}%")
        
        with col3:
            slow_deliveries = len(filtered_df[filtered_df['Delivery_Time_Min'] > 60])
            st.metric("Slow Deliveries (>60 min)", f"{slow_deliveries:,}",
                     delta=f"{slow_deliveries/len(filtered_df)*100:.1f}%")
    
    if 'Delivery_Rating' in filtered_df.columns:
        with col4:
            avg_rating = filtered_df['Delivery_Rating'].mean()
            st.metric("Average Rating", f"{avg_rating:.2f}/5",
                     delta="⭐" * int(round(avg_rating)))

# ============================================================================
# TAB 4: RESTAURANT INSIGHTS
# ============================================================================
with tab4:
    st.header("Restaurant Performance Insights")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🏆 Top 10 Restaurants by Orders")
        if 'Restaurant_Name' in filtered_df.columns:
            top_restaurants = filtered_df.groupby('Restaurant_Name').agg({
                'Order_ID': 'count',
                'Restaurant_Rating': 'mean',
                'Final_Amount': 'sum'
            }).reset_index()
            top_restaurants.columns = ['Restaurant', 'Orders', 'Avg Rating', 'Revenue']
            top_restaurants = top_restaurants.sort_values('Orders', ascending=False).head(10)
            
            fig = px.bar(
                top_restaurants,
                y='Restaurant',
                x='Orders',
                orientation='h',
                title='Top 10 Restaurants by Order Volume',
                color='Avg Rating',
                color_continuous_scale='RdYlGn',
                labels={'Orders': 'Number of Orders', 'Restaurant': 'Restaurant'}
            )
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True)
        
        st.subheader("📊 Restaurant Ratings Distribution")
        if 'Restaurant_Rating' in filtered_df.columns:
            fig = px.histogram(
                filtered_df,
                x='Restaurant_Rating',
                nbins=20,
                title='Distribution of Restaurant Ratings',
                color_discrete_sequence=['#00A896']
            )
            fig.update_layout(height=300)
            st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("🍽️ Cuisine Performance Analysis")
        if 'Cuisine_Type' in filtered_df.columns and 'Final_Amount' in filtered_df.columns:
            cuisine_performance = filtered_df.groupby('Cuisine_Type').agg({
                'Order_ID': 'count',
                'Final_Amount': 'sum',
                'Restaurant_Rating': 'mean'
            }).reset_index()
            cuisine_performance.columns = ['Cuisine', 'Orders', 'Revenue', 'Avg Rating']
            cuisine_performance = cuisine_performance.sort_values('Revenue', ascending=False)
            
            fig = px.treemap(
                cuisine_performance,
                path=['Cuisine'],
                values='Revenue',
                color='Avg Rating',
                color_continuous_scale='Teal',
                title='Cuisine Revenue Distribution'
            )
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True)
        
        st.subheader("❌ Cancellation Analysis by Restaurant")
        if 'Restaurant_Name' in filtered_df.columns and 'Order_Status' in filtered_df.columns:
            restaurant_cancellation = filtered_df.groupby('Restaurant_Name').agg({
                'Order_ID': 'count',
                'Order_Status': lambda x: (x == 'Cancelled').sum()
            }).reset_index()
            restaurant_cancellation.columns = ['Restaurant', 'Total Orders', 'Cancelled']
            restaurant_cancellation['Cancellation Rate'] = (
                restaurant_cancellation['Cancelled'] / restaurant_cancellation['Total Orders'] * 100
            )
            restaurant_cancellation = restaurant_cancellation[restaurant_cancellation['Total Orders'] >= 10]
            restaurant_cancellation = restaurant_cancellation.sort_values('Cancellation Rate', ascending=False).head(10)
            
            st.dataframe(
                restaurant_cancellation.style.format({
                    'Total Orders': '{:,.0f}',
                    'Cancelled': '{:,.0f}',
                    'Cancellation Rate': '{:.1f}%'
                }).background_gradient(subset=['Cancellation Rate'], cmap='Reds'),
                use_container_width=True
            )
    
    # Cancellation Reasons
    if 'Cancellation_Reason' in filtered_df.columns:
        st.subheader("📋 Cancellation Reasons")
        cancelled_df = filtered_df[filtered_df['Order_Status'] == 'Cancelled']
        if len(cancelled_df) > 0:
            cancellation_reasons = cancelled_df['Cancellation_Reason'].value_counts().reset_index()
            cancellation_reasons.columns = ['Reason', 'Count']
            
            col1, col2 = st.columns([2, 1])
            with col1:
                fig = px.bar(
                    cancellation_reasons,
                    x='Count',
                    y='Reason',
                    orientation='h',
                    title='Top Cancellation Reasons',
                    color='Count',
                    color_continuous_scale='Reds'
                )
                fig.update_layout(height=300)
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                st.dataframe(
                    cancellation_reasons.style.format({'Count': '{:,.0f}'}),
                    use_container_width=True
                )

# ============================================================================
# TAB 5: ADVANCED ANALYTICS
# ============================================================================
with tab5:
    st.header("Advanced Analytics & Insights")
    
    # Profit Analysis
    st.subheader("💰 Profit Margin Analysis")
    col1, col2 = st.columns(2)
    
    with col1:
        if 'Profit_Margin_Percent' in filtered_df.columns:
            fig = px.histogram(
                filtered_df,
                x='Profit_Margin_Percent',
                nbins=30,
                title='Distribution of Profit Margins',
                color_discrete_sequence=['#028090'],
                labels={'Profit_Margin_Percent': 'Profit Margin (%)'}
            )
            fig.update_layout(height=350)
            st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        if 'Profit_Margin_Percent' in filtered_df.columns and 'City' in filtered_df.columns:
            city_profit = filtered_df.groupby('City')['Profit_Margin_Percent'].mean().sort_values(ascending=False).head(10).reset_index()
            
            fig = px.bar(
                city_profit,
                x='City',
                y='Profit_Margin_Percent',
                title='Average Profit Margin by City (Top 10)',
                color='Profit_Margin_Percent',
                color_continuous_scale='Greens'
            )
            fig.update_layout(height=350)
            st.plotly_chart(fig, use_container_width=True)
    
    # Correlation Heatmap
    st.subheader("🔥 Feature Correlation Analysis")
    numeric_cols = filtered_df.select_dtypes(include=[np.number]).columns.tolist()
    if len(numeric_cols) > 1:
        corr_cols = ['Order_Value', 'Delivery_Time_Min', 'Distance_km', 'Delivery_Rating', 
                     'Restaurant_Rating', 'Profit_Margin_Percent']
        corr_cols = [col for col in corr_cols if col in numeric_cols]
        
        if len(corr_cols) > 1:
            correlation = filtered_df[corr_cols].corr()
            
            fig = px.imshow(
                correlation,
                text_auto='.2f',
                aspect='auto',
                color_continuous_scale='RdBu_r',
                title='Correlation Matrix of Key Metrics'
            )
            fig.update_layout(height=500)
            st.plotly_chart(fig, use_container_width=True)
    
    # Customer Segmentation
    st.subheader("👥 Customer Segmentation (RFM Analysis)")
    
    if all(col in filtered_df.columns for col in ['Customer_ID', 'Order_Date', 'Final_Amount']):
        # Calculate RFM metrics
        rfm_df = filtered_df.groupby('Customer_ID').agg({
            'Order_Date': lambda x: (pd.Timestamp.now() - x.max()).days,
            'Order_ID': 'count',
            'Final_Amount': 'sum'
        }).reset_index()
        rfm_df.columns = ['Customer_ID', 'Recency', 'Frequency', 'Monetary']
        
        # Create segments
        rfm_df['R_Score'] = pd.qcut(rfm_df['Recency'], 4, labels=[4, 3, 2, 1], duplicates='drop')
        rfm_df['F_Score'] = pd.qcut(rfm_df['Frequency'].rank(method='first'), 4, labels=[1, 2, 3, 4], duplicates='drop')
        rfm_df['M_Score'] = pd.qcut(rfm_df['Monetary'], 4, labels=[1, 2, 3, 4], duplicates='drop')
        
        rfm_df['RFM_Score'] = rfm_df['R_Score'].astype(str) + rfm_df['F_Score'].astype(str) + rfm_df['M_Score'].astype(str)
        
        # Segment customers
        def segment_customer(score):
            r, f, m = int(score[0]), int(score[1]), int(score[2])
            if r >= 3 and f >= 3 and m >= 3:
                return 'Champions'
            elif r >= 3 and f >= 2:
                return 'Loyal Customers'
            elif r >= 3:
                return 'Potential Loyalists'
            elif f >= 3:
                return 'At Risk'
            else:
                return 'Lost'
        
        rfm_df['Segment'] = rfm_df['RFM_Score'].apply(segment_customer)
        
        col1, col2 = st.columns(2)
        
        with col1:
            segment_counts = rfm_df['Segment'].value_counts().reset_index()
            segment_counts.columns = ['Segment', 'Count']
            
            fig = px.pie(
                segment_counts,
                values='Count',
                names='Segment',
                title='Customer Segmentation Distribution',
                color_discrete_sequence=px.colors.sequential.Teal
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            segment_stats = rfm_df.groupby('Segment').agg({
                'Recency': 'mean',
                'Frequency': 'mean',
                'Monetary': 'mean'
            }).reset_index()
            
            st.dataframe(
                segment_stats.style.format({
                    'Recency': '{:.0f} days',
                    'Frequency': '{:.1f} orders',
                    'Monetary': '₹{:,.0f}'
                }),
                use_container_width=True
            )


