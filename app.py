import streamlit as st
import pandas as pd

# -----------------------
# Load Data
# -----------------------
df = pd.read_csv("C:/Users/ektap/Desktop/Ekta/insternship/Customer_Churn_Project/European_Bank.csv")

# -----------------------
# Page Config
# -----------------------
st.set_page_config(page_title="Churn Analytics Dashboard", layout="wide")

st.title(" Customer Segmentation & Churn Analytics")

# -----------------------
# Sidebar Filters
# -----------------------
st.sidebar.header(" Filters")

geo_filter = st.sidebar.multiselect(
    "Geography",
    df["Geography"].unique(),
    default=df["Geography"].unique()
)

gender_filter = st.sidebar.multiselect(
    "Gender",
    df["Gender"].unique(),
    default=df["Gender"].unique()
)

age_filter = st.sidebar.slider(
    "Age Range",
    int(df["Age"].min()),
    int(df["Age"].max()),
    (20, 60)
)

balance_filter = st.sidebar.slider(
    "Balance Range",
    int(df["Balance"].min()),
    int(df["Balance"].max()),
    (0, int(df["Balance"].max()))
)

# -----------------------
# Apply Filters
# -----------------------
filtered_df = df[
    (df["Geography"].isin(geo_filter)) &
    (df["Gender"].isin(gender_filter)) &
    (df["Age"].between(age_filter[0], age_filter[1])) &
    (df["Balance"].between(balance_filter[0], balance_filter[1]))
]

# -----------------------
# KPI Section
# -----------------------
st.subheader("Key Performance Indicators")

col1, col2, col3, col4 = st.columns(4)

churn_rate = filtered_df["Exited"].mean() * 100
total_customers = filtered_df.shape[0]
active_rate = filtered_df["IsActiveMember"].mean() * 100
avg_balance = filtered_df["Balance"].mean()

col1.metric("Churn Rate", f"{churn_rate:.2f}%")
col2.metric("Customers", total_customers)
col3.metric("Active %", f"{active_rate:.2f}%")
col4.metric("Avg Balance", f"{avg_balance:.0f}")

# -----------------------
# Tabs Layout
# -----------------------
tab1, tab2, tab3, tab4 = st.tabs([
    "Geography",
    "Demographics",
    "High Value",
    "Data"
])

# -----------------------
# Tab 1: Geography
# -----------------------
with tab1:
    st.subheader("Geography-wise Churn")

    geo_churn = filtered_df.groupby("Geography")["Exited"].mean()
    st.bar_chart(geo_churn)

# -----------------------
# Tab 2: Demographics
# -----------------------
with tab2:
    st.subheader("Age vs Churn")
    age_churn = filtered_df.groupby("Age")["Exited"].mean()
    st.line_chart(age_churn)

    st.subheader("Tenure vs Churn")
    tenure_churn = filtered_df.groupby("Tenure")["Exited"].mean()
    st.line_chart(tenure_churn)

    st.subheader("Gender-wise Churn")
    gender_churn = filtered_df.groupby("Gender")["Exited"].mean()
    st.bar_chart(gender_churn)

# -----------------------
# Tab 3: High Value Customers
# -----------------------
with tab3:
    st.subheader("High-Value Customer Analysis")

    threshold = st.slider(
        "Select High Balance Threshold",
        int(df["Balance"].min()),
        int(df["Balance"].max()),
        100000
    )

    hv_df = filtered_df[filtered_df["Balance"] > threshold]

    if len(hv_df) > 0:
        hv_churn = hv_df["Exited"].mean() * 100
        st.metric("High Value Churn Rate", f"{hv_churn:.2f}%")

        hv_geo = hv_df.groupby("Geography")["Exited"].mean()
        st.bar_chart(hv_geo)

    else:
        st.warning("No high-value customers in selected range")

# -----------------------
# Tab 4: Drill-down Data
# -----------------------
with tab4:
    st.subheader("Filtered Dataset View")
    st.dataframe(filtered_df)
