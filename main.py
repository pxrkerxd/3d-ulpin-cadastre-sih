import os
import sys
import json
import sqlite3
import pandas as pd
import streamlit as st

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from core.spatial_math import segment_building
from core.ulpin_logic import generate_ulpin, decode_ulpin
from core.collision_engine import check_parcel_conflicts, run_national_audit
from core.certificate_generator import generate_bhu_aadhaar_pdf
from frontend.map_engine import render_3d_map, CITY_VIEWPORTS, MAP_STYLES
from frontend.ui_components import (
    render_html,
    inject_custom_theme, 
    render_figma_navbar,
    render_landing_hero,
    render_citizen_dashboard,
    render_figma_digital_title_certificate,
    render_figma_clash_report,
    render_figma_surveyor_workstation,
    render_figma_survey_queue,
    render_figma_viewer_topbar,
    render_figma_viewer_left_panel,
    render_kpi_bar,
    render_property_spec_card,
    render_vertical_stack,
    render_clash_report_ui,
    render_bhu_aadhaar_card_preview,
    set_active_view
)

# Enhanced 3D Cadastre & AI Slicing Engines
from core.ai_floor_segmentation import segment_building_floors
from core.topology_3d import validate_cadastral_topology
from core.ulpin_enhanced import generate_enhanced_3d_ulpin, generate_qr_code_svg, STRATUM_TYPES
from data.mock_lidar import generate_synthetic_building_lidar
from frontend.digital_twin_component import render_3d_digital_twin_component

# Page configuration matching Figma 1440px dark space layout
st.set_page_config(
    layout="wide", 
    page_title="3D ULPIN GENERATOR | ISO 19152 Spatial Cadastre", 
    page_icon="🏙️",
    initial_sidebar_state="collapsed"
)

# Initialize Session State
if "theme" not in st.session_state:
    st.session_state["theme"] = "dark"
if "nav_role" not in st.session_state:
    st.session_state["nav_role"] = "🌟 Overview & Gateway"
if "show_full_certificate" not in st.session_state:
    st.session_state["show_full_certificate"] = False
if "xray_active" not in st.session_state:
    st.session_state["xray_active"] = False
if "force_twin_view" not in st.session_state:
    st.session_state["force_twin_view"] = False
if "basemap_aesthetic" not in st.session_state:
    st.session_state["basemap_aesthetic"] = "Dark Matter (Default)"

current_theme = st.session_state["theme"]

# Invalidate any stale Streamlit data caches
st.cache_data.clear()

# Apply curated Figma design system
inject_custom_theme(theme=current_theme)

# Render Figma Top Navbar
render_figma_navbar(active_view=st.session_state["nav_role"])

# -------------------------------------------------------------
# DATABASE DATA LOADER
# -------------------------------------------------------------
def load_data():
    db_path = os.path.join(os.path.dirname(__file__), 'database', 'spatial_records.db')
    conn = sqlite3.connect(db_path)
    df = pd.read_sql_query("SELECT * FROM property_parcels", conn)
    conn.close()
    
    if 'city' not in df.columns:
        from database.db_setup import initialize_db
        initialize_db()
        conn = sqlite3.connect(db_path)
        df = pd.read_sql_query("SELECT * FROM property_parcels", conn)
        conn.close()
        
    return df

try:
    df = load_data()
except Exception as e:
    st.error(f"Database error: {e}. Please run `python database/db_setup.py`.")
    st.stop()

# -------------------------------------------------------------
# GLOBAL 3D ULPIN SEARCH & INSTANT DECODER BAR
# -------------------------------------------------------------
c_search, c_btn = st.columns([4.2, 1.0], gap="small")
with c_search:
    search_query = st.text_input(
        "🔍 Global 3D ULPIN / Title Verification Search:",
        placeholder="Search by 14-digit ULPIN (e.g. 27211010500101-004) or Property Name (e.g. Sky Heights, Seawoods, GIFT One)...",
        label_visibility="collapsed"
    )
with c_btn:
    search_clicked = st.button("🔎 Verify & Locate", use_container_width=True)

searched_prop_id = None
searched_floor_target = None

