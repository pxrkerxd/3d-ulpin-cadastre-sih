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
        target = "🌐 3D Cadastre & Digital Twin"
    elif "citizen" in v:
        target = "🏠 Citizen Title Portal"
    elif "surveyor" in v:
        target = "📐 GIS Surveyor Workstation"
    elif "clash" in v or "subsurface" in v:
        target = "⚠️ Subsurface Clash Engine"
    elif "registrar" in v or "deed" in v or "conveyance" in v:
        target = "⚖️ Sub-Registrar Conveyance"
    else:
        target = "🏛️ Overview & Gateway"

    st.session_state["active_view"] = target
    st.session_state["nav_role"] = target


# -------------------------------------------------------------
# SVG ICONS (Authentic Government & Administrative Vectors)
# -------------------------------------------------------------
ICONS_SVG = {
    "ashoka_emblem": """<svg width="36" height="42" viewBox="0 0 70 82" fill="none" xmlns="http://www.w3.org/2000/svg">
        <path d="M35 4C35 4 28 6 25 12C22 18 24 24 24 24C24 24 20 25 18 29C16 33 18 38 18 38C18 38 15 41 15 46C15 51 18 55 20 57C22 59 25 60 25 60C25 60 24 64 27 68C30 72 35 72 35 72C35 72 40 72 43 68C46 64 45 60 45 60C45 60 48 59 50 57C52 55 55 51 55 46C55 41 52 38 52 38C52 38 54 33 52 29C50 25 46 24 46 24C46 24 48 18 45 12C42 6 35 4 35 4Z" fill="#0B3C5D" stroke="#0B3C5D" stroke-width="1.5"/>
        <circle cx="35" cy="62" r="6" stroke="#FFFFFF" stroke-width="1.5" fill="#0B3C5D"/>
        <line x1="35" y1="56" x2="35" y2="68" stroke="#FFFFFF" stroke-width="1"/>
        <line x1="29" y1="62" x2="41" y2="62" stroke="#FFFFFF" stroke-width="1"/>
        <rect x="18" y="74" width="34" height="4" rx="1" fill="#0B3C5D"/>
    </svg>""",
    "nic_logo": """<svg width="42" height="24" viewBox="0 0 80 40" fill="none" xmlns="http://www.w3.org/2000/svg">
        <rect width="80" height="40" rx="3" fill="#0B3C5D"/>
        <text x="40" y="26" font-family="'Noto Sans', Arial, sans-serif" font-size="17" font-weight="900" fill="#FFFFFF" text-anchor="middle" letter-spacing="1">NIC</text>
    </svg>""",
    "search": """<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
        <circle cx="11" cy="11" r="8"></circle><line x1="21" y1="21" x2="16.65" y2="16.65"></line>
    </svg>""",
    "layers": """<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
        <polygon points="12 2 2 7 12 12 22 7 12 2"></polygon>
        <polyline points="2 17 12 22 22 17"></polyline>
        <polyline points="2 12 12 17 22 12"></polyline>
    </svg>""",
    "shield_check": """<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#138808" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
        <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"></path>
        <polyline points="9 12 11 14 15 10"></polyline>
    </svg>""",
    "alert_triangle": """<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#C53030" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
        <path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"></path>
        <line x1="12" y1="9" x2="12" y2="13"></line>
        <line x1="12" y1="17" x2="12.01" y2="17"></line>
    </svg>""",
    "compass": """<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
        <circle cx="12" cy="12" r="10"></circle>
        <polygon points="16.24 7.76 14.12 14.12 7.76 16.24 9.88 9.88 16.24 7.76"></polygon>
    </svg>""",
    "user": """<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
        <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"></path><circle cx="12" cy="7" r="4"></circle>
    </svg>""",
    "bell": """<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
        <path d="M18 8A6 6 0 0 0 6 8c0 7-3 9-3 9h18s-3-2-3-9"></path><path d="M13.73 21a2 2 0 0 1-3.46 0"></path>
    </svg>""",
    "file_text": """<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
        <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path>
        <polyline points="14 2 14 8 20 8"></polyline>
        <line x1="16" y1="13" x2="8" y2="13"></line>
        <line x1="16" y1="17" x2="8" y2="17"></line>
        <polyline points="10 9 9 9 8 9"></polyline>
    </svg>""",
    "building": """<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
        <rect x="4" y="2" width="16" height="20" rx="2" ry="2"></rect>
        <line x1="9" y1="22" x2="9" y2="2"></line>
        <line x1="8" y1="6" x2="8.01" y2="6"></line>
        <line x1="16" y1="6" x2="16.01" y2="6"></line>
        <line x1="8" y1="10" x2="8.01" y2="10"></line>
        <line x1="16" y1="10" x2="16.01" y2="10"></line>
        <line x1="8" y1="14" x2="8.01" y2="14"></line>
        <line x1="16" y1="14" x2="16.01" y2="14"></line>
        <line x1="8" y1="18" x2="8.01" y2="18"></line>
        <line x1="16" y1="18" x2="16.01" y2="18"></line>
    </svg>"""
}

