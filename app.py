"""
National Energy Forecasting & Monitoring Portal | energy.gov.in
Government of India | Ministry of Power & Bureau of Energy Efficiency
Aligned with UN Sustainable Development Goal 7: Affordable and Clean Energy
Tagline: AI-Driven Energy Forecasting for a Smarter and Sustainable India
"""

import os
import json
import base64
import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta

# Import core modules
from config import (
    PERSONA_PROFILES,
    EMISSION_FACTORS,
    DEFAULT_TARIFF_RATE,
    APPLIANCE_BENCHMARKS
)
from core.validator import validate_dataframe, validate_manual_inputs, sanitize_user_text
from core.forecaster import calculate_usage_statistics, generate_forecast
from core.peak_detector import (
    detect_peak_days_and_anomalies,
    generate_load_shifting_recommendations,
    generate_diurnal_hourly_profile,
    get_persona_appliance_breakdown
)
from core.carbon_calc import calculate_carbon_footprint, project_savings, generate_multi_tier_projections
from core.rag_engine import get_knowledge_retriever
from core.llm_advisor import (
    generate_offline_explanation,
    generate_offline_recommendations,
    ask_advisor_bot
)
from core.national_data import (
    REGIONAL_GRID_DATA,
    STATE_ENERGY_DB,
    SCHEMES_DATABASE,
    AI_MODELS_BENCHMARK,
    DATA_REPOSITORY_CATALOG,
    OFFICIAL_REPORTS_LIST,
    generate_sample_dataset_csv
)
from core.three_d_twin import (
    get_national_grid_3d_html,
    get_renewable_twin_3d_html
)