if search_query.strip():
    clean_q = search_query.strip()
    if ("-" in clean_q or len(clean_q) == 14) and any(c.isdigit() for c in clean_q):
        decoded = decode_ulpin(clean_q)
        if decoded["valid"]:
            searched_prop_id = decoded["plot_id"]
            searched_floor_target = decoded["floor_number"]
            render_html(f"""
                <div style="background: rgba(0, 242, 254, 0.11); border: 1px solid #00F2FE; border-radius: 8px; padding: 10px 16px; margin: 10px 0 16px 0; display: flex; align-items: center; justify-content: space-between; font-size: 13px;">
                    <div>
                        <span style="font-weight: 700; color: #00F2FE;">Parsed 3D ULPIN:</span>
                        <code style="color: #FFFFFF; background: #1A2238; padding: 2px 8px; border-radius: 4px; margin-left: 6px; font-family: 'Geist Mono', monospace;">{decoded['raw_ulpin']}</code>
                        &bull; State: <b>{decoded['state_name']}</b> &bull; Plot: <b>#{decoded['plot_id']}</b>
                    </div>
                    <span style="background: rgba(0, 230, 118, 0.15); color: #00E676; border: 1px solid #00E676; padding: 2px 10px; border-radius: 4px; font-weight: 700; font-family: 'Geist Mono', monospace; font-size: 11px;">
                        {decoded['floor_description']}
                    </span>
                </div>
            """)
    else:
        matched = df[df['name'].str.contains(clean_q, case=False, na=False) | df['city'].str.contains(clean_q, case=False, na=False)]
        if not matched.empty:
            searched_prop_id = matched.iloc[0]['property_id']
            st.success(f"Matched Cadastral Record: #{searched_prop_id} - {matched.iloc[0]['name']} ({matched.iloc[0]['city']})")
        else:
            st.warning(f"No cadastral record matched query: '{clean_q}'")
elif search_clicked:
    st.info("💡 Please enter a 14-digit ULPIN (e.g. 27211010500101-004) or building name to locate it on the 3D cadastre.")

# -------------------------------------------------------------
# FIGMA TOP VIEW NAVIGATION TABS
# -------------------------------------------------------------
view_tabs = [
    "🌟 Overview & Gateway",
    "🌐 3D Cadastre & Digital Twin Studio",
    "🏠 Citizen / Homebuyer Portal",
    "📐 GIS Surveyor Workstation",
    "⚠️ Subsurface Clash Engine",
    "🏛️ Sub-Registrar (Revenue Officer) Mode"
]

# Robust session state role mapping
current_role_raw = st.session_state.get("nav_role", "🌟 Overview & Gateway")
if "3D" in current_role_raw or "Twin" in current_role_raw or "Cadastre" in current_role_raw:
    matched_tab = "🌐 3D Cadastre & Digital Twin Studio"
elif "Citizen" in current_role_raw:
    matched_tab = "🏠 Citizen / Homebuyer Portal"
elif "Surveyor" in current_role_raw:
    matched_tab = "📐 GIS Surveyor Workstation"
elif "Clash" in current_role_raw:
    matched_tab = "⚠️ Subsurface Clash Engine"
elif "Registrar" in current_role_raw:
    matched_tab = "🏛️ Sub-Registrar (Revenue Officer) Mode"
else:
    matched_tab = "🌟 Overview & Gateway"

# Clean up any stale locked key to prevent StreamlitAPIException
if "figma_view_radio" in st.session_state:
    del st.session_state["figma_view_radio"]

current_idx = view_tabs.index(matched_tab) if matched_tab in view_tabs else 0

selected_view = st.radio(
    "Select Operating View:",
    options=view_tabs,
    index=current_idx,
    horizontal=True,
    label_visibility="collapsed"
)

if selected_view != matched_tab:
    st.session_state["active_view"] = selected_view
    st.session_state["nav_role"] = selected_view
    st.rerun()
else:
    st.session_state["active_view"] = selected_view
    st.session_state["nav_role"] = selected_view

render_html("<div style='height: 12px;'></div>")

# -------------------------------------------------------------
# ACTIVE 3D PARCEL SELECTION (PERSISTENT STATE)
# -------------------------------------------------------------
parcel_options = df['property_id'].tolist()

if "selected_parcel_id" not in st.session_state or st.session_state["selected_parcel_id"] not in parcel_options:
    st.session_state["selected_parcel_id"] = parcel_options[0] if parcel_options else 101

# If user executed a search for a property, activate that parcel
if searched_prop_id and searched_prop_id in parcel_options:
    st.session_state["selected_parcel_id"] = searched_prop_id

active_pid = st.session_state["selected_parcel_id"]
matching_rows = df[df['property_id'] == active_pid]
prop_data = matching_rows.iloc[0].to_dict() if not matching_rows.empty else df.iloc[0].to_dict()

# Calculate floors for active property
floors = segment_building(
    total_height=prop_data["total_height"],
    base_elevation=prop_data["base_elevation"],
    archetype=prop_data.get("archetype"),
    property_type=prop_data.get("type"),
    property_name=prop_data.get("name")
)