# -------------------------------------------------------------
# INDIAN GOVERNMENT DESIGN SYSTEM (CLEAN + MINIMALISTIC GIGW 3.0)
# -------------------------------------------------------------
def inject_custom_theme(theme="light"):
    is_dark = (theme == "dark")
    dark_css = """
        /* ============================================================= */
        /* COMPREHENSIVE GLASSMORPHIC DARK MODE SYSTEM                   */
        /* ============================================================= */
        .stApp {
            background-color: #070B14 !important;
            background: 
                radial-gradient(at 0% 0%, rgba(14, 165, 233, 0.22) 0px, transparent 50%),
                radial-gradient(at 100% 100%, rgba(56, 189, 248, 0.15) 0px, transparent 50%),
                radial-gradient(at 50% 20%, rgba(99, 102, 241, 0.14) 0px, transparent 60%),
                #070B14 !important;
            background-attachment: fixed !important;
            color: #F8FAFC !important;
        }

        /* Typography in Dark Mode */
        h1, h2, h3, h4, h5, h6 {
            color: #38BDF8 !important;
            text-shadow: 0 0 20px rgba(56, 189, 248, 0.3) !important;
        }
        p, span, div, label {
            color: #CBD5E1;
        }
        code, pre, .mono-font {
            background: rgba(30, 41, 59, 0.8) !important;
            backdrop-filter: blur(8px) !important;
            -webkit-backdrop-filter: blur(8px) !important;
            color: #38BDF8 !important;
            border-color: rgba(56, 189, 248, 0.25) !important;
        }

        /* Universal Glassmorphic Overrides in Dark Mode */
        .glass-panel,
        .glass-card,
        .glass-navbar,
        .glass-pill,
        .glass-kpi-bar,
        div[style*="background: #FFFFFF"],
        div[style*="background:#FFFFFF"],
        div[style*="background: #ffffff"],
        div[style*="background:#ffffff"],
        div[style*="background-color: #FFFFFF"],
        div[style*="background-color:#FFFFFF"],
        div[style*="background: rgb(255, 255, 255)"],
        div[style*="background-color: rgb(255, 255, 255)"] {
            background: rgba(15, 23, 42, 0.72) !important;
            background-color: rgba(15, 23, 42, 0.72) !important;
            backdrop-filter: blur(20px) saturate(190%) !important;
            -webkit-backdrop-filter: blur(20px) saturate(190%) !important;
            border: 1px solid rgba(56, 189, 248, 0.22) !important;
            border-radius: 14px !important;
            color: #F8FAFC !important;
            box-shadow: 0 12px 40px rgba(0, 0, 0, 0.5), inset 0 1px 1px rgba(255, 255, 255, 0.1) !important;
        }

        /* Light Gray / Off-white Containers to Deep Frosted Slate */
        div[style*="background: #F8FAFC"],
        div[style*="background: #F1F5F9"],
        div[style*="background: #F4F6F9"],
        div[style*="background:#F8FAFC"],
        div[style*="background:#F1F5F9"],
        div[style*="background:#F4F6F9"] {
            background: rgba(19, 30, 51, 0.68) !important;
            background-color: rgba(19, 30, 51, 0.68) !important;
            backdrop-filter: blur(14px) !important;
            -webkit-backdrop-filter: blur(14px) !important;
            border: 1px solid rgba(56, 189, 248, 0.16) !important;
            border-radius: 12px !important;
        }

        /* Glass Utility Bar in Dark Mode */
        .glass-utility-bar {
            background: rgba(10, 17, 32, 0.85) !important;
            border-bottom: 1px solid rgba(56, 189, 248, 0.2) !important;
        }

        /* Notice Banner in Dark Mode */
        .glass-notice,
        div[style*="background: #FFFBEB"] {
            background: rgba(30, 27, 75, 0.7) !important;
            backdrop-filter: blur(14px) !important;
            -webkit-backdrop-filter: blur(14px) !important;
            border: 1px solid rgba(224, 109, 16, 0.4) !important;
            border-left: 4px solid #E06D10 !important;
        }

        /* Text Overrides for Dark Mode */
        div[style*="color: #0B3C5D"],
        span[style*="color: #0B3C5D"],
        b[style*="color: #0B3C5D"],
        div[style*="color:#0B3C5D"],
        span[style*="color:#0B3C5D"],
        b[style*="color:#0B3C5D"],
        div[style*="color: #07253B"],
        span[style*="color: #07253B"] {
            color: #38BDF8 !important;
        }

        div[style*="color: #0F172A"],
        span[style*="color: #0F172A"],
        div[style*="color:#0F172A"],
        span[style*="color:#0F172A"] {
            color: #F8FAFC !important;
        }

        div[style*="color: #64748B"],
        span[style*="color: #64748B"],
        div[style*="color:#64748B"],
        span[style*="color:#64748B"],
        div[style*="color: #475569"],
        span[style*="color: #475569"] {
            color: #94A3B8 !important;
        }

        /* Border Overrides in Dark Mode */
        div[style*="border: 1px solid #CBD5E1"],
        div[style*="border:1px solid #CBD5E1"],
        div[style*="border: 1px solid #D0D7DE"],
        div[style*="border:1px solid #D0D7DE"] {
            border-color: rgba(56, 189, 248, 0.2) !important;
        }

        /* Form Inputs & Selects in Dark Mode (Glassmorphic) */
        div[data-baseweb="select"] > div,
        div[data-baseweb="popover"] div,
        div[data-baseweb="input"],
        div[data-baseweb="input"] > div,
        div[data-baseweb="base-input"],
        div[data-baseweb="base-input"] > input,
        div[data-testid="stTextInput"] input,
        div[data-testid="stNumberInput"] input {
            background: rgba(30, 41, 59, 0.72) !important;
            background-color: rgba(30, 41, 59, 0.72) !important;
            backdrop-filter: blur(12px) !important;
            -webkit-backdrop-filter: blur(12px) !important;
            border: 1.5px solid rgba(56, 189, 248, 0.28) !important;
            border-radius: 10px !important;
            color: #F8FAFC !important;
            box-shadow: 0 4px 14px rgba(0, 0, 0, 0.25), inset 0 1px 1px rgba(255, 255, 255, 0.06) !important;
        }
        div[data-testid="stTextInput"] input:focus,
        div[data-testid="stNumberInput"] input:focus {
            background: rgba(30, 41, 59, 0.95) !important;
            border-color: #38BDF8 !important;
            box-shadow: 0 0 0 3px rgba(56, 189, 248, 0.25), 0 4px 16px rgba(0, 0, 0, 0.3) !important;
        }
        div[data-baseweb="select"] * {
            color: #F8FAFC !important;
        }
        input::placeholder {
            color: #64748B !important;
        }

        /* Metrics & KPI Cards */
        div[data-testid="stMetric"] {
            background: rgba(15, 23, 42, 0.72) !important;
            backdrop-filter: blur(20px) saturate(190%) !important;
            -webkit-backdrop-filter: blur(20px) saturate(190%) !important;
            border: 1px solid rgba(56, 189, 248, 0.25) !important;
            border-radius: 14px !important;
            box-shadow: 0 8px 30px rgba(0, 0, 0, 0.45), inset 0 1px 1px rgba(255, 255, 255, 0.08) !important;
        }
        div[data-testid="stMetric"] label {
            color: #94A3B8 !important;
        }
        div[data-testid="stMetric"] div[data-testid="stMetricValue"] {
            color: #38BDF8 !important;
            text-shadow: 0 0 16px rgba(56, 189, 248, 0.4) !important;
        }

        /* Navigation Tabs in Dark Mode */
        div[data-testid="stRadio"] [role="radiogroup"] {
            background: rgba(10, 17, 32, 0.82) !important;
            backdrop-filter: blur(20px) !important;
            -webkit-backdrop-filter: blur(20px) !important;
            border: 1px solid rgba(56, 189, 248, 0.25) !important;
            border-radius: 14px !important;
            box-shadow: 0 10px 32px rgba(0, 0, 0, 0.5), inset 0 1px 1px rgba(255, 255, 255, 0.08) !important;
        }
        div[data-testid="stRadio"] div[role="radiogroup"] > label:has(input:checked) {
            background: rgba(30, 41, 59, 0.95) !important;
            border-bottom: 3px solid #38BDF8 !important;
            box-shadow: 0 0 16px rgba(56, 189, 248, 0.4) !important;
        }
        div[data-testid="stRadio"] div[role="radiogroup"] > label:has(input:checked) span,
        div[data-testid="stRadio"] div[role="radiogroup"] > label:has(input:checked) p {
            color: #38BDF8 !important;
        }

        /* Dark Toggle Track Checked */
        div[data-testid="stToggle"] [data-baseweb="checkbox"]:has(input:checked) > div,
        div[data-testid="stToggle"] input[type="checkbox"]:checked + div {
            background-color: #0284C7 !important;
            border-color: #38BDF8 !important;
            box-shadow: 0 0 10px rgba(56, 189, 248, 0.4) !important;
        }
        div[data-testid="stToggle"] label p,
        div[data-testid="stToggle"] label span,
        div[data-testid="stCheckbox"] label p,
        div[data-testid="stCheckbox"] label span {
            color: #F8FAFC !important;
        }

        /* Buttons in Dark Mode (Glassmorphic) */
        .stButton > button,
        button[kind="secondary"],
        button[data-testid*="secondary"] {
            background: rgba(30, 41, 59, 0.75) !important;
            backdrop-filter: blur(12px) !important;
            -webkit-backdrop-filter: blur(12px) !important;
            border: 1.5px solid rgba(56, 189, 248, 0.4) !important;
            border-radius: 10px !important;
            color: #38BDF8 !important;
            box-shadow: 0 4px 16px rgba(0, 0, 0, 0.3), inset 0 1px 0 rgba(255, 255, 255, 0.1) !important;
            transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1) !important;
        }
        .stButton > button:hover {
            background: #0284C7 !important;
            border-color: #38BDF8 !important;
            color: #FFFFFF !important;
            transform: translateY(-1px) !important;
            box-shadow: 0 6px 20px rgba(2, 132, 199, 0.5) !important;
        }
        button[kind="primary"],
        button[data-testid*="primary"],
        .stButton > button[kind="primary"],
        .stButton > button[data-testid*="primary"] {
            background: linear-gradient(135deg, #0284C7 0%, #0369A1 100%) !important;
            backdrop-filter: blur(12px) !important;
            -webkit-backdrop-filter: blur(12px) !important;
            border: 1.5px solid rgba(56, 189, 248, 0.6) !important;
            border-radius: 10px !important;
            color: #FFFFFF !important;
            box-shadow: 0 6px 20px rgba(2, 132, 199, 0.45), inset 0 1px 0 rgba(255, 255, 255, 0.25) !important;
            transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1) !important;
        }
        button[kind="primary"]:hover,
        button[data-testid*="primary"]:hover {
            background: #0284C7 !important;
            transform: translateY(-1px) !important;
            box-shadow: 0 8px 24px rgba(56, 189, 248, 0.55) !important;
        }

        /* Tables and DataFrames in Dark Mode */
        div[data-testid="stDataFrame"],
        div[data-testid="stExpander"] {
            background: rgba(15, 23, 42, 0.75) !important;
            backdrop-filter: blur(20px) saturate(190%) !important;
            -webkit-backdrop-filter: blur(20px) saturate(190%) !important;
            border: 1px solid rgba(56, 189, 248, 0.22) !important;
            border-radius: 14px !important;
            box-shadow: 0 10px 32px rgba(0, 0, 0, 0.45) !important;
        }

        /* Scrollbars in Dark Mode */
        ::-webkit-scrollbar-track {
            background: rgba(11, 17, 32, 0.6);
        }
        ::-webkit-scrollbar-thumb {
            background: #334155;
            border-radius: 4px;
        }
        ::-webkit-scrollbar-thumb:hover {
            background: #475569;
        }
    """ if is_dark else ""

    render_html("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+Devanagari:wght@400;600;700&family=Noto+Sans:wght@400;500;600;700&display=swap');

        /* Hide Streamlit default header, footer, burger */
        header[data-testid="stHeader"] {
            display: none !important;
        }
        footer {
            display: none !important;
        }
        #MainMenu {
            visibility: hidden;
        }

        /* ============================================================= */
        /* GLASSMORPHIC LIGHT BASE SYSTEM                                */
        /* ============================================================= */
        .stApp {
            background-color: #F4F6F9 !important;
            background: 
                radial-gradient(at 0% 0%, rgba(56, 189, 248, 0.16) 0px, transparent 50%),
                radial-gradient(at 100% 0%, rgba(14, 165, 233, 0.12) 0px, transparent 50%),
                radial-gradient(at 50% 100%, rgba(224, 109, 16, 0.08) 0px, transparent 50%),
                radial-gradient(at 80% 50%, rgba(19, 136, 8, 0.05) 0px, transparent 40%),
                #F1F5F9 !important;
            background-attachment: fixed !important;
            color: #0F172A !important;
            font-family: 'Noto Sans', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif !important;
        }

        .block-container {
            padding-top: 0.25rem !important;
            padding-bottom: 2rem !important;
            max-width: 1400px !important;
            margin: 0 auto !important;
        }

        /* Glass Utility Classes (Light Mode Default) */
        .glass-panel,
        .glass-card,
        .glass-navbar,
        .glass-pill,
        .glass-kpi-bar,
        div[style*="background: #FFFFFF"],
        div[style*="background:#FFFFFF"],
        div[style*="background: #ffffff"],
        div[style*="background:#ffffff"],
        div[style*="background-color: #FFFFFF"],
        div[style*="background-color:#FFFFFF"] {
            background: rgba(255, 255, 255, 0.74) !important;
            background-color: rgba(255, 255, 255, 0.74) !important;
            backdrop-filter: blur(18px) saturate(180%) !important;
            -webkit-backdrop-filter: blur(18px) saturate(180%) !important;
            border: 1px solid rgba(255, 255, 255, 0.8) !important;
            border-radius: 14px !important;
            box-shadow: 0 8px 32px 0 rgba(11, 60, 93, 0.08), inset 0 1px 2px 0 rgba(255, 255, 255, 0.95) !important;
        }

        /* Light Sub-containers to Frosted Translucent */
        div[style*="background: #F8FAFC"],
        div[style*="background: #F1F5F9"],
        div[style*="background: #F4F6F9"],
        div[style*="background:#F8FAFC"],
        div[style*="background:#F1F5F9"],
        div[style*="background:#F4F6F9"] {
            background: rgba(248, 250, 252, 0.65) !important;
            background-color: rgba(248, 250, 252, 0.65) !important;
            backdrop-filter: blur(12px) !important;
            -webkit-backdrop-filter: blur(12px) !important;
            border: 1px solid rgba(255, 255, 255, 0.65) !important;
            border-radius: 10px !important;
        }

        /* Notice Banner in Light Mode */
        .glass-notice,
        div[style*="background: #FFFBEB"] {
            background: rgba(254, 243, 199, 0.78) !important;
            backdrop-filter: blur(14px) !important;
            -webkit-backdrop-filter: blur(14px) !important;
            border: 1px solid rgba(253, 230, 138, 0.8) !important;
            border-left: 4px solid #E06D10 !important;
            border-radius: 12px !important;
        }

        /* Interactive card hover lift */
        .glass-card {
            transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1) !important;
        }
        .glass-card:hover {
            transform: translateY(-2px) !important;
            box-shadow: 0 12px 32px rgba(11, 60, 93, 0.12), inset 0 1px 2px rgba(255, 255, 255, 1.0) !important;
            border-color: rgba(56, 189, 248, 0.45) !important;
        }

        /* Typography Hierarchy (Government Standards) */
        h1, h2, h3, h4, h5, h6 {
            font-family: 'Noto Sans', 'Noto Sans Devanagari', sans-serif !important;
            color: #0B3C5D !important;
            font-weight: 700;
            letter-spacing: -0.01em;
        }
        h1 { font-size: 26px !important; line-height: 1.3 !important; }
        h2 { font-size: 20px !important; line-height: 1.3 !important; }
        h3 { font-size: 16px !important; line-height: 1.3 !important; }
        
        p, span, div, label {
            font-family: 'Noto Sans', -apple-system, BlinkMacSystemFont, sans-serif;
            color: #1E293B;
        }
        code, pre, .mono-font {
            font-family: 'Consolas', 'Courier New', monospace !important;
        }

        /* Scrollbars */
        ::-webkit-scrollbar {
            width: 7px;
            height: 7px;
        }
        ::-webkit-scrollbar-track {
            background: rgba(241, 245, 249, 0.5);
        }
        ::-webkit-scrollbar-thumb {
            background: #CBD5E1;
            border-radius: 4px;
        }
        ::-webkit-scrollbar-thumb:hover {
            background: #94A3B8;
        }

        /* Form Inputs & Selects (Glassmorphic) */
        div[data-baseweb="select"] > div,
        div[data-baseweb="popover"] div,
        div[data-baseweb="input"],
        div[data-baseweb="input"] > div,
        div[data-baseweb="base-input"],
        div[data-baseweb="base-input"] > input,
        div[data-testid="stTextInput"] input,
        div[data-testid="stNumberInput"] input {
            background: rgba(255, 255, 255, 0.75) !important;
            background-color: rgba(255, 255, 255, 0.75) !important;
            backdrop-filter: blur(12px) !important;
            -webkit-backdrop-filter: blur(12px) !important;
            border: 1.5px solid rgba(203, 213, 225, 0.8) !important;
            border-radius: 10px !important;
            color: #0F172A !important;
            font-size: 13px !important;
            box-shadow: 0 2px 8px rgba(11, 60, 93, 0.04), inset 0 1px 1px rgba(255, 255, 255, 0.8) !important;
            transition: all 0.2s ease !important;
        }
        div[data-testid="stTextInput"] input:focus,
        div[data-testid="stNumberInput"] input:focus {
            background: rgba(255, 255, 255, 0.95) !important;
            border-color: #0284C7 !important;
            box-shadow: 0 0 0 3px rgba(2, 132, 199, 0.18), 0 4px 12px rgba(11, 60, 93, 0.08) !important;
        }
        div[data-baseweb="select"] * {
            color: #0F172A !important;
            font-family: 'Noto Sans', sans-serif !important;
        }
        input::placeholder {
            color: #64748B !important;
        }

        /* Glassmorphic Government Buttons */
        .stButton > button,
        button[kind="secondary"],
        button[data-testid*="secondary"] {
            background: rgba(255, 255, 255, 0.8) !important;
            backdrop-filter: blur(12px) !important;
            -webkit-backdrop-filter: blur(12px) !important;
            border: 1.5px solid rgba(11, 60, 93, 0.8) !important;
            border-radius: 10px !important;
            color: #0B3C5D !important;
            font-family: 'Noto Sans', sans-serif !important;
            font-weight: 700 !important;
            font-size: 13px !important;
            padding: 9px 20px !important;
            transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1) !important;
            box-shadow: 0 2px 10px rgba(11, 60, 93, 0.08), inset 0 1px 1px rgba(255, 255, 255, 0.9) !important;
        }
        .stButton > button * {
            color: #0B3C5D !important;
            font-weight: 700 !important;
        }
        .stButton > button:hover {
            background: #0B3C5D !important;
            border-color: #07253B !important;
            color: #FFFFFF !important;
            transform: translateY(-1px) !important;
            box-shadow: 0 6px 18px rgba(11, 60, 93, 0.25) !important;
        }
        .stButton > button:hover * {
            color: #FFFFFF !important;
        }

        /* Primary Action Button */
        button[kind="primary"],
        button[data-testid*="primary"],
        .stButton > button[kind="primary"],
        .stButton > button[data-testid*="primary"] {
            background: linear-gradient(135deg, #0B3C5D 0%, #0369A1 100%) !important;
            backdrop-filter: blur(12px) !important;
            -webkit-backdrop-filter: blur(12px) !important;
            border: 1.5px solid rgba(255, 255, 255, 0.35) !important;
            color: #FFFFFF !important;
            font-weight: 700 !important;
            border-radius: 10px !important;
            padding: 9px 20px !important;
            box-shadow: 0 4px 16px rgba(11, 60, 93, 0.25), inset 0 1px 1px rgba(255, 255, 255, 0.3) !important;
            transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1) !important;
        }
        button[kind="primary"] *,
        button[data-testid*="primary"] *,
        .stButton > button[kind="primary"] *,
        .stButton > button[data-testid*="primary"] * {
            color: #FFFFFF !important;
            font-weight: 700 !important;
        }
        button[kind="primary"]:hover,
        button[data-testid*="primary"]:hover {
            background: linear-gradient(135deg, #07253B 0%, #0284C7 100%) !important;
            transform: translateY(-1px) !important;
            box-shadow: 0 6px 22px rgba(11, 60, 93, 0.35) !important;
        }

        /* High-Contrast Government Toggle Switches (st.toggle) */
        div[data-testid="stCheckbox"] label,
        div[data-testid="stToggle"] label {
            cursor: pointer !important;
            display: inline-flex !important;
            align-items: center !important;
            gap: 8px !important;
            background: transparent !important;
            background-color: transparent !important;
            border: none !important;
            box-shadow: none !important;
        }

        /* Explicitly guarantee label text and tooltip are NEVER styled as tracks or thumbs */
        div[data-testid="stToggle"] div[data-testid="stWidgetLabel"],
        div[data-testid="stToggle"] div[data-testid="stWidgetLabel"] *,
        div[data-testid="stCheckbox"] div[data-testid="stWidgetLabel"],
        div[data-testid="stCheckbox"] div[data-testid="stWidgetLabel"] * {
            background-color: transparent !important;
            background: transparent !important;
            border: none !important;
            box-shadow: none !important;
            border-radius: 0 !important;
        }

        div[data-testid="stCheckbox"] label p,
        div[data-testid="stCheckbox"] label span,
        div[data-testid="stToggle"] label p,
        div[data-testid="stToggle"] label span {
            color: #0F172A !important;
            font-size: 13px !important;
            font-weight: 600 !important;
            font-family: 'Noto Sans', sans-serif !important;
            margin: 0 !important;
            padding: 0 !important;
        }

        /* Toggle Track when UNCHECKED */
        div[data-testid="stToggle"] [data-baseweb="checkbox"] > div,
        div[data-testid="stToggle"] [data-baseweb="toggle"] > div,
        div[data-testid="stToggle"] input[type="checkbox"] + div {
            background-color: rgba(203, 213, 225, 0.8) !important;
            backdrop-filter: blur(8px) !important;
            -webkit-backdrop-filter: blur(8px) !important;
            border: 2px solid #64748B !important;
            border-radius: 9999px !important;
            transition: all 0.2s ease-in-out !important;
            box-shadow: inset 0 1px 2px rgba(0, 0, 0, 0.15) !important;
        }

        /* Toggle Track when CHECKED */
        div[data-testid="stToggle"] [data-baseweb="checkbox"]:has(input:checked) > div,
        div[data-testid="stToggle"] [data-baseweb="toggle"]:has(input:checked) > div,
        div[data-testid="stToggle"]:has(input:checked) [data-baseweb="checkbox"] > div,
        div[data-testid="stToggle"] input[type="checkbox"]:checked + div {
            background-color: #0B3C5D !important;
            border-color: #07253B !important;
            box-shadow: 0 0 10px rgba(11, 60, 93, 0.3) !important;
        }

        /* Sliding thumb inside toggle */
        div[data-testid="stToggle"] [data-baseweb="checkbox"] > div > div,
        div[data-testid="stToggle"] [data-baseweb="toggle"] > div > div,
        div[data-testid="stToggle"] input[type="checkbox"] + div > div {
            background-color: #FFFFFF !important;
            border: 1px solid #475569 !important;
            border-radius: 50% !important;
            box-shadow: 0 2px 6px rgba(0, 0, 0, 0.35) !important;
        }

        /* Checkbox Track when UNCHECKED */
        div[data-testid="stCheckbox"] [data-baseweb="checkbox"] > div,
        div[data-testid="stCheckbox"] input[type="checkbox"] + div {
            background-color: rgba(203, 213, 225, 0.8) !important;
            border: 2px solid #64748B !important;
            border-radius: 4px !important;
            transition: all 0.2s ease-in-out !important;
        }

        /* Checkbox Track when CHECKED */
        div[data-testid="stCheckbox"]:has(input:checked) [data-baseweb="checkbox"] > div,
        div[data-testid="stCheckbox"] input[type="checkbox"]:checked + div {
            background-color: #0B3C5D !important;
            border-color: #07253B !important;
        }

        div[data-testid="stCheckbox"] svg,
        div[data-testid="stToggle"] svg {
            fill: #FFFFFF !important;
            stroke: #FFFFFF !important;
        }

        /* Glassmorphic Navigation Bar (Radio Group Tabs) */
        div[data-testid="stRadio"] [role="radiogroup"] {
            display: flex !important;
            flex-wrap: wrap !important;
            justify-content: flex-start !important;
            gap: 4px !important;
            background: rgba(11, 60, 93, 0.88) !important;
            backdrop-filter: blur(18px) saturate(180%) !important;
            -webkit-backdrop-filter: blur(18px) saturate(180%) !important;
            border: 1px solid rgba(255, 255, 255, 0.25) !important;
            border-radius: 14px !important;
            padding: 5px 8px !important;
            margin-bottom: 14px !important;
            box-shadow: 0 8px 30px rgba(11, 60, 93, 0.18), inset 0 1px 1px rgba(255, 255, 255, 0.2) !important;
        }
        div[data-testid="stRadio"] input[type="radio"] {
            display: none !important;
        }
        div[data-testid="stRadio"] div[role="radiogroup"] > label > div:first-child {
            display: none !important;
        }
        div[data-testid="stRadio"] div[role="radiogroup"] > label {
            background: transparent !important;
            border: none !important;
            border-bottom: 3px solid transparent !important;
            border-radius: 8px !important;
            padding: 8px 16px !important;
            cursor: pointer !important;
            margin: 0 !important;
            transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1) !important;
        }
        div[data-testid="stRadio"] div[role="radiogroup"] > label:hover {
            background: rgba(255, 255, 255, 0.14) !important;
        }
        div[data-testid="stRadio"] div[role="radiogroup"] > label:has(input:checked) {
            background: rgba(7, 37, 59, 0.95) !important;
            border-bottom: 3px solid #E06D10 !important;
            box-shadow: 0 4px 14px rgba(0, 0, 0, 0.35) !important;
        }
        div[data-testid="stRadio"] div[role="radiogroup"] > label:has(input:checked) span,
        div[data-testid="stRadio"] div[role="radiogroup"] > label:has(input:checked) p {
            color: #FFFFFF !important;
            font-weight: 700 !important;
        }
        div[data-testid="stRadio"] div[role="radiogroup"] > label span,
        div[data-testid="stRadio"] div[role="radiogroup"] > label p {
            color: #E2E8F0 !important;
            font-family: 'Noto Sans', sans-serif !important;
            font-size: 13px !important;
            font-weight: 500 !important;
            margin: 0 !important;
        }

        /* Glassmorphic Metrics */
        div[data-testid="stMetric"] {
            background: rgba(255, 255, 255, 0.74) !important;
            backdrop-filter: blur(18px) saturate(180%) !important;
            -webkit-backdrop-filter: blur(18px) saturate(180%) !important;
            border: 1px solid rgba(255, 255, 255, 0.8) !important;
            border-radius: 14px !important;
            padding: 14px 18px !important;
            box-shadow: 0 6px 24px rgba(11, 60, 93, 0.06), inset 0 1px 1px rgba(255, 255, 255, 0.95) !important;
        }
        div[data-testid="stMetricLabel"] p {
            color: #64748B !important;
            font-size: 11px !important;
            font-weight: 700 !important;
            font-family: 'Noto Sans', sans-serif !important;
            text-transform: uppercase !important;
            letter-spacing: 0.03em !important;
        }
        div[data-testid="stMetricValue"] {
            color: #0B3C5D !important;
            font-family: 'Noto Sans', monospace !important;
            font-size: 24px !important;
            font-weight: 800 !important;
        }

        /* Tabs */
        button[data-baseweb="tab"] {
            font-family: 'Noto Sans', sans-serif !important;
            font-weight: 600 !important;
            font-size: 13px !important;
            color: #64748B !important;
            padding: 8px 18px !important;
            border-radius: 8px 8px 0 0 !important;
            transition: all 0.15s ease !important;
        }
        button[data-baseweb="tab"][aria-selected="true"] {
            color: #0B3C5D !important;
            border-bottom: 2.5px solid #0B3C5D !important;
            background: rgba(255, 255, 255, 0.4) !important;
        }

        /* Expanders */
        div[data-testid="stExpander"] {
            background: rgba(255, 255, 255, 0.74) !important;
            backdrop-filter: blur(18px) saturate(180%) !important;
            -webkit-backdrop-filter: blur(18px) saturate(180%) !important;
            border: 1px solid rgba(255, 255, 255, 0.8) !important;
            border-radius: 14px !important;
            box-shadow: 0 8px 30px rgba(11, 60, 93, 0.06), inset 0 1px 1px rgba(255, 255, 255, 0.9) !important;
        }

        /* Tables & DataFrames */
        div[data-testid="stDataFrame"] {
            border: 1px solid rgba(255, 255, 255, 0.8) !important;
            border-radius: 14px !important;
            background: rgba(255, 255, 255, 0.74) !important;
            backdrop-filter: blur(18px) saturate(180%) !important;
            -webkit-backdrop-filter: blur(18px) saturate(180%) !important;
            box-shadow: 0 8px 30px rgba(11, 60, 93, 0.06) !important;
            overflow: hidden !important;
        }
        </style>
    """ + (f"<style>{dark_css}</style>" if is_dark else ""))


# -------------------------------------------------------------
# 1. OFFICIAL GOVERNMENT UTILITY BAR & HEADER
# -------------------------------------------------------------
def render_figma_navbar(active_view="overview", theme="light"):
    """
    Renders standard Government of India utility bar and official clean header with glassmorphic styling.
    Follows MeitY GIGW 3.0 standards.
    """
    render_html(f"""
        <!-- Top Government Utility Bar -->
        <div class="glass-utility-bar" style="background: rgba(7, 37, 59, 0.88); backdrop-filter: blur(14px); -webkit-backdrop-filter: blur(14px); color: #E2E8F0; padding: 5px 20px; font-size: 12px; display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid rgba(255, 255, 255, 0.12); border-radius: 10px 10px 0 0;">
            <div style="display: flex; align-items: center; gap: 8px;">
                <span>🇮🇳</span>
                <span style="font-weight: 700; color: #FFFFFF; letter-spacing: 0.02em;">भारत सरकार</span>
                <span style="color: #64748B;">|</span>
                <span style="color: #CBD5E1;">Government of India</span>
            </div>
            <div style="display: flex; align-items: center; gap: 14px; font-size: 11px; color: #CBD5E1;">
                <span style="cursor: pointer;" title="Screen Reader Accessible">Screen Reader Access</span>
                <span>|</span>
                <span style="cursor: pointer; font-weight: 600;" title="Text Size Adjust">A- A A+</span>
                <span>|</span>
                <span style="background: rgba(11, 60, 93, 0.8); border: 1px solid rgba(255, 255, 255, 0.2); padding: 2px 8px; border-radius: 4px; color: #FFFFFF; font-weight: 600;">English</span>
                <span style="cursor: pointer; color: #CBD5E1;">हिन्दी</span>
            </div>
        </div>

        <!-- Official Department Header (Glassmorphic) -->
        <div class="glass-navbar" style="background: rgba(255, 255, 255, 0.76); backdrop-filter: blur(20px) saturate(180%); -webkit-backdrop-filter: blur(20px) saturate(180%); border: 1px solid rgba(255, 255, 255, 0.85); border-bottom: 3.5px solid #E06D10; padding: 14px 22px; display: flex; justify-content: space-between; align-items: center; border-radius: 0 0 14px 14px; box-shadow: 0 8px 32px rgba(11, 60, 93, 0.08), inset 0 1px 2px rgba(255, 255, 255, 0.95); margin-bottom: 14px;">
            <div style="display: flex; align-items: center; gap: 18px;">
                <div style="display: flex; align-items: center; justify-content: center; width: 46px; height: 52px; filter: drop-shadow(0 2px 4px rgba(11, 60, 93, 0.15));">
                    {ICONS_SVG['ashoka_emblem']}
                </div>
                <div style="display: flex; flex-direction: column; justify-content: center;">
                    <div style="font-size: 12px; font-weight: 700; color: #475569; letter-spacing: 0.03em;">
                        भूमि संसाधन विभाग &bull; Department of Land Resources
                    </div>
                    <div style="font-size: 11px; color: #64748B;">
                        ग्रामीण विकास मंत्रालय &bull; Ministry of Rural Development
                    </div>
                    <div style="font-size: 19px; font-weight: 800; color: #0B3C5D; margin-top: 2px; letter-spacing: -0.01em;">
                        3D ULPIN & Digital Cadastre Portal
                        <span style="font-size: 13px; font-weight: 700; color: #E06D10; margin-left: 8px;">(त्रि-आयामी भू-आधार)</span>
                    </div>
                </div>
            </div>

            <div style="display: flex; align-items: center; gap: 18px;">
                <div style="display: flex; flex-direction: column; align-items: flex-end; font-size: 11px; color: #64748B;">
                    <span style="font-weight: 700; color: #0B3C5D; letter-spacing: 0.02em;">ISO 19152 LADM STANDARDIZED</span>
                    <span style="color: #64748B;">National Cadastre Core Platform</span>
                </div>
                <div style="display: flex; align-items: center; filter: drop-shadow(0 2px 6px rgba(11, 60, 93, 0.15));">
                    {ICONS_SVG['nic_logo']}
                </div>
            </div>
        </div>
    """)

def render_breadcrumb(active_view: str, detail_name: str = None):
    """
    Renders official government breadcrumb hierarchy with glassmorphic styling:
    Home > Section > Detail
    """
    clean_view = active_view.replace("🏛️", "").replace("🌐", "").replace("🏠", "").replace("📐", "").replace("⚠️", "").replace("⚖️", "").strip()
    detail_html = f" &gt; <span style='color: #0F172A; font-weight: 700;'>{detail_name}</span>" if detail_name else ""
    
    render_html(f"""
        <div class="glass-pill" style="background: rgba(255, 255, 255, 0.72); backdrop-filter: blur(14px); -webkit-backdrop-filter: blur(14px); border: 1px solid rgba(255, 255, 255, 0.75); border-radius: 12px; padding: 8px 18px; margin-bottom: 14px; font-size: 12px; color: #64748B; display: flex; align-items: center; gap: 8px; box-shadow: 0 4px 16px rgba(11, 60, 93, 0.05), inset 0 1px 1px rgba(255, 255, 255, 0.9);">
            <span style="color: #0B3C5D; font-weight: 700;">मुख्य पृष्ठ (Home)</span>
            <span style="color: #94A3B8;">&gt;</span>
            <span style="color: #0B3C5D; font-weight: 600;">{clean_view}</span>
            {detail_html}
        </div>
    """)


# -------------------------------------------------------------
# 2. MINIMALIST GOVERNMENT DASHBOARD & KPI BAR
# -------------------------------------------------------------
def render_kpi_bar(df, theme="light"):
    """
    Renders glassmorphic government 4-item KPI row:
    25 Parcels | 08 States | 25 3D Records | ₹26,770 Cr Registered
    """
    total_parcels = len(df)
    subsurface_count = len(df[df['base_elevation'] < 0]) if 'base_elevation' in df.columns else 0
    states_count = df['state'].nunique() if 'state' in df.columns else 8
    total_val = df['valuation_cr'].sum() if 'valuation_cr' in df.columns else 26770

    render_html(f"""
        <div class="glass-kpi-bar" style="display: grid; grid-template-columns: repeat(4, 1fr); background: rgba(255, 255, 255, 0.76); backdrop-filter: blur(20px) saturate(180%); -webkit-backdrop-filter: blur(20px) saturate(180%); border: 1.5px solid rgba(255, 255, 255, 0.85); border-radius: 14px; margin-bottom: 18px; overflow: hidden; box-shadow: 0 8px 32px rgba(11, 60, 93, 0.08), inset 0 1px 2px rgba(255, 255, 255, 0.95);">
            <div style="padding: 16px 20px; border-right: 1px solid rgba(226, 232, 240, 0.7);">
                <div style="font-size: 28px; font-weight: 800; color: #0B3C5D; line-height: 1;">
                    {total_parcels:02d}
                </div>
                <div style="font-size: 13px; font-weight: 700; color: #1E293B; margin-top: 5px;">
                    Parcels Registered
                </div>
                <div style="font-size: 11px; color: #64748B; margin-top: 2px;">
                    ISO 19152 3D Spatial Units
                </div>
            </div>

            <div style="padding: 16px 20px; border-right: 1px solid rgba(226, 232, 240, 0.7);">
                <div style="font-size: 28px; font-weight: 800; color: #0B3C5D; line-height: 1;">
                    {states_count:02d}
                </div>
                <div style="font-size: 13px; font-weight: 700; color: #1E293B; margin-top: 5px;">
                    States & UTs Active
                </div>
                <div style="font-size: 11px; color: #64748B; margin-top: 2px;">
                    National Cadastre Grids
                </div>
            </div>

            <div style="padding: 16px 20px; border-right: 1px solid rgba(226, 232, 240, 0.7);">
                <div style="font-size: 28px; font-weight: 800; color: #0B3C5D; line-height: 1;">
                    {total_parcels:02d}
                </div>
                <div style="font-size: 13px; font-weight: 700; color: #1E293B; margin-top: 5px;">
                    3D Cadastre Records
                </div>
                <div style="font-size: 11px; color: #64748B; margin-top: 2px;">
                    {subsurface_count} Subsurface & Air Rights
                </div>
            </div>

            <div style="padding: 16px 20px;">
                <div style="font-size: 28px; font-weight: 800; color: #138808; line-height: 1;">
                    ₹ {total_val:,.0f} Cr
                </div>
                <div style="font-size: 13px; font-weight: 700; color: #1E293B; margin-top: 5px;">
                    Registered Valuation
                </div>
                <div style="font-size: 11px; color: #64748B; margin-top: 2px;">
                    Secured Spatial Assets
                </div>
            </div>
        </div>
    """)

def render_landing_hero(df, active_prop=None):
    """
    Renders clean, functional government dashboard with Quick Services and announcements.
    Replaces flashy SaaS hero with functional administrative controls.
    """
    render_html(f"""
        <!-- Official Notice Bar -->
        <div style="background: #FFFBEB; border: 1px solid #FDE68A; border-left: 4px solid #E06D10; border-radius: 4px; padding: 10px 16px; margin-bottom: 16px; font-size: 13px; display: flex; justify-content: space-between; align-items: center;">
            <div>
                <span style="font-weight: 700; color: #92400E;">सूचना / Official Notice:</span>
                <span style="color: #78350F; margin-left: 6px;">
                    National Land Records Modernization Programme (DILRMP) — 3D Volumetric Cadastre & Digital Twin operational across pilot metros.
                </span>
            </div>
            <span style="background: #FEF3C7; color: #B45309; font-weight: 700; font-size: 11px; padding: 2px 8px; border-radius: 3px;">
                SIH 2026 PROTOTYPE
            </span>
        </div>

        <!-- Quick Services Section -->
        <div style="background: #FFFFFF; border: 1px solid #CBD5E1; border-radius: 4px; padding: 18px 20px; margin-bottom: 20px;">
            <div style="font-size: 16px; font-weight: 700; color: #0B3C5D; margin-bottom: 4px;">
                Quick Services / त्वरित सेवाएं
            </div>
            <div style="font-size: 13px; color: #64748B; margin-bottom: 14px;">
                Access core cadastre services, title deed verification, and spatial analysis tools directly.
            </div>

            <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 12px;">
                <div style="border: 1px solid #E2E8F0; border-radius: 4px; padding: 12px 14px; background: #F8FAFC;">
                    <div style="font-weight: 700; font-size: 13px; color: #0B3C5D;">🔍 ULPIN Title Verification</div>
                    <div style="font-size: 12px; color: #64748B; margin-top: 3px;">Verify 14-digit Bhu-Aadhaar ULPIN vertical titles and encumbrances.</div>
                </div>

                <div style="border: 1px solid #E2E8F0; border-radius: 4px; padding: 12px 14px; background: #F8FAFC;">
                    <div style="font-weight: 700; font-size: 13px; color: #0B3C5D;">🌐 3D Digital Twin Viewer</div>
                    <div style="font-size: 12px; color: #64748B; margin-top: 3px;">Explore procedural 3D architectural digital twins with floor slices.</div>
                </div>

                <div style="border: 1px solid #E2E8F0; border-radius: 4px; padding: 12px 14px; background: #F8FAFC;">
                    <div style="font-weight: 700; font-size: 13px; color: #0B3C5D;">🗺️ GIS Cadastre Map</div>
                    <div style="font-size: 12px; color: #64748B; margin-top: 3px;">Pan-India topographic parcel footprints with height extrusions.</div>
                </div>

                <div style="border: 1px solid #E2E8F0; border-radius: 4px; padding: 12px 14px; background: #F8FAFC;">
                    <div style="font-weight: 700; font-size: 13px; color: #0B3C5D;">📄 Bhu-Aadhaar Certificate</div>
                    <div style="font-size: 12px; color: #64748B; margin-top: 3px;">Download authenticated 3D Title Certificates with QR codes.</div>
                </div>

                <div style="border: 1px solid #E2E8F0; border-radius: 4px; padding: 12px 14px; background: #F8FAFC;">
                    <div style="font-weight: 700; font-size: 13px; color: #0B3C5D;">⚠️ Subsurface Clash Audit</div>
                    <div style="font-size: 12px; color: #64748B; margin-top: 3px;">Analyze underground metro, gas pipeline, and foundation clashes.</div>
                </div>

                <div style="border: 1px solid #E2E8F0; border-radius: 4px; padding: 12px 14px; background: #F8FAFC;">
                    <div style="font-weight: 700; font-size: 13px; color: #0B3C5D;">⚖️ Sub-Registrar Conveyance</div>
                    <div style="font-size: 12px; color: #64748B; margin-top: 3px;">Execute digital deed transfers with automated 6% stamp duty.</div>
                </div>
            </div>
        </div>

        <!-- Master Registry Highlights Table -->
        <div style="background: #FFFFFF; border: 1px solid #CBD5E1; border-radius: 4px; padding: 18px 20px;">
            <div style="font-size: 16px; font-weight: 700; color: #0B3C5D; margin-bottom: 4px;">
                Verified 3D Cadastral Records Directory / सत्यापित भू-अभिलेख
            </div>
            <div style="font-size: 13px; color: #64748B; margin-bottom: 12px;">
                Summary of indexed volumetric parcels registered under ISO 19152 LADM framework.
            </div>
        </div>
    """)

    cols_to_show = [c for c in ['property_id', 'name', 'city', 'state', 'type', 'total_height', 'base_elevation', 'valuation_cr', 'status'] if c in df.columns]
    st.dataframe(df[cols_to_show], use_container_width=True, hide_index=True)


# -------------------------------------------------------------
# 3. CITIZEN PORTAL & BHU-AADHAAR 3D CERTIFICATE
# -------------------------------------------------------------
def render_citizen_dashboard(prop_data, floors, ulpin_str="27221040120105-004"):
    effective_owner = prop_data.get('owner', 'Rajesh Sharma & Anita Sharma')
    prop_name = prop_data.get('name', 'Sky Heights - Block A')
    prop_city = prop_data.get('city', 'Pune')

    render_html(f"""
        <div style="background: #FFFFFF; border: 1px solid #CBD5E1; border-radius: 4px; padding: 16px 20px; margin-bottom: 16px; display: flex; justify-content: space-between; align-items: center;">
            <div>
                <div style="font-size: 12px; font-weight: 600; color: #E06D10; text-transform: uppercase;">
                    नागरिक सेवा पोर्टल / Citizen Portal
                </div>
                <div style="font-size: 20px; font-weight: 700; color: #0B3C5D; margin-top: 2px;">
                    Welcome, {effective_owner}
                </div>
                <div style="font-size: 13px; color: #64748B; margin-top: 2px;">
                    Linked Aadhaar / Land Registry ID: <code style="font-weight: 600; color: #0B3C5D;">UID-2026-****-8819</code> &bull; Primary Jurisdiction: <b>{prop_city}</b>
                </div>
            </div>
            <div style="display: flex; gap: 8px;">
                <span style="background: #F0FDF4; border: 1px solid #BBF7D0; color: #138808; padding: 4px 10px; border-radius: 3px; font-size: 12px; font-weight: 700;">
                    ✓ KYC & Title Verified
                </span>
            </div>
        </div>
    """)

def render_bhu_aadhaar_card_preview(prop, floor_dict, ulpin_str, theme="light"):
    """
    Renders authentic Bhu-Aadhaar 3D Title Card following Government of India identity card layout.
    """
    z_range = f"{floor_dict.get('z_start', 0)}m to {floor_dict.get('z_end', 0)}m MSL"
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

    c_card, c_qr = st.columns([3.2, 1.2], gap="medium")
    with c_card:
        render_html(f"""
            <div style="background: #FFFFFF; border: 1px solid #CBD5E1; border-radius: 4px; box-shadow: 0 1px 3px rgba(0,0,0,0.06); overflow: hidden;">
                <!-- Tricolor Accent Top Bar -->
                <div style="height: 4px; background: linear-gradient(90deg, #E06D10 0%, #E06D10 33%, #FFFFFF 33%, #FFFFFF 66%, #138808 66%, #138808 100%);"></div>

                <div style="padding: 14px 18px;">
                    <div style="display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid #E2E8F0; padding-bottom: 8px; margin-bottom: 10px;">
                        <div style="display: flex; align-items: center; gap: 8px;">
                            <span style="font-size: 16px;">🏛️</span>
                            <div>
                                <div style="font-size: 12px; font-weight: 700; color: #0B3C5D; text-transform: uppercase;">
                                    BHU-AADHAAR 3D DIGITAL TITLE CERTIFICATE
                                </div>
                                <div style="font-size: 10px; color: #64748B;">Department of Land Resources &bull; ISO 19152 LADM</div>
                            </div>
                        </div>
                        <span style="background: #F0FDF4; color: #138808; border: 1px solid #BBF7D0; font-size: 10px; font-weight: 700; padding: 2px 8px; border-radius: 3px;">
                            GOVERNMENT CERTIFIED
                        </span>
                    </div>

                    <div style="background: #F8FAFC; border: 1px solid #E2E8F0; border-radius: 4px; padding: 6px 12px; margin-bottom: 10px; display: flex; justify-content: space-between; align-items: center;">
                        <span style="font-size: 11px; color: #64748B; font-weight: 600;">14-DIGIT 3D ULPIN:</span>
                        <span style="font-family: 'Consolas', monospace; font-size: 14px; font-weight: 700; color: #0B3C5D; letter-spacing: 0.05em;">
                            {ulpin_str}
                        </span>
                    </div>

                    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 8px; font-size: 12px; color: #334155; margin-bottom: 10px;">
                        <div><span style="color: #64748B;">Title Holder:</span> <b style="color: #0F172A;">{effective_owner}</b></div>
                        <div><span style="color: #64748B;">Vertical Elevation:</span> <b style="color: #0F172A;">{z_range}</b></div>
                        <div><span style="color: #64748B;">Property Complex:</span> <b style="color: #0F172A;">{prop.get('name', '')}</b></div>
                        <div><span style="color: #64748B;">Unit Designation:</span> <b style="color: #0B3C5D;">{floor_dict.get('floor_name', f"Level {floor_dict.get('floor_number')}")}</b></div>
                        <div><span style="color: #64748B;">Jurisdiction:</span> <b style="color: #0F172A;">{prop.get('city', '')}, {prop.get('state', '')}</b></div>
                        <div><span style="color: #64748B;">Encumbrance:</span> <b style="color: #138808;">NIL (Clear Title)</b></div>
                    </div>

                    <div style="font-family: 'Consolas', monospace; font-size: 10px; color: #64748B; background: #F1F5F9; padding: 4px 8px; border-radius: 3px; overflow: hidden; text-overflow: ellipsis; white-space: nowrap;">
                        SHA-256 SEAL: {sha_hash}
                    </div>
                </div>
            </div>
        """)
    with c_qr:
        st.image(qr_bytes, caption="Verify Digital 3D Title", width=130)

def render_figma_digital_title_certificate(prop, floor_dict, ulpin_str):
    """
    Renders authentic official legal title deed parchment following Government of India registration standards.
    """
    effective_owner = floor_dict.get('owner') or prop.get('owner', 'Rajesh Sharma & Anita Sharma')
    z_range = f"+{floor_dict.get('z_start', 12.4):.1f}m to +{floor_dict.get('z_end', 15.6):.1f}m MSL"
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
        <div style="display: flex; justify-content: center; margin-top: 10px; margin-bottom: 24px;">
            <div style="width: 100%; max-width: 820px; background: #FFFFFF; border: 2px solid #0B3C5D; border-radius: 4px; padding: 36px 40px; color: #0F172A; box-shadow: 0 1px 4px rgba(0,0,0,0.08);">
                
                <!-- Deed Header -->
                <div style="display: flex; justify-content: space-between; align-items: center; border-bottom: 2px solid #0B3C5D; padding-bottom: 16px; margin-bottom: 20px;">
                    <div style="width: 50px; height: 50px; display: flex; align-items: center; justify-content: center;">
                        {ICONS_SVG['ashoka_emblem']}
                    </div>
                    <div style="text-align: center;">
                        <div style="font-size: 14px; font-weight: 800; color: #0B3C5D; letter-spacing: 0.05em;">
                            भारत सरकार &bull; GOVERNMENT OF INDIA
                        </div>
                        <div style="font-size: 12px; font-weight: 600; color: #475569; margin-top: 2px;">
                            भूमि संसाधन विभाग &bull; DEPARTMENT OF LAND RESOURCES
                        </div>
                        <div style="font-size: 17px; font-weight: 800; color: #0B3C5D; margin-top: 4px;">
                            CERTIFICATE OF 3D PROPERTY TITLE (भू-आधार)
                        </div>
                    </div>
                    <div style="width: 60px; height: 60px; border: 1px solid #CBD5E1; padding: 2px; background: #FFFFFF;">
                        <img src="data:image/png;base64,{qr_b64}" style="width: 100%; height: 100%; object-fit: contain;"/>
                    </div>
                </div>

                <!-- Schedule of Property Table -->
                <div style="border: 1px solid #CBD5E1; border-radius: 4px; overflow: hidden; margin-bottom: 20px;">
                    <div style="background: #0B3C5D; color: #FFFFFF; padding: 6px 12px; font-size: 12px; font-weight: 700; text-transform: uppercase;">
                        Schedule of Vertical Spatial Asset (अनुसूची)
                    </div>
                    <table style="width: 100%; border-collapse: collapse; font-size: 12px;">
                        <tr style="border-bottom: 1px solid #E2E8F0;">
                            <td style="padding: 8px 12px; background: #F8FAFC; width: 30%; font-weight: 600; color: #475569;">14-Digit 3D ULPIN</td>
                            <td style="padding: 8px 12px; font-family: 'Consolas', monospace; font-weight: 700; color: #0B3C5D;">{ulpin_str}</td>
                        </tr>
                        <tr style="border-bottom: 1px solid #E2E8F0;">
                            <td style="padding: 8px 12px; background: #F8FAFC; font-weight: 600; color: #475569;">Registered Titleholder</td>
                            <td style="padding: 8px 12px; font-weight: 700; color: #0F172A;">{effective_owner.upper()}</td>
                        </tr>
                        <tr style="border-bottom: 1px solid #E2E8F0;">
                            <td style="padding: 8px 12px; background: #F8FAFC; font-weight: 600; color: #475569;">Spatial Address</td>
                            <td style="padding: 8px 12px; color: #1E293B;">Flat 402, Block A, {prop.get('name', 'Sky Heights')}, {prop.get('city', 'Pune')}</td>
                        </tr>
                        <tr style="border-bottom: 1px solid #E2E8F0;">
                            <td style="padding: 8px 12px; background: #F8FAFC; font-weight: 600; color: #475569;">Vertical Elevation Range</td>
                            <td style="padding: 8px 12px; font-family: 'Consolas', monospace; font-weight: 600; color: #0F172A;">{z_range}</td>
                        </tr>
                        <tr>
                            <td style="padding: 8px 12px; background: #F8FAFC; font-weight: 600; color: #475569;">Volumetric Built Space</td>
                            <td style="padding: 8px 12px; color: #1E293B;">1,450 Sq.Ft Built-up Area (Approx. 4,640 Cu.Ft Volume)</td>
                        </tr>
                    </table>
                </div>

                <!-- Boundaries & Legal Containment -->
                <div style="background: #F8FAFC; border: 1px solid #E2E8F0; border-radius: 4px; padding: 12px 14px; margin-bottom: 20px; font-size: 12px; line-height: 1.6;">
                    <div style="font-weight: 700; color: #0B3C5D; margin-bottom: 4px;">Cadastral Boundaries & Adjoining Strata:</div>
                    &bull; <b>North / South / East / West:</b> Contained within Parent Cadastral Plot #{prop.get('property_id', 101)}<br/>
                    &bull; <b>Zenith Boundary:</b> Floor 05 Underside (+15.6m MSL) &bull; <b>Nadir Boundary:</b> Structural Floor 04 Slab (+12.4m MSL)<br/>
                    &bull; <b>ISO 19152 Compliance:</b> LADM-3D-IN-2026 Watertight Unit &bull; Zero Detected Subsurface Clashes
                </div>

                <!-- Sign-off Block -->
                <div style="display: flex; justify-content: space-between; align-items: flex-end; padding-top: 10px; border-top: 1px solid #CBD5E1;">
                    <div style="font-size: 11px; color: #64748B;">
                        Date of Issue: <b>14-November-2026</b><br/>
                        Registering Authority: <b>Office of Sub-Registrar, {prop.get('city', 'Pune')}</b><br/>
                        Cryptographic Hash: <code style="font-size: 10px;">{sha_hash[:24]}...</code>
                    </div>
                    <div style="text-align: center;">
                        <div style="font-size: 15px; font-weight: 700; color: #0B3C5D; font-style: italic;">Amit Patwardhan</div>
                        <div style="width: 140px; height: 1px; background: #0B3C5D; margin: 4px 0;"></div>
                        <div style="font-size: 11px; font-weight: 700; color: #0F172A;">Sub-Registrar of Assurances</div>
                    </div>
                </div>

            </div>
        </div>
    """)


