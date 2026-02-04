import streamlit as st
import pandas as pd
import plotly.express as px

# -----------------------
# Page Setup
# -----------------------
st.set_page_config(page_title="Laptop Price Dashboard", layout="wide")
st.title("💻 Laptop Price Analysis Dashboard")

# -----------------------
# Load Data
# -----------------------
@st.cache_data
def load_data():
    # Fix encoding issue
    df = pd.read_csv("data/laptop_price.csv", encoding="latin1")

    # Rename columns
    df.columns = [
        "Index", "Company", "Product", "TypeName", "Inches", "ScreenResolution",
        "CPU", "RAM", "Memory", "GPU", "OpSys", "Weight", "Price"
    ]

    # Clean numeric columns
    df["RAM"] = df["RAM"].str.replace("GB", "", regex=False).astype(int)
    df["Weight"] = df["Weight"].str.replace("kg", "", regex=False).astype(float)
    df["Price"] = df["Price"].astype(float)
    df["Inches"] = df["Inches"].astype(float)

    return df

df = load_data()

# -----------------------
# Sidebar Filters
# -----------------------
st.sidebar.header("🔎 Filter Laptops")

company_filter = st.sidebar.multiselect(
    "Select Company",
    df["Company"].unique(),
    default=df["Company"].unique()
)

type_filter = st.sidebar.multiselect(
    "Select Type",
    df["TypeName"].unique(),
    default=df["TypeName"].unique()
)

price_filter = st.sidebar.slider(
    "Maximum Price ($)",
    min_value=int(df["Price"].min()),
    max_value=int(df["Price"].max()),
    value=int(df["Price"].max())
)

ram_filter = st.sidebar.multiselect(
    "RAM (GB)",
    sorted(df["RAM"].unique()),
    default=sorted(df["RAM"].unique())
)

filtered_df = df[
    (df["Company"].isin(company_filter)) &
    (df["TypeName"].isin(type_filter)) &
    (df["Price"] <= price_filter) &
    (df["RAM"].isin(ram_filter))
]

# -----------------------
# Top Metrics
# -----------------------
col1, col2, col3 = st.columns(3)

col1.metric("💻 Total Laptops", len(filtered_df))
col2.metric("💰 Average Price", f"${filtered_df['Price'].mean():.2f}")
col3.metric("🧠 Average RAM", f"{filtered_df['RAM'].mean():.1f} GB")

st.divider()

# -----------------------
# Charts Row 1
# -----------------------
col4, col5 = st.columns(2)

with col4:
    st.subheader("💰 Price Distribution")
    fig_price = px.histogram(filtered_df, x="Price", nbins=15)
    st.plotly_chart(fig_price, use_container_width=True)

with col5:
    st.subheader("🏢 Price by Company")
    fig_company = px.box(filtered_df, x="Company", y="Price", color="Company")
    st.plotly_chart(fig_company, use_container_width=True)

# -----------------------
# Charts Row 2
# -----------------------
col6, col7 = st.columns(2)

with col6:
    st.subheader("🧠 RAM vs Price")
    fig_ram = px.scatter(
        filtered_df,
        x="RAM",
        y="Price",
        size="Inches",
        color="Company",
        hover_data=["Product"]
    )
    st.plotly_chart(fig_ram, use_container_width=True)

with col7:
    st.subheader("⚖️ Weight vs Price")
    fig_weight = px.scatter(
        filtered_df,
        x="Weight",
        y="Price",
        color="TypeName",
        hover_data=["Product"]
    )
    st.plotly_chart(fig_weight, use_container_width=True)

# -----------------------
# Data Table
# -----------------------
st.subheader("📋 Filtered Laptop Data")
st.dataframe(filtered_df, use_container_width=True)