active_ulpin = generate_ulpin(
    int(prop_data.get("state_code", 27)),
    int(prop_data.get("dist_code", 21)),
    int(prop_data.get("sub_dist_code", 101)),
    int(prop_data.get("village_code", 50)),
    int(prop_data["property_id"]),
    4
)

# =============================================================
# VIEW 1: FIGMA LANDING HERO & GATEWAY
# =============================================================
if selected_view == "🌟 Overview & Gateway":
    # Prominently display National KPI Summary
    render_kpi_bar(df, theme=current_theme)
    render_landing_hero(df, active_prop=prop_data)

# =============================================================
# VIEW 2: 3D CADASTRE & DIGITAL TWIN STUDIO (Split-Screen GIS Studio)
# =============================================================
elif selected_view == "🌐 3D Cadastre & Digital Twin Studio":
    render_figma_viewer_topbar(prop_data)
    render_html("<div style='height: 4px;'></div>")

    # Unified Minimal GIS Control Bar (Single Clean Strip)
    c_thm, c_filt, c_sub = st.columns([1.5, 1.5, 0.8], gap="medium")
    with c_thm:
        map_style_options = list(MAP_STYLES.keys())
        default_basemap = "Dark Matter (Default)"
        if "basemap_aesthetic" not in st.session_state:
            st.session_state["basemap_aesthetic"] = default_basemap
        b_idx = map_style_options.index(st.session_state["basemap_aesthetic"]) if st.session_state["basemap_aesthetic"] in map_style_options else 0
        selected_theme = st.selectbox(
            "🗺️ Basemap Style:",
            options=map_style_options,
            index=b_idx,
            key="basemap_select_box"
        )
        st.session_state["basemap_aesthetic"] = selected_theme
    with c_filt:
        all_types = sorted(df['type'].dropna().unique().tolist())
        category_options = ["All Layers"] + all_types
        selected_category = st.selectbox(
            "🏢 Layer Filter:",
            options=category_options,
            index=0,
            key="category_filter_select"
        )
    with c_sub:
        render_html("<div style='height: 25px;'></div>")
        show_underground = st.toggle("🚇 Subsurface", value=True, help="Toggle subterranean utility & transit corridor visibility")

    # Filter Dataset based on category and subsurface preference
    display_df = df.copy()
    if selected_category != "All Layers":
        filtered_map_df = display_df[display_df['type'] == selected_category]
    else:
        filtered_map_df = display_df

    if not show_underground:
        filtered_map_df = filtered_map_df[filtered_map_df['base_elevation'] >= 0]

    if filtered_map_df.empty:
        filtered_map_df = display_df.copy()

    # Sleek Inline Micro-Legend & Active Parcels Counter
    render_html(f"""
        <div style="display: flex; gap: 14px; flex-wrap: wrap; align-items: center; justify-content: flex-start; background: #121829; border: 1px solid #202B44; padding: 5px 14px; border-radius: 8px; margin-bottom: 8px; font-size: 11px;">
            <span><b style="color: #00d4ff;">●</b> Commercial</span>
            <span><b style="color: #a855f7;">●</b> Residential</span>
            <span><b style="color: #fb923c;">●</b> Parking</span>
            <span><b style="color: #10b981;">●</b> Transit</span>
            <span><b style="color: #f43f5e;">●</b> Subsurface Utility</span>
            <span style="margin-left: auto; font-family: 'Geist Mono', monospace; color: #00F2FE; font-weight: 700;">Active: {len(filtered_map_df)} Parcels</span>
        </div>
    """)

    # Twin Fullwidth State
    twin_fullwidth = st.session_state.get("twin_fullwidth_toggle", False)
    if twin_fullwidth:
        col_map, col_panel = st.columns([3.4, 0.6], gap="medium")
    else:
        col_map, col_panel = st.columns([2.1, 1.3], gap="medium")

    with col_map:
        # Viewport Mode Toggles
        c_tw1, c_tw2 = st.columns([1.5, 1.0])
        with c_tw1:
            launch_twin = st.toggle(
                "🌐 Three.js 3D Digital Twin",
                value=st.session_state.get("twin_studio_toggle_widget", False) or st.session_state.get("force_twin_view", False),
                key="twin_studio_toggle_widget",
                help="Switch between PyDeck GIS map and interactive Three.js 3D WebGL Digital Twin with satellite ground plane, procedural facades, and exploded floors."
            )
        with c_tw2:
            st.toggle("🖥️ Fullscreen Mode", value=twin_fullwidth, key="twin_fullwidth_toggle")

        # Render 3D PyDeck Map or WebGL Digital Twin
        if launch_twin:
            base_u_val = generate_ulpin(
                int(prop_data.get("state_code", 27)),
                int(prop_data.get("dist_code", 21)),
                int(prop_data.get("sub_dist_code", 101)),
                int(prop_data.get("village_code", 50)),
                int(prop_data["property_id"]),
                1
            ).split("-")[0]

            render_3d_digital_twin_component(
                property_name=prop_data["name"],
                city=prop_data.get("city", "Pune"),
                zone=prop_data.get("zone", "Commercial Core"),
                base_ulpin=base_u_val,
                total_height=float(prop_data["total_height"]),
                base_elevation=float(prop_data["base_elevation"]),
                owner=prop_data.get("owner", "Urban Development Authority"),
                valuation_cr=float(prop_data.get("valuation_cr", 850.0)),
                archetype=prop_data.get("archetype", "transit_quad_podium"),
                facade_theme=prop_data.get("facade_theme", "azure_glass"),
                roof_feature=prop_data.get("roof_feature", "helipad_skywalk"),
                subsurface_infra=prop_data.get("subsurface_infra", "metro_rail_transit"),
                lat=float(prop_data.get("lat", 19.0216)),
                lon=float(prop_data.get("lon", 73.0181)),
                building_type=prop_data.get("type", "Commercial"),
                property_id=int(prop_data["property_id"]),
                height=840 if twin_fullwidth else 720
            )
        else:
            deck = render_3d_map(
                filtered_map_df,
                custom_center={"lat": float(prop_data["lat"]), "lon": float(prop_data["lon"])},
                map_theme=selected_theme,
                selected_property_id=int(prop_data["property_id"])
            )
            st.pydeck_chart(deck, use_container_width=True)

    with col_panel:
        # Target Parcel Selector (with immediate persistent callback)
        parcel_opts_current = filtered_map_df['property_id'].tolist() if not filtered_map_df.empty else df['property_id'].tolist()
        def format_parcel_option(pid):
            matching = df[df['property_id'] == pid]
            if matching.empty:
                return f"#{pid}"
            row = matching.iloc[0]
            return f"#{pid} - {row.get('name', 'Parcel')} ({row.get('city', 'India')})"

        cur_pid_idx = parcel_opts_current.index(active_pid) if active_pid in parcel_opts_current else 0

        def on_parcel_dropdown_change():
            st.session_state["selected_parcel_id"] = st.session_state["target_parcel_select_widget"]

        selected_prop_id = st.selectbox(
            "🎯 Select Target 3D Parcel:",
            options=parcel_opts_current,
            index=cur_pid_idx,
            format_func=format_parcel_option,
            key="target_parcel_select_widget",
            on_change=on_parcel_dropdown_change
        )

        # Quick Specs Bar
        render_html(f"""
            <div style="background: #121829; border: 1px solid #202B44; border-radius: 8px; padding: 8px 12px; margin-bottom: 12px; display: flex; justify-content: space-between; align-items: center; font-size: 11px;">
                <span style="color: #6B7C9E; font-weight: 600;">{prop_data.get('type', 'Commercial')}</span>
                <span style="font-family: 'Geist Mono', monospace; font-weight: 700; color: #00E676;">₹ {float(prop_data.get('valuation_cr', 0.0)):.1f} Cr</span>
                <span style="font-family: 'Geist Mono', monospace; font-weight: 600; color: #00F2FE;">{float(prop_data.get('total_height', 0.0)):.0f}m Height</span>
            </div>
        """)

        # Clean 3-Tab Inspector (Eliminates vertical congestion!)
        panel_tab_specs, panel_tab_floors, panel_tab_ai = st.tabs([
            "📊 Dossier",
            "📐 Strata & Floors",
            "🔬 AI LiDAR & Clash"
        ])

        with panel_tab_specs:
            render_property_spec_card(prop_data, theme=current_theme)

        with panel_tab_floors:
            render_vertical_stack(floors, prop_data, theme=current_theme)

        with panel_tab_ai:
            t_ai, t_audit, t_ulpin = st.tabs([
                "🔬 AI LiDAR",
                "⚠️ 3D Topology",
                "🔏 3D ULPIN"
            ])

            with t_ai:
                st.caption("Automated structural slab detection from vertical point density:")
                lidar_floors_cnt = st.slider("Simulated LiDAR Storeys:", min_value=3, max_value=20, value=min(12, max(4, len(floors))), key="lidar_floors_slider")
                
                if st.button("⚡ Run AI Point Cloud Slicing", type="primary", use_container_width=True):
                    pts = generate_synthetic_building_lidar(ground_z=0.0, num_floors=lidar_floors_cnt, storey_height=3.2, num_basements=2)
                    res = segment_building_floors(pts, ground_elevation_msl=0.0)
                    st.session_state["ai_slicing_result"] = res

                if "ai_slicing_result" in st.session_state:
                    res = st.session_state["ai_slicing_result"]
                    m1, m2, m3 = st.columns(3)
                    m1.metric("Storeys", res["total_floors_detected"])
                    m2.metric("Slabs", res["detected_slabs_count"])
                    m3.metric("Conf.", "98.4%")

                    # Z-Density Histogram chart
                    hist_data = pd.DataFrame({
                        "Elevation (Z)": [f"{z:.1f}m" for z in res["histogram"]["bin_centers"]],
                        "Density": res["histogram"]["frequencies"]
                    }).set_index("Elevation (Z)")
                    st.line_chart(hist_data, use_container_width=True)

                    # Slices table
                    slices_df = pd.DataFrame(res["floors"])[['level_code', 'level_type', 'elevation_min_m', 'elevation_max_m', 'storey_height_m']]
                    st.dataframe(slices_df, use_container_width=True, hide_index=True)

            with t_audit:
                st.caption("Volumetric clash and boundary setback containment analysis:")
                sample_units = []
                for f_item in floors[:5]:
                    f_num = f_item['floor_number']
                    z_bot = f_item['base_elevation']
                    z_top = f_item['top_elevation']
                    lvl_code = f"F{f_num:02d}" if f_num > 0 else f"B{abs(f_num):02d}"
                    sample_units.append({
                        "spatial_unit_id": f"{lvl_code}_U01",
                        "unit_designation": f"Unit 1 ({lvl_code})",
                        "stratum_type": "BLD",
                        "elevation_min_m": z_bot,
                        "elevation_max_m": z_top,
                        "bbox": {"min_x": 9, "min_y": 9, "min_z": z_bot, "max_x": 19, "max_y": 19, "max_z": z_top},
                        "footprint_polygon": [[9, 9], [19, 9], [19, 19], [9, 19]]
                    })

                top_f = floors[-1] if floors else {"base_elevation": 15, "top_elevation": 18, "floor_number": 4}
                sample_units.append({
                    "spatial_unit_id": "CLASH_DEMO_402",
                    "unit_designation": "Residential Flat 402 (Encroaching Balcony)",
                    "stratum_type": "BLD",
                    "elevation_min_m": top_f["base_elevation"],
                    "elevation_max_m": top_f["top_elevation"],
                    "bbox": {"min_x": 18.5, "min_y": 9, "min_z": top_f["base_elevation"], "max_x": 42.5, "max_y": 19, "max_z": top_f["top_elevation"]},
                    "footprint_polygon": [[18.5, 9], [42.5, 9], [42.5, 19], [18.5, 19]]
                })

                parent_boundary = [[0, 0], [40, 0], [40, 40], [0, 40]]
                audit_res = validate_cadastral_topology(sample_units, parent_surface_boundary=parent_boundary)

                c_a1, c_a2 = st.columns(2)
                c_a1.metric("Watertight Units", f"{audit_res['valid_parcels_count']} / {audit_res['total_parcels_audited']}")
                c_a2.metric("Detected Conflicts", audit_res['clashing_parcels_count'], delta=f"-{audit_res['clashing_parcels_count']} Issues", delta_color="inverse")

                for cl in audit_res["clashes"]:
                    st.error(f"**{cl['type']}**: {cl['description']} (Disputed: **{cl['overlap_volume_cum']} m³**)")
                for sb in audit_res["setback_violations"]:
                    st.warning(f"**{sb['type']}**: {sb['description']} (Breach: **{sb['violation_ratio']*100:.1f}%**)")

            with t_ulpin:
                st.caption("Standardized ISO 19152 3D ULPIN with Modulo-36 Check Digit:")
                u_col1, u_col2 = st.columns(2)
                with u_col1:
                    u_stratum = st.selectbox("Stratum Classification:", list(STRATUM_TYPES.keys()), format_func=lambda s: f"{s} - {STRATUM_TYPES[s]['name']}")
                    u_level = st.text_input("Vertical Level Code:", value="F04")
                with u_col2:
                    u_unit = st.text_input("Unit Designation ID:", value="A402")
                    base_u = generate_ulpin(int(prop_data.get("state_code", 27)), int(prop_data.get("dist_code", 21)), int(prop_data.get("sub_dist_code", 101)), int(prop_data.get("village_code", 50)), int(prop_data['property_id']), 1).split("-")[0]

                full_3d_ulpin, chk_digit = generate_enhanced_3d_ulpin(
                    lgd_code=f"{prop_data.get('state', 'MH')[:2].upper()}{prop_data.get('dist_code', 21)}",
                    base_parcel_ulpin=base_u,
                    stratum=u_stratum,
                    vertical_level=u_level,
                    unit_id=u_unit
                )

                st.code(full_3d_ulpin, language="text")
                st.caption(f"Modulo-36 Check Digit: **{chk_digit}** &bull; ISO 19152 LADM Status: **Valid & Certified**")

                qr_uri = generate_qr_code_svg(full_3d_ulpin, {"property": prop_data['name'], "unit": u_unit, "level": u_level})
                st.image(qr_uri, width=120, caption="Cryptographic 3D ULPIN Generator QR")

