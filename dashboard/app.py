import streamlit as st
import pandas as pd
import plotly.express as px
from styling import inject_custom_css, insight_box, PRIMARY, ACCENT, SUCCESS, PLOTLY_TEMPLATE, COLOR_SEQUENCE

st.set_page_config(
    page_title="Shipsense — Delivery Risk Dashboard",
    page_icon="📦",
    layout="wide",
    initial_sidebar_state="expanded"
)
inject_custom_css()

# ---------- Load data ----------
import os

@st.cache_data
def load_data():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    csv_path = os.path.join(base_dir, '..', 'data_processed', 'dashboard_data.csv')
    df = pd.read_csv(csv_path, parse_dates=['purchase_date'])
    df['month'] = df['purchase_date'].dt.to_period('M').astype(str)
    return df
df = load_data()

# ---------- Sidebar ----------
with st.sidebar:
    st.markdown("### 📦 Shipsense")
    st.caption("Delivery & Revenue Risk Intelligence Platform")
    st.markdown("---")
    states = sorted(df['customer_state'].dropna().unique().tolist())
    selected_states = st.multiselect("Filter by state", states, default=[])
    st.markdown("---")
    st.caption("Built on the Olist e-commerce dataset · LightGBM risk model (test ROC-AUC 0.758)")

if selected_states:
    df = df[df['customer_state'].isin(selected_states)]

# ---------- Header ----------
st.title("Shipsense: Delivery & Revenue Risk Dashboard")
st.markdown("Tracking which orders are at risk of arriving late, and what that costs the business.")

# ---------- KPI row ----------
k1, k2, k3, k4 = st.columns(4)
k1.metric("Total Orders", f"{len(df):,}")
k2.metric("Overall Late Rate", f"{df['is_late'].mean()*100:.2f}%")
k3.metric("Revenue at Risk", f"${df[df['is_late']==1]['total_payment_value'].sum():,.0f}")
k4.metric("On-Time Revenue", f"${df[df['is_late']==0]['total_payment_value'].sum():,.0f}")

st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)

# ---------- Row 1: Trend + State risk ----------
c1, c2 = st.columns(2)

with c1:
    st.subheader("Late Delivery Rate Over Time")
    monthly = df.groupby('month')['is_late'].mean().reset_index()
    monthly['is_late'] = monthly['is_late'] * 100
    fig1 = px.line(monthly, x='month', y='is_late', markers=True, template=PLOTLY_TEMPLATE,
                   color_discrete_sequence=[PRIMARY])
    fig1.update_layout(yaxis_title="Late rate (%)", xaxis_title="", height=360)
    st.plotly_chart(fig1, use_container_width=True)
    insight_box("Watch for spikes during peak shopping months — a sign fulfillment capacity is stretched.")

with c2:
    st.subheader("Revenue at Risk by State (Top 10)")
    state_risk = (df[df['is_late']==1].groupby('customer_state')['total_payment_value']
                  .sum().sort_values(ascending=False).head(10).reset_index())
    fig2 = px.bar(state_risk, x='customer_state', y='total_payment_value', template=PLOTLY_TEMPLATE,
                  color_discrete_sequence=[ACCENT])
    fig2.update_layout(yaxis_title="Revenue at risk ($)", xaxis_title="", height=360)
    st.plotly_chart(fig2, use_container_width=True)
    insight_box("Prioritize carrier renegotiation or warehouse review in the top 2-3 states here first.")

st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)

# ---------- Row 2: Volume + repeat-rate proxy ----------
c3, c4 = st.columns(2)

with c3:
    st.subheader("Order Volume Over Time")
    volume = df.groupby('month').size().reset_index(name='order_count')
    fig3 = px.bar(volume, x='month', y='order_count', template=PLOTLY_TEMPLATE,
                  color_discrete_sequence=[PRIMARY])
    fig3.update_layout(yaxis_title="Orders", xaxis_title="", height=360)
    st.plotly_chart(fig3, use_container_width=True)
    insight_box("Overlay this with the late-rate chart above — rising volume often precedes rising delay rates.")

with c4:
    st.subheader("Repeat-Purchase Rate: On-Time vs Late")
    repeat_df = pd.DataFrame({
        'Delivery Outcome': ['On-time first order', 'Late first order'],
        'Repeat Rate (%)': [3.04, 2.52]
    })
    fig4 = px.bar(repeat_df, x='Delivery Outcome', y='Repeat Rate (%)', template=PLOTLY_TEMPLATE,
                  color='Delivery Outcome', color_discrete_sequence=[SUCCESS, ACCENT])
    fig4.update_layout(showlegend=False, height=360)
    st.plotly_chart(fig4, use_container_width=True)
    insight_box("Statistically significant (p=0.0195): late delivery measurably reduces repeat purchases.")

st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
st.caption("Shipsense — built end-to-end: PostgreSQL → SQL analytics → LightGBM model → FastAPI → this dashboard.")
