import streamlit as st
import pandas as pd
import plotly.express as px

# ----------------
# Load Data
# ----------------
df = pd.read_csv("Data/sales_data_sample.csv", encoding="latin1")

# Fix date column (if available)
if "ORDERDATE" in df.columns:
    df["ORDERDATE"] = pd.to_datetime(df["ORDERDATE"], errors="coerce")

# ----------------
# Dashboard Title
# ----------------
st.title("📊 Sales Dashboard")

# ----------------
# Sidebar Filters
# ----------------
st.sidebar.header("Filter Data")

# Country filter
countries = df['COUNTRY'].dropna().unique()
selected_country = st.sidebar.multiselect("Select Country", countries, default=countries)

# Year filter (only if date exists)
if "ORDERDATE" in df.columns:
    years = df["ORDERDATE"].dt.year.dropna().unique()
    selected_year = st.sidebar.multiselect("Select Year", years, default=years)
else:
    selected_year = None

# Apply filters
filtered_df = df[df['COUNTRY'].isin(selected_country)]
if selected_year is not None:
    filtered_df = filtered_df[filtered_df["ORDERDATE"].dt.year.isin(selected_year)]

# ----------------
# Tabs
# ----------------
tab1, tab2, tab3 = st.tabs(["📌 KPIs", "🌍 Regional Analysis", "📦 Product Analysis"])

# ---- Tab 1: KPIs ----
with tab1:
    st.subheader("Key Metrics")

    total_sales = filtered_df['SALES'].sum()
    avg_sales = filtered_df['SALES'].mean()
    num_orders = filtered_df['ORDERNUMBER'].nunique()

    col1, col2, col3 = st.columns(3)
    col1.metric("Total Sales", f"${total_sales:,.0f}")
    col2.metric("Average Order Value", f"${avg_sales:,.0f}")
    col3.metric("Unique Orders", num_orders)

    # Sales trend
    if "ORDERDATE" in filtered_df.columns:
        sales_trend = filtered_df.groupby("ORDERDATE")["SALES"].sum().reset_index()
        fig = px.line(sales_trend, x="ORDERDATE", y="SALES", title="Sales Over Time")
        st.plotly_chart(fig, use_container_width=True)

# ---- Tab 2: Regional Analysis ----
with tab2:
    st.subheader("Revenue by Country")
    sales_by_country = filtered_df.groupby("COUNTRY")["SALES"].sum().reset_index()
    fig2 = px.bar(sales_by_country, x="COUNTRY", y="SALES", title="Total Sales by Country")
    st.plotly_chart(fig2, use_container_width=True)

    st.subheader("Revenue by Deal Size")
    if "DEALSIZE" in df.columns:
        sales_by_dealsize = filtered_df.groupby("DEALSIZE")["SALES"].sum().reset_index()
        fig3 = px.pie(sales_by_dealsize, names="DEALSIZE", values="SALES", title="Sales by Deal Size")
        st.plotly_chart(fig3, use_container_width=True)

# ---- Tab 3: Product Analysis ----
with tab3:
    st.subheader("Revenue by Product Line")
    sales_by_product = filtered_df.groupby("PRODUCTLINE")["SALES"].sum().reset_index()
    fig4 = px.bar(sales_by_product, x="PRODUCTLINE", y="SALES", title="Sales by Product Line")
    st.plotly_chart(fig4, use_container_width=True)

    st.subheader("Top 10 Products")
    if "PRODUCTCODE" in df.columns:
        top_products = filtered_df.groupby("PRODUCTCODE")["SALES"].sum().reset_index().nlargest(10, "SALES")
        fig5 = px.bar(top_products, x="PRODUCTCODE", y="SALES", title="Top 10 Products by Sales")
        st.plotly_chart(fig5, use_container_width=True)
