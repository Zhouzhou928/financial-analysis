import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import plotly.subplots as sp

st.set_page_config(page_title="Advanced WRDS Dashboard", layout="wide")
st.title("📊 Advanced Tech Financial Analysis (WRDS)")
st.subheader("AAPL | MSFT | GOOGL | AMZN | Industry Benchmark")

# Load data
try:
    df = pd.read_csv("wrds_final_data.csv")
except:
    st.warning("Data file not found. Please run the Jupyter notebook first to generate 'wrds_final_data.csv'.")
    st.stop()

# Sidebar
with st.sidebar:
    st.header("Control Panel")
    companies = st.multiselect("Select Companies", df['tic'].unique(), default=["AAPL","MSFT","INDUSTRY"])
    year_min, year_max = st.slider("Year Range", 2015, 2023, (2015,2023))
    log_scale = st.checkbox("Log Scale for Revenue", value=True)

filt = df[(df['tic'].isin(companies)) & (df['year'] >= year_min) & (df['year'] <= year_max)]

# Table
st.subheader("📋 Summary Table")
st.dataframe(filt.sort_values(["tic","year"]).round(2), use_container_width=True)
st.divider()

# Plot 1
st.subheader("📈 Net Profit Margin")
fig1 = px.line(filt, x="year", y="profit_margin", color="tic", markers=True)
st.plotly_chart(fig1, use_container_width=True)

# Plot 2
st.subheader("📊 ROE Comparison")
fig2 = px.bar(filt, x="year", y="roe", color="tic", barmode="group")
st.plotly_chart(fig2, use_container_width=True)

# Plot 3
st.subheader("💲 Revenue")
fig3 = px.line(filt, x="year", y="revt", color="tic", markers=True)
if log_scale:
    fig3.update_layout(yaxis_type="log")
st.plotly_chart(fig3, use_container_width=True)

# Plot 4
st.subheader("🎯 2023 Financial Radar")
latest = df[df["year"] == 2023]
rad_comp = st.multiselect("Compare Radar", latest["tic"].unique(), default=["AAPL","MSFT"])
rad = latest[latest["tic"].isin(rad_comp)]
fig4 = go.Figure()
for _, r in rad.iterrows():
    fig4.add_trace(go.Scatterpolar(
        r=[r.profit_margin, r.roe, r.roa, 100-r.debt_asset],
        theta=["Profit Margin","ROA","ROE","Low Debt"],
        fill="toself", name=r.tic
    ))
st.plotly_chart(fig4, use_container_width=True)

# Plot 5
st.subheader("🔥 Correlation Heatmap")
corr = df[["profit_margin","roe","roa","debt_asset"]].corr()
fig5 = px.imshow(corr, text_auto=True, color_continuous_scale="RdBu_r")
st.plotly_chart(fig5, use_container_width=True)

st.success("✅ All data from WRDS | Interactive Dashboard | Advanced Analysis")