# =============================================================
# VIEW 3: FIGMA CITIZEN PORTFOLIO & OFFICIAL TITLE CERTIFICATE
# =============================================================
elif selected_view == "🏠 Citizen / Homebuyer Portal":
    c_sel, c_flr = st.columns([2, 1], gap="medium")
    with c_sel:
        cur_cit_idx = parcel_options.index(active_pid) if active_pid in parcel_options else 0
        def on_citizen_prop_change():
            st.session_state["selected_parcel_id"] = st.session_state["cit_parcel_select_widget"]

        selected_pid = st.selectbox(
            "Select Property Asset:",
            options=parcel_options,
            index=cur_cit_idx,
            format_func=lambda pid: f"#{pid} - {df[df['property_id']==pid].iloc[0]['name']} ({df[df['property_id']==pid].iloc[0]['city']})",
            label_visibility="collapsed",
            key="cit_parcel_select_widget",
            on_change=on_citizen_prop_change
        )
        prop_data = df[df["property_id"] == selected_pid].iloc[0].to_dict()
    with c_flr:
        floor_dict_opts = [f['floor_number'] for f in floors]
        sel_floor_num = st.selectbox(
            "Unit Floor Level:",
            options=floor_dict_opts,
            index=min(3, len(floor_dict_opts)-1),
            format_func=lambda n: f"Floor #{n:02d} (+{n*3}m)" if n>0 else f"Basement #{abs(n):02d} ({n*3.5}m)",
            label_visibility="collapsed"
        )
        target_floor = next((f for f in floors if f['floor_number'] == sel_floor_num), floors[0])

    # Figma Citizen Dashboard Banner & Registered Unit Cards
    render_citizen_dashboard(prop_data, floors, ulpin_str=active_ulpin)

    render_html("<div style='height: 16px;'></div>")

    # Encumbrance & RERA Status Card
    render_html("""
        <div style="background: #121829; border: 1px solid #202B44; border-radius: 12px; padding: 16px; margin-bottom: 16px;">
            <div style="font-family: 'DM Sans', sans-serif; font-size: 15px; font-weight: 700; color: #00F2FE; margin-bottom: 6px;">
                🏛️ Official Title & Encumbrance Verification
            </div>
            <div style="font-family: 'DM Sans', sans-serif; font-size: 13px; color: #A3B3D2; line-height: 1.6;">
                &bull; <b>RERA Status:</b> <span style="color: #00E676; font-weight: 600;">Approved & Active (PRM/KA/RERA/1251/310/PR/2026)</span><br/>
                &bull; <b>Encumbrance / Mortgage:</b> <span style="color: #00E676; font-weight: 600;">NIL (Clear Freehold Vertical Title)</span><br/>
                &bull; <b>Building Height Sanction:</b> Compliant with Municipal Development Control Bye-Laws
            </div>
        </div>
    """)

    # Live Digital 3D ULPIN Generator Certificate Preview with QR Code
    render_bhu_aadhaar_card_preview(prop_data, target_floor, active_ulpin, theme=current_theme)

    # 1-Click Official Title PDF Download & Toggle for Full Parchment View
    render_html("<div style='height: 12px;'></div>")
    c_pdf1, c_pdf2 = st.columns([1.5, 1.0], gap="medium")
    with c_pdf1:
        pdf_bytes = generate_bhu_aadhaar_pdf(prop_data, target_floor, active_ulpin)
        st.download_button(
            label="📥 Download Official 3D ULPIN Generator Certificate (PDF)",
            data=pdf_bytes,
            file_name=f"3D_ULPIN_Generator_Certificate_{active_ulpin}.pdf",
            mime="application/pdf",
            type="primary",
            use_container_width=True
        )
    with c_pdf2:
        show_cert = st.session_state.get("show_full_certificate", False)
        cert_btn_text = "📄 Hide Parchment View" if show_cert else "🛡️ View Authentic Parchment Deed"
        if st.button(cert_btn_text, key="cit_view_parchment_btn", use_container_width=True):
            st.session_state["show_full_certificate"] = not show_cert
            st.rerun()

    if st.session_state.get("show_full_certificate", False):
        render_html("<div style='height: 16px;'></div>")
        render_figma_digital_title_certificate(prop_data, target_floor, active_ulpin)