# Page configuration
st.set_page_config(
    page_title="National Energy Forecasting & Monitoring Portal | energy.gov.in",
    page_icon="🏛️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# =====================================================================
# STYLING: AUTHENTIC INDIAN GOVERNMENT WEB PORTAL DESIGN SYSTEM
# =====================================================================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=Inter:wght@400;500;600;700&display=swap');

    /* Global Typography & Palette */
    html, body, [class*="css"], .stApp {
        font-family: 'Plus Jakarta Sans', 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
        background-color: #F8FAFC !important;
        color: #0F172A;
    }

    /* Hide Default Sidebar */
    [data-testid="stSidebar"], [data-testid="collapsedControl"] {
        display: none !important;
    }

    .block-container {
        padding-top: 0rem !important;
        padding-bottom: 2rem !important;
        padding-left: 1.25rem !important;
        padding-right: 1.25rem !important;
        max-width: 100% !important;
    }

    /* 1. Official Top Utility Strip */
    .gov-top-utility {
        background-color: #0B192C;
        color: #E2E8F0;
        padding: 6px 20px;
        font-size: 0.78rem;
        display: flex;
        justify-content: space-between;
        align-items: center;
        border-bottom: 2px solid #FF9933;
        margin-left: -1.25rem;
        margin-right: -1.25rem;
        font-weight: 500;
    }

    .gov-top-utility a {
        color: #E2E8F0;
        text-decoration: none;
        margin: 0 6px;
    }
    .gov-top-utility a:hover {
        color: #FF9933;
        text-decoration: underline;
    }

    /* 2. Official Government Portal Header */
    .gov-header-container {
        background: #FFFFFF;
        border-bottom: 1px solid #CBD5E1;
        padding: 16px 24px;
        margin-left: -1.25rem;
        margin-right: -1.25rem;
        box-shadow: 0 2px 5px rgba(0,0,0,0.03);
    }

    .gov-header-flex {
        display: flex;
        align-items: center;
        justify-content: space-between;
        flex-wrap: wrap;
        gap: 16px;
    }

    .gov-emblem-title-group {
        display: flex;
        align-items: center;
        gap: 18px;
    }

    .gov-emblem-svg {
        width: 58px;
        height: auto;
        display: block;
    }

    .gov-title-block h1 {
        font-size: 1.55rem;
        font-weight: 800;
        color: #0B3C68;
        line-height: 1.15;
        margin: 0;
        letter-spacing: -0.3px;
    }

    .gov-title-block h2 {
        font-size: 0.88rem;
        font-weight: 600;
        color: #475569;
        margin: 3px 0 0 0;
        letter-spacing: 0.2px;
    }

    .gov-tagline-strip {
        font-size: 0.78rem;
        color: #059669;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.6px;
        margin-top: 3px;
    }

    .gov-search-box {
        display: flex;
        align-items: center;
        background: #F1F5F9;
        border: 1px solid #CBD5E1;
        border-radius: 4px;
        padding: 4px 10px;
    }

    /* 3. Real Indian Government Top Navigation Bar (Tabs) */
    .stTabs [data-baseweb="tab-list"] {
        background-color: #0B3C68 !important;
        border-radius: 4px !important;
        padding: 4px 6px !important;
        gap: 3px !important;
        border-bottom: 3.5px solid #FF9933 !important;
        box-shadow: 0 3px 8px rgba(11, 60, 104, 0.16) !important;
        display: flex !important;
        flex-wrap: wrap !important;
        justify-content: flex-start !important;
        margin-top: 10px !important;
        margin-bottom: 20px !important;
    }

    .stTabs [data-baseweb="tab"] {
        color: #E2E8F0 !important;
        font-weight: 700 !important;
        font-size: 0.81rem !important;
        letter-spacing: 0.3px !important;
        text-transform: uppercase !important;
        padding: 9px 13px !important;
        background-color: transparent !important;
        border: none !important;
        border-bottom: 3.5px solid transparent !important;
        margin-bottom: -3.5px !important;
        border-radius: 3px 3px 0 0 !important;
        transition: all 0.18s ease-in-out !important;
        cursor: pointer !important;
    }

    .stTabs [data-baseweb="tab"]:hover {
        color: #FFFFFF !important;
        background-color: rgba(255, 255, 255, 0.16) !important;
    }

    .stTabs [aria-selected="true"] {
        color: #FFFFFF !important;
        background-color: #052648 !important;
        border-bottom: 3.5px solid #FF9933 !important;
        font-weight: 800 !important;
        box-shadow: inset 0 -2px 0 #FF9933 !important;
    }

    /* 4. National Schemes & Directives Buttons Bar */
    .schemes-section-card {
        background: #FFFFFF;
        border: 1px solid #CBD5E1;
        border-radius: 4px;
        padding: 12px 16px;
        margin-top: 14px;
        margin-bottom: 12px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.03);
    }

    .schemes-title-bar {
        font-size: 0.84rem;
        font-weight: 800;
        color: #0B3C68;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin-bottom: 10px;
        display: flex;
        align-items: center;
        gap: 8px;
        border-left: 4px solid #FF9933;
        padding-left: 8px;
    }

    /* Interactive Scheme Details Modal/Card */
    .scheme-details-card {
        background: #FFFFFF;
        border: 2px solid #0B3C68;
        border-top: 5px solid #FF9933;
        border-radius: 4px;
        padding: 20px 24px;
        margin-top: 10px;
        margin-bottom: 20px;
        box-shadow: 0 8px 24px rgba(11, 60, 104, 0.12);
        animation: fadeIn 0.3s ease-in-out;
    }

    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(-6px); }
        to { opacity: 1; transform: translateY(0); }
    }

    .scheme-hero-title {
        font-size: 1.35rem;
        font-weight: 800;
        color: #0B3C68;
        margin-bottom: 4px;
    }

    .scheme-ministry-badge {
        display: inline-block;
        background: #EBF3FA;
        color: #0B3C68;
        border: 1px solid #B9D5ED;
        padding: 3px 10px;
        border-radius: 3px;
        font-size: 0.78rem;
        font-weight: 700;
        margin-bottom: 12px;
    }

    /* 5. Side Banner Graphic */
    .side-banner-card {
        background: #FFFFFF;
        border: 1px solid #CBD5E1;
        border-top: 4px solid #FF9933;
        border-radius: 4px;
        padding: 12px;
        box-shadow: 0 2px 6px rgba(0,0,0,0.04);
        text-align: center;
        margin-bottom: 16px;
    }

    .side-banner-header {
        font-size: 0.8rem;
        font-weight: 800;
        color: #0B3C68;
        text-transform: uppercase;
        margin-bottom: 8px;
        letter-spacing: 0.5px;
    }

    /* 6. Official Government KPI Card */
    .gov-kpi-card {
        background: #FFFFFF;
        border: 1px solid #CBD5E1;
        border-top: 3.5px solid #0B3C68;
        border-radius: 3px;
        padding: 14px 12px;
        text-align: center;
        box-shadow: 0 1px 3px rgba(0,0,0,0.02);
        min-height: 105px;
    }

    .gov-kpi-card.saffron { border-top-color: #FF9933; }
    .gov-kpi-card.green { border-top-color: #10B981; }
    .gov-kpi-card.blue { border-top-color: #0284C7; }
    .gov-kpi-card.red { border-top-color: #DC2626; }

    .gov-kpi-label {
        font-size: 0.74rem;
        font-weight: 700;
        color: #64748B;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin-bottom: 4px;
    }

    .gov-kpi-value {
        font-size: 1.85rem;
        font-weight: 800;
        color: #0B3C68;
        line-height: 1.1;
    }

    .gov-kpi-sub {
        font-size: 0.74rem;
        color: #059669;
        font-weight: 600;
        margin-top: 4px;
    }

    /* 7. Section Container */
    .gov-section-panel {
        background: #FFFFFF;
        border: 1px solid #CBD5E1;
        border-radius: 4px;
        padding: 18px 20px;
        margin-bottom: 18px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.03);
    }

    .gov-panel-header {
        font-size: 1.05rem;
        font-weight: 800;
        color: #0B3C68;
        margin-bottom: 14px;
        border-left: 4px solid #0B3C68;
        padding-left: 10px;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }

    /* 8. Official Indian Government Footer */
    .gov-official-footer {
        background: #0B192C;
        color: #CBD5E1;
        padding: 36px 24px 20px 24px;
        margin-top: 40px;
        margin-left: -1.25rem;
        margin-right: -1.25rem;
        border-top: 4px solid #FF9933;
        font-size: 0.82rem;
    }

    .gov-footer-links-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
        gap: 20px;
        margin-bottom: 28px;
        border-bottom: 1px solid #1E293B;
        padding-bottom: 24px;
    }

    .gov-footer-col h4 {
        color: #FFFFFF;
        font-size: 0.88rem;
        font-weight: 700;
        margin-bottom: 10px;
        border-bottom: 2px solid #FF9933;
        display: inline-block;
        padding-bottom: 3px;
    }

    .gov-footer-col ul {
        list-style: none;
        padding: 0;
        margin: 0;
    }

    .gov-footer-col li {
        margin-bottom: 6px;
    }

    .gov-footer-col a {
        color: #94A3B8;
        text-decoration: none;
        font-size: 0.78rem;
    }
    .gov-footer-col a:hover {
        color: #38BDF8;
        text-decoration: underline;
    }

    .gov-footer-disclaimer-strip {
        text-align: center;
        padding-top: 14px;
        color: #94A3B8;
        font-size: 0.75rem;
        line-height: 1.6;
    }

    .gov-footer-disclaimer-strip b {
        color: #F8FAFC;
    }
</style>
""", unsafe_allow_html=True)


# =====================================================================
# SESSION STATE INITIALIZATION
# =====================================================================
if "active_scheme" not in st.session_state:
    st.session_state.active_scheme = None

if "selected_persona" not in st.session_state:
    st.session_state.selected_persona = "Residential Home (2-3 BHK)"

if "selected_mode" not in st.session_state:
    st.session_state.selected_mode = "Benchmark Profile (Preloaded)"

if "chat_history" not in st.session_state:
    st.session_state.chat_history = [
        {
            "role": "assistant",
            "content": "🏛️ **राष्ट्रीय स्वच्छ ऊर्जा सलाहकार डेस्क / National Clean Energy AI Advisory Desk**\n\nWelcome to the official decision-support portal (aligned with **UN Sustainable Development Goal 7**).\n\nYou can query verified demand forecasts, Time-of-Day (ToD) peak-shifting schedules, BEE 5-star appliance benchmarks, and decarbonization strategies. How can I assist your evaluation today?"
        }
    ]

# =====================================================================
# 1. TOP UTILITY STRIP
# =====================================================================
current_date_str = datetime.now().strftime("%A, %d %B %Y | %H:%M IST")

st.markdown(f"""
<div class="gov-top-utility">
    <div>
        <span>🏛️ भारत सरकार | Government of India</span>
        <span style="color: #475569; margin: 0 8px;">|</span>
        <span>विद्युत मंत्रालय | Ministry of Power</span>
        <span style="color: #475569; margin: 0 8px;">|</span>
        <span>केंद्रीय विद्युत प्राधिकरण | Central Electricity Authority</span>
    </div>
    <div>
        <span>📅 {current_date_str}</span>
        <span style="color: #475569; margin: 0 8px;">|</span>
        <a href="#accessibility">♿ A-</a>
        <a href="#accessibility"><b>A</b></a>
        <a href="#accessibility">A+</a>
        <span style="color: #475569; margin: 0 8px;">|</span>
        <span style="cursor: pointer;">हिंदी | English</span>
        <span style="color: #475569; margin: 0 8px;">|</span>
        <a href="#main-content">Skip to Main Content</a>
        <span style="margin-left: 8px;">🇮🇳</span>
    </div>
</div>
""", unsafe_allow_html=True)


# =====================================================================
# 2. GRAND GOVERNMENT HEADER WITH OFFICIAL LION CAPITAL EMBLEM
# =====================================================================
st.markdown("""
<div class="gov-header-container" id="main-content">
    <div class="gov-header-flex">
        <div class="gov-emblem-title-group">
            <!-- Official State Emblem of India (Ashoka Lion Capital) -->
            <svg class="gov-emblem-svg" viewBox="0 0 100 135" xmlns="http://www.w3.org/2000/svg">
                <g fill="#0B3C68">
                    <!-- Abacus base -->
                    <rect x="15" y="112" width="70" height="6" rx="1"/>
                    <rect x="22" y="120" width="56" height="3" rx="1"/>
                    <!-- Ashoka Chakra in Center of Base -->
                    <circle cx="50" cy="103" r="7" fill="none" stroke="#0B3C68" stroke-width="1.8"/>
                    <circle cx="50" cy="103" r="2.2" fill="#0B3C68"/>
                    <!-- Central Lion Body & Mane -->
                    <path d="M50,8 C42,8 37,16 37,24 C37,32 41,36 43,41 C35,41 27,47 27,58 C27,69 34,75 40,78 C38,84 38,90 42,94 L32,99 L32,106 L68,106 L68,99 L58,94 C62,90 62,84 60,78 C66,75 73,69 73,58 C73,47 65,41 57,41 C59,36 63,32 63,24 C63,16 58,8 50,8 Z"/>
                    <!-- Left Lion silhouette -->
                    <path d="M37,28 C32,28 27,33 27,40 C27,46 30,50 32,54 C26,56 22,62 22,70 C22,78 27,84 33,87 L33,96 L41,94 C38,90 38,82 39,78 C35,74 33,68 33,60 C33,52 38,46 43,44 Z" opacity="0.9"/>
                    <!-- Right Lion silhouette -->
                    <path d="M63,28 C68,28 73,33 73,40 C73,46 70,50 68,54 C74,56 78,62 78,70 C78,78 73,84 67,87 L67,96 L59,94 C62,90 62,82 61,78 C65,74 67,68 67,60 C67,52 62,46 57,44 Z" opacity="0.9"/>
                    <!-- Satyameva Jayate Inscription -->
                    <text x="50" y="132" font-size="7.8" font-family="'Plus Jakarta Sans', sans-serif" font-weight="bold" text-anchor="middle" fill="#0B3C68">सत्यमेव जयते</text>
                </g>
            </svg>
            <div class="gov-title-block">
                <h1>National Energy Forecasting & Monitoring Portal</h1>
                <h2>विद्युत मंत्रालय | Ministry of Power &bull; Government of India</h2>
                <div class="gov-tagline-strip">🇮🇳 AI-Driven Energy Forecasting for a Smarter and Sustainable India</div>
            </div>
        </div>
        <div>
            <div style="font-size: 0.72rem; color: #64748B; font-weight: 600; text-align: right; margin-bottom: 4px;">National Power Grid Status: <span style="color:#059669; font-weight:700;">● SYNCHRONIZED (50.01 Hz)</span></div>
            <div class="gov-search-box">
                <span style="margin-right: 6px;">🔍</span>
                <input type="text" placeholder="Search Portal, Schemes, Directives..." style="border:none; background:transparent; font-size:0.8rem; width:220px; outline:none;" />
            </div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)


# =====================================================================
# 3. INTERACTIVE SCHEMES & DIRECTIVES (11 CLICKABLE ITEMS)
# =====================================================================
st.markdown('<div class="schemes-section-card">', unsafe_allow_html=True)
st.markdown("""
<div class="schemes-title-bar">
    <span>🔥 प्रमुख राष्ट्रीय योजनाएं, मानक एवं प्रत्यक्ष दिशा-निर्देश / National Schemes & Directives (Click to View Official Details)</span>
</div>
""", unsafe_allow_html=True)

scheme_names = list(SCHEMES_DATABASE.keys())

# Render 11 buttons in 2 clean responsive rows
row1_cols = st.columns(6)
for idx in range(6):
    s_name = scheme_names[idx]
    with row1_cols[idx]:
        if st.button(s_name, key=f"btn_scheme_{idx}", use_container_width=True):
            st.session_state.active_scheme = s_name

row2_cols = st.columns(5)
for idx in range(6, 11):
    s_name = scheme_names[idx]
    with row2_cols[idx - 6]:
        if st.button(s_name, key=f"btn_scheme_{idx}", use_container_width=True):
            st.session_state.active_scheme = s_name

st.markdown('</div>', unsafe_allow_html=True)

# Detailed Scheme View Modal / Panel (Appears when any button is clicked)
if st.session_state.active_scheme and st.session_state.active_scheme in SCHEMES_DATABASE:
    scheme_info = SCHEMES_DATABASE[st.session_state.active_scheme]
    
    st.markdown(f"""
    <div class="scheme-details-card">
        <div style="display: flex; justify-content: space-between; align-items: flex-start;">
            <div>
                <span class="scheme-ministry-badge">🏛️ {scheme_info['ministry']} &bull; Category: {scheme_info['category']}</span>
                <div class="scheme-hero-title">{scheme_info['icon']} {scheme_info['title_hi']} | {scheme_info['title_en']}</div>
                <p style="color: #059669; font-weight: 700; font-size: 0.92rem; margin-top: 4px;">"{scheme_info['tagline']}"</p>
            </div>
        </div>
        <hr style="border: none; border-top: 1px solid #E2E8F0; margin: 12px 0;">
        <p style="font-size: 0.88rem; line-height: 1.6; color: #1E293B;"><b>सार / Executive Summary:</b> {scheme_info['summary']}</p>
    </div>
    """, unsafe_allow_html=True)

    c_sc1, c_sc2, c_sc3 = st.columns([4, 4, 4])
    with c_sc1:
        st.markdown("**📌 प्रमुख पहल एवं दिशा-निर्देश (Key Directives):**")
        for init in scheme_info['key_initiatives']:
            st.markdown(f"- {init}")
    with c_sc2:
        st.markdown("**💰 वित्तीय लाभ एवं सब्सिडी (Financial Subsidies):**")
        st.info(scheme_info['subsidies_and_benefits'])
        st.markdown("**🌱 कार्बन एवं ऊर्जा प्रभाव (Environmental Impact):**")
        st.success(scheme_info['carbon_impact'])
    with c_sc3:
        st.markdown("**📋 नागरिक / उपभोक्ता कार्यसूची (Action Checklist):**")
        for chk in scheme_info['citizen_action_checklist']:
            st.markdown(f"✓ {chk}")
        
        st.markdown(f"[🔗 Go to Official Portal ({scheme_info['official_link']})]({scheme_info['official_link']})")

    if st.button("❌ Close Directive Details View", key="close_scheme_btn"):
        st.session_state.active_scheme = None
        st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)