# -------------------------------------------------------------
# 4. 3D PROPERTY DOSSIER & ARCHITECTURAL STACK
# -------------------------------------------------------------
def render_property_spec_card(prop, theme="light"):
    """Renders clean administrative property dossier table."""
    base_elev = prop.get('base_elevation', 0)
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
    height = float(prop.get('total_height', 0.0))

    render_html(f"""
        <div style="background: #FFFFFF; border: 1px solid #CBD5E1; border-radius: 4px; padding: 14px 16px; margin-bottom: 14px;">
            <div style="display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid #E2E8F0; padding-bottom: 8px; margin-bottom: 10px;">
                <div>
                    <div style="font-size: 11px; font-weight: 700; color: #64748B; text-transform: uppercase;">
                        PARCEL #{pid} &bull; {str(city).upper()}
                    </div>
                    <div style="font-size: 16px; font-weight: 700; color: #0B3C5D;">
                        {name}
                    </div>
                </div>
                <span style="background: #F1F5F9; color: #0B3C5D; border: 1px solid #CBD5E1; font-size: 11px; font-weight: 700; padding: 2px 8px; border-radius: 3px;">
                    {prop_type}
                </span>
            </div>

            <table style="width: 100%; border-collapse: collapse; font-size: 12px;">
                <tr style="border-bottom: 1px solid #F1F5F9;">
                    <td style="padding: 5px 0; color: #64748B; width: 40%;">Titleholder:</td>
                    <td style="padding: 5px 0; font-weight: 600; color: #0F172A;">{owner}</td>
                </tr>
                <tr style="border-bottom: 1px solid #F1F5F9;">
                    <td style="padding: 5px 0; color: #64748B;">Zoning Classification:</td>
                    <td style="padding: 5px 0; font-weight: 600; color: #0F172A;">{zone}</td>
                </tr>
                <tr style="border-bottom: 1px solid #F1F5F9;">
                    <td style="padding: 5px 0; color: #64748B;">Vertical Extent:</td>
                    <td style="padding: 5px 0; font-weight: 600; color: #0B3C5D;">{height:.1f}m (Base: {base_elev}m MSL)</td>
                </tr>
                <tr style="border-bottom: 1px solid #F1F5F9;">
                    <td style="padding: 5px 0; color: #64748B;">Coordinates:</td>
                    <td style="padding: 5px 0; font-family: 'Consolas', monospace; color: #0F172A;">{lat:.4f}, {lon:.4f}</td>
                </tr>
                <tr>
                    <td style="padding: 5px 0; color: #64748B;">Cadastral Valuation:</td>
                    <td style="padding: 5px 0; font-weight: 700; color: #138808;">₹ {val:.1f} Crores</td>
                </tr>
            </table>
        </div>
    """)