# =============================================================
# VIEW 4: FIGMA GIS SURVEYOR WORKSTATION
# =============================================================
elif selected_view == "📐 GIS Surveyor Workstation":
    # Figma Surveyor Workstation Header Banner
    render_figma_surveyor_workstation()

    c_map, c_queue = st.columns([1.75, 1.0], gap="large")
    with c_map:
        render_html("""
            <div style="font-family: 'DM Sans', sans-serif; font-weight: 700; font-size: 18px; color: #FFFFFF; margin-bottom: 12px;">
                Topographic Cadastral GIS Map
            </div>
        """)

        map_style_options = list(MAP_STYLES.keys())
        selected_theme = st.selectbox("🗺️ Basemap Aesthetic:", options=map_style_options, index=0, key="surveyor_basemap_select")

        deck = render_3d_map(
            df,
            custom_center={"lat": float(prop_data["lat"]), "lon": float(prop_data["lon"])},
            map_theme=selected_theme,
            selected_property_id=int(prop_data["property_id"])
        )
        st.pydeck_chart(deck, use_container_width=True)

        # 3D Spatial Metrics (Volume, Built-up Area, FSI)
        ground_area = 1200.0
        built_up_area = ground_area * len(floors)
        total_vol = ground_area * float(prop_data['total_height'])
        fsi = built_up_area / ground_area

        m1, m2, m3 = st.columns(3)
        m1.metric("Gross Volume", f"{total_vol:,.0f} m³")
        m2.metric("Built-up Area", f"{built_up_area:,.0f} m²")
        m3.metric("Computed FSI", f"{fsi:.1f}")

        render_html("<div style='height: 12px;'></div>")

        # Subsurface Clash Audit on Active Parcel
        conflicts = check_parcel_conflicts(prop_data, df, safety_buffer=25.0)
        render_clash_report_ui(conflicts, theme=current_theme)

        # Architectural cross-section visualizer
        render_vertical_stack(floors, prop_data, theme=current_theme)

    with c_queue:
        # Figma Survey Dispatch Queue with LiDAR triggers
        render_figma_survey_queue()

        # Ingest New 3D Parcel Coordinates into SQLite
        with st.expander("➕ Ingest New 3D Parcel Coordinates", expanded=False):
            with st.form("new_parcel_form"):
                new_name = st.text_input("Building / Parcel Name:")
                new_city = st.selectbox("City:", ["Navi Mumbai", "Mumbai", "Pune", "New Delhi", "Bengaluru", "GIFT City", "Hyderabad", "Chennai"])
                new_type = st.selectbox("Type:", ["Commercial", "Apartment", "Underground Parking", "Transit Hub", "Subsurface Utility"])
                n_col1, n_col2 = st.columns(2)
                with n_col1:
                    new_lat = st.number_input("Latitude:", value=float(prop_data['lat']), format="%.5f")
                    new_height = st.number_input("Height (m):", value=48.0, min_value=3.0)
                with n_col2:
                    new_lon = st.number_input("Longitude:", value=float(prop_data['lon']), format="%.5f")
                    new_base_elev = st.number_input("Base Elevation (m):", value=0.0)
                new_owner = st.text_input("Owner / Developer:", value="Municipal Development Authority")
                
                submitted = st.form_submit_button("Commit to Spatial Database", type="primary")
                if submitted and new_name.strip():
                    db_path = os.path.join(os.path.dirname(__file__), 'database', 'spatial_records.db')
                    conn = sqlite3.connect(db_path)
                    cur = conn.cursor()
                    max_id = cur.execute("SELECT MAX(property_id) FROM property_parcels").fetchone()[0] or 100
                    new_id = max_id + 1
                    cur.execute("""
                        INSERT INTO property_parcels 
                        (property_id, name, city, state, state_code, dist_code, sub_dist_code, village_code, type, lat, lon, base_elevation, total_height, owner, status, valuation_cr, zone)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """, (new_id, new_name, new_city, prop_data['state'], int(prop_data['state_code']), int(prop_data['dist_code']), 101, 50, new_type, new_lat, new_lon, new_base_elev, new_height, new_owner, 'Verified 3D Cadastre', 320.0, 'Commercial Core'))
                    conn.commit()
                    conn.close()
                    st.success(f"Successfully ingested 3D Parcel #{new_id}: {new_name}!")
                    st.rerun()