# =====================================================================
# HELPER: SIDE BANNER DISPLAYING image.png
# =====================================================================
def render_side_banner():
    """Renders the user's saved image.png as an authentic official side banner."""
    if os.path.exists("image.png"):
        st.markdown('<div class="side-banner-card">', unsafe_allow_html=True)
        st.markdown('<div class="side-banner-header">🏛️ Official Energy Portal Spotlight</div>', unsafe_allow_html=True)
        st.image("image.png", use_container_width=True)
        st.markdown("""
        <div style="font-size: 0.76rem; color: #475569; text-align: center; margin-top: 8px;">
            <b>WattWise AI Energy Management System</b><br>
            Aligned with UN SDG 7 &bull; Ministry of Power<br>
            <span style="color: #059669; font-weight: 700;">Data-Driven &bull; AI-Powered &bull; Sustainable</span>
        </div>
        """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)


# =====================================================================
# 4. REAL INDIAN GOVERNMENT TOP NAVIGATION BAR (ALL SECTIONS VISIBLE)
# =====================================================================
(
    tab_home,
    tab_about,
    tab_data,
    tab_forecast,
    tab_dashboard,
    tab_renewable,
    tab_peak,
    tab_statemap,
    tab_consumer,
    tab_planner,
    tab_advisor,
    tab_reports,
    tab_contact
) = st.tabs([
    "🏠 HOME",
    "🏛️ ABOUT",
    "📁 ENERGY DATA",
    "🔮 FORECASTING",
    "📊 DASHBOARD",
    "☀️ RENEWABLE ENERGY",
    "⚡ PEAK DEMAND & ALERTS",
    "🗺️ STATE MAP",
    "🔍 CONSUMER AUDIT",
    "💡 SAVINGS PLANNER",
    "🤖 AI ADVISOR",
    "📑 REPORTS",
    "📞 CONTACT"
])