def render_vertical_stack(floors, prop_data, theme="light"):
    """
    Renders clean architectural vertical strata diagram.
    """
    sorted_floors = sorted(floors, key=lambda x: x['z_end'], reverse=True)
    html_blocks = []

    for f in sorted_floors:
        floor_num = f['floor_number']
        z_start = f['z_start']
        z_end = f['z_end']

        if floor_num < 0:
            bg = "#FFFBEB"
            border_col = "#FDE68A"
            badge_col = "#B45309"
            default_title = f"Basement {abs(floor_num):02d} (Subsurface)"
            z_badge = f"{z_end:.1f}m to {z_start:.1f}m"
        else:
            bg = "#F8FAFC"
            border_col = "#E2E8F0"
            badge_col = "#0B3C5D"
            default_title = f"Level {floor_num:02d} (Superstructure)"
            z_badge = f"+{z_start:.1f}m to +{z_end:.1f}m"

        lvl_code = f.get('level_code', f"#{abs(floor_num):02d}")
        flr_title = f.get('floor_name', default_title)

        block = f"""
            <div style="display: flex; justify-content: space-between; align-items: center; padding: 6px 10px; background: {bg}; border: 1px solid {border_col}; border-radius: 3px; margin-bottom: 4px; font-size: 12px;">
                <div style="display: flex; align-items: center; gap: 6px; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; max-width: 70%;">
                    <span style="font-weight: 700; color: {badge_col}; font-family: 'Consolas', monospace; flex-shrink: 0;">{lvl_code}</span>
                    <span style="color: #1E293B; font-weight: 500; overflow: hidden; text-overflow: ellipsis; white-space: nowrap;">{flr_title}</span>
                </div>
                <div style="font-family: 'Consolas', monospace; font-size: 11px; color: #475569; background: #FFFFFF; border: 1px solid #CBD5E1; padding: 1px 6px; border-radius: 2px; flex-shrink: 0;">
                    {z_badge}
                </div>
            </div>
        """
        html_blocks.append(block)

    render_html(f"""
        <div style="background: #FFFFFF; border: 1px solid #CBD5E1; border-radius: 4px; padding: 14px 16px; margin-bottom: 14px;">
            <div style="font-size: 11px; font-weight: 700; text-transform: uppercase; color: #64748B; margin-bottom: 8px;">
                ARCHITECTURAL VERTICAL STRATA ({len(floors)} LEVELS)
            </div>
            <div style="max-height: 240px; overflow-y: auto; padding-right: 2px;">
                {''.join(html_blocks)}
            </div>
        </div>
    """)


