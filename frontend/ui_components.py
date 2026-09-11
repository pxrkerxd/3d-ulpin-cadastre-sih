import base64
import textwrap
import streamlit as st
from core.certificate_generator import generate_qr_code_image, generate_title_hash

def render_html(content: str):
    """
    Renders HTML safely in Streamlit by stripping all leading and trailing whitespace
    from every line and joining into a single clean string.
    This guarantees that Markdown NEVER treats any line as an indented code block (<pre><code>).
    """
    clean = " ".join(line.strip() for line in content.splitlines() if line.strip())
    st.markdown(clean, unsafe_allow_html=True)

def set_active_view(view_name: str):
    """
    Bulletproof navigation state setter.
    Sets the active view without conflicting with Streamlit widget keys.
    """
    v = str(view_name).lower()
    if "3d" in v or "twin" in v or "cadastre" in v or "explorer" in v:
        target = "🌐 3D Cadastre & Digital Twin Studio"
    elif "citizen" in v:
        target = "🏠 Citizen / Homebuyer Portal"
    elif "surveyor" in v:
        target = "📐 GIS Surveyor Workstation"
    elif "clash" in v or "subsurface" in v:
        target = "⚠️ Subsurface Clash Engine"
    elif "registrar" in v or "deed" in v:
        target = "🏛️ Sub-Registrar (Revenue Officer) Mode"
    else:
        target = "🌟 Overview & Gateway"

    st.session_state["active_view"] = target
    st.session_state["nav_role"] = target


# -------------------------------------------------------------
# SVG ICONS (Figma Native Vectors)
# -------------------------------------------------------------
ICONS_SVG = {
    "layers": """<svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
        <path d="M12 2L2 7L12 12L22 7L12 2Z" stroke="#FFFFFF" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
        <path d="M2 17L12 22L22 17" stroke="#FFFFFF" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
        <path d="M2 12L12 17L22 12" stroke="#FFFFFF" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
    </svg>""",
    "ashoka_emblem": """<svg width="32" height="32" viewBox="0 0 32 32" fill="none" xmlns="http://www.w3.org/2000/svg">
        <circle cx="16" cy="16" r="15" fill="#121829" stroke="#EAB308" stroke-width="1.5"/>
        <circle cx="16" cy="16" r="10" stroke="#00F2FE" stroke-width="1.2" stroke-dasharray="2 2"/>
        <circle cx="16" cy="16" r="4" fill="#EAB308"/>
        <line x1="16" y1="6" x2="16" y2="26" stroke="#EAB308" stroke-width="1"/>
        <line x1="6" y1="16" x2="26" y2="16" stroke="#EAB308" stroke-width="1"/>
        <line x1="9" y1="9" x2="23" y2="23" stroke="#EAB308" stroke-width="0.8"/>
        <line x1="9" y1="23" x2="23" y2="9" stroke="#EAB308" stroke-width="0.8"/>
    </svg>""",
    "user": """<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#FFFFFF" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
        <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"></path>
        <circle cx="12" cy="7" r="4"></circle>
    </svg>""",
    "compass": """<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#00F2FE" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
        <circle cx="12" cy="12" r="10"></circle>
        <polygon points="16.24 7.76 14.12 14.12 7.76 16.24 9.88 9.88 16.24 7.76"></polygon>
    </svg>""",
    "shield": """<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#A3B3D2" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
        <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"></path>
    </svg>""",
    "box": """<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#00F2FE" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
        <path d="M21 16V8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16z"></path>
        <polyline points="3.27 6.96 12 12.01 20.73 6.96"></polyline>
        <line x1="12" y1="22.08" x2="12" y2="12"></line>
    </svg>""",
    "alert_triangle": """<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#FF9F0A" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
        <path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"></path>
        <line x1="12" y1="9" x2="12" y2="13"></line>
        <line x1="12" y1="17" x2="12.01" y2="17"></line>
    </svg>""",
    "shield_check": """<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#00E676" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
        <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"></path>
        <polyline points="9 12 11 14 15 10"></polyline>
    </svg>""",
    "cuboid": """<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="#00F2FE" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
        <polygon points="12 2 2 7 12 12 22 7 12 2"></polygon>
        <polyline points="2 17 12 22 22 17"></polyline>
        <polyline points="2 12 12 17 22 12"></polyline>
    </svg>""",
    "bell": """<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#FFFFFF" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
        <path d="M18 8A6 6 0 0 0 6 8c0 7-3 9-3 9h18s-3-2-3-9"></path>
        <path d="M13.73 21a2 2 0 0 1-3.46 0"></path>
    </svg>""",
    "eye": """<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#00F2FE" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
        <path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"></path>
        <circle cx="12" cy="12" r="3"></circle>
    </svg>""",
    "plus": """<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#A3B3D2" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
        <line x1="12" y1="5" x2="12" y2="19"></line>
        <line x1="5" y1="12" x2="19" y2="12"></line>
    </svg>""",
    "arrow_right": """<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#00F2FE" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
        <line x1="5" y1="12" x2="19" y2="12"></line>
        <polyline points="12 5 19 12 12 19"></polyline>
    </svg>""",
    "crosshair": """<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="#00F2FE" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
        <circle cx="12" cy="12" r="10"></circle>
        <line x1="22" y1="12" x2="18" y2="12"></line>
        <line x1="6" y1="12" x2="2" y2="12"></line>
        <line x1="12" y1="6" x2="12" y2="2"></line>
        <line x1="12" y1="22" x2="12" y2="18"></line>
    </svg>"""
}