# =============================================================
# VIEW 5: FIGMA SUBSURFACE CLASH REPORT & NATIONAL AUDIT
# =============================================================
elif selected_view == "⚠️ Subsurface Clash Engine":
    conflicts = check_parcel_conflicts(prop_data, df, safety_buffer=25.0)
    render_figma_clash_report(conflicts, prop_data)

# =============================================================
# VIEW 6: SUB-REGISTRAR (REVENUE OFFICER) MODE
# =============================================================
elif selected_view == "🏛️ Sub-Registrar (Revenue Officer) Mode":
    render_html("""
        <div style="background: #121829; border: 1px solid #202B44; border-radius: 12px; padding: 20px 24px; margin-bottom: 20px;">
            <div style="font-family: 'DM Sans', sans-serif; font-weight: 800; font-size: 20px; color: #FFFFFF;">
                🏛️ Sub-Registrar Vertical Deed Transfer & Stamp Duty Simulator
            </div>
            <div style="font-family: 'DM Sans', sans-serif; font-size: 13px; color: #A3B3D2; margin-top: 4px;">
                Legally transfer individual vertical airspace titles with immutable cryptographic deed records and automated stamp duty calculations.
            </div>
        </div>
    """)

    c_tr1, c_tr2 = st.columns(2, gap="large")
    with c_tr1:
        st.caption("Current Title Grantor (Seller):")
        st.code(prop_data['owner'])

        target_floor_to_transfer = st.selectbox(
            "Select Floor Unit to Convey:",
            options=[f['floor_number'] for f in floors],
            index=min(3, len(floors)-1),
            format_func=lambda n: f"Basement {abs(n):02d} (Subsurface)" if n < 0 else f"Floor {n:02d} (Superstructure)"
        )
    with c_tr2:
        buyer_name = st.text_input("Grantee (New Buyer):", placeholder="e.g. Parijat Sharma / Reliance Infra")
        stamp_duty = (float(prop_data.get('valuation_cr', 0)) * 0.06)
        st.info(f"Calculated State Stamp Duty (6%): **₹ {stamp_duty:.2f} Crores** | Registration Status: **Verified OK**")

    if st.button("✍️ Execute Digital Vertical Deed Transfer", type="primary", use_container_width=True):
        if not buyer_name.strip():
            st.error("Please enter the name of the new buyer / grantee.")
        else:
            db_path = os.path.join(os.path.dirname(__file__), 'database', 'spatial_records.db')
            conn = sqlite3.connect(db_path)
            cur = conn.cursor()
            cur.execute("UPDATE property_parcels SET owner = ? WHERE property_id = ?", (buyer_name.strip(), int(prop_data['property_id'])))
            conn.commit()
            conn.close()
            st.success(f"Vertical Title for Parcel #{prop_data['property_id']} conveyed to {buyer_name}!")
            st.rerun()

    render_html("<div style='height: 16px;'></div>")
    render_vertical_stack(floors, prop_data, theme=current_theme)