# -------------------------------------------------------------
# 5. SUBSURFACE CLASH REPORT & SURVEYOR QUEUE
# -------------------------------------------------------------
def render_clash_report_ui(conflicts, theme="light"):
    """
    Renders 3D collision & spatial encroachment detection findings with clean government styling.
    """
    if not conflicts:
        render_html("""
            <div style="display: flex; align-items: center; gap: 10px; background: #F0FDF4; border: 1px solid #BBF7D0; border-left: 4px solid #138808; padding: 10px 14px; border-radius: 4px; margin-bottom: 12px;">
                <span style="font-size: 18px;">✓</span>
                <div>
                    <div style="font-weight: 700; color: #138808; font-size: 13px;">Zero Spatial Encroachments Detected</div>
                    <div style="font-size: 12px; color: #475569;">All subsurface foundation piles and underground utility safety corridors are compliant.</div>
                </div>
            </div>
        """)
        return

    render_html(f"""
        <div style="margin-bottom: 10px; font-size: 12px; font-weight: 700; color: #C53030; text-transform: uppercase; letter-spacing: 0.05em;">
            ⚠️ Identified {len(conflicts)} Spatial Conflicts / Safety Buffer Infringements
        </div>
    """)

    for c in conflicts:
        is_crit = c.get('severity') == "CRITICAL_COLLISION"
        badge_bg = "#FEF2F2" if is_crit else "#FFFBEB"
        badge_border = "#FCA5A5" if is_crit else "#FDE68A"
        badge_fg = "#991B1B" if is_crit else "#92400E"

        render_html(f"""
            <div style="background: #FFFFFF; border: 1px solid #CBD5E1; border-left: 4px solid {badge_fg}; border-radius: 4px; padding: 10px 14px; margin-bottom: 8px;">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 4px;">
                    <span style="font-family: 'Consolas', monospace; font-size: 11px; font-weight: 700; color: {badge_fg}; background: {badge_bg}; border: 1px solid {badge_border}; padding: 1px 6px; border-radius: 3px;">
                        {c.get('badge', 'CONFLICT')}
                    </span>
                    <span style="font-size: 11px; color: #64748B; font-family: 'Consolas', monospace;">
                        Dist: {c.get('distance_m', 0)}m &bull; Overlap: {c.get('overlap_z_m', 0)}m
                    </span>
                </div>
                <div style="font-size: 13px; color: #0F172A; margin-bottom: 2px;">
                    Asset: <b>{c.get('conflicting_name', 'Unknown')}</b> (#{c.get('conflicting_id', '')}) &bull; <i style="color: #64748B;">{c.get('conflicting_type', '')}</i>
                </div>
                <div style="font-size: 12px; color: #475569;">
                    {c.get('description', '')}
                </div>
            </div>
        """)

