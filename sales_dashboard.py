import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import numpy as np

# Page settings
st.set_page_config(
    page_title="Sales Insights Dashboard",
    page_icon="📊",
    layout="wide"
)

# Title
st.title("📊 Sales Insights Dashboard")
st.markdown("By Aslan Akhundov")


@st.cache_data
def generate_sample_data():
    
    np.random.seed(42)
    dates = pd.date_range(start='2024-01-01', end='2024-03-31', freq='D')
    
    data = []
    for date in dates:
        for product in ['MacBook', 'iPhone', 'iPad', 'AirPods']:
            sales = np.random.randint(1, 20)
            revenue = sales * np.random.randint(100, 1000)
            profit = revenue * np.random.uniform(0.1, 0.3)
            
            data.append({
                'date': date,
                'product': product,
                'category': 'Electronics',
                'sales': sales,
                'revenue': revenue,
                'profit': profit,
                'region': np.random.choice(['Europe', 'North America', 'Asia', 'Middle East'])
            })
    
    return pd.DataFrame(data)

# Load data
df = generate_sample_data()

# Sidebar - Filtreler
st.sidebar.header("🔧 Filters")

# Date filter
date_range = st.sidebar.date_input(
    "Select Date Range",
    value=(df['date'].min(), df['date'].max()),
    min_value=df['date'].min(),
    max_value=df['date'].max()
)

# Product Filter
selected_products = st.sidebar.multiselect(
    "Select Products",
    options=df['product'].unique(),
    default=df['product'].unique()
)

# Regional Filter
selected_regions = st.sidebar.multiselect(
    "Select Regions",
    options=df['region'].unique(),
    default=df['region'].unique()
)

# Filter data
filtered_df = df[
    (df['date'].between(pd.to_datetime(date_range[0]), pd.to_datetime(date_range[1]))) &
    (df['product'].isin(selected_products)) &
    (df['region'].isin(selected_regions))
]

# Metrics
st.header("📈 Key Performance Indicators")

col1, col2, col3, col4 = st.columns(4)

with col1:
    total_sales = filtered_df['sales'].sum()
    st.metric("Total Sales", f"{total_sales:,}")

with col2:
    total_revenue = filtered_df['revenue'].sum()
    st.metric("Total Revenue", f"${total_revenue:,.0f}")

with col3:
    total_profit = filtered_df['profit'].sum()
    st.metric("Total Profit", f"${total_profit:,.0f}")

with col4:
    avg_profit_margin = (filtered_df['profit'].sum() / filtered_df['revenue'].sum()) * 100
    st.metric("Avg Profit Margin", f"{avg_profit_margin:.1f}%")

# Graphics
st.header("📊 Sales Insights")

# Tablar
tab1, tab2, tab3 = st.tabs(["Sales Trend", "Product Performance", "Regional Analysis"])

with tab1:
    
    monthly_sales = filtered_df.groupby(pd.Grouper(key='date', freq='ME'))['sales'].sum().reset_index()
    fig_trend = px.line(monthly_sales, x='date', y='sales', 
                        title="Monthly Sales Trend",
                        labels={'sales': 'Sales Quantity', 'date': 'Month'})
    st.plotly_chart(fig_trend, use_container_width=True)

with tab2:
    # Product performance
    product_performance = filtered_df.groupby('product').agg({
        'sales': 'sum',
        'revenue': 'sum',
        'profit': 'sum'
    }).reset_index()
    
    col1, col2 = st.columns(2)
    
    with col1:
        fig_products = px.bar(product_performance, x='product', y='sales',
                             title="Sales by Product")
        st.plotly_chart(fig_products, use_container_width=True)
    
    with col2:
        fig_revenue = px.pie(product_performance, values='revenue', names='product',
                            title="Revenue Distribution")
        st.plotly_chart(fig_revenue, use_container_width=True)

with tab3:
    # Regional analysis
    regional_sales = filtered_df.groupby('region').agg({
        'sales': 'sum',
        'revenue': 'sum'
    }).reset_index()
    
    fig_region = px.bar(regional_sales, x='region', y='revenue',
                       title="Revenue by Region",
                       color='region')
    st.plotly_chart(fig_region, use_container_width=True)

# Data Table
st.header("📋 Sales Data")
st.dataframe(filtered_df.sort_values('date', ascending=False).head(20), 
             use_container_width=True)

# download button
csv = filtered_df.to_csv(index=False)
st.download_button(
    label="📥 Download Filtered Data as CSV",
    data=csv,
    file_name="filtered_sales_data.csv",
    mime="text/csv"
)

# Footer
st.markdown("---")
st.markdown("### Developed by Aslan Akhundov")
st.markdown("Data Analyst | Python | SQL | Pandas")