# -------------------------------------------------------------
# FIGMA DESIGN SYSTEM INJECTION (CSS)
# -------------------------------------------------------------
def inject_custom_theme(theme="dark"):
    render_html("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=DM+Sans:ital,opsz,wght@0,9..40,100..1000;1,9..40,100..1000&family=Geist+Mono:wght@100..900&family=JetBrains+Mono:wght@400;600;700&display=swap');

        header[data-testid="stHeader"] {
            display: none !important;
        }
        footer {
            display: none !important;
        }
        #MainMenu {
            visibility: hidden;
        }

        .stApp {
            background-color: #0A0D1A !important;
            background: #0A0D1A !important;
            color: #FFFFFF !important;
            font-family: 'DM Sans', -apple-system, BlinkMacSystemFont, sans-serif !important;
        }

        .block-container {
            padding-top: 0.5rem !important;
            padding-bottom: 2rem !important;
            max-width: 1440px !important;
            margin: 0 auto !important;
        }

        h1, h2, h3, h4, h5, h6 {
            font-family: 'DM Sans', sans-serif !important;
            color: #FFFFFF !important;
            font-weight: 700;
        }
        p, span, div, label {
            font-family: 'DM Sans', sans-serif;
            color: #A3B3D2;
        }
        code, pre, .mono-font {
            font-family: 'Geist Mono', monospace !important;
        }

        ::-webkit-scrollbar {
            width: 8px;
            height: 8px;
        }
        ::-webkit-scrollbar-track {
            background: #0A0D1A;
        }
        ::-webkit-scrollbar-thumb {
            background: #202B44;
            border-radius: 4px;
        }
        ::-webkit-scrollbar-thumb:hover {
            background: #00F2FE;
        }

        div[data-baseweb="select"] > div {
            background-color: #121829 !important;
            border: 1px solid #202B44 !important;
            border-radius: 8px !important;
            color: #FFFFFF !important;
            font-family: 'DM Sans', sans-serif !important;
        }
        div[data-baseweb="select"] * {
            color: #FFFFFF !important;
            font-family: 'DM Sans', sans-serif !important;
        }
        div[data-baseweb="popover"] div {
            background-color: #121829 !important;
            border: 1px solid #202B44 !important;
            color: #FFFFFF !important;
        }

        div[data-baseweb="input"] {
            background-color: #121829 !important;
            border: 1px solid #202B44 !important;
            border-radius: 8px !important;
        }
        input[data-testid="stTextInput"], input[data-testid="stNumberInput"] {
            color: #FFFFFF !important;
            background-color: transparent !important;
            font-family: 'DM Sans', sans-serif !important;
        }
        input::placeholder {
            color: #6B7C9E !important;
        }

        .stButton > button,
        button[kind="secondary"],
        button[data-testid*="secondary"] {
            background: #121829 !important;
            border: 1px solid #202B44 !important;
            border-radius: 8px !important;
            color: #FFFFFF !important;
            font-family: 'DM Sans', sans-serif !important;
            font-weight: 600 !important;
            font-size: 13px !important;
            padding: 8px 16px !important;
            transition: all 0.2s ease !important;
        }
        .stButton > button * {
            color: inherit !important;
        }
        .stButton > button:hover {
            border-color: #00F2FE !important;
            color: #00F2FE !important;
            transform: translateY(-1px);
            box-shadow: 0 4px 14px rgba(0, 242, 254, 0.15) !important;
        }

        /* High-contrast primary buttons (Cyan Gradient with Jet-Black text) */
        button[kind="primary"],
        button[data-testid*="primary"],
        .stButton > button[kind="primary"],
        .stButton > button[data-testid*="primary"] {
            background: linear-gradient(90deg, #00F2FE 0%, #0072FF 100%) !important;
            border: none !important;
            color: #0A0D1A !important;
            font-weight: 800 !important;
        }
        button[kind="primary"] *,
        button[data-testid*="primary"] *,
        .stButton > button[kind="primary"] *,
        .stButton > button[data-testid*="primary"] * {
            color: #0A0D1A !important;
            font-weight: 800 !important;
        }
        button[kind="primary"]:hover,
        button[data-testid*="primary"]:hover {
            opacity: 0.95;
            box-shadow: 0 4px 20px rgba(0, 242, 254, 0.4) !important;
        }
        button[kind="primary"]:hover *,
        button[data-testid*="primary"]:hover * {
            color: #0A0D1A !important;
        }

        /* High-visibility alert action button (Notify Metro Authority) */
        div:has(.btn-metro-anchor) button,
        div[data-testid="column"]:has(.btn-metro-anchor) button,
        .btn-metro-dispatch {
            background: linear-gradient(90deg, #FF9F0A 0%, #F59E0B 100%) !important;
            border: 1px solid #FF9F0A !important;
            color: #000000 !important;
            font-weight: 800 !important;
            box-shadow: 0 4px 18px rgba(255, 159, 10, 0.45) !important;
        }
        div:has(.btn-metro-anchor) button *,
        div[data-testid="column"]:has(.btn-metro-anchor) button *,
        .btn-metro-dispatch * {
            color: #000000 !important;
            font-weight: 800 !important;
        }
        div:has(.btn-metro-anchor) button:hover,
        div[data-testid="column"]:has(.btn-metro-anchor) button:hover,
        .btn-metro-dispatch:hover {
            background: linear-gradient(90deg, #F59E0B 0%, #D97706 100%) !important;
            box-shadow: 0 6px 24px rgba(255, 159, 10, 0.65) !important;
            transform: translateY(-1px) !important;
        }
        div:has(.btn-metro-anchor) button:hover *,
        div[data-testid="column"]:has(.btn-metro-anchor) button:hover *,
        .btn-metro-dispatch:hover * {
            color: #000000 !important;
        }

        div[data-testid="stRadio"] [role="radiogroup"] {
            display: flex !important;
            justify-content: center !important;
            gap: 6px !important;
            background: #121829 !important;
            border: 1px solid #202B44 !important;
            border-radius: 10px !important;
            padding: 4px 6px !important;
            margin-bottom: 8px !important;
        }
        div[data-testid="stRadio"] input[type="radio"] {
            display: none !important;
        }
        div[data-testid="stRadio"] div[role="radiogroup"] > label {
            background: transparent !important;
            border: 1px solid transparent !important;
            border-radius: 7px !important;
            padding: 6px 14px !important;
            cursor: pointer !important;
            margin: 0 !important;
            transition: all 0.2s ease !important;
        }
        div[data-testid="stRadio"] div[role="radiogroup"] > label:hover {
            background: #1A2238 !important;
            border-color: #202B44 !important;
        }
        div[data-testid="stRadio"] div[role="radiogroup"] > label:has(input:checked) {
            background: rgba(0, 242, 254, 0.12) !important;
            border-color: #00F2FE !important;
        }
        div[data-testid="stRadio"] div[role="radiogroup"] > label:has(input:checked) span,
        div[data-testid="stRadio"] div[role="radiogroup"] > label:has(input:checked) p {
            color: #00F2FE !important;
            font-weight: 700 !important;
        }
        div[data-testid="stRadio"] div[role="radiogroup"] > label span,
        div[data-testid="stRadio"] div[role="radiogroup"] > label p {
            color: #A3B3D2 !important;
            font-family: 'DM Sans', sans-serif !important;
            font-size: 12px !important;
            font-weight: 600 !important;
            margin: 0 !important;
        }

        div[data-testid="stMetric"] {
            background: #121829 !important;
            border: 1px solid #202B44 !important;
            border-radius: 8px !important;
            padding: 16px !important;
        }
        div[data-testid="stMetricLabel"] p {
            color: #6B7C9E !important;
            font-size: 12px !important;
            font-weight: 400 !important;
            font-family: 'DM Sans', sans-serif !important;
            text-transform: none !important;
        }
        div[data-testid="stMetricValue"] {
            color: #00F2FE !important;
            font-family: 'Geist Mono', monospace !important;
            font-size: 28px !important;
            font-weight: 700 !important;
        }

        button[data-baseweb="tab"] {
            font-family: 'DM Sans', sans-serif !important;
            font-weight: 600 !important;
            font-size: 14px !important;
            color: #A3B3D2 !important;
            transition: all 0.25s cubic-bezier(0.16, 1, 0.3, 1) !important;
        }
        button[data-baseweb="tab"]:hover {
            color: #00F2FE !important;
        }
        button[data-baseweb="tab"][aria-selected="true"] {
            color: #00F2FE !important;
            border-bottom-color: #00F2FE !important;
        }

        /* ======================================================== */
        /* FLUID ANIMATION & MICRO-INTERACTION ENGINE               */
        /* ======================================================== */
        @keyframes fluidSlideUp {
            0% {
                opacity: 0;
                transform: translateY(12px);
            }
            100% {
                opacity: 1;
                transform: translateY(0);
            }
        }
        @keyframes fluidFadeIn {
            0% {
                opacity: 0;
            }
            100% {
                opacity: 1;
            }
        }
        @keyframes cyberPulseRing {
            0% {
                box-shadow: 0 0 0 0 rgba(0, 242, 254, 0.6);
            }
            70% {
                box-shadow: 0 0 0 8px rgba(0, 242, 254, 0);
            }
            100% {
                box-shadow: 0 0 0 0 rgba(0, 242, 254, 0);
            }
        }
        @keyframes radarGreenPing {
            0% {
                transform: scale(0.95);
                box-shadow: 0 0 0 0 rgba(0, 230, 118, 0.7);
            }
            70% {
                transform: scale(1.1);
                box-shadow: 0 0 0 8px rgba(0, 230, 118, 0);
            }
            100% {
                transform: scale(0.95);
                box-shadow: 0 0 0 0 rgba(0, 230, 118, 0);
            }
        }
        @keyframes amberHazardBreathing {
            0%, 100% {
                box-shadow: 0 0 8px rgba(255, 159, 10, 0.35);
                border-color: #FF9F0A;
            }
            50% {
                box-shadow: 0 0 18px rgba(255, 159, 10, 0.65);
                border-color: #F59E0B;
            }
        }
        @keyframes shimmerGlow {
            0% { background-position: 0% 50%; }
            50% { background-position: 100% 50%; }
            100% { background-position: 0% 50%; }
        }

        /* Fluid Entrance on View Switch */
        .block-container {
            animation: fluidFadeIn 0.35s cubic-bezier(0.16, 1, 0.3, 1) both;
        }

        /* Interactive Card Physics */
        div[data-testid="stMetric"],
        div[data-testid="stExpander"],
        div[data-testid="stForm"],
        div[data-testid="stDeckGlJsonChart"] {
            animation: fluidSlideUp 0.4s cubic-bezier(0.16, 1, 0.3, 1) both;
            transition: all 0.28s cubic-bezier(0.16, 1, 0.3, 1) !important;
        }
        div[data-testid="stMetric"]:hover {
            transform: translateY(-3px) !important;
            border-color: rgba(0, 242, 254, 0.5) !important;
            box-shadow: 0 10px 28px rgba(0, 242, 254, 0.16) !important;
        }
        div[data-testid="stExpander"]:hover {
            border-color: rgba(0, 242, 254, 0.3) !important;
        }

        /* Generic Card Hover Micro-Interactions */
        div[style*="background: #121829"],
        div[style*="background: #1A2238"] {
            transition: all 0.28s cubic-bezier(0.16, 1, 0.3, 1) !important;
        }
        div[style*="background: #121829"]:hover {
            border-color: rgba(0, 242, 254, 0.35) !important;
            box-shadow: 0 8px 24px rgba(0, 0, 0, 0.4), 0 0 16px rgba(0, 242, 254, 0.08) !important;
        }
        div[style*="background: #1A2238"]:hover {
            border-color: rgba(0, 242, 254, 0.45) !important;
            transform: translateY(-2px);
        }
        div[style*="background: linear-gradient(90deg, #00F2FE 0%, #0072FF 100%)"]:hover {
            transform: scale(1.05);
            box-shadow: 0 0 20px rgba(0, 242, 254, 0.5) !important;
            transition: all 0.3s ease !important;
        }

        /* Fluid Button Transitions */
        .stButton > button {
            transition: all 0.22s cubic-bezier(0.16, 1, 0.3, 1) !important;
        }
        .stButton > button:hover {
            transform: translateY(-2px) !important;
            box-shadow: 0 6px 20px rgba(0, 242, 254, 0.2) !important;
        }
        .stButton > button:active {
            transform: translateY(1px) scale(0.98) !important;
            transition: transform 0.08s ease !important;
        }

        /* Primary Button Shimmer */
        button[kind="primary"],
        button[data-testid*="primary"] {
            background-size: 200% auto !important;
            animation: shimmerGlow 5s ease infinite !important;
        }

        /* Smooth Floor Slice Expansion */
        div[style*="background: rgba(0, 242, 254, 0.08)"],
        div[style*="background: rgba(255, 159, 10, 0.09)"] {
            transition: all 0.22s cubic-bezier(0.16, 1, 0.3, 1) !important;
        }
        div[style*="background: rgba(0, 242, 254, 0.08)"]:hover {
            transform: translateX(5px) !important;
            background: rgba(0, 242, 254, 0.16) !important;
            border-color: #00F2FE !important;
            box-shadow: 0 2px 14px rgba(0, 242, 254, 0.22) !important;
        }
        div[style*="background: rgba(255, 159, 10, 0.09)"]:hover {
            transform: translateX(5px) !important;
            background: rgba(255, 159, 10, 0.18) !important;
            border-color: #FF9F0A !important;
            box-shadow: 0 2px 14px rgba(255, 159, 10, 0.22) !important;
        }

        /* Pulsing Status Indicators */
        span[style*="background: #00E676; border-radius: 50%"],
        span[style*="background-color: #00E676; border-radius: 50%"] {
            display: inline-block !important;
            animation: radarGreenPing 2s infinite ease-in-out !important;
        }
        span[style*="background: #FF9F0A; border-radius: 50%"] {
            display: inline-block !important;
            animation: amberHazardBreathing 2.4s infinite ease-in-out !important;
        }
        span[style*="background: #00F2FE; border-radius: 50%"] {
            display: inline-block !important;
            animation: cyberPulseRing 2s infinite ease-in-out !important;
        }

        /* Smooth Radio Pill Tabs */
        div[data-testid="stRadio"] div[role="radiogroup"] > label {
            transition: all 0.22s cubic-bezier(0.16, 1, 0.3, 1) !important;
        }
        div[data-testid="stRadio"] div[role="radiogroup"] > label:hover {
            transform: translateY(-1px) !important;
        }
        div[data-testid="stRadio"] div[role="radiogroup"] > label:has(input:checked) {
            box-shadow: 0 0 16px rgba(0, 242, 254, 0.25) !important;
        }
        </style>
    """)

# -------------------------------------------------------------
# 1. FIGMA TOP NAVIGATION BAR (nav)
# -------------------------------------------------------------
def render_figma_navbar(active_view="overview"):
    render_html(f"""
        <div style="box-sizing: border-box; display: flex; flex-direction: row; justify-content: space-between; align-items: center; padding: 12px 24px; width: 100%; min-height: 76px; background: #0A0D1A; border-bottom: 1px solid #202B44; margin-bottom: 20px; border-radius: 8px;">
            <div style="display: flex; flex-direction: row; align-items: center; gap: 12px;">
                <div style="display: flex; justify-content: center; align-items: center; width: 40px; height: 40px; background: linear-gradient(90deg, #00F2FE 0%, #0072FF 100%); border-radius: 8px; box-shadow: 0 4px 14px rgba(0, 242, 254, 0.3);">
                    {ICONS_SVG['layers']}
                </div>
                <div style="display: flex; flex-direction: column; align-items: flex-start; gap: 2px;">
                    <span style="font-family: 'DM Sans', sans-serif; font-weight: 800; font-size: 18px; line-height: 22px; color: #FFFFFF; letter-spacing: -0.01em;">
                        3D ULPIN GENERATOR
                    </span>
                    <span style="font-family: 'Geist Mono', monospace; font-weight: 600; font-size: 10px; line-height: 13px; color: #00F2FE; letter-spacing: 0.08em;">
                        ISO 19152 CADASTRE
                    </span>
                </div>
            </div>

            <div style="display: flex; flex-direction: row; align-items: center; gap: 10px; background: #121829; border: 1px solid #202B44; padding: 6px 14px; border-radius: 20px;">
                {ICONS_SVG['ashoka_emblem']}
                <div style="display: flex; flex-direction: column; align-items: flex-start; gap: 1px;">
                    <span style="font-family: 'DM Sans', sans-serif; font-weight: 700; font-size: 11px; line-height: 14px; color: #FFFFFF; letter-spacing: 0.02em;">
                        GOVERNMENT OF INDIA
                    </span>
                    <span style="font-family: 'DM Sans', sans-serif; font-weight: 400; font-size: 9px; line-height: 12px; color: #6B7C9E;">
                        Dept. of Land Resources
                    </span>
                </div>
            </div>
        </div>
    """)

# -------------------------------------------------------------
# 2. LANDING HERO & FEATURES (landing-hero)
# -------------------------------------------------------------
def render_landing_hero(df, active_prop=None):
    prop = active_prop if active_prop else (df.iloc[0].to_dict() if not df.empty else {})
    prop_name = prop.get('name', 'Sky Heights - Block A')
    prop_city = prop.get('city', 'Pune')
    prop_id = prop.get('property_id', 101)

    c_left, c_right = st.columns([1.15, 0.85], gap="large")

    with c_left:
        render_html(f"""
            <div style="display: flex; flex-direction: column; align-items: flex-start; gap: 20px;">
                <div style="display: inline-flex; align-items: center; padding: 4px 10px; background: rgba(0, 230, 118, 0.086); border: 1px solid #00E676; border-radius: 4px;">
                    <span style="font-family: 'Geist Mono', monospace; font-weight: 700; font-size: 11px; line-height: 14px; color: #00E676; letter-spacing: 0.08em;">
                        SIH 2026 PROTOTYPE
                    </span>
                </div>

                <h1 style="font-family: 'DM Sans', sans-serif; font-weight: 800; font-size: 46px; line-height: 115%; color: #FFFFFF; margin: 0; letter-spacing: -0.02em;">
                    India's Spatial Land Registry.<br/><span style="background: linear-gradient(90deg, #00F2FE 0%, #0072FF 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">Engineered in 3D.</span>
                </h1>

                <p style="font-family: 'DM Sans', sans-serif; font-weight: 400; font-size: 16px; line-height: 160%; color: #A3B3D2; margin: 0;">
                    Extending the 14-digit Bhu-Aadhaar ULPIN below the surface and into the skies. Register absolute vertical property rights, analyze subsurface utility clashes, and secure instant spatial deeds.
                </p>

                <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 14px; width: 100%; margin-top: 6px;">
                    <div style="background: #121829; border: 1px solid #202B44; border-radius: 8px; padding: 14px;">
                        <div style="font-family: 'Geist Mono', monospace; font-weight: 700; font-size: 24px; line-height: 30px; color: #00F2FE;">14.2M+</div>
                        <div style="font-family: 'DM Sans', sans-serif; font-size: 12px; color: #6B7C9E; margin-top: 4px;">Properties Indexed</div>
                    </div>
                    <div style="background: #121829; border: 1px solid #202B44; border-radius: 8px; padding: 14px;">
                        <div style="font-family: 'Geist Mono', monospace; font-weight: 700; font-size: 24px; line-height: 30px; color: #00E676;">28</div>
                        <div style="font-family: 'DM Sans', sans-serif; font-size: 12px; color: #6B7C9E; margin-top: 4px;">States & UTs Active</div>
                    </div>
                    <div style="background: #121829; border: 1px solid #202B44; border-radius: 8px; padding: 14px;">
                        <div style="font-family: 'Geist Mono', monospace; font-weight: 700; font-size: 24px; line-height: 30px; color: #FF9F0A;">86.4K</div>
                        <div style="font-family: 'DM Sans', sans-serif; font-size: 12px; color: #6B7C9E; margin-top: 4px;">Subsurface Clashes Solved</div>
                    </div>
                </div>

                <div style="font-family: 'DM Sans', sans-serif; font-weight: 700; font-size: 13px; color: #FFFFFF; letter-spacing: 0.06em; margin-top: 8px; text-transform: uppercase;">
                    ACCESS SYSTEM GATEWAYS
                </div>
            </div>
        """)

        c_g1, c_g2, c_g3 = st.columns(3, gap="small")
        with c_g1:
            if st.button("🏠 Citizen Portal\nVerify, View & Download", key="gw_citizen_btn", use_container_width=True):
                set_active_view("🏠 Citizen / Homebuyer Portal")
                st.rerun()
        with c_g2:
            if st.button("📐 GIS Surveyor\nCapture Cadastral Twins", key="gw_surveyor_btn", use_container_width=True):
                set_active_view("📐 GIS Surveyor Workstation")
                st.rerun()
        with c_g3:
            if st.button("🏛️ Sub-Registrar\nApprove 3D Deeds & Clashes", key="gw_registrar_btn", use_container_width=True):
                set_active_view("🏛️ Sub-Registrar (Revenue Officer) Mode")
                st.rerun()

    with c_right:
        render_html(f"""
            <div style="box-sizing: border-box; background: #121829; border: 1px solid #202B44; border-radius: 16px; padding: 20px; display: flex; flex-direction: column; gap: 16px;">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <div style="display: flex; align-items: center; gap: 8px;">
                        <span style="width: 10px; height: 10px; background: #00F2FE; border-radius: 50%; display: inline-block; box-shadow: 0 0 8px #00F2FE;"></span>
                        <span style="font-family: 'DM Sans', sans-serif; font-weight: 700; font-size: 13px; color: #FFFFFF;">INTERACTIVE 3D CADASTRE</span>
                    </div>
                    <span style="background: rgba(0, 242, 254, 0.11); border: 1px solid #00F2FE; border-radius: 4px; padding: 2px 8px; font-family: 'Geist Mono', monospace; font-size: 10px; font-weight: 700; color: #00F2FE;">
                        ISO 19152 MODEL
                    </span>
                </div>

                <div style="position: relative; width: 100%; height: 260px; background: radial-gradient(circle at 50% 50%, #172033 0%, #080C16 100%); border: 1px solid #202B44; border-radius: 10px; overflow: hidden; display: flex; flex-direction: column; align-items: center; justify-content: center;">
                    <div style="font-size: 54px; filter: drop-shadow(0 0 16px rgba(0, 242, 254, 0.4));">🏙️</div>
                    <div style="font-family: 'DM Sans', sans-serif; font-weight: 700; font-size: 14px; color: #FFFFFF; margin-top: 8px;">{prop_name}</div>
                    <div style="font-family: 'Geist Mono', monospace; font-size: 11px; color: #00F2FE; margin-top: 2px;">{prop_city.upper()} &bull; PARCEL #{prop_id}</div>
                    <div style="position: absolute; bottom: 10px; left: 14px; display: flex; gap: 8px;">
                        <span style="background: rgba(0, 230, 118, 0.15); color: #00E676; border: 1px solid #00E676; padding: 2px 6px; border-radius: 4px; font-size: 9px; font-family: 'Geist Mono', monospace; font-weight: 700;">VOLUMETRIC SLICED</span>
                        <span style="background: rgba(0, 242, 254, 0.15); color: #00F2FE; border: 1px solid #00F2FE; padding: 2px 6px; border-radius: 4px; font-size: 9px; font-family: 'Geist Mono', monospace; font-weight: 700;">SATELLITE GROUND ON</span>
                    </div>
                </div>

                <div style="background: #0F1422; border: 1px solid #202B44; border-radius: 8px; padding: 12px; display: flex; flex-direction: column; gap: 6px;">
                    <div style="font-family: 'Geist Mono', monospace; font-size: 11px; color: #00F2FE; font-weight: 600;">
                        ACTIVE SELECTION: FL-04 (RESIDENTIAL UNIT)
                    </div>
                    <div style="width: 100%; height: 1px; background: #202B44;"></div>
                    <div style="display: flex; justify-content: space-between; align-items: center; font-size: 12px;">
                        <span style="color: #6B7C9E;">3D ULPIN Prefix</span>
                        <span style="font-family: 'Geist Mono', monospace; color: #FFFFFF; font-weight: 600;">IN-MH-PUN-FL04-U12</span>
                    </div>
                </div>
            </div>
        """)

        if st.button("🌐 Launch Full 3D WebGL Digital Twin Studio", key="btn_launch_hero_twin", type="primary", use_container_width=True):
            st.session_state["selected_parcel_id"] = 101
            st.session_state["twin_studio_toggle_widget"] = True
            st.session_state["force_twin_view"] = True
            set_active_view("🌐 3D Cadastre & Digital Twin Studio")
            st.rerun()

    # Features Row
    render_html("<div style='height: 28px;'></div>")
    f1, f2, f3 = st.columns(3, gap="medium")
    with f1:
        render_html(f"""
            <div style="background: #121829; border: 1px solid #202B44; border-radius: 12px; padding: 20px; display: flex; flex-direction: column; gap: 12px; min-height: 160px;">
                <div style="width: 36px; height: 36px; background: rgba(0, 242, 254, 0.11); border-radius: 8px; display: flex; align-items: center; justify-content: center;">
                    {ICONS_SVG['box']}
                </div>
                <div style="font-family: 'DM Sans', sans-serif; font-weight: 700; font-size: 18px; color: #FFFFFF;">
                    Vertical 3D ULPIN
                </div>
                <div style="font-family: 'DM Sans', sans-serif; font-size: 13px; line-height: 150%; color: #A3B3D2;">
                    Standardizing block, floor, and unit coordinates to legally secure sky and air rights above parcels.
                </div>
            </div>
        """)
    with f2:
        render_html(f"""
            <div style="background: #121829; border: 1px solid #202B44; border-radius: 12px; padding: 20px; display: flex; flex-direction: column; gap: 12px; min-height: 160px;">
                <div style="width: 36px; height: 36px; background: rgba(255, 159, 10, 0.11); border-radius: 8px; display: flex; align-items: center; justify-content: center;">
                    {ICONS_SVG['alert_triangle']}
                </div>
                <div style="font-family: 'DM Sans', sans-serif; font-weight: 700; font-size: 18px; color: #FFFFFF;">
                    Subsurface Clash Engine
                </div>
                <div style="font-family: 'DM Sans', sans-serif; font-size: 13px; line-height: 150%; color: #A3B3D2;">
                    Detects encroachment of foundation pilings with city gas, metro tunnels, and water networks.
                </div>
            </div>
        """)
    with f3:
        render_html(f"""
            <div style="background: #121829; border: 1px solid #202B44; border-radius: 12px; padding: 20px; display: flex; flex-direction: column; gap: 12px; min-height: 160px;">
                <div style="width: 36px; height: 36px; background: rgba(0, 230, 118, 0.086); border-radius: 8px; display: flex; align-items: center; justify-content: center;">
                    {ICONS_SVG['shield_check']}
                </div>
                <div style="font-family: 'DM Sans', sans-serif; font-weight: 700; font-size: 18px; color: #FFFFFF;">
                    Sealed Spatial Deeds
                </div>
                <div style="font-family: 'DM Sans', sans-serif; font-size: 13px; line-height: 150%; color: #A3B3D2;">
                    Cryptographically signed 3D cadastral land certificates verifiable on state ledgers with instant QR lookup.
                </div>
            </div>
        """)

# -------------------------------------------------------------
# 3. CITIZEN DASHBOARD (citizen-dashboard)
# -------------------------------------------------------------
def render_citizen_dashboard(prop_data, floors, ulpin_str="27221040120105-004"):
    effective_owner = prop_data.get('owner', 'Rajesh Sharma & Anita Sharma')
    prop_name = prop_data.get('name', 'Sky Heights - Block A')
    prop_city = prop_data.get('city', 'Pune')

    render_html(f"""
        <div style="display: flex; justify-content: space-between; align-items: center; background: #121829; border: 1px solid #202B44; border-radius: 12px; padding: 20px 24px; margin-bottom: 20px;">
            <div>
                <div style="font-family: 'DM Sans', sans-serif; font-weight: 800; font-size: 26px; color: #FFFFFF;">
                    Namaste, {effective_owner}
                </div>
                <div style="font-family: 'DM Sans', sans-serif; font-size: 14px; color: #A3B3D2; margin-top: 4px;">
                    Manage and verify your registered vertical assets below.
                </div>
            </div>
            <div style="display: flex; align-items: center; gap: 14px;">
                <div style="width: 40px; height: 40px; background: #1A2238; border: 1px solid #202B44; border-radius: 50%; display: flex; align-items: center; justify-content: center;">
                    {ICONS_SVG['bell']}
                </div>
                <div style="display: flex; align-items: center; gap: 10px; background: #1D253A; border: 1px solid #202B44; padding: 6px 14px; border-radius: 30px;">
                    <div style="width: 26px; height: 26px; background: linear-gradient(90deg, #00F2FE, #0072FF); border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 12px; font-weight: 700; color: #fff;">
                        RS
                    </div>
                    <span style="font-family: 'DM Sans', sans-serif; font-weight: 600; font-size: 13px; color: #FFFFFF;">
                        {effective_owner.split('&')[0].strip()}
                    </span>
                </div>
            </div>
        </div>
    """)

    b1, b2, b3 = st.columns(3, gap="medium")
    with b1:
        if st.button("👁️ Launch 3D Explorer", key="cit_launch_3d_btn", use_container_width=True):
            st.session_state["selected_parcel_id"] = 101
            st.session_state["twin_studio_toggle_widget"] = True
            st.session_state["force_twin_view"] = True
            set_active_view("🌐 3D Cadastre & Digital Twin Studio")
            st.rerun()
    with b2:
        show_cert = st.session_state.get("show_full_certificate", False)
        cert_label = "📄 Hide Certificate View" if show_cert else "🛡️ Verify Spatial Certificate"
        if st.button(cert_label, key="cit_verify_cert_btn", use_container_width=True):
            st.session_state["show_full_certificate"] = not show_cert
            st.rerun()
    with b3:
        if st.button("➕ Request 3D Re-Survey", key="cit_resurvey_btn", use_container_width=True):
            st.session_state["resurvey_ticket"] = "Token #SR-2026-9912 generated. Municipal Surveyor Amit Patwardhan assigned for physical RTK verification."
            st.rerun()

    if st.session_state.get("resurvey_ticket"):
        st.success(f"✅ {st.session_state['resurvey_ticket']}")

    render_html("<div style='height: 20px;'></div>")

    # Property Cards Portfolio Grid
    render_html("""
        <div style="font-family: 'DM Sans', sans-serif; font-weight: 700; font-size: 16px; color: #FFFFFF; margin-bottom: 12px;">
            Registered 3D Property Portfolio
        </div>
    """)

    p1, p2 = st.columns(2, gap="medium")
    with p1:
        render_html(f"""
            <div style="background: #121829; border: 1px solid #202B44; border-radius: 12px; overflow: hidden; display: flex; flex-direction: column;">
                <div style="height: 120px; background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%); display: flex; align-items: center; justify-content: center; position: relative;">
                    <div style="font-size: 44px; filter: drop-shadow(0 0 10px rgba(0, 242, 254, 0.3));">🏙️</div>
                    <div style="position: absolute; top: 12px; right: 12px; background: rgba(0, 230, 118, 0.15); border: 1px solid #00E676; border-radius: 4px; padding: 2px 8px; font-family: 'Geist Mono', monospace; font-size: 11px; font-weight: 700; color: #00E676;">
                        Verified 3D Cadastre
                    </div>
                </div>
                <div style="padding: 16px; display: flex; flex-direction: column; gap: 10px;">
                    <div style="display: flex; align-items: center; gap: 6px; background: #1A2238; border: 1px solid #202B44; border-radius: 4px; padding: 4px 8px; width: fit-content;">
                        {ICONS_SVG['cuboid']}
                        <span style="font-family: 'Geist Mono', monospace; font-size: 12px; font-weight: 600; color: #00F2FE;">
                            MH-PUN-W04-BLK12-FL04
                        </span>
                    </div>
                    <div>
                        <div style="font-family: 'DM Sans', sans-serif; font-weight: 700; font-size: 15px; color: #FFFFFF;">
                            Flat 402, Block A, {prop_name}, {prop_city}
                        </div>
                        <div style="font-family: 'DM Sans', sans-serif; font-size: 12px; color: #6B7C9E; margin-top: 2px;">
                            Floor 4 [Height Reference +12.4m] &bull; 1,450 Sq.Ft
                        </div>
                    </div>
                </div>
            </div>
        """)
        if st.button("Inspect in 3D Viewer →", key="inspect_card_1_btn", use_container_width=True):
            st.session_state["selected_parcel_id"] = 101
            st.session_state["twin_studio_toggle_widget"] = True
            st.session_state["force_twin_view"] = True
            set_active_view("🌐 3D Cadastre & Digital Twin Studio")
            st.rerun()

    with p2:
        render_html(f"""
            <div style="background: #121829; border: 1px solid #202B44; border-radius: 12px; overflow: hidden; display: flex; flex-direction: column;">
                <div style="height: 120px; background: linear-gradient(135deg, #3d2314 0%, #170d06 100%); display: flex; align-items: center; justify-content: center; position: relative;">
                    <div style="font-size: 44px; filter: drop-shadow(0 0 10px rgba(255, 159, 10, 0.4));">🚇</div>
                    <div style="position: absolute; top: 12px; right: 12px; background: rgba(255, 159, 10, 0.15); border: 1px solid #FF9F0A; border-radius: 4px; padding: 2px 8px; font-family: 'Geist Mono', monospace; font-size: 11px; font-weight: 700; color: #FF9F0A;">
                        Clash Detected
                    </div>
                </div>
                <div style="padding: 16px; display: flex; flex-direction: column; gap: 10px;">
                    <div style="display: flex; align-items: center; gap: 6px; background: #1A2238; border: 1px solid #202B44; border-radius: 4px; padding: 4px 8px; width: fit-content;">
                        {ICONS_SVG['cuboid']}
                        <span style="font-family: 'Geist Mono', monospace; font-size: 12px; font-weight: 600; color: #00F2FE;">
                            MH-PUN-W04-BLK12-BSM01
                        </span>
                    </div>
                    <div>
                        <div style="font-family: 'DM Sans', sans-serif; font-weight: 700; font-size: 15px; color: #FFFFFF;">
                            Basement Unit B1, {prop_name}, Hinjewadi, {prop_city}
                        </div>
                        <div style="font-family: 'DM Sans', sans-serif; font-size: 12px; color: #6B7C9E; margin-top: 2px;">
                            Basement 1 [Subsurface Reference -3.5m] &bull; Subsurface Foundation
                        </div>
                    </div>
                </div>
            </div>
        """)
        if st.button("Inspect Subsurface Clash →", key="inspect_card_2_btn", use_container_width=True):
            st.session_state["selected_parcel_id"] = 102
            set_active_view("⚠️ Subsurface Clash Engine")
            st.rerun()

    render_html(f"""
        <div style="background: #121829; border: 1px solid #202B44; border-radius: 12px; padding: 20px; margin-top: 20px;">
            <div style="font-family: 'DM Sans', sans-serif; font-weight: 700; font-size: 15px; color: #FFFFFF; margin-bottom: 12px;">
                Registry Ledger Actions
            </div>
            <div style="display: flex; justify-content: space-between; align-items: center; padding: 8px 0;">
                <div style="display: flex; align-items: center; gap: 10px;">
                    <span style="width: 8px; height: 8px; background: #00E676; border-radius: 50%; display: inline-block;"></span>
                    <span style="font-size: 13px; color: #A3B3D2;">SHA-256 Title Certificate generated for MH-PUN-W04-BLK12-FLR04</span>
                </div>
                <span style="font-family: 'Geist Mono', monospace; font-size: 12px; color: #6B7C9E;">Today, 10:24 AM</span>
            </div>
            <div style="width: 100%; height: 1px; background: #202B44; margin: 4px 0;"></div>
            <div style="display: flex; justify-content: space-between; align-items: center; padding: 8px 0;">
                <div style="display: flex; align-items: center; gap: 10px;">
                    <span style="width: 8px; height: 8px; background: #FF9F0A; border-radius: 50%; display: inline-block;"></span>
                    <span style="font-size: 13px; color: #A3B3D2;">Subsurface gas pipeline clash detected on Basement B1 asset</span>
                </div>
                <span style="font-family: 'Geist Mono', monospace; font-size: 12px; color: #6B7C9E;">2 days ago</span>
            </div>
        </div>
    """)

# -------------------------------------------------------------
# 4. DIGITAL TITLE CERTIFICATE VIEW (digital-title-certificate)
# -------------------------------------------------------------
def render_figma_digital_title_certificate(prop, floor_dict, ulpin_str):
    effective_owner = floor_dict.get('owner') or prop.get('owner', 'Rajesh Sharma & Anita Sharma')
    z_range = f"+{floor_dict.get('z_start', 12.4):.1f}m to +{floor_dict.get('z_end', 15.6):.1f}m from Ground Reference Datum"
    sha_hash = generate_title_hash(
        ulpin_str,
        effective_owner,
        prop.get('lat', 19.0216),
        prop.get('lon', 73.0181),
        z_range,
        prop.get('valuation_cr', 4.5)
    )

    qr_payload = {
        "ulpin": ulpin_str,
        "owner": effective_owner,
        "plot": int(prop.get('property_id', 101)),
        "z_range": z_range,
        "sha": sha_hash[:16]
    }
    qr_bytes = generate_qr_code_image(qr_payload)
    qr_b64 = base64.b64encode(qr_bytes.getvalue()).decode('utf-8')

    render_html(f"""
        <div style="display: flex; justify-content: center; margin-top: 10px; margin-bottom: 30px;">
            <div style="box-sizing: border-box; width: 100%; max-width: 800px; background: #FAF7F2; border-radius: 12px; box-shadow: 0px 16px 40px rgba(0, 0, 0, 0.45); padding: 48px; color: #0F1729;">
                <div style="display: flex; justify-content: space-between; align-items: center; border-bottom: 2px solid #D1D5DB; padding-bottom: 20px; margin-bottom: 24px;">
                    <div style="width: 60px; height: 60px; display: flex; align-items: center; justify-content: center;">
                        {ICONS_SVG['ashoka_emblem']}
                    </div>
                    <div style="display: flex; flex-direction: column; align-items: center; text-align: center;">
                        <span style="font-family: 'DM Sans', sans-serif; font-weight: 800; font-size: 14px; color: #0F1729; letter-spacing: 0.05em;">
                            GOVERNMENT OF INDIA
                        </span>
                        <span style="font-family: 'DM Sans', sans-serif; font-weight: 600; font-size: 11px; color: #4B5563; margin-top: 2px;">
                            DEPARTMENT OF LAND RESOURCES
                        </span>
                        <span style="font-family: 'DM Sans', sans-serif; font-weight: 800; font-size: 16px; color: #0F1729; margin-top: 6px; letter-spacing: -0.01em;">
                            CERTIFICATE OF 3D PROPERTY TITLE
                        </span>
                    </div>
                    <div style="width: 64px; height: 64px; border: 1px solid #D1D5DB; border-radius: 6px; padding: 2px; background: #FFFFFF;">
                        <img src="data:image/png;base64,{qr_b64}" style="width: 100%; height: 100%; object-fit: contain;"/>
                    </div>
                </div>

                <div style="display: flex; flex-direction: column; gap: 14px; margin-bottom: 24px;">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <span style="font-family: 'DM Sans', sans-serif; font-weight: 700; font-size: 12px; color: #6B7280;">3D ULPIN CODE</span>
                        <span style="font-family: 'Geist Mono', monospace; font-weight: 700; font-size: 14px; color: #00ABA3;">{ulpin_str}</span>
                    </div>
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <span style="font-family: 'DM Sans', sans-serif; font-weight: 700; font-size: 12px; color: #6B7280;">REGISTERED OWNER</span>
                        <span style="font-family: 'DM Sans', sans-serif; font-weight: 700; font-size: 14px; color: #0F1729;">{effective_owner.upper()}</span>
                    </div>
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <span style="font-family: 'DM Sans', sans-serif; font-weight: 700; font-size: 12px; color: #6B7280;">SPATIAL ADDRESS</span>
                        <span style="font-family: 'DM Sans', sans-serif; font-weight: 500; font-size: 13px; color: #0F1729;">Flat 402, Block A, {prop.get('name', 'Sky Heights')}, {prop.get('city', 'Pune')}</span>
                    </div>
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <span style="font-family: 'DM Sans', sans-serif; font-weight: 700; font-size: 12px; color: #6B7280;">POLYHEDRON HEIGHT RANGE</span>
                        <span style="font-family: 'Geist Mono', monospace; font-weight: 500; font-size: 13px; color: #0F1729;">{z_range}</span>
                    </div>
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <span style="font-family: 'DM Sans', sans-serif; font-weight: 700; font-size: 12px; color: #6B7280;">BUILT SPATIAL VOLUME</span>
                        <span style="font-family: 'Geist Mono', monospace; font-weight: 500; font-size: 13px; color: #0F1729;">1,450 Sq.Ft (Approx. 4,640 Cu.Ft Volume)</span>
                    </div>
                </div>

                <div style="width: 100%; height: 1px; background: #D1D5DB; margin-bottom: 20px;"></div>

                <div style="margin-bottom: 20px;">
                    <div style="font-family: 'DM Sans', sans-serif; font-weight: 700; font-size: 12px; color: #6B7280; margin-bottom: 8px;">
                        CERTIFIED 3D TWIN GEOMETRY
                    </div>
                    <div style="width: 100%; height: 130px; background: #0A0D1A; border-radius: 8px; display: flex; align-items: center; justify-content: center; border: 1px solid #202B44; position: relative;">
                        <div style="text-align: center;">
                            <span style="font-size: 32px;">📐</span>
                            <div style="font-family: 'Geist Mono', monospace; font-size: 11px; color: #00F2FE; margin-top: 4px;">ISO 19152 BOUNDARY POLYHEDRON OK</div>
                            <div style="font-family: 'DM Sans', sans-serif; font-size: 10px; color: #A3B3D2;">Validated Zero 3D Spatial Encroachment with Adjacent Parcels</div>
                        </div>
                    </div>
                </div>

                <div style="background: #E5E7EB; border-radius: 6px; padding: 12px; display: flex; flex-direction: column; gap: 6px; margin-bottom: 24px;">
                    <div style="display: flex; justify-content: space-between; font-size: 11px;">
                        <span style="font-family: 'DM Sans', sans-serif; font-weight: 700; color: #4B5563;">LEDGER SHA-256 SPATIAL HASH</span>
                        <span style="font-family: 'Geist Mono', monospace; color: #111827; font-weight: 600;">{sha_hash[:32]}...</span>
                    </div>
                    <div style="display: flex; justify-content: space-between; font-size: 11px;">
                        <span style="font-family: 'DM Sans', sans-serif; font-weight: 700; color: #4B5563;">ISO 19152 COMPLIANCE CODE</span>
                        <span style="font-family: 'Geist Mono', monospace; color: #111827; font-weight: 600;">ISO-19152-LADM:3D-IN-2026</span>
                    </div>
                </div>

                <div style="display: flex; justify-content: space-between; align-items: flex-end; padding-top: 10px;">
                    <div style="font-family: 'DM Sans', sans-serif; font-size: 12px; color: #4B5563; line-height: 18px;">
                        Issue Date: <b>14-Nov-2026</b><br/>
                        Verifying Authority: <b>{prop.get('city', 'Pune')} Municipal Corp.</b>
                    </div>
                    <div style="display: flex; flex-direction: column; align-items: center;">
                        <div style="font-family: 'Brush Script MT', cursive, sans-serif; font-size: 22px; color: #1E3A8A; transform: rotate(-3deg);">
                            Amit Patwardhan
                        </div>
                        <div style="width: 140px; height: 1px; background: #4B5563; margin: 4px 0;"></div>
                        <span style="font-family: 'DM Sans', sans-serif; font-weight: 700; font-size: 11px; color: #0F1729;">
                            Sub-Registrar of Assurances
                        </span>
                    </div>
                </div>

            </div>
        </div>
    """)

# -------------------------------------------------------------
# 5. SUBSURFACE CLASH REPORT (clash-detection-report)
# -------------------------------------------------------------
def render_figma_clash_report(conflicts, prop_data):
    prop_name = prop_data.get('name', 'Grand Central Subsurface Concourse')
    prop_city = prop_data.get('city', 'Navi Mumbai')
    prop_state = prop_data.get('state', 'Maharashtra')
    prop_id = prop_data.get('property_id', 102)

    st_code = prop_state[:2].upper() if prop_state else "MH"
    c_code = prop_city[:3].upper() if prop_city else "PUN"
    ulpin_code = f"IN-{st_code}-{c_code}-BLK{prop_id}-BSM01"

    # Minimal Integrated Header Bar
    c_head_info, c_head_acts = st.columns([2.0, 1.4], gap="medium")
    with c_head_info:
        render_html(f"""
            <div style="display: flex; flex-direction: column; gap: 3px; padding: 2px 0;">
                <div style="display: flex; align-items: center; gap: 8px;">
                    <span style="background: rgba(255, 159, 10, 0.15); border: 1px solid #FF9F0A; border-radius: 4px; padding: 2px 8px; font-family: 'Geist Mono', monospace; font-size: 10px; font-weight: 700; color: #FF9F0A; letter-spacing: 0.05em;">
                        SPATIAL CLASH DOSSIER
                    </span>
                    <span style="background: #1A2238; border: 1px solid #202B44; border-radius: 4px; padding: 2px 8px; font-family: 'Geist Mono', monospace; font-size: 10px; color: #00F2FE;">
                        {ulpin_code}
                    </span>
                </div>
                <div style="font-family: 'DM Sans', sans-serif; font-weight: 800; font-size: 20px; color: #FFFFFF; line-height: 1.2; margin-top: 2px;">
                    Subsurface Encroachment Analysis &bull; <span style="font-size: 15px; color: #A3B3D2; font-weight: 500;">{prop_name} ({prop_city})</span>
                </div>
            </div>
        """)
    with c_head_acts:
        ca1, ca2 = st.columns([1.0, 1.6], gap="small")
        with ca1:
            csv_rows = [
                "Conflict_ID,Asset_Name,Depth_m,Buffer_Threshold_m,Severity,Regulation,Recommended_Action",
                f"CLASH-01,Hinjewadi Metro Line II (Subway Shaft),-12.4,2.00,CRITICAL_COLLISION,Metro Railways Act 1978,Structural re-engineering of foundation piling required",
                f"CLASH-02,PNGRB City Gas Pipeline Grid,-2.1,2.00,ADVISORY_SAFETY_BUFFER,PNGRB Act 2006,Re-align utility conduit pathway or reinforce sleeve"
            ]
            st.download_button(
                label="📥 Export CSV",
                data="\n".join(csv_rows),
                file_name=f"clash_audit_{prop_id}.csv",
                mime="text/csv",
                key="btn_export_clash_csv",
                use_container_width=True
            )
        with ca2:
            render_html("""
                <style>
                div[data-testid="column"]:has(.btn-metro-anchor) button {
                    background: linear-gradient(90deg, #FF9F0A 0%, #F59E0B 100%) !important;
                    border: 1px solid #FF9F0A !important;
                    color: #000000 !important;
                    font-weight: 800 !important;
                    font-size: 13px !important;
                    box-shadow: 0 4px 18px rgba(255, 159, 10, 0.45) !important;
                }
                div[data-testid="column"]:has(.btn-metro-anchor) button * {
                    color: #000000 !important;
                    font-weight: 800 !important;
                }
                div[data-testid="column"]:has(.btn-metro-anchor) button:hover {
                    background: linear-gradient(90deg, #F59E0B 0%, #D97706 100%) !important;
                    box-shadow: 0 6px 24px rgba(255, 159, 10, 0.65) !important;
                    transform: translateY(-1px) !important;
                }
                div[data-testid="column"]:has(.btn-metro-anchor) button:hover * {
                    color: #000000 !important;
                }
                </style>
                <span class="btn-metro-anchor" style="display:none;"></span>
            """)
            btn_label = "✅ Notice Dispatched (Active)" if st.session_state.get("metro_notified") else "⚠️ Notify Spatial & Metro Authority"
            if st.button(btn_label, key="btn_notify_metro", use_container_width=True):
                st.session_state["metro_notified"] = not st.session_state.get("metro_notified", False)
                st.rerun()

    # Dynamic Alert Bar when notice is active
    if st.session_state.get("metro_notified"):
        render_html("""
            <div style="background: rgba(0, 230, 118, 0.12); border: 1px solid #00E676; border-radius: 8px; padding: 8px 14px; margin-top: 4px; margin-bottom: 12px; display: flex; align-items: center; justify-content: space-between; font-size: 12px;">
                <div style="display: flex; align-items: center; gap: 8px;">
                    <span>🚨</span>
                    <span style="color: #00E676; font-weight: 600;">
                        Official Notice Dispatched to Pune Metro Rail Corp (PMRCL) & Municipal Fire Dept (Ticket: #METRO-2026-9912).
                    </span>
                </div>
                <span style="background: #0F1422; border: 1px solid #00E676; border-radius: 4px; padding: 2px 8px; color: #00E676; font-family: 'Geist Mono', monospace; font-size: 10px; font-weight: 700;">
                    STATUS: ACTIVE DISPATCH (Click button to toggle)
                </span>
            </div>
        """)

    # Clean 2-Column Minimal Incident Layout
    c_left, c_right = st.columns([1.3, 0.9], gap="medium")

    with c_left:
        # Violation 1 (Critical)
        render_html(f"""
            <div style="background: #121829; border: 1px solid rgba(255, 159, 10, 0.3); border-left: 4px solid #FF9F0A; border-radius: 10px; padding: 14px 16px; margin-bottom: 10px;">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
                    <div style="display: flex; align-items: center; gap: 8px;">
                        {ICONS_SVG['alert_triangle']}
                        <span style="font-family: 'DM Sans', sans-serif; font-weight: 700; font-size: 15px; color: #FFFFFF;">
                            Hinjewadi Metro Line II (Subway Shaft)
                        </span>
                    </div>
                    <span style="background: rgba(255, 159, 10, 0.15); border: 1px solid #FF9F0A; border-radius: 4px; padding: 2px 8px; font-family: 'Geist Mono', monospace; font-size: 10px; font-weight: 700; color: #FF9F0A;">
                        CRITICAL CLASH &bull; -12.4m
                    </span>
                </div>
                <div style="display: flex; justify-content: space-between; font-size: 12px; margin-bottom: 10px;">
                    <span style="color: #6B7C9E;">Affected: <b style="color: #FFFFFF;">Foundation Piling 4-A Encroachment</b></span>
                    <span style="color: #6B7C9E;">Buffer Breach: <b style="color: #FF9F0A; font-family: 'Geist Mono', monospace;">-2.00m Standard</b></span>
                </div>
                <div style="background: #1A2238; border-radius: 6px; padding: 8px 12px; font-size: 12px; color: #A3B3D2; border-left: 2px solid #FF9F0A;">
                    <b style="color: #FFFFFF;">Recommended Action:</b> Structural re-engineering of piling required. Engineering dispatch notified.
                </div>
            </div>
        """)

        # Violation 2 (Warning)
        render_html(f"""
            <div style="background: #121829; border: 1px solid rgba(0, 242, 254, 0.3); border-left: 4px solid #00F2FE; border-radius: 10px; padding: 14px 16px; margin-bottom: 10px;">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
                    <div style="display: flex; align-items: center; gap: 8px;">
                        {ICONS_SVG['box']}
                        <span style="font-family: 'DM Sans', sans-serif; font-weight: 700; font-size: 15px; color: #FFFFFF;">
                            PNGRB City Gas Pipeline Grid
                        </span>
                    </div>
                    <span style="background: rgba(0, 242, 254, 0.12); border: 1px solid #00F2FE; border-radius: 4px; padding: 2px 8px; font-family: 'Geist Mono', monospace; font-size: 10px; font-weight: 700; color: #00F2FE;">
                        ADVISORY &bull; -2.1m
                    </span>
                </div>
                <div style="display: flex; justify-content: space-between; font-size: 12px; margin-bottom: 10px;">
                    <span style="color: #6B7C9E;">Affected: <b style="color: #FFFFFF;">Basement-B1 Support Slab Perimeter</b></span>
                    <span style="color: #6B7C9E;">Proximity: <b style="color: #00F2FE; font-family: 'Geist Mono', monospace;">1.85m Clearance</b></span>
                </div>
                <div style="background: #1A2238; border-radius: 6px; padding: 8px 12px; font-size: 12px; color: #A3B3D2; border-left: 2px solid #00F2FE;">
                    <b style="color: #FFFFFF;">Recommended Action:</b> Re-align utility conduit pathway or reinforce structural isolation sleeve.
                </div>
            </div>
        """)

    with c_right:
        # Blueprint Diagram
        render_html("""
            <div style="background: #121829; border: 1px solid #202B44; border-radius: 10px; padding: 16px;">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
                    <span style="font-family: 'DM Sans', sans-serif; font-weight: 700; font-size: 13px; color: #FFFFFF;">
                        SUBTERRANEAN STRATA BLUEPRINT
                    </span>
                    <span style="font-family: 'Geist Mono', monospace; font-size: 10px; color: #6B7C9E;">ISO 19152 LADM</span>
                </div>
                <div style="height: 136px; background: #0A0D1A; border: 1px solid #202B44; border-radius: 6px; padding: 10px 14px; display: flex; flex-direction: column; justify-content: space-between; position: relative;">
                    <div>
                        <div style="display: flex; justify-content: space-between; font-size: 10px; color: #00E676; font-family: 'Geist Mono', monospace;">
                            <span>0.0m GROUND SURFACE</span>
                            <span>MSL +540.0m</span>
                        </div>
                        <div style="width: 100%; height: 2px; background: #00E676; margin-top: 2px;"></div>
                    </div>
                    <div>
                        <div style="display: flex; justify-content: space-between; font-size: 10px; color: #00F2FE; font-family: 'Geist Mono', monospace;">
                            <span>-2.1m PNGRB GAS CONDUIT</span>
                            <span>Advisory Zone</span>
                        </div>
                        <div style="width: 100%; height: 2px; background: #00F2FE; margin-top: 2px;"></div>
                    </div>
                    <div>
                        <div style="display: flex; justify-content: space-between; font-size: 10px; color: #FF9F0A; font-family: 'Geist Mono', monospace;">
                            <span>-12.4m METRO LINE II BUFFER</span>
                            <span style="color: #FF9F0A; font-weight: 700;">CRITICAL BREACH</span>
                        </div>
                        <div style="width: 100%; height: 3px; background: repeating-linear-gradient(45deg, #FF9F0A, #FF9F0A 6px, #121829 6px, #121829 12px); margin-top: 2px;"></div>
                    </div>
                </div>
                <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 8px; margin-top: 10px; font-size: 11px;">
                    <div style="background: #1A2238; border-radius: 6px; padding: 8px 10px;">
                        <span style="color: #6B7C9E;">Buffer Limit</span>
                        <div style="font-family: 'Geist Mono', monospace; font-weight: 700; color: #FFFFFF; font-size: 13px;">2.00 Metres</div>
                    </div>
                    <div style="background: #1A2238; border-radius: 6px; padding: 8px 10px;">
                        <span style="color: #6B7C9E;">Violations</span>
                        <div style="font-family: 'Geist Mono', monospace; font-weight: 700; color: #FF9F0A; font-size: 13px;">1 Crit / 1 Adv</div>
                    </div>
                </div>
            </div>
        """)

# -------------------------------------------------------------
# 6. GIS SURVEYOR WORKSTATION (surveyor-portal)
# -------------------------------------------------------------
def render_figma_surveyor_workstation():
    render_html(f"""
        <div style="background: #121829; border: 1px solid #202B44; border-radius: 12px; padding: 20px 24px; margin-bottom: 20px; display: flex; justify-content: space-between; align-items: center;">
            <div style="display: flex; align-items: center; gap: 12px;">
                <div style="width: 40px; height: 40px; background: linear-gradient(90deg, #00F2FE 0%, #0072FF 100%); border-radius: 8px; display: flex; align-items: center; justify-content: center;">
                    {ICONS_SVG['compass']}
                </div>
                <div>
                    <div style="font-family: 'DM Sans', sans-serif; font-weight: 800; font-size: 18px; color: #FFFFFF;">
                        GIS SURVEYOR WORKSTATION
                    </div>
                    <div style="font-family: 'DM Sans', sans-serif; font-size: 12px; color: #00F2FE;">
                        Authorized User: Amit Patwardhan (M-9912)
                    </div>
                </div>
            </div>
            <div style="display: flex; align-items: center; gap: 32px;">
                <div>
                    <div style="font-family: 'DM Sans', sans-serif; font-size: 11px; color: #6B7C9E;">COMPLETED SURVEYS</div>
                    <div style="font-family: 'Geist Mono', monospace; font-weight: 700; font-size: 20px; color: #00E676;">128</div>
                </div>
                <div>
                    <div style="font-family: 'DM Sans', sans-serif; font-size: 11px; color: #6B7C9E;">PENDING QUEUE</div>
                    <div style="font-family: 'Geist Mono', monospace; font-weight: 700; font-size: 20px; color: #FF9F0A;">14</div>
                </div>
                <div>
                    <div style="font-family: 'DM Sans', sans-serif; font-size: 11px; color: #6B7C9E;">ACTIVE SATELLITE SYNC</div>
                    <div style="font-family: 'Geist Mono', monospace; font-weight: 700; font-size: 12px; color: #00F2FE; margin-top: 4px;">LIDAR RTK ON</div>
                </div>
            </div>
        </div>
    """)

def render_figma_survey_queue():
    render_html("""
        <div style="font-family: 'DM Sans', sans-serif; font-weight: 700; font-size: 14px; color: #FFFFFF; margin-bottom: 12px;">
            SURVEY DISPATCH QUEUE
        </div>
    """)

    render_html("""
        <div style="background: #1A2238; border: 1px solid #202B44; border-radius: 8px; padding: 14px; margin-bottom: 12px;">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
                <span style="background: rgba(0, 242, 254, 0.11); border: 1px solid #00F2FE; border-radius: 4px; padding: 2px 6px; font-family: 'Geist Mono', monospace; font-size: 10px; font-weight: 700; color: #00F2FE;">
                    New 3D Survey
                </span>
                <span style="background: rgba(255, 159, 10, 0.11); border: 1px solid #FF9F0A; border-radius: 4px; padding: 2px 6px; font-family: 'Geist Mono', monospace; font-size: 10px; font-weight: 700; color: #FF9F0A;">
                    High Priority
                </span>
            </div>
            <div style="font-family: 'DM Sans', sans-serif; font-weight: 700; font-size: 15px; color: #FFFFFF;">
                Sector 3, Hinjewadi
            </div>
            <div style="font-family: 'DM Sans', sans-serif; font-size: 12px; color: #A3B3D2; margin-top: 2px;">
                Requester: Amit G. Patel &bull; Received Today
            </div>
        </div>
    """)
    if st.button("⚡ Initialize LiDAR Acquisition", key="btn_lidar_1", type="primary", use_container_width=True):
        st.session_state["lidar_mission_msg"] = "Sector 3, Hinjewadi: Airborne LiDAR Flight Vector synched! RTK drone dispatched. Point cloud ingestion active."
        st.rerun()

    render_html("""
        <div style="background: #1A2238; border: 1px solid #202B44; border-radius: 8px; padding: 14px; margin-top: 14px; margin-bottom: 12px;">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
                <span style="background: rgba(0, 242, 254, 0.11); border: 1px solid #00F2FE; border-radius: 4px; padding: 2px 6px; font-family: 'Geist Mono', monospace; font-size: 10px; font-weight: 700; color: #00F2FE;">
                    Resurvey (Dispute)
                </span>
                <span style="background: rgba(0, 242, 254, 0.11); border: 1px solid #00F2FE; border-radius: 4px; padding: 2px 6px; font-family: 'Geist Mono', monospace; font-size: 10px; font-weight: 700; color: #00F2FE;">
                    Medium
                </span>
            </div>
            <div style="font-family: 'DM Sans', sans-serif; font-weight: 700; font-size: 15px; color: #FFFFFF;">
                Phase II, IT Park
            </div>
            <div style="font-family: 'DM Sans', sans-serif; font-size: 12px; color: #A3B3D2; margin-top: 2px;">
                Requester: Karan Johar Ltd &bull; Received Yesterday
            </div>
        </div>
    """)
    if st.button("⚡ Initialize LiDAR Acquisition", key="btn_lidar_2", use_container_width=True):
        st.session_state["lidar_mission_msg"] = "Phase II, IT Park: Terrestrial RTK Scanner deployed! Computing volumetric floor slice boundaries."
        st.rerun()

    if st.session_state.get("lidar_mission_msg"):
        st.info(f"📡 {st.session_state['lidar_mission_msg']}")

# -------------------------------------------------------------
# 7. 3D PROPERTY VIEWER SIDEBARS (3d-property-viewer)
# -------------------------------------------------------------
def render_figma_viewer_topbar(prop_data):
    name = prop_data.get('name', 'Sky Heights - Block A')
    city = prop_data.get('city', 'Pune')
    state = prop_data.get('state', 'Maharashtra')
    prop_id = prop_data.get('property_id', 101)
    prop_type = prop_data.get('type', 'Commercial')

    state_map = {"Maharashtra": "MH", "Delhi": "DL", "Karnataka": "KA", "Gujarat": "GJ", "Telangana": "TS", "Tamil Nadu": "TN", "Haryana": "HR"}
    st_code = state_map.get(state, "IN")
    c_code = str(city)[:3].upper()
    cad_id = f"IN-{st_code}-{c_code}-BLK{prop_id}"

    c_title, c_act = st.columns([2.8, 1.2], gap="medium")
    with c_title:
        render_html(f"""
            <div style="display: flex; align-items: center; gap: 10px; flex-wrap: wrap; padding: 2px 0 6px 0;">
                <span style="font-family: 'DM Sans', sans-serif; font-weight: 800; font-size: 19px; color: #FFFFFF;">
                    {name}
                </span>
                <span style="background: rgba(0, 242, 254, 0.1); color: #00F2FE; border: 1px solid rgba(0, 242, 254, 0.3); border-radius: 6px; padding: 2px 8px; font-size: 11px; font-weight: 600;">
                    {city}, {state}
                </span>
                <span style="background: #1A2238; border: 1px solid #202B44; border-radius: 6px; padding: 2px 8px; font-family: 'Geist Mono', monospace; font-size: 11px; color: #6B7C9E;">
                    {cad_id}
                </span>
            </div>
        """)
    with c_act:
        ca1, ca2 = st.columns(2, gap="small")
        with ca1:
            if st.button("🔗 Share Link", key=f"btn_share_{prop_id}", use_container_width=True):
                st.session_state["show_share_modal"] = not st.session_state.get("show_share_modal", False)
                st.rerun()
        with ca2:
            dxf_content = f"0\nSECTION\n2\nHEADER\n0\nENDSEC\n0\nSECTION\n2\nENTITIES\n0\n3DFACE\n8\nCADASTRE_3D_PARCEL\n10\n{prop_data.get('lat', 18.5204):.5f}\n20\n{prop_data.get('lon', 73.8567):.5f}\n30\n{prop_data.get('total_height', 48.0):.1f}\n0\nENDSEC\n0\nEOF\n"
            st.download_button(
                label="💾 Export DXF",
                data=dxf_content,
                file_name=f"Cadastre_Polyhedron_{prop_id}.dxf",
                mime="application/dxf",
                type="primary",
                key=f"btn_export_dxf_{prop_id}",
                use_container_width=True
            )

    if st.session_state.get("show_share_modal"):
        share_url = f"https://3d-ulpin-generator.gov.in/cadastre/view?pid={prop_id}&auth=0x9f8b1c4e72"
        st.info(f"🔗 **Cryptographic 3D Viewer Link:** `{share_url}`")

def render_figma_viewer_left_panel(prop_data, active_floor_name="Residential Floor 04"):
    owner = prop_data.get('owner', 'Rajesh Sharma & Anita Sharma')
    area = prop_data.get('area_sqft', 1450)
    
    render_html(f"""
        <div style="background: #121829; border: 1px solid #202B44; border-radius: 12px; padding: 18px; display: flex; flex-direction: column; gap: 14px;">
            <div>
                <div style="font-family: 'DM Sans', sans-serif; font-weight: 700; font-size: 11px; color: #6B7C9E; letter-spacing: 0.05em; margin-bottom: 6px;">
                    ISO 19152 METADATA
                </div>
                <div style="background: #1A2238; border: 1px solid #202B44; border-radius: 4px; padding: 4px 8px; width: fit-content;">
                    <span style="font-family: 'Geist Mono', monospace; font-size: 12px; font-weight: 600; color: #00F2FE;">
                        MH-PUN-BLK12-FL04
                    </span>
                </div>
            </div>

            <div style="display: flex; flex-direction: column; gap: 10px; font-size: 12px;">
                <div>
                    <span style="color: #6B7C9E;">Owner of Record</span>
                    <div style="font-family: 'DM Sans', sans-serif; font-weight: 600; font-size: 13px; color: #FFFFFF; margin-top: 1px;">{owner}</div>
                </div>
                <div>
                    <span style="color: #6B7C9E;">Total Built Area</span>
                    <div style="font-family: 'DM Sans', sans-serif; font-weight: 600; font-size: 13px; color: #FFFFFF; margin-top: 1px;">{area:,.0f} Sq.Ft (3D Polyhedron)</div>
                </div>
                <div>
                    <span style="color: #6B7C9E;">Floor Level Code</span>
                    <div style="font-family: 'DM Sans', sans-serif; font-weight: 600; font-size: 13px; color: #FFFFFF; margin-top: 1px;">{active_floor_name} (H.Ref: +12.40m)</div>
                </div>
                <div>
                    <span style="color: #6B7C9E;">Registration Date</span>
                    <div style="font-family: 'DM Sans', sans-serif; font-weight: 600; font-size: 13px; color: #FFFFFF; margin-top: 1px;">12-Nov-2024</div>
                </div>
                <div>
                    <span style="color: #6B7C9E;">Assigned Surveyor</span>
                    <div style="font-family: 'DM Sans', sans-serif; font-weight: 600; font-size: 13px; color: #FFFFFF; margin-top: 1px;">Amit Patwardhan (M-9912)</div>
                </div>
            </div>

            <div style="width: 100%; height: 1px; background: #202B44;"></div>

            <div>
                <div style="font-family: 'DM Sans', sans-serif; font-weight: 700; font-size: 12px; color: #FFFFFF; margin-bottom: 8px;">
                    DIAGNOSTIC STATUS
                </div>
                <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 6px;">
                    <span style="width: 8px; height: 8px; background: #00E676; border-radius: 50%; display: inline-block;"></span>
                    <span style="font-size: 12px; color: #A3B3D2;">Vertical Cadastre Integrity OK</span>
                </div>
                <div style="display: flex; align-items: center; gap: 8px;">
                    <span style="width: 8px; height: 8px; background: #FF9F0A; border-radius: 50%; display: inline-block;"></span>
                    <span style="font-size: 12px; color: #A3B3D2;">1 Subsurface clash on basement level</span>
                </div>
            </div>
        </div>
    """)

# -------------------------------------------------------------
# FULLY RESTORED & RESTYLED FIGMA CORE COMPONENTS
# -------------------------------------------------------------
def render_header(theme="dark"):
    render_figma_navbar(active_view="overview")

def render_kpi_bar(df, theme="dark"):
    """Renders high-level national summary KPIs in sleek Figma dark cards."""
    total_parcels = len(df)
    subsurface_count = len(df[df['base_elevation'] < 0]) if 'base_elevation' in df.columns else 0
    cities_count = df['city'].nunique() if 'city' in df.columns else 1
    total_val = df['valuation_cr'].sum() if 'valuation_cr' in df.columns else 0

    render_html(f"""
        <div style="display: grid; grid-template-columns: repeat(4, 1fr); gap: 16px; margin-bottom: 20px;">
            <div style="background: #121829; border: 1px solid #202B44; border-radius: 12px; padding: 16px 20px;">
                <div style="font-family: 'DM Sans', sans-serif; font-size: 11px; font-weight: 700; color: #6B7C9E; text-transform: uppercase; letter-spacing: 0.05em;">
                    TOTAL 3D PARCELS
                </div>
                <div style="font-family: 'Geist Mono', monospace; font-size: 26px; font-weight: 800; color: #00F2FE; margin: 4px 0 2px 0;">
                    {total_parcels:,}
                </div>
                <div style="font-family: 'DM Sans', sans-serif; font-size: 12px; color: #A3B3D2;">
                    ISO 19152 LADM Registered
                </div>
            </div>
            <div style="background: #121829; border: 1px solid #202B44; border-radius: 12px; padding: 16px 20px;">
                <div style="font-family: 'DM Sans', sans-serif; font-size: 11px; font-weight: 700; color: #6B7C9E; text-transform: uppercase; letter-spacing: 0.05em;">
                    PAN-INDIA METRO HUBS
                </div>
                <div style="font-family: 'Geist Mono', monospace; font-size: 26px; font-weight: 800; color: #00F2FE; margin: 4px 0 2px 0;">
                    {cities_count} Metros
                </div>
                <div style="font-family: 'DM Sans', sans-serif; font-size: 12px; color: #A3B3D2;">
                    Active High-Density Grids
                </div>
            </div>
            <div style="background: #121829; border: 1px solid #202B44; border-radius: 12px; padding: 16px 20px;">
                <div style="font-family: 'DM Sans', sans-serif; font-size: 11px; font-weight: 700; color: #6B7C9E; text-transform: uppercase; letter-spacing: 0.05em;">
                    SUBSURFACE ASSETS
                </div>
                <div style="font-family: 'Geist Mono', monospace; font-size: 26px; font-weight: 800; color: #00F2FE; margin: 4px 0 2px 0;">
                    {subsurface_count} Nodes
                </div>
                <div style="font-family: 'DM Sans', sans-serif; font-size: 12px; color: #A3B3D2;">
                    Subterranean Tunnels & Utilities
                </div>
            </div>
            <div style="background: #121829; border: 1px solid #202B44; border-radius: 12px; padding: 16px 20px;">
                <div style="font-family: 'DM Sans', sans-serif; font-size: 11px; font-weight: 700; color: #6B7C9E; text-transform: uppercase; letter-spacing: 0.05em;">
                    CADASTRAL VALUATION
                </div>
                <div style="font-family: 'Geist Mono', monospace; font-size: 26px; font-weight: 800; color: #00E676; margin: 4px 0 2px 0;">
                    ₹ {total_val:,.0f} Cr
                </div>
                <div style="font-family: 'DM Sans', sans-serif; font-size: 12px; color: #A3B3D2;">
                    Verified Spatial Assets
                </div>
            </div>
        </div>
    """)

def render_property_spec_card(prop, theme="dark"):
    """Renders a sleek property specification dossier card styled in Figma dark space theme."""
    base_elev = prop.get('base_elevation', 0)
    is_underground = base_elev < 0
    type_badge_color = "#f43f5e" if is_underground else "#00F2FE"
    city = prop.get('city', 'Unknown')
    state = prop.get('state', 'India')
    name = prop.get('name', f"Parcel #{prop.get('property_id')}")
    prop_type = prop.get('type', 'Standard')
    owner = prop.get('owner', 'Government / Private')
    zone = prop.get('zone', 'Urban Commercial')
    lat = float(prop.get('lat', 0.0))
    lon = float(prop.get('lon', 0.0))
    val = float(prop.get('valuation_cr', 0.0))
    pid = prop.get('property_id', 101)

    render_html(f"""
        <div style="background: #121829; border: 1px solid #202B44; border-radius: 12px; padding: 16px; margin-bottom: 16px;">
            <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 12px;">
                <div>
                    <div style="font-family: 'DM Sans', sans-serif; font-size: 11px; text-transform: uppercase; color: #6B7C9E; font-weight: 700; letter-spacing: 0.05em;">
                        PARCEL #{pid} &bull; {str(city).upper()}, {str(state).upper()}
                    </div>
                    <div style="font-family: 'DM Sans', sans-serif; font-size: 18px; font-weight: 800; color: #FFFFFF; margin-top: 2px;">
                        {name}
                    </div>
                </div>
                <span style="background: rgba(0, 242, 254, 0.11); color: {type_badge_color}; border: 1px solid {type_badge_color}; font-family: 'Geist Mono', monospace; font-size: 11px; font-weight: 700; padding: 3px 10px; border-radius: 6px;">
                    {prop_type}
                </span>
            </div>
            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 10px; font-size: 13px; background: #1A2238; padding: 12px; border-radius: 8px; border: 1px solid #202B44;">
                <div><span style="color: #6B7C9E;">Owner:</span> <b style="color: #FFFFFF;">{owner}</b></div>
                <div><span style="color: #6B7C9E;">Zone:</span> <b style="color: #FFFFFF;">{zone}</b></div>
                <div><span style="color: #6B7C9E;">GPS Coordinates:</span> <code style="font-family: 'Geist Mono', monospace; color: #00F2FE; font-size: 12px; background: #0F1422; padding: 2px 6px; border-radius: 4px;">{lat:.4f}, {lon:.4f}</code></div>
                <div><span style="color: #6B7C9E;">Cadastral Valuation:</span> <b style="font-family: 'Geist Mono', monospace; color: #00E676;">₹ {val:.1f} Cr</b></div>
            </div>
        </div>
    """)

def render_vertical_stack(floors, prop_data, theme="dark"):
    """
    Renders an interactive cross-section diagram of the building's
    vertical parcel stack showing above-ground and subterranean levels.
    """
    sorted_floors = sorted(floors, key=lambda x: x['z_end'], reverse=True)
    html_blocks = []
    
    for f in sorted_floors:
        floor_num = f['floor_number']
        z_start = f['z_start']
        z_end = f['z_end']
        
        if floor_num < 0:
            bg = "rgba(255, 159, 10, 0.09)"
            border_col = "rgba(255, 159, 10, 0.28)"
            badge_col = "#FF9F0A"
            default_title = f"Basement {abs(floor_num):02d} (Subsurface)"
            z_badge = f"{z_end:.1f}m to {z_start:.1f}m"
        else:
            bg = "rgba(0, 242, 254, 0.08)"
            border_col = "rgba(0, 242, 254, 0.22)"
            badge_col = "#00F2FE"
            default_title = f"Level {floor_num:02d} (Superstructure)"
            z_badge = f"+{z_start:.1f}m to +{z_end:.1f}m"

        lvl_code = f.get('level_code', f"#{abs(floor_num):02d}")
        flr_title = f.get('floor_name', default_title)

        block = f"""
            <div style="display: flex; justify-content: space-between; align-items: center; padding: 7px 12px; background: {bg}; border: 1px solid {border_col}; border-radius: 6px; margin-bottom: 5px; font-size: 12px;">
                <div style="display: flex; align-items: center; gap: 8px; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; max-width: 68%;">
                    <span style="font-weight: 700; color: {badge_col}; font-family: 'Geist Mono', monospace; flex-shrink: 0;">{lvl_code}</span>
                    <span style="color: #FFFFFF; font-weight: 600; overflow: hidden; text-overflow: ellipsis; white-space: nowrap;">{flr_title}</span>
                </div>
                <div style="font-family: 'Geist Mono', monospace; font-size: 11px; color: {badge_col}; background: #0F1422; padding: 2px 6px; border-radius: 4px; flex-shrink: 0;">
                    {z_badge}
                </div>
            </div>
        """
        html_blocks.append(block)

    render_html(f"""
        <div style="background: #121829; border: 1px solid #202B44; border-radius: 12px; padding: 16px; margin-bottom: 16px;">
            <div style="font-family: 'DM Sans', sans-serif; font-size: 11px; font-weight: 700; text-transform: uppercase; letter-spacing: 0.06em; color: #6B7C9E; margin-bottom: 10px;">
                VERTICAL ARCHITECTURAL CROSS-SECTION
            </div>
            <div style="max-height: 220px; overflow-y: auto; padding-right: 4px;">
                {''.join(html_blocks)}
            </div>
        </div>
    """)

def render_clash_report_ui(conflicts, theme="dark"):
    """
    Renders 3D collision & spatial encroachment detection findings with theme support.
    """
    if not conflicts:
        render_html("""
            <div style="display: flex; align-items: center; gap: 12px; background: rgba(0, 230, 118, 0.12); border: 1px solid #00E676; padding: 14px 18px; border-radius: 10px; margin-bottom: 12px;">
                <span style="font-size: 20px;">✅</span>
                <div>
                    <div style="font-family: 'DM Sans', sans-serif; font-weight: 700; color: #00E676; font-size: 14px;">No 3D Encroachments Detected</div>
                    <div style="font-family: 'DM Sans', sans-serif; font-size: 12px; color: #A3B3D2;">All subsurface foundations and utility safety buffers comply with municipal spatial regulations.</div>
                </div>
            </div>
        """)
        return

    render_html(f"""
        <div style="margin-bottom: 12px; font-family: 'DM Sans', sans-serif; font-size: 13px; font-weight: 800; color: #FF9F0A; text-transform: uppercase; letter-spacing: 0.05em;">
            ⚠️ Identified {len(conflicts)} Spatial Conflicts / Buffer Violations
        </div>
    """)

    for c in conflicts:
        is_crit = c.get('severity') == "CRITICAL_COLLISION"
        border_c = "#FF9F0A" if is_crit else "#00F2FE"
        badge_bg = "rgba(255, 159, 10, 0.15)" if is_crit else "rgba(0, 242, 254, 0.15)"
        badge_fg = "#FF9F0A" if is_crit else "#00F2FE"

        render_html(f"""
            <div style="background: #1A2238; border: 1px solid {border_c}; border-radius: 10px; padding: 14px; margin-bottom: 10px;">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 6px;">
                    <span style="font-family: 'Geist Mono', monospace; font-size: 12px; font-weight: 800; color: {badge_fg}; background: {badge_bg}; padding: 2px 8px; border-radius: 4px;">
                        {c.get('badge', 'CONFLICT')}
                    </span>
                    <span style="font-size: 11px; color: #A3B3D2; font-family: 'Geist Mono', monospace;">
                        Dist: {c.get('distance_m', 0)}m &bull; Z-Overlap: {c.get('overlap_z_m', 0)}m
                    </span>
                </div>
                <div style="font-family: 'DM Sans', sans-serif; font-size: 13px; color: #FFFFFF; margin-bottom: 4px;">
                    Conflicting Asset: <b>{c.get('conflicting_name', 'Unknown')}</b> (#{c.get('conflicting_id', '')}) &bull; <i>{c.get('conflicting_type', '')}</i>
                </div>
                <div style="font-family: 'DM Sans', sans-serif; font-size: 12px; color: #A3B3D2;">
                    {c.get('description', '')}
                </div>
            </div>
        """)

def render_bhu_aadhaar_card_preview(prop, floor_dict, ulpin_str, theme="dark"):
    """
    Renders a live digital certificate card preview with scannable QR code in Figma dark styling.
    """
    z_range = f"{floor_dict.get('z_start', 0)}m to {floor_dict.get('z_end', 0)}m"
    effective_owner = floor_dict.get('owner') or prop.get('owner', 'Government Cadastral Registry')
    sha_hash = generate_title_hash(
        ulpin_str,
        effective_owner,
        prop.get('lat', 0.0),
        prop.get('lon', 0.0),
        z_range,
        prop.get('valuation_cr', 0)
    )

    qr_payload = {
        "ulpin": ulpin_str,
        "owner": effective_owner,
        "plot": int(prop.get('property_id', 101)),
        "level": floor_dict.get('floor_number', 1),
        "z_range": z_range,
        "sha": sha_hash[:16]
    }
    qr_bytes = generate_qr_code_image(qr_payload)

    c_card, c_qr = st.columns([3.2, 1.3], gap="medium")
    with c_card:
        render_html(f"""
            <div style="background: #121829; border: 1px solid #00F2FE; border-radius: 12px; padding: 16px; box-shadow: 0 4px 20px rgba(0, 242, 254, 0.15);">
                <div style="display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid #202B44; padding-bottom: 8px; margin-bottom: 10px;">
                    <div style="font-family: 'DM Sans', sans-serif; font-size: 11px; text-transform: uppercase; color: #00F2FE; font-weight: 800; letter-spacing: 0.06em;">
                        3D ULPIN GENERATOR SPATIAL TITLE CERTIFICATE
                    </div>
                    <span style="font-family: 'Geist Mono', monospace; font-size: 10px; background: rgba(0, 230, 118, 0.15); color: #00E676; border: 1px solid #00E676; padding: 2px 8px; border-radius: 4px; font-weight: 700;">
                        DIGITALLY VERIFIED
                    </span>
                </div>
                <div style="font-family: 'Geist Mono', monospace; font-size: 16px; font-weight: 800; color: #FFFFFF; margin-bottom: 8px; letter-spacing: 0.02em;">
                    {ulpin_str}
                </div>
                <div style="font-family: 'DM Sans', sans-serif; font-size: 12px; color: #A3B3D2; display: grid; grid-template-columns: 1fr 1fr; gap: 6px; margin-bottom: 8px;">
                    <div><span style="color: #6B7C9E;">Title Holder:</span> <b style="color: #FFFFFF;">{effective_owner}</b></div>
                    <div><span style="color: #6B7C9E;">Vertical Span:</span> <b style="color: #FFFFFF;">{z_range}</b></div>
                    <div style="grid-column: span 2;"><span style="color: #6B7C9E;">Unit Designation:</span> <b style="color: #00F2FE;">{floor_dict.get('floor_name', f"Level {floor_dict.get('floor_number')}")}</b></div>
                    <div><span style="color: #6B7C9E;">Complex:</span> <b style="color: #FFFFFF;">{prop.get('name', '')}</b></div>
                    <div><span style="color: #6B7C9E;">Jurisdiction:</span> <b style="color: #FFFFFF;">{prop.get('city', '')}, {prop.get('state', '')}</b></div>
                </div>
                <div style="font-family: 'Geist Mono', monospace; font-size: 11px; color: #6B7C9E; background: #0F1422; padding: 4px 8px; border-radius: 4px; overflow-x: hidden; text-overflow: ellipsis; white-space: nowrap;">
                    SHA-256: {sha_hash}
                </div>
            </div>
        """)
    with c_qr:
        st.image(qr_bytes, caption="Scan to Verify 3D Title", width=140)

# Alias for backward compatibility & modern naming
render_3d_ulpin_card_preview = render_bhu_aadhaar_card_preview
