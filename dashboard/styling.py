import streamlit as st

PRIMARY = "#2E5EAA"      # deep blue — headers, primary accents
ACCENT = "#E8743B"       # warm orange — risk/alert highlights
SUCCESS = "#2E9E5B"      # green — on-time/good metrics
BG_CARD = "#F7F9FC"
TEXT_MUTED = "#5B6470"

PLOTLY_TEMPLATE = "plotly_white"
COLOR_SEQUENCE = [PRIMARY, ACCENT, SUCCESS, "#8E7CC3", "#D9534F"]


def inject_custom_css():
    st.markdown(f"""
        <style>
        .main {{ background-color: #FFFFFF; }}
        .block-container {{ padding-top: 1.5rem; padding-bottom: 2rem; }}

        [data-testid="stMetric"] {{
            background-color: {BG_CARD};
            border: 1px solid #E3E8EF;
            border-radius: 10px;
            padding: 16px 18px;
        }}
        [data-testid="stMetricLabel"] {{
            color: {TEXT_MUTED};
            font-weight: 500;
        }}
        [data-testid="stMetricValue"] {{
            color: {PRIMARY};
            font-weight: 700;
        }}

        h1 {{
            color: {PRIMARY};
            font-weight: 800;
            letter-spacing: -0.5px;
        }}
        h2, h3 {{
            color: #1A1F2B;
            font-weight: 600;
        }}

        .caption-box {{
            background-color: {BG_CARD};
            border-left: 4px solid {PRIMARY};
            padding: 10px 14px;
            border-radius: 4px;
            color: {TEXT_MUTED};
            font-size: 0.9rem;
            margin-top: -8px;
            margin-bottom: 20px;
        }}

        .section-divider {{
            border-top: 1px solid #E3E8EF;
            margin: 28px 0 20px 0;
        }}
        </style>
    """, unsafe_allow_html=True)


def insight_box(text: str):
    st.markdown(f'<div class="caption-box">💡 {text}</div>', unsafe_allow_html=True)
