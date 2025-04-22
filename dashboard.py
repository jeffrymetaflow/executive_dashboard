import streamlit as st
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(page_title="Unified Executive Dashboard", layout="wide")
st.title("\U0001F4CA Unified Executive Dashboard")

# --- Sample Inputs (would eventually link to live modules) ---
st.sidebar.header("\U0001F4B0 High-Level Inputs")
revenue = st.sidebar.number_input("Annual Revenue ($M)", min_value=1, value=100) * 1_000_000

category_data = {
    "Hardware": 320_000,
    "Software": 280_000,
    "Personnel": 500_000,
    "Maintenance": 160_000,
    "Telecom": 120_000,
    "Cybersecurity": 220_000,
    "BC/DR": 140_000
}

risk_impact = {
    "Cybersecurity": {"Revenue Protected %": 25, "ROPR": 6.5},
    "BC/DR": {"Revenue Protected %": 18, "ROPR": 4.2}
}

# --- KPI Summary ---
st.subheader("\U0001F4C8 Key Metrics")
total_spend = sum(category_data.values())
it_ratio = total_spend / revenue * 100

col1, col2, col3 = st.columns(3)
col1.metric("Total IT Spend", f"${total_spend:,.0f}")
col2.metric("IT Spend / Revenue", f"{it_ratio:.2f}%")
col3.metric("Revenue at Risk (Protected)", f"{sum([v['Revenue Protected %'] for v in risk_impact.values()])}%")

# --- Bar Chart: IT Spend Breakdown ---
st.subheader("\U0001F4C9 IT Spend Breakdown by Category")
spend_df = pd.DataFrame.from_dict(category_data, orient='index', columns=['Spend ($)']).reset_index()
spend_df.columns = ['Category', 'Spend ($)']
fig1 = go.Figure(go.Bar(
    x=spend_df['Category'],
    y=spend_df['Spend ($)'],
    marker_color='lightskyblue',
    text=spend_df['Spend ($)'].apply(lambda x: f"${x:,.0f}"),
    textposition='auto'))
fig1.update_layout(yaxis_title='Spend ($)', height=400)
st.plotly_chart(fig1, use_container_width=True)

# --- Line Chart: Risk Prevention ROI ---
st.subheader("\U0001F4A1 Risk-Related ROI (ROPR)")
ropr_df = pd.DataFrame([(k, v['ROPR']) for k, v in risk_impact.items()], columns=['Category', 'ROPR'])
fig2 = go.Figure(go.Scatter(
    x=ropr_df['Category'],
    y=ropr_df['ROPR'],
    mode='lines+markers',
    marker=dict(color='seagreen'),
    line=dict(width=3)
))
fig2.update_layout(yaxis_title='Return on Risk Prevention (x)', height=400)
st.plotly_chart(fig2, use_container_width=True)

# --- Pie Chart: Revenue Protection Impact ---
st.subheader("\U0001F4B8 Revenue Protected by Category")
protection_df = pd.DataFrame([(k, v['Revenue Protected %']) for k, v in risk_impact.items()], columns=['Category', 'Protected %'])
fig3 = go.Figure(go.Pie(
    labels=protection_df['Category'],
    values=protection_df['Protected %'],
    textinfo='label+percent',
    hole=0.4
))
fig3.update_layout(height=400)
st.plotly_chart(fig3, use_container_width=True)

# --- Summary ---
st.markdown("""
### \U0001F4DD Summary
This executive dashboard provides a high-level view of IT financials, risk-adjusted investments, and revenue protection. It enables leadership to:
- Understand where IT spend is concentrated
- Track ROI on cybersecurity and continuity investments
- Align technology strategy with margin and mission protection
""")