def render_figma_clash_report(conflicts, prop_data):
    """Renders comprehensive spatial clash dossier with export options."""
    prop_name = prop_data.get('name', 'Grand Central Subsurface Concourse')
    prop_city = prop_data.get('city', 'Navi Mumbai')
    prop_id = prop_data.get('property_id', 102)

    render_html(f"""
        <div style="background: #FFFFFF; border: 1px solid #CBD5E1; border-radius: 4px; padding: 14px 18px; margin-bottom: 14px; display: flex; justify-content: space-between; align-items: center;">
            <div>
                <div style="font-size: 11px; font-weight: 700; color: #C53030; text-transform: uppercase;">
                    SPATIAL ENCROACHMENT & BUFFER DOSSIER
                </div>
                <div style="font-size: 18px; font-weight: 700; color: #0B3C5D; margin-top: 2px;">
                    Subsurface Corridor Audit &bull; {prop_name} ({prop_city})
                </div>
            </div>
        </div>
    """)

    c1, c2 = st.columns([1.0, 1.4], gap="medium")
    with c1:
        csv_rows = [
            "Conflict_ID,Asset_Name,Depth_m,Buffer_Threshold_m,Severity,Regulation,Recommended_Action",
            f"CLASH-01,Hinjewadi Metro Line II (Subway Shaft),-12.4,2.00,CRITICAL_COLLISION,Metro Railways Act 1978,Structural re-engineering of foundation piling required",
            f"CLASH-02,PNGRB City Gas Pipeline Grid,-2.1,2.00,ADVISORY_SAFETY_BUFFER,PNGRB Act 2006,Re-align utility conduit pathway or reinforce sleeve"
        ]
        st.download_button(
            label="📥 Export Spatial Clash Audit (CSV)",
            data="\n".join(csv_rows),
            file_name=f"clash_audit_{prop_id}.csv",
            mime="text/csv",
            key="btn_export_clash_csv",
            use_container_width=True
        )
    with c2:
        btn_label = "✅ Official Municipal Notice Dispatched" if st.session_state.get("metro_notified") else "⚠️ Dispatch Official Notice to Metro / Municipal Authority"
        if st.button(btn_label, key="btn_notify_metro", type="primary", use_container_width=True):
            st.session_state["metro_notified"] = not st.session_state.get("metro_notified", False)
            st.rerun()

    if st.session_state.get("metro_notified"):
        st.success("🚨 Official Notice Dispatched to Metro Rail Corp & Municipal Chief Engineer (Docket #METRO-2026-9912).")

    render_html("<div style='height: 10px;'></div>")
    render_clash_report_ui(conflicts, theme="light")

