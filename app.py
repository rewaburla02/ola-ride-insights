import streamlit as st
import pandas as pd
import plotly.express as px

# Load dataset (make sure ola_dataset_2_clean.csv is in the same folder)
df = pd.read_csv("ola_dataset_2_clean.csv")

st.title("🚖 Ola Ride Insights")

# Sidebar filters
st.sidebar.header("Filters")
vehicle = st.sidebar.multiselect("Select Vehicle Type", df["Vehicle_Type"].unique())
status = st.sidebar.multiselect("Select Booking Status", df["Booking_Status"].unique())

df_filtered = df.copy()
if vehicle:
    df_filtered = df_filtered[df_filtered["Vehicle_Type"].isin(vehicle)]
if status:
    df_filtered = df_filtered[df_filtered["Booking_Status"].isin(status)]

# KPIs
st.subheader("Key Metrics")
col1, col2, col3 = st.columns(3)
col1.metric("Total Rides", len(df_filtered))
col2.metric("Successful Rides", len(df_filtered[df_filtered["Booking_Status"]=="Success"]))
col3.metric("Avg Ride Distance", round(df_filtered["Ride_Distance"].mean(),2))

# Ride Volume Over Time
st.subheader("📈 Ride Volume Over Time")
rides_per_day = df_filtered.groupby("Date").size().reset_index(name="Count")
fig1 = px.line(rides_per_day, x="Date", y="Count")
st.plotly_chart(fig1, use_container_width=True)

# Revenue by Payment Method
st.subheader("💳 Revenue by Payment Method")
revenue = df_filtered.groupby("Payment_Method")["Booking_Value"].sum().reset_index()
fig2 = px.bar(revenue, x="Payment_Method", y="Booking_Value")
st.plotly_chart(fig2, use_container_width=True)

# Driver Ratings Distribution
st.subheader("⭐ Driver Ratings Distribution")
fig3 = px.histogram(df_filtered, x="Driver_Ratings", nbins=20)
st.plotly_chart(fig3, use_container_width=True)