# =====================================================================
# TAB 1: 🏠 HOME & 3D DIGITAL TWIN
# =====================================================================
with tab_home:
    col_main, col_side = st.columns([8.8, 3.2])

    with col_main:
        # Hero Section
        st.markdown("""
        <div class="gov-section-panel" style="background: linear-gradient(180deg, #0B2545 0%, #0E355F 100%); color: #FFFFFF; border: none; padding: 28px;">
            <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap;">
                <div>
                    <span style="background: #FF9933; color: #FFFFFF; font-size: 0.74rem; font-weight: 800; padding: 3px 10px; border-radius: 3px; letter-spacing: 0.6px; text-transform: uppercase;">
                        National Decision-Support Infrastructure
                    </span>
                    <h2 style="font-size: 2.1rem; font-weight: 800; color: #FFFFFF; margin: 10px 0 6px 0; letter-spacing: -0.5px;">
                        AI-Powered Energy Forecasting for India
                    </h2>
                    <p style="font-size: 1.02rem; color: #E2E8F0; max-width: 780px; line-height: 1.5;">
                        Forecasting electricity demand to support efficient grid management, renewable integration, and sustainable energy planning across all 5 regional interconnections.
                    </p>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # 5 Regional Energy Demand Indicators Strip
        st.markdown("""
        <div style="font-size: 0.88rem; font-weight: 800; color: #0B3C68; text-transform: uppercase; margin-bottom: 10px; border-left: 4px solid #0B3C68; padding-left: 8px;">
            ⚡ Regional Power Grid Telemetry & Demand Status
        </div>
        """, unsafe_allow_html=True)

        r_cols = st.columns(5)
        reg_items = list(REGIONAL_GRID_DATA.items())
        for r_idx, (r_name, r_data) in enumerate(reg_items):
            with r_cols[r_idx]:
                st.markdown(f"""
                <div class="gov-kpi-card" style="padding: 10px 8px;">
                    <div class="gov-kpi-label">{r_name}</div>
                    <div class="gov-kpi-value" style="font-size: 1.45rem;">{r_data['current_demand_gw']} <span style="font-size:0.75rem;">GW</span></div>
                    <div style="font-size: 0.72rem; color: {r_data['status_color']}; font-weight: 700; margin-top: 3px;">
                        {r_data['status']}
                    </div>
                    <div style="font-size: 0.7rem; color: #64748B; margin-top: 2px;">
                        Peak: {r_data['peak_demand_gw']} GW | {r_data['renewable_share_pct']}% Clean
                    </div>
                </div>
                """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        # 3D Digital Energy Twin Component
        st.markdown("""
        <div class="gov-section-panel" style="padding: 14px 16px;">
            <div class="gov-panel-header">
                <span>🌐 3D National Energy Grid Visualization (GIS Digital Twin)</span>
                <span style="font-size: 0.75rem; color: #64748B; font-weight: normal;">Three.js WebGL &bull; Restrained Government GIS Palette</span>
            </div>
            <p style="font-size: 0.82rem; color: #475569; margin-bottom: 10px;">
                Interactive 3D model representing India's regional dispatch zones, high-voltage transmission lines, solar/wind parks, and major city substations. <b>Click on pins or use the HUD dropdown</b> to inspect state-level demand, predicted generation, and peak trends.
            </p>
        """, unsafe_allow_html=True)

        grid_3d_code = get_national_grid_3d_html(selected_state_default="Maharashtra", height=580)
        components.html(grid_3d_code, height=590, scrolling=False)

        st.markdown('</div>', unsafe_allow_html=True)

        # AI-Based Energy Insights Section
        st.markdown("""
        <div class="gov-section-panel">
            <div class="gov-panel-header">
                <span>🧠 AI-Based Energy Insights & Executive Decision Support</span>
                <span style="font-size: 0.75rem; color: #059669; font-weight: 700;">LIVE INFERENCE STREAM</span>
            </div>
            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 14px;">
                <div style="background: #F8FAFC; border: 1px solid #E2E8F0; border-left: 3px solid #0B3C68; padding: 12px; border-radius: 3px;">
                    <div style="font-size: 0.75rem; font-weight: 700; color: #64748B;">NATIONAL DEMAND TRAJECTORY</div>
                    <div style="font-size: 0.88rem; font-weight: 600; color: #0F172A; margin-top: 4px;">
                        "National electricity demand is forecast to increase by <b>8.7%</b> over the next 24 hours driven by northern industrial loads."
                    </div>
                </div>
                <div style="background: #F8FAFC; border: 1px solid #E2E8F0; border-left: 3px solid #DC2626; padding: 12px; border-radius: 3px;">
                    <div style="font-size: 0.75rem; font-weight: 700; color: #64748B;">PEAK LOAD OCCURRENCE</div>
                    <div style="font-size: 0.88rem; font-weight: 600; color: #0F172A; margin-top: 4px;">
                        "Peak national demand is expected between <b>18:00 and 21:00 hours</b> (estimated peak: 235.2 GW)."
                    </div>
                </div>
                <div style="background: #F8FAFC; border: 1px solid #E2E8F0; border-left: 3px solid #10B981; padding: 12px; border-radius: 3px;">
                    <div style="font-size: 0.75rem; font-weight: 700; color: #64748B;">CLEAN RENEWABLE PENETRATION</div>
                    <div style="font-size: 0.88rem; font-weight: 600; color: #0F172A; margin-top: 4px;">
                        "Renewable generation is expected to contribute approximately <b>38%</b> of forecast demand during peak solar noon."
                    </div>
                </div>
                <div style="background: #F8FAFC; border: 1px solid #E2E8F0; border-left: 3px solid #F59E0B; padding: 12px; border-radius: 3px;">
                    <div style="font-size: 0.75rem; font-weight: 700; color: #64748B;">REGIONAL GROWTH VARIANCE</div>
                    <div style="font-size: 0.88rem; font-weight: 600; color: #0F172A; margin-top: 4px;">
                        "Western Region shows the highest predicted demand growth (+5.6%), requiring proactive ToD load shaving."
                    </div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col_side:
        # Saved Banner Image from Document
        render_side_banner()

        # National Grid Quick Hotlines & Alerts Card
        st.markdown("""
        <div class="gov-section-panel" style="padding: 14px;">
            <div style="font-size: 0.82rem; font-weight: 800; color: #0B3C68; text-transform: uppercase; margin-bottom: 10px;">
                ⚡ Statutory Directives Desk
            </div>
            <p style="font-size: 0.78rem; color: #475569; line-height: 1.5;">
                DISCOMs and State Load Despatch Centres (SLDCs) must maintain spinning reserves in accordance with CEA Grid Standards (2026).
            </p>
            <hr style="border: none; border-top: 1px solid #E2E8F0; margin: 10px 0;">
            <div style="font-size: 0.75rem; color: #64748B;">
                <b>Emergency Grid Hotline:</b> 1912<br>
                <b>CEA Technical Cell:</b> 011-26732000<br>
                <b>BEE Standards Desk:</b> 1800-180-1122
            </div>
        </div>
        """, unsafe_allow_html=True)


# =====================================================================
# TAB 2: 🏛️ ABOUT
# =====================================================================
with tab_about:
    st.markdown("### 🏛️ About National Energy Forecasting & Monitoring Portal")
    st.caption("Institutional Mandate, Legislative Acts & UN Sustainable Development Goal 7 Alignment")

    col_ab1, col_ab2 = st.columns(2)
    with col_ab1:
        st.markdown('<div class="gov-section-panel">', unsafe_allow_html=True)
        st.markdown('<div class="gov-panel-header">📜 Institutional Vision & Mandate</div>', unsafe_allow_html=True)
        st.markdown("""
        The **National Energy Forecasting & Monitoring Portal** is the official digital-twin decision-support system of the Ministry of Power, Government of India. It unifies predictive machine learning, high-voltage transmission telemetry, and municipal demand-side management into an integrated national platform.

        **Strategic Policy Objectives:**
        - **Accurate National Demand Forecasting:** Hourly and multi-day lookahead projections for the 5 regional synchronously interconnected grids.
        - **Accelerating Renewable Integration:** Real-time visibility into 192+ GW of non-fossil generation to achieve 500 GW by 2030.
        - **Peak Demand Smoothing:** Promoting Time-of-Day (ToD) tariff optimization, reducing stress on thermal peaker infrastructure.
        - **Citizen Decarbonization:** Providing actionable guidelines for households, educational campuses, and commercial establishments under Mission LiFE.
        """)
        st.markdown('</div>', unsafe_allow_html=True)

    with col_ab2:
        st.markdown('<div class="gov-section-panel">', unsafe_allow_html=True)
        st.markdown('<div class="gov-panel-header">⚖️ Statutory & Legislative Framework</div>', unsafe_allow_html=True)
        st.markdown("""
        **Governing Acts & Official Standards:**
        - **Electricity Act, 2003:** Section 25 & 28 governing regional dispatch, National Load Despatch Centre (NLDC) coordination, and grid reliability.
        - **Energy Conservation (Amendment) Act, 2022:** Mandating carbon credit trading, appliance star labeling, and industrial energy audits.
        - **Bureau of Energy Efficiency (BEE) Standards:** Gazette Notification S.O. 4235(E) for default 24°C AC temperature regulations.
        - **UN Sustainable Development Goal 7:** Target 7.1 (Universal Access), Target 7.2 (Renewable Energy Expansion), and Target 7.3 (Doubling Energy Efficiency).
        """)
        st.markdown('</div>', unsafe_allow_html=True)


# =====================================================================
# TAB 3: 📁 ENERGY DATA REPOSITORY & UPLOADS
# =====================================================================
with tab_data:
    st.markdown("### 📁 Energy Data Repository")
    st.caption("National Power System Time-Series Datasets, Meteorological Covariates & Standard Formats")

    st.markdown('<div class="gov-section-panel">', unsafe_allow_html=True)
    st.markdown('<div class="gov-panel-header">📋 Certified Energy Data Inventory</div>', unsafe_allow_html=True)
    df_repo = pd.DataFrame(DATA_REPOSITORY_CATALOG)
    st.dataframe(df_repo, use_container_width=True, hide_index=True)
    st.markdown('</div>', unsafe_allow_html=True)

    u_col1, u_col2 = st.columns(2)
    with u_col1:
        st.markdown('<div class="gov-section-panel">', unsafe_allow_html=True)
        st.markdown('<div class="gov-panel-header">📤 Upload Dataset</div>', unsafe_allow_html=True)
        st.caption("Supported formats: CSV, Excel (.xlsx), JSON")
        up_file = st.file_uploader("Select Energy Data File:", type=["csv", "xlsx", "json"], key="repo_uploader")
        if up_file:
            st.success(f"✓ Uploaded {up_file.name} successfully. Ready for validation.")
        st.markdown('</div>', unsafe_allow_html=True)

    with u_col2:
        st.markdown('<div class="gov-section-panel">', unsafe_allow_html=True)
        st.markdown('<div class="gov-panel-header">📥 Download Sample Dataset</div>', unsafe_allow_html=True)
        st.caption("Standard National Grid 30-Day Multi-Variable Baseline Dataset (CSV)")
        sample_csv_data = generate_sample_dataset_csv()
        st.download_button(
            label="⬇️ Download Sample Energy Dataset (CSV)",
            data=sample_csv_data,
            file_name="national_grid_sample_telemetry_30d.csv",
            mime="text/csv",
            use_container_width=True,
            key="download_sample_repo_btn"
        )
        st.markdown('</div>', unsafe_allow_html=True)


# =====================================================================
# TAB 4: 🔮 FORECASTING
# =====================================================================
with tab_forecast:
    st.markdown("### 🔮 Electricity Demand Forecast")
    st.caption("AI-Powered Multi-Horizon Demand Prediction & Machine Learning Methodology")

    # Selectors Ribbon
    st.markdown('<div class="gov-section-panel" style="padding: 12px 18px;">', unsafe_allow_html=True)
    fc_c1, fc_c2, fc_c3, fc_c4 = st.columns([3, 3, 3, 3])
    with fc_c1:
        sel_region = st.selectbox("Select Geographical Region:", ["India (National)", "Northern Region", "Southern Region", "Eastern Region", "Western Region", "North-Eastern Region"], index=0, key="fc_reg_sel")
    with fc_c2:
        sel_period = st.selectbox("Forecast Horizon Period:", ["24 Hours", "7 Days", "30 Days"], index=1, key="fc_per_sel")
    with fc_c3:
        sel_res = st.selectbox("Forecast Resolution:", ["Hourly", "Daily"], index=1, key="fc_res_sel")
    with fc_c4:
        st.markdown("<div style='height: 24px;'></div>", unsafe_allow_html=True)
        gen_btn = st.button("⚡ Generate Forecast", use_container_width=True, type="primary", key="fc_gen_action_btn")
    st.markdown('</div>', unsafe_allow_html=True)

    # Interactive Graph: Actual Demand vs Forecast Demand
    # Blue line = Actual, Green line = Forecast, Light shaded region = Confidence interval
    num_pts = 24 if "24 Hours" in sel_period else (7 if "7 Days" in sel_period else 30)
    if "Hourly" in sel_res:
        time_labels = [f"T+{h}h" for h in range(1, num_pts + 1)]
    else:
        time_labels = [(datetime.today() + timedelta(days=d)).strftime("%d %b") for d in range(1, num_pts + 1)]

    base_val = 214.6 if "National" in sel_region else 65.0
    np.random.seed(99)
    actual_pts = [round(base_val + np.sin(i / 2.5) * 8 + np.random.normal(0, 1.8), 1) for i in range(num_pts)]
    forecast_pts = [round(actual_pts[i] + np.random.normal(0, 2.0), 1) for i in range(num_pts)]
    upper_band = [round(forecast_pts[i] + 4.2 + (i * 0.1), 1) for i in range(num_pts)]
    lower_band = [round(forecast_pts[i] - 4.2 - (i * 0.1), 1) for i in range(num_pts)]

    st.markdown('<div class="gov-section-panel">', unsafe_allow_html=True)
    st.markdown('<div class="gov-panel-header">📈 Actual Demand vs AI Forecast Demand Trajectory (GW)</div>', unsafe_allow_html=True)

    fig_fc = go.Figure()
    # Actual Demand: Blue line
    fig_fc.add_trace(go.Scatter(
        x=time_labels, y=actual_pts,
        mode="lines+markers", name="Actual Demand (Blue)",
        line=dict(color="#0284C7", width=2.5),
        marker=dict(size=5)
    ))
    # Forecast Demand: Green line
    fig_fc.add_trace(go.Scatter(
        x=time_labels, y=forecast_pts,
        mode="lines+markers", name="Forecast Demand (Green)",
        line=dict(color="#10B981", width=3),
        marker=dict(size=6, symbol="diamond")
    ))
    # Shaded confidence band
    fig_fc.add_trace(go.Scatter(
        x=time_labels + time_labels[::-1],
        y=upper_band + lower_band[::-1],
        fill="toself",
        fillcolor="rgba(16, 185, 129, 0.12)",
        line=dict(color="rgba(255,255,255,0)"),
        name="Confidence Interval (95%)",
        hoverinfo="skip"
    ))

    fig_fc.update_layout(
        paper_bgcolor="#FFFFFF", plot_bgcolor="#FFFFFF",
        height=380, margin=dict(l=20, r=20, t=20, b=20),
        xaxis=dict(showgrid=True, gridcolor="#F1F5F9", title="Timeline Horizon"),
        yaxis=dict(showgrid=True, gridcolor="#F1F5F9", title="Gigawatts (GW)"),
        hovermode="x unified",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    st.plotly_chart(fig_fc, use_container_width=True)

    # Metrics strip: MAE, RMSE, MAPE, R2, Forecast Confidence
    m_col1, m_col2, m_col3, m_col4, m_col5 = st.columns(5)
    with m_col1: st.metric("MAE (Mean Abs Error)", "1.78 GW", "-0.12 GW")
    with m_col2: st.metric("RMSE (Root Mean Sq)", "2.45 GW", "Optimal")
    with m_col3: st.metric("MAPE (Percentage Error)", "1.82%", "State-of-Art")
    with m_col4: st.metric("R² Score", "0.988", "+0.004")
    with m_col5: st.metric("Forecast Confidence", "95.4%", "Calibrated")
    st.markdown('</div>', unsafe_allow_html=True)

    # AI Forecasting Model Methodology Section
    st.markdown('<div class="gov-section-panel">', unsafe_allow_html=True)
    st.markdown('<div class="gov-panel-header">🔬 Forecasting Methodology & Machine Learning Pipeline</div>', unsafe_allow_html=True)

    st.markdown("""
    ```mermaid
    graph LR
        A[Historical Energy Data] --> B[Data Preprocessing]
        B --> C[Weather & Calendar Features]
        C --> D[ML / Deep Learning Models]
        D --> E[Demand Forecast]
        E --> F[Peak Demand Detection]
        F --> G[Government Decision Support]
    ```
    """)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("##### 📊 Production AI Model Performance Comparison Benchmark")
    df_models = pd.DataFrame(AI_MODELS_BENCHMARK)
    st.dataframe(df_models, use_container_width=True, hide_index=True)
    st.caption("Evaluated on 52,600+ hourly national grid dispatch records (2020-2026). Ensemble model currently deployed as primary inference engine.")
    st.markdown('</div>', unsafe_allow_html=True)


# =====================================================================
# TAB 5: 📊 DASHBOARD
# =====================================================================
with tab_dashboard:
    st.markdown("### 📊 National Energy Demand Dashboard")
    st.caption("Official High-Level Grid Telemetry & Key Performance Indicators (National Load Despatch Centre)")

    # 6 Government KPI Panels
    k_col1, k_col2, k_col3, k_col4, k_col5, k_col6 = st.columns(6)
    with k_col1:
        st.markdown("""
        <div class="gov-kpi-card blue">
            <div class="gov-kpi-label">Current Demand</div>
            <div class="gov-kpi-value">214.6 <span style="font-size:0.8rem">GW</span></div>
            <div class="gov-kpi-sub">National Real-Time</div>
        </div>
        """, unsafe_allow_html=True)
    with k_col2:
        st.markdown("""
        <div class="gov-kpi-card">
            <div class="gov-kpi-label">Forecast Demand</div>
            <div class="gov-kpi-value">221.8 <span style="font-size:0.8rem">GW</span></div>
            <div class="gov-kpi-sub">+3.3% 24h Outlook</div>
        </div>
        """, unsafe_allow_html=True)
    with k_col3:
        st.markdown("""
        <div class="gov-kpi-card red">
            <div class="gov-kpi-label">Peak Demand</div>
            <div class="gov-kpi-value">235.2 <span style="font-size:0.8rem">GW</span></div>
            <div class="gov-kpi-sub" style="color:#DC2626;">Expected 19:30 IST</div>
        </div>
        """, unsafe_allow_html=True)
    with k_col4:
        st.markdown("""
        <div class="gov-kpi-card green">
            <div class="gov-kpi-label">Renewable Generation</div>
            <div class="gov-kpi-value">92.4 <span style="font-size:0.8rem">GW</span></div>
            <div class="gov-kpi-sub">43.0% Grid Share</div>
        </div>
        """, unsafe_allow_html=True)
    with k_col5:
        st.markdown("""
        <div class="gov-kpi-card saffron">
            <div class="gov-kpi-label">Forecast Accuracy</div>
            <div class="gov-kpi-value">94.8<span style="font-size:0.85rem">%</span></div>
            <div class="gov-kpi-sub">CEA Standard Compliant</div>
        </div>
        """, unsafe_allow_html=True)
    with k_col6:
        st.markdown("""
        <div class="gov-kpi-card green">
            <div class="gov-kpi-label">CO₂ Avoided</div>
            <div class="gov-kpi-value">18.7 <span style="font-size:0.8rem">Lakh T</span></div>
            <div class="gov-kpi-sub">Monthly Metric Tons</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # 2-Column Dashboard Graphs: Regional Breakdown + National Hourly Load Flow
    d_g1, d_g2 = st.columns([6, 6])
    with d_g1:
        st.markdown('<div class="gov-section-panel">', unsafe_allow_html=True)
        st.markdown('<div class="gov-panel-header">⚡ Inter-Regional Demand & Renewable Injection (GW)</div>', unsafe_allow_html=True)
        
        reg_df = pd.DataFrame([
            {"Region": k, "Demand GW": v["current_demand_gw"], "Renewable GW": v["renewable_gen_gw"], "Peak GW": v["peak_demand_gw"]}
            for k, v in REGIONAL_GRID_DATA.items()
        ])
        fig_reg = go.Figure()
        fig_reg.add_trace(go.Bar(x=reg_df["Region"], y=reg_df["Demand GW"], name="Current Demand", marker_color="#0B3C68"))
        fig_reg.add_trace(go.Bar(x=reg_df["Region"], y=reg_df["Renewable GW"], name="Renewable Dispatch", marker_color="#10B981"))
        fig_reg.update_layout(
            barmode="group",
            paper_bgcolor="#FFFFFF", plot_bgcolor="#FFFFFF",
            height=320, margin=dict(l=10, r=10, t=10, b=10),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
        )
        st.plotly_chart(fig_reg, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with d_g2:
        st.markdown('<div class="gov-section-panel">', unsafe_allow_html=True)
        st.markdown('<div class="gov-panel-header">📈 24-Hour Diurnal Dispatch Profile vs Frequency (Hz)</div>', unsafe_allow_html=True)
        hours = [f"{h:02d}:00" for h in range(24)]
        np.random.seed(101)
        hourly_demand = [185 + np.sin((h - 5) / 3.8) * 45 + np.random.normal(0, 1.5) for h in range(24)]
        fig_hourly = go.Figure()
        fig_hourly.add_trace(go.Scatter(x=hours, y=hourly_demand, mode="lines+markers", name="National Load (GW)", line=dict(color="#0B3C68", width=2.5)))
        fig_hourly.add_hline(y=235.2, line_dash="dash", line_color="#DC2626", annotation_text="Peak Capacity Threshold")
        fig_hourly.update_layout(
            paper_bgcolor="#FFFFFF", plot_bgcolor="#FFFFFF",
            height=320, margin=dict(l=10, r=10, t=10, b=10),
            xaxis=dict(showgrid=True, gridcolor="#F1F5F9"),
            yaxis=dict(showgrid=True, gridcolor="#F1F5F9", title="Gigawatts (GW)"),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
        )
        st.plotly_chart(fig_hourly, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)


# =====================================================================
# TAB 6: ☀️ RENEWABLE ENERGY
# =====================================================================
with tab_renewable:
    st.markdown("### ☀️ Renewable Energy Dashboard & 3D Clean Infrastructure")
    st.caption("National Non-Fossil Generation Capacity & 3D Digital Twin of Green Assets")

    # KPI Row
    r_k1, r_k2, r_k3, r_k4 = st.columns(4)
    with r_k1:
        st.markdown("""
        <div class="gov-kpi-card saffron">
            <div class="gov-kpi-label">India Renewable Capacity</div>
            <div class="gov-kpi-value">192.5 <span style="font-size:0.8rem">GW</span></div>
            <div class="gov-kpi-sub">Target: 500 GW by 2030</div>
        </div>
        """, unsafe_allow_html=True)
    with r_k2:
        st.markdown("""
        <div class="gov-kpi-card green">
            <div class="gov-kpi-label">Current Renewable Gen</div>
            <div class="gov-kpi-value">92.4 <span style="font-size:0.8rem">GW</span></div>
            <div class="gov-kpi-sub">Real-Time Dispatch</div>
        </div>
        """, unsafe_allow_html=True)
    with r_k3:
        st.markdown("""
        <div class="gov-kpi-card blue">
            <div class="gov-kpi-label">Forecast Renewable Gen</div>
            <div class="gov-kpi-value">98.6 <span style="font-size:0.8rem">GW</span></div>
            <div class="gov-kpi-sub">+6.7% Tomorrow Afternoon</div>
        </div>
        """, unsafe_allow_html=True)
    with r_k4:
        st.markdown("""
        <div class="gov-kpi-card green">
            <div class="gov-kpi-label">Renewable Share</div>
            <div class="gov-kpi-value">43.0<span style="font-size:0.85rem">%</span></div>
            <div class="gov-kpi-sub">Of Total Grid Load</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # 3D Renewable Infrastructure Twin
    st.markdown('<div class="gov-section-panel" style="padding: 14px 16px;">', unsafe_allow_html=True)
    st.markdown('<div class="gov-panel-header">🌐 3D Renewable Infrastructure Digital Twin</div>', unsafe_allow_html=True)
    st.caption("Interactive 3D model: Rotating Wind Turbines, Solar Photovoltaic Tracking Arrays, and Hydro Dam Spillway.")
    ren_3d_html = get_renewable_twin_3d_html(height=500)
    components.html(ren_3d_html, height=510, scrolling=False)
    st.markdown('</div>', unsafe_allow_html=True)

    # Breakdown by Source
    r_col_left, r_col_right = st.columns([6, 6])
    with r_col_left:
        st.markdown('<div class="gov-section-panel">', unsafe_allow_html=True)
        st.markdown('<div class="gov-panel-header">⚡ Renewable Generation Breakdown by Source</div>', unsafe_allow_html=True)
        source_df = pd.DataFrame([
            {"Source": "Solar Generation", "GW": 52.6},
            {"Source": "Wind Generation", "GW": 24.2},
            {"Source": "Hydro Generation", "GW": 15.6},
            {"Source": "Biomass Power", "GW": 5.8},
            {"Source": "Other Renewable", "GW": 2.4}
        ])
        fig_src = px.pie(
            source_df, names="Source", values="GW", hole=0.45,
            color_discrete_sequence=["#F59E0B", "#10B981", "#38BDF8", "#84CC16", "#A855F7"]
        )
        fig_src.update_traces(textposition='inside', textinfo='percent+label')
        fig_src.update_layout(paper_bgcolor="#FFFFFF", plot_bgcolor="#FFFFFF", height=300, margin=dict(l=10, r=10, t=10, b=10))
        st.plotly_chart(fig_src, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with r_col_right:
        st.markdown('<div class="gov-section-panel">', unsafe_allow_html=True)
        st.markdown('<div class="gov-panel-header">🏆 Top 5 States by Installed Renewable Capacity</div>', unsafe_allow_html=True)
        top_re = [
            {"State": "Rajasthan", "Renewable GW": 14.8, "Solar GW": 11.8, "Wind GW": 2.8},
            {"State": "Gujarat", "Renewable GW": 13.6, "Solar GW": 7.2, "Wind GW": 5.9},
            {"State": "Karnataka", "Renewable GW": 11.4, "Solar GW": 7.5, "Wind GW": 3.2},
            {"State": "Maharashtra", "Renewable GW": 11.2, "Solar GW": 4.8, "Wind GW": 5.1},
            {"State": "Tamil Nadu", "Renewable GW": 10.8, "Solar GW": 4.9, "Wind GW": 5.3},
        ]
        st.dataframe(pd.DataFrame(top_re), use_container_width=True, hide_index=True)
        st.markdown('</div>', unsafe_allow_html=True)


# =====================================================================
# TAB 7: ⚡ PEAK DEMAND & ALERTS
# =====================================================================
with tab_peak:
    st.markdown("### ⚡ Peak Demand Monitoring & Grid Alerts")
    st.caption("Real-Time Load Straining Indicators, 24x7 Demand Intensity Heatmaps & Statutory Directives")

    # Metrics
    p_c1, p_c2, p_c3, p_c4, p_c5 = st.columns(5)
    with p_c1: st.metric("Current Peak Demand", "235.2 GW", "+4.2% vs yesterday")
    with p_c2: st.metric("Predicted Peak Demand", "238.4 GW", "+1.3%")
    with p_c3: st.metric("Peak Demand Time", "19:30 - 21:00 IST", "Evening Surcharge")
    with p_c4: st.metric("Peak Probability", "96.4%", "High Alert")
    with p_c5: st.metric("Demand Growth", "+5.4%", "Year-on-Year")

    st.markdown("<br>", unsafe_allow_html=True)

    # Official-looking alert
    st.markdown("""
    <div style="background: #FEF2F2; border: 2px solid #EF4444; border-left: 6px solid #DC2626; border-radius: 4px; padding: 14px 18px; margin-bottom: 20px;">
        <div style="font-weight: 800; color: #991B1B; font-size: 0.92rem; display: flex; align-items: center; gap: 8px;">
            🚨 STATUTORY GRID DESPATCH ADVISORY
        </div>
        <p style="font-size: 0.86rem; color: #7F1D1D; margin-top: 5px; line-height: 1.5;">
            <b>High demand is forecast during the evening peak period.</b> Grid operators and State Load Despatch Centres (SLDCs) may consider appropriate demand-side management measures, activate spinning gas peaker units, and enforce industrial load staggering.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Heatmap: Hour x Day
    st.markdown('<div class="gov-section-panel">', unsafe_allow_html=True)
    st.markdown('<div class="gov-panel-header">🔥 7-Day × 24-Hour Electricity Demand Intensity Heatmap (GW)</div>', unsafe_allow_html=True)
    
    days_list = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    hours_list = [f"{h:02d}:00" for h in range(24)]
    np.random.seed(42)
    heat_matrix = []
    for d in range(7):
        row = []
        for h in range(24):
            val = 170 + (45 if 18 <= h <= 21 else (30 if 9 <= h <= 12 else 10)) + np.random.normal(0, 3)
            row.append(round(val, 1))
        heat_matrix.append(row)

    fig_heat = px.imshow(
        heat_matrix,
        x=hours_list,
        y=days_list,
        color_continuous_scale="Blues",
        labels=dict(x="Hour of Day (IST)", y="Day of Week", color="Load (GW)")
    )
    fig_heat.update_layout(
        paper_bgcolor="#FFFFFF", plot_bgcolor="#FFFFFF",
        height=320, margin=dict(l=10, r=10, t=10, b=10)
    )
    st.plotly_chart(fig_heat, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # Energy System Alerts
    st.markdown("##### 🚨 Active Energy System Notifications")
    al_c1, al_c2 = st.columns(2)
    with al_c1:
        st.error("⚠️ **HIGH DEMAND ALERT**: High electricity demand is forecast for the Western Region exceeding 76.5 GW during 18:30-21:00.")
        st.warning("⚠️ **DEMAND ANOMALY**: An unusual electricity consumption pattern (+14.2% surge) has been detected across industrial clusters.")
    with al_c2:
        st.success("☀️ **RENEWABLE OPPORTUNITY**: Solar generation is expected to remain high during the afternoon period (>52 GW available).")
        st.info("ℹ️ **FORECAST UPDATE**: National electricity demand forecast has been updated with latest IMD temperature covariates.")


# =====================================================================
# TAB 8: 🗺️ STATE MAP
# =====================================================================
with tab_statemap:
    st.markdown("### 🗺️ State-Wise GIS Electricity & Renewable Telemetry")
    st.caption("Geographic Information System (GIS) Data for 28 Indian States & Union Territories")

    # Filters
    f_c1, f_c2, f_c3, f_c4 = st.columns(4)
    with f_c1: filter_type = st.selectbox("Filter Metric View:", ["All Metrics", "High Demand (>15 GW)", "High Renewable (>5 GW)", "High Risk Only"], index=0, key="st_filter_sel")
    with f_c2: sel_st = st.selectbox("Select State to Inspect:", list(STATE_ENERGY_DB.keys()), index=0, key="st_name_sel")
    with f_c3: st.write("")
    with f_c4: st.write("")

    # State Details Card
    st_data = STATE_ENERGY_DB[sel_st]
    st.markdown(f"""
    <div class="scheme-details-card" style="border-top-color: #0B3C68;">
        <div style="display: flex; justify-content: space-between; align-items: center;">
            <div>
                <h3 style="color: #0B3C68; margin: 0; font-size: 1.4rem;">🏛️ {sel_st} ({st_data['region']})</h3>
                <p style="color: #64748B; font-size: 0.82rem; margin-top: 2px;">SLDC Real-Time Telemetry & Forecast Verification</p>
            </div>
            <span style="background: {'#FEF2F2' if st_data['risk']=='High' else '#F0FDF4'}; color: {'#DC2626' if st_data['risk']=='High' else '#16A34A'}; padding: 4px 12px; border-radius: 4px; font-weight: 800; font-size: 0.82rem; border: 1px solid currentColor;">
                Risk Level: {st_data['risk']}
            </span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    sc1, sc2, sc3, sc4, sc5, sc6 = st.columns(6)
    with sc1: st.metric("Current Demand", f"{st_data['current_gw']} GW")
    with sc2: st.metric("Forecast Demand", f"{st_data['forecast_gw']} GW")
    with sc3: st.metric("Renewable Gen", f"{st_data['renewable_gw']} GW")
    with sc4: st.metric("Peak Demand", f"{st_data['peak_gw']} GW")
    with sc5: st.metric("Demand Growth", f"+{st_data['growth_pct']}%")
    with sc6: st.metric("Forecast Accuracy", f"{st_data['accuracy_pct']}%")

    st.markdown("<br>", unsafe_allow_html=True)

    # Full State Database Table
    st.markdown('<div class="gov-section-panel">', unsafe_allow_html=True)
    st.markdown('<div class="gov-panel-header">📋 State-Wise Telemetry Database</div>', unsafe_allow_html=True)
    
    table_rows = []
    for s_name, s_val in STATE_ENERGY_DB.items():
        if filter_type == "High Demand (>15 GW)" and s_val["current_gw"] < 15: continue
        if filter_type == "High Renewable (>5 GW)" and s_val["renewable_gw"] < 5: continue
        if filter_type == "High Risk Only" and s_val["risk"] != "High": continue

        table_rows.append({
            "State / UT": s_name,
            "Region": s_val["region"],
            "Current Demand (GW)": s_val["current_gw"],
            "Forecast Demand (GW)": s_val["forecast_gw"],
            "Renewable (GW)": s_val["renewable_gw"],
            "Peak Demand (GW)": s_val["peak_gw"],
            "Growth (%)": f"+{s_val['growth_pct']}%",
            "Forecast Accuracy": f"{s_val['accuracy_pct']}%",
            "Risk Assessment": s_val["risk"]
        })
    st.dataframe(pd.DataFrame(table_rows), use_container_width=True, hide_index=True)
    st.markdown('</div>', unsafe_allow_html=True)


# =====================================================================
# TAB 9: 🔍 CONSUMER AUDIT (PRESERVED 8 PLOTLY CHARTS)
# =====================================================================
with tab_consumer:
    st.markdown("### 🔍 Consumer Metered Electricity Demand Audit & Diurnal Profile")
    st.caption("Municipal & Citizen Benchmark Ingestion with 8 Interactive Analytics Graphs")

    # Ingestion Controls
    st.markdown('<div class="schemes-section-card">', unsafe_allow_html=True)
    col_persona, col_source, col_tariff = st.columns([4, 5, 3])
    with col_persona:
        selected_persona = st.selectbox("Select Consumer Profile:", list(PERSONA_PROFILES.keys()), index=1, key="aud_pers_sel")
        st.session_state.selected_persona = selected_persona
    with col_source:
        selected_mode = st.selectbox("Data Ingestion Mode:", ["Benchmark Profile (Preloaded)", "Upload Meter CSV File", "Manual Parameter Ingestion"], index=0, key="aud_mode_sel")
        st.session_state.selected_mode = selected_mode
    with col_tariff:
        tariff_rate = st.number_input("Official Tariff Rate (₹/kWh):", min_value=1.0, max_value=30.0, value=7.5, step=0.5, key="aud_tariff_inp")
    st.markdown('</div>', unsafe_allow_html=True)

    # Load Data
    profile_info = PERSONA_PROFILES[selected_persona]
    sample_path = profile_info["default_sample_file"]
    df_usage = None

    if selected_mode == "Upload Meter CSV File":
        uploaded_file = st.file_uploader("Upload CSV containing Date and kWh columns:", type=["csv"], key="aud_uploader")
        if uploaded_file:
            try:
                df_raw = pd.read_csv(uploaded_file)
                valid, err, df_usage = validate_dataframe(df_raw)
                if valid: st.success(f"Ingested {len(df_usage)} meter records.")
            except Exception as e: st.error(str(e))
    elif selected_mode == "Manual Parameter Ingestion":
        np.random.seed(42)
        dates = [datetime.today() - timedelta(days=i) for i in range(14, 0, -1)]
        df_usage = pd.DataFrame({"date": dates, "kwh": [18.5 + np.random.normal(0, 2) for _ in range(14)]})
    else:
        if os.path.exists(sample_path):
            df_raw = pd.read_csv(sample_path)
            _, _, df_usage = validate_dataframe(df_raw)

    if df_usage is not None and not df_usage.empty:
        stats = calculate_usage_statistics(df_usage)
        peak_info = detect_peak_days_and_anomalies(df_usage)
        diurnal_df = generate_diurnal_hourly_profile(selected_persona, stats['mean_kwh'])
        appliance_breakdown_df = get_persona_appliance_breakdown(selected_persona, stats['total_kwh'], tariff_rate)

        # 5 KPI Cards
        c1, c2, c3, c4, c5 = st.columns(5)
        with c1: st.markdown(f'<div class="gov-kpi-card"><div class="gov-kpi-label">Total Load</div><div class="gov-kpi-value">{stats["total_kwh"]:,.1f} <span style="font-size:0.8rem">kWh</span></div><div class="gov-kpi-sub">{stats["sample_count"]} Days</div></div>', unsafe_allow_html=True)
        with c2: st.markdown(f'<div class="gov-kpi-card"><div class="gov-kpi-label">Daily Mean</div><div class="gov-kpi-value">{stats["mean_kwh"]} <span style="font-size:0.8rem">kWh/d</span></div><div class="gov-kpi-sub">Median: {stats["median_kwh"]}</div></div>', unsafe_allow_html=True)
        with c3: st.markdown(f'<div class="gov-kpi-card"><div class="gov-kpi-label">Tariff Incurred</div><div class="gov-kpi-value">₹{stats["total_kwh"]*tariff_rate:,.1f}</div><div class="gov-kpi-sub">@₹{tariff_rate}/kWh</div></div>', unsafe_allow_html=True)
        with c4: st.markdown(f'<div class="gov-kpi-card green"><div class="gov-kpi-label">Carbon Impact</div><div class="gov-kpi-value">{stats["total_kwh"]*0.716:,.1f} <span style="font-size:0.8rem">kg</span></div><div class="gov-kpi-sub">CEA Grid Factor</div></div>', unsafe_allow_html=True)
        with c5: st.markdown(f'<div class="gov-kpi-card red"><div class="gov-kpi-label">Peak/Avg Ratio</div><div class="gov-kpi-value">{stats["peak_to_avg_ratio"]}x</div><div class="gov-kpi-sub">{stats["trend_direction"]}</div></div>', unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        # Graph Row 1: Daily Trend & Diurnal 24h Load Curve
        g1, g2 = st.columns([7, 5])
        with g1:
            st.markdown('<div class="gov-section-panel">', unsafe_allow_html=True)
            st.markdown('<div class="gov-panel-header">📈 GRAPH 1: Daily Demand Trajectory & 7-Day Moving Average</div>', unsafe_allow_html=True)
            df_rolling = df_usage.copy()
            df_rolling['rolling_7d'] = df_rolling['kwh'].rolling(window=7, min_periods=1).mean()
            fig1 = go.Figure()
            fig1.add_trace(go.Bar(x=df_rolling['date'], y=df_rolling['kwh'], name='Daily Metered kWh', marker_color='#B9D5ED'))
            fig1.add_trace(go.Scatter(x=df_rolling['date'], y=df_rolling['rolling_7d'], mode='lines', name='7-Day Trend', line=dict(color='#0B3C68', width=2.5)))
            fig1.update_layout(paper_bgcolor="#FFFFFF", plot_bgcolor="#FFFFFF", height=320, margin=dict(l=10, r=10, t=10, b=10))
            st.plotly_chart(fig1, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)

        with g2:
            st.markdown('<div class="gov-section-panel">', unsafe_allow_html=True)
            st.markdown('<div class="gov-panel-header">🕒 GRAPH 2: 24-Hour Diurnal Load by ToD Tariff Zones</div>', unsafe_allow_html=True)
            fig2 = px.bar(
                diurnal_df, x='hour_label', y='current_load_kwh', color='tod_category',
                color_discrete_map={"Morning Peak (ToD +20%)": "#DC2626", "Evening Peak (ToD +25%)": "#B91C1C", "Solar Hours (Clean Energy)": "#F59E0B", "Night Off-Peak (ToD -15%)": "#0F766E"}
            )
            fig2.update_layout(paper_bgcolor="#FFFFFF", plot_bgcolor="#FFFFFF", height=320, margin=dict(l=10, r=10, t=10, b=10))
            st.plotly_chart(fig2, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)

        # Graph Row 2: Appliance Donut & Day-of-Week
        g3, g4 = st.columns([6, 6])
        with g3:
            st.markdown('<div class="gov-section-panel">', unsafe_allow_html=True)
            st.markdown('<div class="gov-panel-header">🍩 GRAPH 3: Appliance Consumption Share</div>', unsafe_allow_html=True)
            fig3 = px.pie(appliance_breakdown_df, names='Appliance Group', values='Consumption (kWh)', hole=0.45)
            fig3.update_layout(paper_bgcolor="#FFFFFF", plot_bgcolor="#FFFFFF", height=300, margin=dict(l=10, r=10, t=10, b=10))
            st.plotly_chart(fig3, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)

        with g4:
            st.markdown('<div class="gov-section-panel">', unsafe_allow_html=True)
            st.markdown('<div class="gov-panel-header">📅 GRAPH 4: Day-of-Week Load Distribution</div>', unsafe_allow_html=True)
            df_dow = pd.DataFrame(peak_info['dow_breakdown'])
            fig4 = px.bar(df_dow, x='day_name', y='kwh', color='kwh', color_continuous_scale="Blues")
            fig4.update_layout(paper_bgcolor="#FFFFFF", plot_bgcolor="#FFFFFF", height=300, margin=dict(l=10, r=10, t=10, b=10), coloraxis_showscale=False)
            st.plotly_chart(fig4, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)


# =====================================================================
# TAB 10: 💡 SAVINGS PLANNER (PRESERVED)
# =====================================================================
with tab_planner:
    st.markdown("### 💡 Peak Shaving & Decarbonization Planner")
    st.caption("Time-of-Day (ToD) Load Flattening & Multi-Tier Carbon Mitigation")

    # Load baseline
    profile_info = PERSONA_PROFILES[st.session_state.selected_persona]
    sample_path = profile_info["default_sample_file"]
    df_raw = pd.read_csv(sample_path)
    _, _, df_usage = validate_dataframe(df_raw)
    stats = calculate_usage_statistics(df_usage)
    diurnal_df = generate_diurnal_hourly_profile(st.session_state.selected_persona, stats['mean_kwh'])
    savings_tiers = generate_multi_tier_projections(stats['total_kwh'], 7.5, 0.716, "₹")

    # Graphs Row: Flattening & Multi-Tier Savings
    op1, op2 = st.columns([7, 5])
    with op1:
        st.markdown('<div class="gov-section-panel">', unsafe_allow_html=True)
        st.markdown('<div class="gov-panel-header">⚡ GRAPH 7: 24-Hour Diurnal Load Flattening (Before vs After)</div>', unsafe_allow_html=True)
        fig7 = go.Figure()
        fig7.add_trace(go.Scatter(x=diurnal_df['hour_label'], y=diurnal_df['current_load_kwh'], mode='lines+markers', name='Current Unmanaged Load', line=dict(color='#DC2626', width=2.5)))
        fig7.add_trace(go.Scatter(x=diurnal_df['hour_label'], y=diurnal_df['shifted_load_kwh'], mode='lines+markers', name='Optimized Shifted Load', line=dict(color='#059669', width=2.5)))
        fig7.add_vrect(x0="18:00", x1="21:00", fillcolor="rgba(220, 38, 38, 0.08)", layer="below", line_width=0, annotation_text="Peak Surcharge Window")
        fig7.update_layout(paper_bgcolor="#FFFFFF", plot_bgcolor="#FFFFFF", height=320, margin=dict(l=10, r=10, t=10, b=10))
        st.plotly_chart(fig7, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with op2:
        st.markdown('<div class="gov-section-panel">', unsafe_allow_html=True)
        st.markdown('<div class="gov-panel-header">💰 GRAPH 8: Cost Savings Across Multi-Tier Goals</div>', unsafe_allow_html=True)
        tier_df = pd.DataFrame([
            {"Tier": "10% Moderate", "Cost Saved (₹)": savings_tiers["10_percent"]["cost_saved"]},
            {"Tier": "20% Recommended", "Cost Saved (₹)": savings_tiers["20_percent"]["cost_saved"]},
            {"Tier": "30% Ambitious", "Cost Saved (₹)": savings_tiers["30_percent"]["cost_saved"]},
        ])
        fig8 = px.bar(tier_df, x='Tier', y='Cost Saved (₹)', color='Cost Saved (₹)', color_continuous_scale="Greens")
        fig8.update_layout(paper_bgcolor="#FFFFFF", plot_bgcolor="#FFFFFF", height=320, margin=dict(l=10, r=10, t=10, b=10), coloraxis_showscale=False)
        st.plotly_chart(fig8, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # Simulator Slider
    st.markdown('<div class="gov-section-panel">', unsafe_allow_html=True)
    st.markdown('<div class="gov-panel-header">🎯 Target Energy Reduction & Bill Simulator</div>', unsafe_allow_html=True)
    tgt = st.slider("Target Energy Reduction (%):", 5, 40, 15, key="plan_tgt_slider")
    custom_sav = project_savings(stats['total_kwh'], 7.5, float(tgt), 0.716, "₹")
    sc1, sc2, sc3, sc4 = st.columns(4)
    with sc1: st.metric("Energy Saved", f"{custom_sav['kwh_saved']} kWh")
    with sc2: st.metric("Bill Savings", f"₹{custom_sav['cost_saved']:,.2f}")
    with sc3: st.metric("CO₂ Mitigated", f"{custom_sav['co2_saved_kg']} kg")
    with sc4: st.metric("Trees Equivalent", f"{custom_sav['trees_equivalent']} Trees/yr")
    st.markdown('</div>', unsafe_allow_html=True)


# =====================================================================
# TAB 11: 🤖 OFFICIAL AI ADVISOR DESK (PRESERVED)
# =====================================================================
with tab_advisor:
    st.markdown("### 🤖 National Clean Energy AI Advisory Desk")
    st.caption("Statutory Decision Support grounded in Bureau of Energy Efficiency (BEE) & UN SDG 7 Standards")

    # Diagnostic Wizard Expander
    with st.expander("🔍 Interactive Appliance Energy Waste Diagnostic Tool", expanded=False):
        c_a1, c_a2 = st.columns(2)
        with c_a1: diag_app = st.selectbox("Select Appliance:", ["Air Conditioner (1.5 Ton)", "Electric Geyser (25L)", "Refrigerator (250L)"], key="diag_app_sel")
        with c_a2: diag_hrs = st.slider("Daily Hours:", 1, 24, 8, key="diag_hrs_slider")
        diag_df = pd.DataFrame([
            {"Tier": "1-Star Inefficient", "Power": "1650 W", "Est. Annual Cost": f"₹{round(1.65*diag_hrs*365*7.5, 0)}"},
            {"Tier": "3-Star Standard", "Power": "1400 W", "Est. Annual Cost": f"₹{round(1.4*diag_hrs*365*7.5, 0)}"},
            {"Tier": "5-Star BEE Inverter", "Power": "950 W", "Est. Annual Cost": f"₹{round(0.95*diag_hrs*365*7.5, 0)}"}
        ])
        st.dataframe(diag_df, use_container_width=True, hide_index=True)

    # Chat Starter Buttons
    st.markdown("**Statutory Policy & Query Prompts:**")
    q_c1, q_c2, q_c3 = st.columns(3)
    quick_q = None
    if q_c1.button("❄️ BEE 24°C AC Mandate", use_container_width=True, key="btn_q_ac"): quick_q = "Explain the BEE 24 degree mandatory AC temperature rule and power savings."
    if q_c2.button("☀️ PM Surya Ghar Rooftop", use_container_width=True, key="btn_q_solar"): quick_q = "What is the subsidy under PM Surya Ghar Muft Bijli Yojana?"
    if q_c3.button("🕒 ToD Peak Load Shifting", use_container_width=True, key="btn_q_tod"): quick_q = "How does Time-of-Day tariff reduce my electricity bill?"

    # Render Chat
    for msg in st.session_state.chat_history:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    user_q = st.chat_input("Ask the Clean Energy Advisory Desk...") or quick_q
    if user_q:
        st.session_state.chat_history.append({"role": "user", "content": user_q})
        with st.chat_message("user"): st.markdown(user_q)
        with st.chat_message("assistant"):
            bot_res = ask_advisor_bot(
                user_query=user_q,
                chat_history=st.session_state.chat_history,
                persona=st.session_state.selected_persona,
                current_stats={"mean_kwh": 18.5, "peak_to_avg_ratio": 1.25},
                api_config={"provider": "offline"}
            )
            st.markdown(bot_res["answer"])
            if bot_res.get("sources"):
                st.caption(f"📚 Verified Statutory Reference: `{', '.join(set(bot_res['sources']))}`")
            st.session_state.chat_history.append({"role": "assistant", "content": bot_res["answer"]})


# =====================================================================
# TAB 12: 📑 REPORTS
# =====================================================================
with tab_reports:
    st.markdown("### 📑 Official Energy Publications & Gazette Reports")
    st.caption("Central Electricity Authority (CEA) & National Load Despatch Centre Periodic Dispatches")

    for rep in OFFICIAL_REPORTS_LIST:
        st.markdown(f"""
        <div class="gov-section-panel" style="margin-bottom: 12px; padding: 14px 18px;">
            <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap;">
                <div>
                    <span style="font-size: 0.72rem; font-weight: 700; color: #0284C7; background: #EBF3FA; padding: 2px 8px; border-radius: 3px;">
                        DOC REF: {rep['doc_number']}
                    </span>
                    <h4 style="font-size: 1.05rem; font-weight: 800; color: #0B3C68; margin: 4px 0 2px 0;">{rep['title']}</h4>
                    <p style="font-size: 0.78rem; color: #64748B; margin: 0;">Period: <b>{rep['date']}</b> &bull; Length: {rep['pages']} Pages &bull; Format: {rep['format']}</p>
                    <p style="font-size: 0.82rem; color: #334155; margin-top: 6px;">{rep['summary']}</p>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        b1, b2, b3, b4 = st.columns([2, 3, 3, 4])
        with b1:
            if st.button(f"👁️ VIEW", key=f"v_{rep['id']}", use_container_width=True):
                st.info(f"Viewing Document: {rep['title']} (Gazette Reference {rep['doc_number']})")
        with b2:
            st.download_button(
                label="⬇️ DOWNLOAD PDF",
                data=f"OFFICIAL GOVERNMENT OF INDIA REPORT: {rep['title']}\nDoc Ref: {rep['doc_number']}\nDate: {rep['date']}\n\nSummary:\n{rep['summary']}",
                file_name=f"{rep['id']}.txt",
                mime="text/plain",
                key=f"pdf_{rep['id']}",
                use_container_width=True
            )
        with b3:
            st.download_button(
                label="⬇️ DOWNLOAD CSV",
                data=generate_sample_dataset_csv(),
                file_name=f"{rep['id']}_data.csv",
                mime="text/csv",
                key=f"csv_{rep['id']}",
                use_container_width=True
            )
        st.markdown("<hr style='border: none; border-top: 1px dashed #CBD5E1; margin: 10px 0 16px 0;'>", unsafe_allow_html=True)


# =====================================================================
# TAB 13: 📞 CONTACT
# =====================================================================
with tab_contact:
    st.markdown("### 📞 Official Contact & Grievance Redressal")
    st.caption("Ministry of Power, Central Electricity Authority & National Informatics Centre")

    col_cnt1, col_cnt2 = st.columns(2)
    with col_cnt1:
        st.markdown('<div class="gov-section-panel">', unsafe_allow_html=True)
        st.markdown('<div class="gov-panel-header">🏛️ Headquarters & Directorate</div>', unsafe_allow_html=True)
        st.markdown("""
        **Ministry of Power, Government of India**  
        Shram Shakti Bhawan, Rafi Marg, New Delhi - 110001  
        - **General Public Inquiries:** 011-23710499  
        - **National Toll-Free Electricity Helpline:** 1912  
        - **EPABX Exchange:** 011-23714367  
        - **Media & Public Relations:** prministry-power@gov.in  
        
        **Working Hours:** 09:00 AM – 05:30 PM (Mon–Fri, except Gazetted Holidays)
        """)
        st.markdown('</div>', unsafe_allow_html=True)

    with col_cnt2:
        st.markdown('<div class="gov-section-panel">', unsafe_allow_html=True)
        st.markdown('<div class="gov-panel-header">💻 Technical Infrastructure & Helpdesk</div>', unsafe_allow_html=True)
        st.markdown("""
        **National Informatics Centre (NIC) Support Desk:**  
        A-Block, CGO Complex, Lodhi Road, New Delhi - 110003  
        - **Technical Support Email:** energy-support@nic.in  
        - **Portal Helpdesk Toll-Free:** 1800-111-555  
        - **Centralized Public Grievance Portal:** [https://pgportal.gov.in](https://pgportal.gov.in)  
        - **Bureau of Energy Efficiency (BEE):** 1800-180-1122  
        """)
        st.markdown('</div>', unsafe_allow_html=True)


# =====================================================================
# 5. AUTHENTIC GOVERNMENT OF INDIA FOOTER
# =====================================================================
st.markdown("""
<div class="gov-official-footer">
<div class="gov-footer-links-grid">
<div class="gov-footer-col">
<h4>Government of India</h4>
<ul>
<li><a href="https://india.gov.in" target="_blank">National Portal of India</a></li>
<li><a href="https://powermin.gov.in" target="_blank">Ministry of Power</a></li>
<li><a href="https://beeindia.gov.in" target="_blank">Bureau of Energy Efficiency</a></li>
<li><a href="https://cea.nic.in" target="_blank">Central Electricity Authority</a></li>
<li><a href="https://mnre.gov.in" target="_blank">Ministry of New & Renewable Energy</a></li>
</ul>
</div>
<div class="gov-footer-col">
<h4>Important Links</h4>
<ul>
<li><a href="#about">About Us</a></li>
<li><a href="#accessibility">Accessibility Statement</a></li>
<li><a href="#policies">Website Policies</a></li>
<li><a href="#privacy">Privacy Policy</a></li>
<li><a href="#terms">Terms & Conditions</a></li>
</ul>
</div>
<div class="gov-footer-col">
<h4>Directives & Policies</h4>
<ul>
<li><a href="#copyright">Copyright Policy</a></li>
<li><a href="#hyperlink">Hyperlinking Policy</a></li>
<li><a href="#contact">Contact Us</a></li>
<li><a href="#feedback">Citizen Feedback</a></li>
<li><a href="#help">Help & FAQ</a></li>
</ul>
</div>
<div class="gov-footer-col">
<h4>Digital India Initiatives</h4>
<ul>
<li><a href="https://pmsuryaghar.gov.in" target="_blank">PM Surya Ghar Portal</a></li>
<li><a href="https://missionlife-moefcc.nic.in" target="_blank">Mission LiFE Portal</a></li>
<li><a href="https://mygov.in" target="_blank">MyGov Citizen Engagement</a></li>
<li><a href="https://data.gov.in" target="_blank">Open Government Data (OGD)</a></li>
</ul>
</div>
</div>
<div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; font-size: 0.76rem; color: #94A3B8; border-bottom: 1px solid #1E293B; padding-bottom: 16px; margin-bottom: 14px;">
<div>
<b>Content Owned by:</b> Ministry of Power & Bureau of Energy Efficiency, Government of India<br>
<b>Designed, Developed and Hosted by:</b> National Informatics Centre (NIC)
</div>
<div style="text-align: right;">
<b>Last Updated:</b> 11 September 2026 &bull; <b>Sitemap</b><br>
<b>Total Official Visitors:</b> <span style="color: #FF9933; font-weight: 700;">2,849,152</span>
</div>
</div>
<div class="gov-footer-disclaimer-strip">
<b>STATUTORY DISCLAIMER:</b> This platform is an advanced AI-driven analytical decision-support prototype interface developed for demonstration and research purposes aligned with UN Sustainable Development Goal 7. It does not replace statutory notifications issued in the Gazette of India.
</div>
</div>
""", unsafe_allow_html=True)