def render_figma_surveyor_workstation():
    """Renders official Surveyor Workstation header."""
    render_html(f"""
        <div style="background: #FFFFFF; border: 1px solid #CBD5E1; border-radius: 4px; padding: 14px 18px; margin-bottom: 16px; display: flex; justify-content: space-between; align-items: center;">
            <div style="display: flex; align-items: center; gap: 10px;">
                <span style="font-size: 20px;">📐</span>
                <div>
                    <div style="font-size: 16px; font-weight: 700; color: #0B3C5D;">
                        GIS Surveyor Technical Terminal / भू-सर्वेक्षक टर्मिनल
                    </div>
                    <div style="font-size: 12px; color: #64748B;">
                        Authorized Land Surveyor: <b>Amit Patwardhan (Licence: M-9912)</b>
                    </div>
                </div>
            </div>
            <div style="display: flex; gap: 24px; font-size: 12px;">
                <div><span style="color: #64748B;">Completed Surveys:</span> <b style="color: #138808;">128</b></div>
                <div><span style="color: #64748B;">Pending RTK Queue:</span> <b style="color: #E06D10;">14</b></div>
                <div><span style="color: #64748B;">CORS Satellite Sync:</span> <b style="color: #0B3C5D;">Active (NavIC)</b></div>
            </div>
        </div>
    """)