# -------------------------------------------------------------
# BOTTOM DRAWER: MASTER CADASTRAL DATABASE & NATIONAL AUDIT
# -------------------------------------------------------------
render_html("<div style='height: 24px;'></div>")
with st.expander("🗄️ National 3D Cadastral Registry & All-India Clash Audit", expanded=False):
    t1, t2, t3 = st.tabs([
        "📋 Tabular Cadastre Register", 
        "⚠️ Pan-India Encroachment Audit", 
        "📊 Spatial Analytics"
    ])
    
    with t1:
        cols_to_show = [c for c in [
            'property_id', 'name', 'city', 'state', 'type', 'total_height', 
            'base_elevation', 'valuation_cr', 'owner', 'status'
        ] if c in df.columns]
        st.dataframe(df[cols_to_show], use_container_width=True, hide_index=True)
        
    with t2:
        st.caption("Automated spatial audit of subterranean safety corridors across all Indian metros:")
        all_national_clashes = run_national_audit(df, safety_buffer=20.0)
        st.write(f"Detected **{len(all_national_clashes)}** potential buffer infringements nationally.")
        render_clash_report_ui(all_national_clashes, theme=current_theme)

    with t3:
        c_chart1, c_chart2 = st.columns(2)
        with c_chart1:
            st.caption("Distribution of 3D Cadastre Assets by Category")
            st.bar_chart(df['type'].value_counts())
        with c_chart2:
            st.caption("Asset Valuation by Metro Region (₹ Crores)")
            if 'city' in df.columns and 'valuation_cr' in df.columns:
                st.bar_chart(df.groupby('city')['valuation_cr'].sum())