def render_figma_survey_queue():
    """Renders clean dispatch queue table."""
    render_html("""
        <div style="font-size: 13px; font-weight: 700; color: #0B3C5D; margin-bottom: 8px;">
            SURVEY DISPATCH QUEUE / फील्ड सर्वे कार्य
        </div>

        <div style="background: #FFFFFF; border: 1px solid #CBD5E1; border-radius: 4px; padding: 10px 12px; margin-bottom: 8px;">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <span style="font-size: 11px; font-weight: 700; color: #0B3C5D;">Sector 3, Hinjewadi</span>
                <span style="background: #FEF2F2; color: #991B1B; border: 1px solid #FCA5A5; font-size: 10px; font-weight: 700; padding: 1px 6px; border-radius: 2px;">HIGH PRIORITY</span>
            </div>
            <div style="font-size: 11px; color: #64748B; margin-top: 2px;">Requester: Amit G. Patel &bull; Drone RTK Pending</div>
        </div>
    """)
    if st.button("⚡ Initialize LiDAR Acquisition (Hinjewadi)", key="btn_lidar_1", use_container_width=True):
        st.session_state["lidar_mission_msg"] = "Sector 3, Hinjewadi: Drone flight vector synched. RTK point cloud acquisition active."
        st.rerun()

    render_html("""
        <div style="background: #FFFFFF; border: 1px solid #CBD5E1; border-radius: 4px; padding: 10px 12px; margin-top: 8px; margin-bottom: 8px;">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <span style="font-size: 11px; font-weight: 700; color: #0B3C5D;">Phase II, IT Park</span>
                <span style="background: #F1F5F9; color: #475569; border: 1px solid #CBD5E1; font-size: 10px; font-weight: 700; padding: 1px 6px; border-radius: 2px;">ROUTINE</span>
            </div>
            <div style="font-size: 11px; color: #64748B; margin-top: 2px;">Requester: Karan Johar Ltd &bull; Re-Survey Request</div>
        </div>
    """)
    if st.button("⚡ Initialize Terrestrial Scan (IT Park)", key="btn_lidar_2", use_container_width=True):
        st.session_state["lidar_mission_msg"] = "Phase II, IT Park: Terrestrial scanner active. Volumetric point density computing."
        st.rerun()

    if st.session_state.get("lidar_mission_msg"):
        st.info(f"📡 {st.session_state['lidar_mission_msg']}")

def render_figma_viewer_topbar(prop_data):
    """Compact property summary header for 3D Cadastre."""
    name = prop_data.get('name', 'Sky Heights - Block A')
    city = prop_data.get('city', 'Pune')
    state = prop_data.get('state', 'Maharashtra')
    prop_id = prop_data.get('property_id', 101)

    render_html(f"""
        <div style="background: #FFFFFF; border: 1px solid #CBD5E1; border-radius: 4px; padding: 10px 16px; margin-bottom: 8px; display: flex; justify-content: space-between; align-items: center;">
            <div style="display: flex; align-items: center; gap: 10px;">
                <span style="font-size: 15px; font-weight: 700; color: #0B3C5D;">{name}</span>
                <span style="color: #64748B; font-size: 12px;">({city}, {state})</span>
                <span style="font-family: 'Consolas', monospace; font-size: 11px; color: #0B3C5D; background: #F1F5F9; border: 1px solid #CBD5E1; padding: 1px 6px; border-radius: 3px;">
                    Parcel ID: #{prop_id}
                </span>
            </div>
            <div style="font-size: 12px; color: #138808; font-weight: 600;">
                ✓ Verified 3D Cadastre Record
            </div>
        </div>
    """)

def render_figma_viewer_left_panel(prop_data, active_floor_name="Residential Floor 04"):
    """Compact metadata dossier panel."""
    render_property_spec_card(prop_data, theme="light")

def render_header(theme="light"):
    render_figma_navbar(active_view="overview")


# -------------------------------------------------------------
# 6. OFFICIAL GOVERNMENT OF INDIA & NIC FOOTER
# -------------------------------------------------------------
def render_government_footer():
    """
    Renders official GIGW 3.0 Indian Government Footer with frosted glassmorphism:
    NIC logo, Ministry of Rural Development, Copyright, Disclaimer, Accessibility.
    """
    render_html(f"""
        <div class="glass-footer" style="margin-top: 40px; border-top: 3.5px solid #E06D10; background: rgba(7, 37, 59, 0.92); backdrop-filter: blur(20px); -webkit-backdrop-filter: blur(20px); color: #CBD5E1; padding: 28px 24px; font-size: 12px; line-height: 1.6; border-radius: 16px 16px 0 0; box-shadow: 0 -8px 32px rgba(0, 0, 0, 0.25);">
            <div style="max-width: 1360px; margin: 0 auto; display: flex; flex-wrap: wrap; justify-content: space-between; gap: 24px; align-items: flex-start;">
                
                <div style="max-width: 520px;">
                    <div style="font-weight: 700; color: #FFFFFF; font-size: 14px; margin-bottom: 4px;">
                        Department of Land Resources &bull; भूमि संसाधन विभाग
                    </div>
                    <div style="color: #94A3B8; font-size: 11px;">
                        Ministry of Rural Development, Government of India &bull; ग्रामीण विकास मंत्रालय, भारत सरकार
                    </div>
                    <div style="color: #94A3B8; font-size: 11px; margin-top: 8px; line-height: 1.5;">
                        Website Content Managed by Department of Land Resources. Designed, Developed and Hosted by <b>National Informatics Centre (NIC)</b>. Standardized under ISO 19152 Land Administration Domain Model (LADM).
                    </div>
                </div>

                <div>
                    <div style="font-weight: 700; color: #FFFFFF; font-size: 12px; margin-bottom: 6px;">
                        महत्वपूर्ण लिंक / Quick Links
                    </div>
                    <div style="display: flex; flex-direction: column; gap: 4px; font-size: 11px; color: #CBD5E1;">
                        <span>&bull; Terms & Conditions (नियम व शर्तें)</span>
                        <span>&bull; Privacy Policy (गोपनीयता नीति)</span>
                        <span>&bull; Hyperlinking Policy (हाइपरलिंकिंग नीति)</span>
                        <span>&bull; Accessibility Statement (सुलभता वक्तव्य)</span>
                    </div>
                </div>

                <div style="text-align: right;">
                    <div style="display: flex; justify-content: flex-end; align-items: center; gap: 8px; margin-bottom: 6px;">
                        {ICONS_SVG['nic_logo']}
                        <span style="font-weight: 700; color: #FFFFFF; font-size: 11px;">National Informatics Centre</span>
                    </div>
                    <div style="color: #94A3B8; font-size: 11px;">
                        Guidelines for Indian Government Websites (GIGW 3.0) Compliant
                    </div>
                    <div style="color: #64748B; font-size: 10px; margin-top: 4px;">
                        Last Reviewed / Updated: 2026 &bull; National Cadastre Portal v2.6
                    </div>
                </div>

            </div>
        </div>
    """)
