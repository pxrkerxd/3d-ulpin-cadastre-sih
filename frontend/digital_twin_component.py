"""
Interactive 3D WebGL Digital Twin & Cadastral Operations Component for Streamlit.
Renders the complete 3D ULPIN Generator platform inside Streamlit matching the official UI:
- Top Header with brand, 4 operational tabs, CORS RTK status
- Left Floating Glassmorphism Controls: Exploded Floor Slider, Subsurface X-Ray Slider, Camera Presets, Strata Checkboxes
- Interactive Three.js WebGL 3D scene (Surface, Apartments, Basements, Metro Tunnel, Water Mains, Air Rights)
- Right Inspection Card with 3D ULPIN, ISO 19152 LADM metadata, QR code, and 3D ULPIN Generator Title Deed Modal
- AI Floor Slicing Studio with Chart.js LiDAR Z-Density Histogram
- 3D Topology Audit & Clash Detection Center
"""

import json
import streamlit.components.v1 as components

def render_3d_digital_twin_component(
    property_name="Seawoods Grand Central",
    city="Navi Mumbai",
    zone="Commercial Core",
    base_ulpin="27211010500101",
    total_height=120,
    base_elevation=0,
    owner="L&T Realty & Seawoods Corp",
    valuation_cr=850.0,
    height=860,
    archetype="transit_quad_podium",
    facade_theme="azure_glass",
    roof_feature="helipad_skywalk",
    subsurface_infra="metro_rail_transit",
    lat=19.0216,
    lon=73.0181,
    building_type="Commercial",
    property_id=101,
    **kwargs
):
    """
    Renders procedural, real-world-accurate 3D architectural digital twins inside Streamlit.
    """
    archetype_title = archetype.replace("_", " ").title()
    elev_str = f"Depth: {base_elevation}m to {base_elevation + total_height}m" if base_elevation < 0 else f"+{total_height}m MSL"

    building_meta_json = json.dumps({
        "id": property_id,
        "name": property_name,
        "city": city,
        "zone": zone,
        "base_ulpin": base_ulpin,
        "total_height": total_height,
        "base_elevation": base_elevation,
        "owner": owner,
        "valuation_cr": valuation_cr,
        "archetype": archetype,
        "facade_theme": facade_theme,
        "roof_feature": roof_feature,
        "subsurface_infra": subsurface_infra,
        "lat": lat,
        "lon": lon,
        "building_type": building_type
    })

    html_code = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
      <meta charset="utf-8">
      <meta name="viewport" content="width=device-width, initial-scale=1.0">
      <title>3D ULPIN Generator - {property_name}</title>
      
      <!-- Tailwind CSS -->
      <script src="https://cdn.tailwindcss.com"></script>
      <!-- Lucide Icons -->
      <script src="https://unpkg.com/lucide@latest"></script>
      <!-- Three.js, OrbitControls, Loaders & Exporters -->
      <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
      <script src="https://cdn.jsdelivr.net/npm/three@0.128.0/examples/js/controls/OrbitControls.js"></script>
      <script src="https://cdn.jsdelivr.net/npm/three@0.128.0/examples/js/loaders/GLTFLoader.js"></script>
      <script src="https://cdn.jsdelivr.net/npm/three@0.128.0/examples/js/loaders/OBJLoader.js"></script>
      <script src="https://cdn.jsdelivr.net/npm/three@0.128.0/examples/js/exporters/GLTFExporter.js"></script>
      <!-- Chart.js for LiDAR Histogram -->
      <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>

      <style>
        :root {{
          --primary: #0B3C5D;
          --primary-hover: #082C44;
          --dark-bg: #0A1120;
          --card-bg: #FFFFFF;
          --border-color: rgba(255, 255, 255, 0.6);
        }}
        * {{ margin: 0; padding: 0; box-sizing: border-box; font-family: 'Noto Sans', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; }}
        body {{ 
          background: radial-gradient(at 0% 0%, rgba(56, 189, 248, 0.12) 0px, transparent 50%), radial-gradient(at 100% 100%, rgba(14, 165, 233, 0.10) 0px, transparent 50%), #0A1120; 
          color: #0F172A; 
          overflow: hidden; 
          height: 100vh; 
          width: 100vw; 
          display: flex; 
          flex-direction: column; 
        }}
        
        /* Universal Glassmorphic Base */
        .glass {{
          background: rgba(255, 255, 255, 0.78);
          backdrop-filter: blur(20px) saturate(180%);
          -webkit-backdrop-filter: blur(20px) saturate(180%);
          border: 1.5px solid rgba(255, 255, 255, 0.85);
          box-shadow: 0 12px 36px rgba(11, 60, 93, 0.15), inset 0 1px 2px rgba(255, 255, 255, 0.95);
          border-radius: 14px;
        }}

        /* Top App Header (Frosted Glass) */
        header {{
          display: flex;
          align-items: center;
          justify-content: space-between;
          padding: 6px 18px;
          height: 46px;
          background: rgba(255, 255, 255, 0.82);
          backdrop-filter: blur(20px) saturate(180%);
          -webkit-backdrop-filter: blur(20px) saturate(180%);
          border-bottom: 1.5px solid rgba(255, 255, 255, 0.75);
          box-shadow: 0 4px 20px rgba(11, 60, 93, 0.08), inset 0 1px 1px rgba(255, 255, 255, 0.95);
          z-index: 50;
          gap: 10px;
          overflow: hidden;
          white-space: nowrap;
        }}
        .emblem-badge {{
          background: linear-gradient(135deg, #0B3C5D 0%, #0369A1 100%);
          color: #FFFFFF;
          font-weight: 700;
          font-size: 11px;
          padding: 4px 10px;
          border-radius: 6px;
          letter-spacing: 0.5px;
          flex-shrink: 0;
          box-shadow: 0 2px 8px rgba(11, 60, 93, 0.25);
        }}
        .nav-tabs {{
          display: flex;
          gap: 3px;
          background: rgba(241, 245, 249, 0.7);
          backdrop-filter: blur(10px);
          -webkit-backdrop-filter: blur(10px);
          padding: 3px;
          border-radius: 8px;
          border: 1px solid rgba(203, 213, 225, 0.8);
          flex-shrink: 1;
        }}
        .tab-btn {{
          background: transparent;
          border: none;
          color: #475569;
          padding: 5px 12px;
          border-radius: 6px;
          font-size: 11px;
          font-weight: 600;
          cursor: pointer;
          transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
          display: flex;
          align-items: center;
          gap: 5px;
          white-space: nowrap;
        }}
        .tab-btn:hover {{ color: #0B3C5D; background: rgba(255, 255, 255, 0.8); }}
        .tab-btn.active {{ 
          background: #0B3C5D; 
          color: #FFFFFF; 
          box-shadow: 0 2px 8px rgba(11, 60, 93, 0.3);
        }}
        
        .badge-cors {{
          display: flex;
          align-items: center;
          gap: 6px;
          font-size: 10px;
          background: rgba(240, 253, 244, 0.8);
          backdrop-filter: blur(8px);
          -webkit-backdrop-filter: blur(8px);
          color: #138808;
          padding: 4px 10px;
          border-radius: 6px;
          border: 1px solid rgba(187, 247, 208, 0.85);
          box-shadow: 0 2px 6px rgba(19, 136, 8, 0.1);
          flex-shrink: 0;
        }}
        .pulse-dot {{
          width: 7px;
          height: 7px;
          background-color: #138808;
          border-radius: 50%;
          box-shadow: 0 0 8px #138808;
        }}

        /* Workspace */
        .workspace {{ display: flex; flex: 1; position: relative; overflow: hidden; }}
        #webgl-container {{ flex: 1; width: 100%; height: 100%; position: relative; outline: none; }}

        /* Floating Dedicated Government Bottom Toolbar (Glassmorphic Pill) */
        .gov-bottom-toolbar {{
          position: absolute;
          bottom: 16px;
          left: 50%;
          transform: translateX(-50%);
          z-index: 35;
          display: flex;
          gap: 8px;
          background: rgba(255, 255, 255, 0.80);
          backdrop-filter: blur(24px) saturate(180%);
          -webkit-backdrop-filter: blur(24px) saturate(180%);
          padding: 8px 18px;
          border-radius: 9999px;
          border: 1.5px solid rgba(255, 255, 255, 0.9);
          box-shadow: 0 14px 40px rgba(11, 60, 93, 0.22), inset 0 1px 2px rgba(255, 255, 255, 0.95);
          align-items: center;
          justify-content: center;
          flex-wrap: wrap;
        }}
        .gov-tb-btn {{
          background: rgba(241, 245, 249, 0.8);
          backdrop-filter: blur(8px);
          -webkit-backdrop-filter: blur(8px);
          border: 1px solid rgba(203, 213, 225, 0.85);
          color: #0B3C5D;
          font-size: 11px;
          font-weight: 700;
          padding: 6px 14px;
          border-radius: 9999px;
          cursor: pointer;
          display: flex;
          align-items: center;
          gap: 5px;
          transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
          white-space: nowrap;
          box-shadow: 0 2px 6px rgba(0, 0, 0, 0.04);
        }}
        .gov-tb-btn:hover {{
          background: #0B3C5D;
          color: #FFFFFF;
          border-color: #0B3C5D;
          transform: translateY(-1px);
          box-shadow: 0 4px 14px rgba(11, 60, 93, 0.35);
        }}
        .gov-tb-btn.active {{
          background: #0B3C5D;
          color: #FFFFFF;
          border-color: #07253B;
          box-shadow: 0 3px 10px rgba(11, 60, 93, 0.4);
        }}

        /* Floating Left Sidebar (Glassmorphic) */
        .left-controls {{
          position: absolute;
          top: 10px;
          left: 10px;
          width: 255px;
          max-height: calc(100vh - 68px);
          overflow-y: auto;
          border-radius: 16px;
          padding: 14px;
          z-index: 20;
          display: flex;
          flex-direction: column;
          gap: 10px;
          background: rgba(255, 255, 255, 0.84);
          backdrop-filter: blur(24px) saturate(180%);
          -webkit-backdrop-filter: blur(24px) saturate(180%);
          color: #0F172A;
          border: 1.5px solid rgba(255, 255, 255, 0.9);
          box-shadow: 0 16px 48px rgba(11, 60, 93, 0.16), inset 0 1px 2px rgba(255, 255, 255, 0.95);
          transition: transform 0.25s cubic-bezier(0.4, 0, 0.2, 1), opacity 0.2s;
        }}
        .left-controls::-webkit-scrollbar {{ width: 3px; }}
        .left-controls::-webkit-scrollbar-thumb {{ background: #CBD5E1; border-radius: 3px; }}
        .left-controls.collapsed {{
          transform: translateX(-115%);
          opacity: 0;
          pointer-events: none;
        }}

        /* Floating Button to re-open Controls */
        .btn-toggle-left {{
          position: absolute;
          top: 10px;
          left: 10px;
          z-index: 22;
          background: rgba(11, 60, 93, 0.9);
          backdrop-filter: blur(14px);
          -webkit-backdrop-filter: blur(14px);
          border: 1.5px solid rgba(255, 255, 255, 0.35);
          color: #FFFFFF;
          padding: 7px 14px;
          border-radius: 9999px;
          font-size: 11px;
          font-weight: 700;
          cursor: pointer;
          display: flex;
          align-items: center;
          gap: 6px;
          box-shadow: 0 4px 16px rgba(11, 60, 93, 0.35);
          transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
        }}
        .btn-toggle-left:hover {{
          background: #07253B;
          transform: translateY(-1px);
          box-shadow: 0 6px 20px rgba(7, 37, 59, 0.45);
        }}
        .btn-toggle-left.visible {{
          display: flex;
        }}

        .panel-title {{
          font-size: 11px;
          font-weight: 700;
          text-transform: uppercase;
          letter-spacing: 0.5px;
          color: #64748B;
          display: flex;
          justify-content: space-between;
          align-items: center;
        }}

        input[type="range"] {{
          -webkit-appearance: none;
          width: 100%;
          height: 6px;
          border-radius: 4px;
          background: rgba(203, 213, 225, 0.6);
          outline: none;
        }}
        input[type="range"]::-webkit-slider-thumb {{
          -webkit-appearance: none;
          width: 16px;
          height: 16px;
          border-radius: 50%;
          background: var(--primary);
          border: 2px solid #FFFFFF;
          cursor: pointer;
          box-shadow: 0 2px 6px rgba(11, 60, 93, 0.4);
        }}

        .camera-grid {{
          display: grid;
          grid-template-columns: 1fr 1fr;
          gap: 6px;
        }}
        .camera-btn {{
          background: rgba(241, 245, 249, 0.7);
          backdrop-filter: blur(8px);
          -webkit-backdrop-filter: blur(8px);
          border: 1px solid rgba(203, 213, 225, 0.8);
          color: #0F172A;
          padding: 6px 8px;
          border-radius: 8px;
          font-size: 11px;
          font-weight: 600;
          cursor: pointer;
          transition: all 0.2s;
          text-align: center;
        }}
        .camera-btn:hover {{ 
          background: #0B3C5D; 
          border-color: #0B3C5D; 
          color: #FFFFFF; 
          box-shadow: 0 2px 8px rgba(11, 60, 93, 0.25);
        }}

        .strata-item {{
          display: flex;
          align-items: center;
          justify-content: space-between;
          font-size: 12px;
          padding: 6px 8px;
          border-radius: 8px;
          background: rgba(248, 250, 252, 0.65);
          border: 1px solid rgba(226, 232, 240, 0.7);
          cursor: pointer;
          transition: all 0.15s;
        }}
        .strata-item:hover {{ 
          background: rgba(255, 255, 255, 0.9); 
          border-color: #38bdf8; 
          box-shadow: 0 2px 6px rgba(0, 0, 0, 0.04);
        }}

        /* Floating Right Inspection Card (Frosted Dark Glass) */
        .right-drawer {{
          position: absolute;
          top: 10px;
          right: 10px;
          width: 265px;
          max-height: calc(100vh - 68px);
          overflow-y: auto;
          border-radius: 16px;
          padding: 14px;
          z-index: 25;
          display: none;
          flex-direction: column;
          gap: 10px;
          background: rgba(15, 23, 42, 0.84);
          backdrop-filter: blur(24px) saturate(190%);
          -webkit-backdrop-filter: blur(24px) saturate(190%);
          border: 1.5px solid rgba(56, 189, 248, 0.35);
          box-shadow: 0 16px 48px rgba(0, 0, 0, 0.65), inset 0 1px 1px rgba(255, 255, 255, 0.12);
          animation: slideInRight 0.25s cubic-bezier(0.4, 0, 0.2, 1);
        }}
        .right-drawer::-webkit-scrollbar {{ width: 3px; }}
        .right-drawer::-webkit-scrollbar-thumb {{ background: rgba(255, 255, 255, 0.2); border-radius: 3px; }}
        @keyframes slideInRight {{
          from {{ transform: translateX(20px); opacity: 0; }}
          to {{ transform: translateX(0); opacity: 1; }}
        }}

        .ulpin-box {{
          background: rgba(30, 41, 59, 0.72);
          backdrop-filter: blur(12px);
          -webkit-backdrop-filter: blur(12px);
          border: 1px solid rgba(56, 189, 248, 0.4);
          border-radius: 10px;
          padding: 10px;
          display: flex;
          flex-direction: column;
          gap: 4px;
          box-shadow: 0 4px 14px rgba(0, 0, 0, 0.3);
        }}
        .ulpin-code {{
          font-family: monospace;
          font-weight: 700;
          font-size: 12px;
          color: #38bdf8;
          word-break: break-all;
          text-shadow: 0 0 12px rgba(56, 189, 248, 0.4);
        }}

        .metrics-grid {{
          display: grid;
          grid-template-columns: 1fr 1fr;
          gap: 6px;
          font-size: 11px;
        }}
        .metric-tile {{
          background: rgba(255, 255, 255, 0.05);
          backdrop-filter: blur(8px);
          -webkit-backdrop-filter: blur(8px);
          border: 1px solid rgba(255, 255, 255, 0.08);
          padding: 7px;
          border-radius: 8px;
        }}
        .metric-tile .lbl {{ font-size: 9px; color: #94a3b8; text-transform: uppercase; }}
        .metric-tile .val {{ font-size: 12px; font-weight: 700; color: #f8fafc; }}

        .btn-primary {{
          background: linear-gradient(135deg, #0284C7 0%, #0369A1 100%);
          backdrop-filter: blur(10px);
          -webkit-backdrop-filter: blur(10px);
          color: #ffffff;
          border: 1px solid rgba(255, 255, 255, 0.3);
          padding: 9px 14px;
          border-radius: 10px;
          font-size: 12px;
          font-weight: 700;
          cursor: pointer;
          transition: all 0.2s;
          display: flex;
          align-items: center;
          justify-content: center;
          gap: 6px;
          box-shadow: 0 4px 14px rgba(2, 132, 199, 0.4), inset 0 1px 0 rgba(255, 255, 255, 0.25);
        }}
        .btn-primary:hover {{ 
          background: linear-gradient(135deg, #0369A1 0%, #0284C7 100%);
          transform: translateY(-1px);
          box-shadow: 0 6px 18px rgba(2, 132, 199, 0.5);
        }}

        /* Modal (Frosted Glassmorphism) */
        .modal-overlay {{
          position: fixed;
          top: 0; left: 0; width: 100vw; height: 100vh;
          background: rgba(7, 11, 20, 0.74);
          backdrop-filter: blur(20px) saturate(180%);
          -webkit-backdrop-filter: blur(20px) saturate(180%);
          display: none;
          align-items: center;
          justify-content: center;
          z-index: 100;
        }}
        .modal-overlay.open {{ display: flex; }}
        .cert-sheet {{
          background: rgba(255, 255, 255, 0.92);
          backdrop-filter: blur(26px);
          -webkit-backdrop-filter: blur(26px);
          color: #1e293b;
          border: 3.5px solid rgba(2, 132, 199, 0.6);
          border-radius: 20px;
          padding: 28px;
          max-width: 750px;
          width: 90%;
          max-height: 85vh;
          overflow-y: auto;
          box-shadow: 0 24px 64px rgba(0, 0, 0, 0.45), inset 0 1px 2px rgba(255, 255, 255, 0.95);
        }}
      </style>
    </head>
    <body>
      <!-- Header -->
      <header>
        <div class="flex items-center gap-2 min-w-0">
          <div class="emblem-badge">GOI 3D CADASTRE</div>
          <div class="truncate">
            <div class="flex items-center gap-1.5">
              <h1 class="font-bold text-xs tracking-tight text-slate-800 truncate max-w-[200px]" title="{property_name}">{property_name}</h1>
              <span class="text-[10px] text-amber-600 font-mono font-bold hidden sm:inline">[{building_type}]</span>
            </div>
            <p class="text-[10px] text-slate-500 truncate hidden md:block">{city} &bull; {zone} &bull; {elev_str}</p>
          </div>
        </div>

        <!-- Center Tabs -->
        <div class="nav-tabs">
          <button class="tab-btn active" id="tab-twin" onclick="switchView('twin')">
            <i data-lucide="box" class="w-3 h-3"></i> 3D Twin
          </button>
          <button class="tab-btn" id="tab-gen" onclick="switchView('gen')">
            <i data-lucide="qr-code" class="w-3 h-3"></i> 3D ULPIN
          </button>
          <button class="tab-btn" id="tab-ai" onclick="switchView('ai')">
            <i data-lucide="cpu" class="w-3 h-3"></i> AI Slicing
          </button>
          <button class="tab-btn" id="tab-topo" onclick="switchView('topo')">
            <i data-lucide="shield-alert" class="w-3 h-3"></i> Audit
          </button>
        </div>

        <!-- Right CORS Status -->
        <div class="flex items-center gap-2">
          <div class="badge-cors" title="rtcm.surveyofindia.gov.in:2101">
            <div class="pulse-dot"></div>
            <span class="font-mono text-[9px] font-bold">CORS RTK ACTIVE</span>
          </div>
        </div>
      </header>

      <!-- Main Workspace -->
      <div class="workspace">
        
        <!-- Toggle button to restore left sidebar when collapsed -->
        <button id="btn-show-controls" class="btn-toggle-left visible" onclick="toggleLeftControls()" title="Open Controls Menu">
          <i data-lucide="sliders" class="w-3.5 h-3.5"></i>
          <span>Layers & Sliders</span>
        </button>

        <!-- Left Sidebar Controls (Collapsed by default for visual priority on 3D twin) -->
        <aside class="left-controls glass collapsed" id="left-sidebar">
          
          <!-- Top bar with Collapse button -->
          <div class="flex items-center justify-between pb-1 border-b border-slate-200">
            <span class="text-[10px] font-bold text-slate-700 uppercase tracking-wider flex items-center gap-1.5">
              <i data-lucide="sliders" class="w-3 h-3"></i> Controls Panel
            </span>
            <button onclick="toggleLeftControls()" class="text-slate-600 hover:text-slate-900 px-1.5 py-0.5 rounded hover:bg-slate-100 text-[10px] flex items-center gap-1 border border-slate-300" title="Collapse Menu to clear 3D view">
              <span>Hide</span>
              <i data-lucide="chevron-left" class="w-3 h-3"></i>
            </button>
          </div>
          
          <!-- Search Bar -->
          <div class="flex gap-1.5">
            <input type="text" id="inp-search" placeholder="Search Unit (e.g. 402)..." class="w-full bg-slate-900/80 border border-white/10 rounded-md px-2 py-1 text-[11px] text-white placeholder-slate-400 outline-none focus:border-sky-500">
            <button onclick="searchParcel()" class="bg-sky-600 hover:bg-sky-500 text-white px-2 py-1 rounded-md text-[11px] font-semibold">
              <i data-lucide="search" class="w-3 h-3"></i>
            </button>
          </div>

          <!-- VIEW 1: 3D Twin Controls -->
          <div id="ctrl-twin-group" class="flex flex-col gap-3">
            <!-- Exploded View Slider -->
            <div>
              <div class="panel-title">
                <span>EXPLODED FLOOR VIEW</span>
                <span class="text-sky-400 font-mono" id="lbl-explode">0%</span>
              </div>
              <input type="range" id="rng-explode" min="0" max="1" step="0.02" value="0">
              <div class="flex justify-between text-[9px] text-slate-400 mt-1">
                <span>Compact</span>
                <span>Expanded Storeys</span>
              </div>
            </div>

            <!-- Subsurface X-Ray Slider -->
            <div>
              <div class="panel-title">
                <span>SUBSURFACE X-RAY MODE</span>
                <span class="text-sky-400 font-mono" id="lbl-xray">100%</span>
              </div>
              <input type="range" id="rng-xray" min="0.1" max="1" step="0.05" value="1">
              <div class="flex justify-between text-[9px] text-slate-400 mt-1">
                <span>Deep Subsurface</span>
                <span>Solid Facade</span>
              </div>
            </div>

            <!-- Camera Presets -->
            <div>
              <div class="panel-title mb-1.5">CAMERA PRESETS</div>
              <div class="camera-grid">
                <button class="camera-btn" onclick="setCam('iso')">3D Isometric</button>
                <button class="camera-btn" onclick="setCam('top')">2D Top Ortho</button>
                <button class="camera-btn" onclick="setCam('sub')">Subsurface Look-up</button>
                <button class="camera-btn" onclick="setCam('front')">Front Elevation</button>
              </div>
            </div>

            <!-- Strata Layers -->
            <div>
              <div class="panel-title mb-1.5">CADASTRAL STRATA LAYERS</div>
              <div class="flex flex-col gap-1">
                <label class="strata-item">
                  <div class="flex items-center gap-2">
                    <span class="w-2.5 h-2.5 rounded bg-emerald-500"></span>
                    <span>Surface Land Parcels (SUR)</span>
                  </div>
                  <input type="checkbox" checked onchange="toggleLayer('SUR', this.checked)">
                </label>
                <label class="strata-item">
                  <div class="flex items-center gap-2">
                    <span class="w-2.5 h-2.5 rounded bg-blue-500"></span>
                    <span>Building Units / Flats (BLD)</span>
                  </div>
                  <input type="checkbox" checked onchange="toggleLayer('BLD', this.checked)">
                </label>
                <label class="strata-item">
                  <div class="flex items-center gap-2">
                    <span class="w-2.5 h-2.5 rounded bg-purple-500"></span>
                    <span>Common Circulation (COM)</span>
                  </div>
                  <input type="checkbox" checked onchange="toggleLayer('COM', this.checked)">
                </label>
                <label class="strata-item">
                  <div class="flex items-center gap-2">
                    <span class="w-2.5 h-2.5 rounded bg-amber-500"></span>
                    <span>Basements & Parking (SUB)</span>
                  </div>
                  <input type="checkbox" checked onchange="toggleLayer('SUB', this.checked)">
                </label>
                <label class="strata-item">
                  <div class="flex items-center gap-2">
                    <span class="w-2.5 h-2.5 rounded bg-pink-500"></span>
                    <span>Metro & Utility Mains (UTL)</span>
                  </div>
                  <input type="checkbox" checked onchange="toggleLayer('UTL', this.checked)">
                </label>
                <label class="strata-item">
                  <div class="flex items-center gap-2">
                    <span class="w-2.5 h-2.5 rounded bg-cyan-500"></span>
                    <span>Elevated Air Rights (AIR)</span>
                  </div>
                  <input type="checkbox" checked onchange="toggleLayer('AIR', this.checked)">
                </label>
              </div>
            </div>
          </div>

          <!-- VIEW 2: 3D ULPIN Generator Tab -->
          <div id="ctrl-gen-group" class="flex-col gap-2 text-xs" style="display: none;">
            <div class="font-bold text-slate-200 border-b border-white/10 pb-1">Generate 3D ULPIN</div>
            <div>
              <label class="text-slate-400 text-[10px]">Stratum Type:</label>
              <select id="gen-strat" class="w-full bg-slate-900 border border-white/10 rounded px-2 py-1 text-white text-xs">
                <option value="BLD">BLD (Building Unit)</option>
                <option value="SUB">SUB (Basement Parking)</option>
                <option value="COM">COM (Common Circulation)</option>
                <option value="UTL">UTL (Subsurface Utility)</option>
                <option value="AIR">AIR (Elevated Air Rights)</option>
              </select>
            </div>
            <div class="grid grid-cols-2 gap-2">
              <div>
                <label class="text-slate-400 text-[10px]">Level Code:</label>
                <input type="text" id="gen-lvl" value="F04" class="w-full bg-slate-900 border border-white/10 rounded px-2 py-1 text-white font-mono">
              </div>
              <div>
                <label class="text-slate-400 text-[10px]">Unit ID:</label>
                <input type="text" id="gen-uid" value="A402" class="w-full bg-slate-900 border border-white/10 rounded px-2 py-1 text-white font-mono">
              </div>
            </div>
            <button onclick="executeGenerateULPIN()" class="btn-primary mt-1">Generate & Sign 3D ULPIN</button>
            <div id="gen-res" class="ulpin-box mt-2" style="display:none;">
              <span class="text-[9px] text-emerald-400 font-bold">CERTIFIED 3D ULPIN</span>
              <span id="gen-out" class="ulpin-code text-xs"></span>
              <span class="text-[10px] text-slate-300">Modulo-36 Check Digit: <b id="gen-chk" class="text-amber-400"></b></span>
            </div>
          </div>

          <!-- VIEW 3: AI Floor Slicing Tab -->
          <div id="ctrl-ai-group" class="flex-col gap-2" style="display: none;">
            <div class="font-bold text-slate-200 border-b border-white/10 pb-1 text-xs">AI LiDAR Floor Slicing</div>
            <p class="text-[10px] text-slate-400">Point cloud density peak detection automatically separates structural floor slabs.</p>
            <div class="w-full h-36 bg-slate-900 rounded p-1.5 border border-white/5">
              <canvas id="lidar-chart"></canvas>
            </div>
            <button onclick="recalculateAI()" class="btn-primary text-xs py-1.5 mt-1">Re-Run AI Slicing Pipeline</button>
            <div class="text-[10px] text-emerald-400 font-semibold mt-1">✓ 8 Slabs Detected with 98.4% Confidence</div>
          </div>

          <!-- VIEW 4: 3D Topology Audit Tab -->
          <div id="ctrl-topo-group" class="flex-col gap-2 text-xs" style="display: none;">
            <div class="flex justify-between items-center border-b border-white/10 pb-1">
              <span class="font-bold text-slate-200">3D Topology Audit</span>
              <button onclick="toggleClashHighlight()" class="bg-red-600 hover:bg-red-500 text-white text-[10px] px-2 py-0.5 rounded font-bold">Highlight Clashes</button>
            </div>
            <div class="bg-red-950/40 border border-red-500/30 p-2 rounded text-[11px] text-red-200">
              <b>⚠️ 1 Volumetric Clash Detected</b><br/>
              Unit 402 encroaches into public airspace by 48.0 m³.
            </div>
            <div class="bg-amber-950/40 border border-amber-500/30 p-2 rounded text-[11px] text-amber-200">
              <b>⚠️ 1 Setback Violation</b><br/>
              Overhanging balcony exceeds boundary by 18.5%.
            </div>
          </div>

        </aside>

        <!-- Center 3D WebGL Canvas -->
        <div id="webgl-container"></div>

        <!-- Floating Hint for User -->
        <div id="canvas-hint" class="pointer-events-none absolute bottom-2.5 left-1/2 -translate-x-1/2 z-10 bg-slate-900/80 backdrop-blur border border-white/10 text-slate-300 text-[10px] px-3 py-1 rounded-full shadow-lg flex items-center gap-1.5 whitespace-nowrap">
          <i data-lucide="mouse-pointer" class="w-3 h-3 text-sky-400"></i>
          <span>Click any 3D unit to inspect &bull; Left Drag: Rotate &bull; Scroll: Zoom</span>
        </div>

        <!-- Right Property Card Drawer -->
        <aside class="right-drawer glass" id="right-drawer">
          <div class="border-b border-white/10 pb-1.5 flex justify-between items-start">
            <div class="truncate max-w-[180px]">
              <span class="text-[8px] text-sky-400 font-bold uppercase tracking-wider">ISO 19152 Spatial Unit</span>
              <h2 class="text-xs font-bold text-white truncate mt-0.5" id="card-title">Residential Flat 402</h2>
            </div>
            <div class="flex items-center gap-1">
              <span class="text-[8px] font-bold text-emerald-400 bg-emerald-950/60 px-1.5 py-0.5 rounded" id="card-status">VERIFIED</span>
              <button onclick="closeRightDrawer()" class="text-slate-400 hover:text-white p-1 rounded hover:bg-white/10 text-xs" title="Dismiss Card">
                <i data-lucide="x" class="w-3.5 h-3.5"></i>
              </button>
            </div>
          </div>

          <div class="ulpin-box">
            <span class="text-[9px] text-slate-400 uppercase font-semibold">3D ULPIN Generator</span>
            <div class="ulpin-code" id="card-ulpin">{base_ulpin}-BLD-F04-A402-K</div>
          </div>

          <div class="metrics-grid">
            <div class="metric-tile">
              <div class="lbl">Stratum & Level</div>
              <div class="val text-sky-400" id="card-lvl">BLD (Floor 4)</div>
            </div>
            <div class="metric-tile">
              <div class="lbl">Elevation Band (Z)</div>
              <div class="val" id="card-z">12.8m - 16.0m</div>
            </div>
            <div class="metric-tile">
              <div class="lbl">Floor Area</div>
              <div class="val" id="card-area">100.0 m²</div>
            </div>
            <div class="metric-tile">
              <div class="lbl">Enclosed Volume</div>
              <div class="val" id="card-vol">320.0 m³</div>
            </div>
          </div>

          <div class="text-xs flex flex-col gap-1 text-slate-300 bg-slate-900/50 p-2.5 rounded-lg border border-white/5">
            <div><span class="text-slate-400">Owner:</span> <b class="text-white" id="card-owner">{owner}</b></div>
            <div><span class="text-slate-400">Valuation:</span> <b class="text-emerald-400" id="card-val">₹ 1.25 Cr</b></div>
            <div><span class="text-slate-400">Right Type:</span> <span>Strata Freehold Title</span></div>
          </div>

          <button onclick="openDeedModal()" class="btn-primary">
            <i data-lucide="file-text" class="w-3.5 h-3.5"></i> View Official 3D ULPIN Generator Deed
          </button>
        </aside>

        <!-- Compact Dedicated Government Bottom Toolbar -->
        <div class="gov-bottom-toolbar" id="gov-toolbar">
          <button onclick="setCam('top')" class="gov-tb-btn" title="2D Top Orthographic">📐 Top View</button>
          <button onclick="setCam('front')" class="gov-tb-btn" title="Front Elevation View">🏛️ Front View</button>
          <button onclick="setCam('iso')" class="gov-tb-btn" title="3D Isometric Perspective">🌐 3D Isometric</button>
          <button onclick="toggleExplodedCompact()" class="gov-tb-btn" id="btn-tb-explode" title="Toggle Exploded Storeys">💥 Exploded</button>
          <button onclick="toggleXrayMode()" class="gov-tb-btn" id="btn-tb-xray" title="Toggle Subsurface X-Ray">🚇 Subsurface X-Ray</button>
          <button onclick="exportModelGLB()" class="gov-tb-btn" title="Export current 3D Digital Twin as standard .GLB 3D model file">📦 Export .GLB</button>
          <label class="gov-tb-btn" style="cursor: pointer;" title="Import external 3D Model (.glb, .gltf, .obj)">
            📂 Import 3D
            <input type="file" id="inp-custom-model" accept=".glb,.gltf,.obj" style="display:none" onchange="loadCustom3DModel(event)">
          </label>
          <button onclick="resetCamGov()" class="gov-tb-btn" title="Reset Camera">🔄 Reset</button>
          <button onclick="toggleLeftControls()" class="gov-tb-btn" style="border-left: 1px solid #CBD5E1; margin-left: 4px;" title="Strata Layers & Sliders">⚙️ Layers</button>
        </div>

      </div>

      <!-- 3D ULPIN Generator Deed Modal -->
      <div class="modal-overlay" id="deed-modal">
        <div class="cert-sheet">
          <div class="text-center border-b-2 border-sky-600 pb-3 mb-4">
            <div class="text-xs font-bold text-sky-800 tracking-wider">GOVERNMENT OF INDIA • MINISTRY OF RURAL DEVELOPMENT</div>
            <div class="text-lg font-extrabold text-slate-900 mt-1">3D ULPIN GENERATOR DIGITAL RECORD OF RIGHTS (RoR)</div>
            <div class="text-xs text-slate-600">VOLUMETRIC PROPERTY OWNERSHIP PASSBOOK • ISO 19152 LADM CERTIFIED</div>
          </div>
          
          <div class="grid grid-cols-2 gap-4 text-xs mb-4">
            <div><b>3D ULPIN:</b> <span class="font-mono text-sky-900 font-bold" id="m-ulpin"></span></div>
            <div><b>Unit Designation:</b> <span id="m-name"></span></div>
            <div><b>Parent Base ULPIN:</b> <span class="font-mono">{base_ulpin}</span></div>
            <div><b>Vertical Bounds:</b> <span id="m-z"></span></div>
            <div><b>Carpet Area / Volume:</b> <span id="m-area"></span> / <span id="m-vol"></span></div>
            <div><b>Owner Title Holder:</b> <b id="m-owner"></b></div>
          </div>

          <div class="p-2 bg-slate-100 rounded text-[11px] text-slate-600 mb-4">
            Certified via National CORS Network (rtcm.surveyofindia.gov.in:2101). Zero boundary encroachments detected.
          </div>

          <div class="flex justify-between items-center pt-2 border-t border-slate-300">
            <button onclick="closeDeedModal()" class="bg-slate-700 text-white text-xs px-4 py-1.5 rounded">Close</button>
            <button onclick="window.print()" class="btn-primary text-xs py-1.5 px-4">Print Certificate</button>
          </div>
        </div>
      </div>

      <script>
        const BUILDING_DATA = {building_meta_json};
        const container = document.getElementById('webgl-container');
        let scene, camera, renderer, controls;
        const meshMap = new Map();
        let selectedMesh = null;
        let isClashActive = false;
        let currentChart = null;

        // Group definitions
        const groups = {{
          SUR: new THREE.Group(),
          BLD: new THREE.Group(),
          COM: new THREE.Group(),
          SUB: new THREE.Group(),
          UTL: new THREE.Group(),
          AIR: new THREE.Group()
        }};

        function init() {{
          const w = container.clientWidth;
          const h = container.clientHeight;

          scene = new THREE.Scene();
          scene.background = new THREE.Color(0xedf2f7);
          scene.fog = new THREE.FogExp2(0xedf2f7, 0.002);

          camera = new THREE.PerspectiveCamera(45, w / h, 0.5, 2500);
          camera.up.set(0, 0, 1);

          renderer = new THREE.WebGLRenderer({{ antialias: true, alpha: true }});
          renderer.setSize(w, h);
          renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
          renderer.shadowMap.enabled = true;
          container.appendChild(renderer.domElement);

          controls = new THREE.OrbitControls(camera, renderer.domElement);
          controls.enableDamping = true;
          controls.dampingFactor = 0.05;

          // Adaptive camera positioning based on building height and elevation
          const isSub = BUILDING_DATA.base_elevation < 0;
          const bH = Math.abs(BUILDING_DATA.total_height) || 40;
          if (isSub) {{
            camera.position.set(48, -40, -10);
            controls.target.set(20, 20, -8);
          }} else if (bH >= 180) {{
            camera.position.set(70, -65, 75);
            controls.target.set(20, 20, 28);
          }} else {{
            camera.position.set(52, -48, 50);
            controls.target.set(20, 20, 14);
          }}

          // Sun Lighting - Simulates Real-Time 10:45 AM Morning Sun Angle
          const hemiLight = new THREE.HemisphereLight(0xdbeafe, 0x1e293b, 0.85);
          scene.add(hemiLight);

          const sun = new THREE.DirectionalLight(0xfffaed, 1.25);
          sun.position.set(75, 55, 120);
          sun.castShadow = true;
          sun.shadow.mapSize.width = 2048;
          sun.shadow.mapSize.height = 2048;
          scene.add(sun);

          // Fill light for architectural facades
          const fillLight = new THREE.DirectionalLight(0x38bdf8, 0.35);
          fillLight.position.set(-50, -40, 60);
          scene.add(fillLight);

          // Real-Time High-Resolution Satellite Ground Plane (100% Free, Zero Keys)
          const groundSize = 180;
          const groundGeo = new THREE.PlaneGeometry(groundSize, groundSize);
          
          const pLat = BUILDING_DATA.lat || 19.0216;
          const pLon = BUILDING_DATA.lon || 73.0181;
          const delta = 0.0016;
          const satUrl = `https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/export?bbox=${{pLon-delta}},${{pLat-delta}},${{pLon+delta}},${{pLat+delta}}&bboxSR=4326&imageSR=4326&size=1024,1024&f=image`;

          const texLoader = new THREE.TextureLoader();
          texLoader.crossOrigin = "anonymous";
          const groundMat = new THREE.MeshStandardMaterial({{
            color: 0xffffff,
            roughness: 0.95,
            metalness: 0.05,
            side: THREE.DoubleSide
          }});

          texLoader.load(
            satUrl,
            (tex) => {{
              groundMat.map = tex;
              groundMat.needsUpdate = true;
            }},
            undefined,
            (err) => {{
              console.warn("Satellite tile load notice:", err);
            }}
          );

          const groundMesh = new THREE.Mesh(groundGeo, groundMat);
          groundMesh.position.set(20, 20, -0.05);
          groundMesh.receiveShadow = true;
          groups.SUR.add(groundMesh);

          // Cadastral Legal Boundary Outline on Ground
          const boundGeo = new THREE.RingGeometry(21.0, 21.8, 4);
          boundGeo.rotateZ(Math.PI / 4);
          const boundMat = new THREE.MeshBasicMaterial({{ color: 0x38bdf8, side: THREE.DoubleSide, transparent: true, opacity: 0.85 }});
          const boundMesh = new THREE.Mesh(boundGeo, boundMat);
          boundMesh.position.set(20, 20, 0.02);
          groups.SUR.add(boundMesh);

          // Subtle coordinate grid at Z=0.01m
          const grid = new THREE.GridHelper(groundSize, 18, 0x38bdf8, 0x334155);
          grid.rotation.x = Math.PI / 2;
          grid.position.set(20, 20, 0.01);
          grid.material.opacity = 0.20;
          grid.material.transparent = true;
          scene.add(grid);

          // Surrounding Urban Context Blocks (Disabled for clear 360-degree model viewing)
          // addSurroundingUrbanContext();

          // Axes
          const axes = new THREE.AxesHelper(15);
          axes.position.set(-5, -5, 0);
          scene.add(axes);

          // Add Groups
          Object.values(groups).forEach(g => scene.add(g));

          // Build Procedural Geometry based on real-time data
          buildProceduralDigitalTwin(BUILDING_DATA);

          // Auto-apply X-Ray if subsurface building
          if (isSub) {{
            applyXRay(0.22);
            document.getElementById('rng-xray').value = 0.22;
            document.getElementById('lbl-xray').textContent = '22%';
          }}

          // Listeners
          window.addEventListener('resize', onResize);
          renderer.domElement.addEventListener('pointerdown', onPointerDown);

          // Sliders
          document.getElementById('rng-explode').addEventListener('input', (e) => {{
            const f = parseFloat(e.target.value);
            document.getElementById('lbl-explode').textContent = Math.round(f * 100) + '%';
            applyExplode(f);
          }});

          document.getElementById('rng-xray').addEventListener('input', (e) => {{
            const f = parseFloat(e.target.value);
            document.getElementById('lbl-xray').textContent = Math.round(f * 100) + '%';
            applyXRay(f);
          }});

          // Init chart
          initChart();
          lucide.createIcons();
          animate();
        }}

        // -------------------------------------------------------------
        // PROCEDURAL ARCHITECTURAL ENGINE (Unique Real-World Models)
        // -------------------------------------------------------------
        function buildProceduralDigitalTwin(data) {{
          const arc = data.archetype || 'transit_quad_podium';

          // 1. Surface Cadastral Master Boundary (SUR)
          createPrism("SUR_01", [[0,0],[40,0],[40,40],[0,40]], -0.2, 0.2, 0x10b981, 0.35, "SUR", 0, {{
            name: `Master Cadastral Parcel (${{data.name}})`,
            ulpin: `${{data.base_ulpin}}-SUR-G00-PL01-8`,
            z: "-0.2m to +0.2m",
            area: "1600 m²",
            vol: "640 m³",
            owner: data.owner,
            val: "₹ " + data.valuation_cr + " Cr"
          }});

          // 2. Dispatch to specific architectural archetype
          if (arc === 'cyber_cylindrical_radial') {{
            buildCyberTowersRadial(data);
          }} else if (arc === 'supertall_tiered') {{
            buildSupertallTiered(data);
          }} else if (arc === 'stepped_spire_luxury') {{
            buildUBcitySteppedSpire(data);
          }} else if (arc === 'crystalline_diamond') {{
            buildDiamondTower(data);
          }} else if (arc === 'circular_heritage_rotunda') {{
            buildHeritageRotunda(data);
          }} else if (arc === 'transit_quad_podium') {{
            buildSeawoodsQuadPodium(data);
          }} else if (arc === 'skybridge_twin') {{
            buildSkybridgeTwin(data);
          }} else if (arc === 'subterranean_multilevel_cavern') {{
            buildSubterraneanCavern(data);
          }} else if (arc === 'underwater_subaqueous_tunnel') {{
            buildUnderwaterShieldTunnel(data);
          }} else if (arc === 'utility_tunnel_trench') {{
            buildUtilityTunnelTrench(data);
          }} else if (arc === 'it_linear_spine') {{
            buildLinearITSpine(data);
          }} else if (arc === 'transit_canopy_terminal' || arc === 'cable_stayed_transit_hub') {{
            buildTransitTerminalCanopy(data);
          }} else {{
            buildModernParametricTower(data);
          }}
        }}

        // ARCHETYPE 1: HITEC Cyber Towers (Hyderabad) - 10-Storey Radial 4-Quadrant Complex with Central Fountain Plaza
        function buildCyberTowersRadial(data) {{
          // 1. Signature Central Fountain Plaza at Ground (Z = 0.0 to 0.8m)
          const fGeo = new THREE.CylinderGeometry(15, 15, 0.4, 36);
          fGeo.rotateX(Math.PI / 2);
          const fMat = new THREE.MeshStandardMaterial({{ color: 0x0284c7, roughness: 0.1, transparent: true, opacity: 0.85 }});
          const fMesh = new THREE.Mesh(fGeo, fMat);
          fMesh.position.set(20, 20, 0.2);
          groups.SUR.add(fMesh);

          // Concentric Stepped Stone Rim
          const rimGeo = new THREE.RingGeometry(14.2, 15.2, 36);
          const rimMat = new THREE.MeshStandardMaterial({{ color: 0x64748b, roughness: 0.8 }});
          const rimMesh = new THREE.Mesh(rimGeo, rimMat);
          rimMesh.position.set(20, 20, 0.41);
          groups.SUR.add(rimMesh);

          // Fountain Spray Ring
          const sprayGeo = new THREE.RingGeometry(2.5, 4.2, 28);
          const sprayMat = new THREE.MeshBasicMaterial({{ color: 0xe0f2fe, side: THREE.DoubleSide }});
          const sprayMesh = new THREE.Mesh(sprayGeo, sprayMat);
          sprayMesh.position.set(20, 20, 0.42);
          groups.SUR.add(sprayMesh);

          const floorNames = [
            "Grand Tech Atrium, Central Fountain & Visitor Reception",
            "FinTech & Global Banking Digital Operations",
            "AI, Deep Learning & Autonomous Systems Labs",
            "Cloud Infrastructure & Enterprise DevOps Hub",
            "Global Software Engineering Suite - Sector North",
            "Global Software Engineering Suite - Sector South",
            "Global Offshore Delivery & Solution Architecture",
            "National Cyber Security Operations Center (SOC)",
            "Executive C-Suite, Boardroom & Panoramic Deck",
            "Cloud Incubation Accelerator & Sky Terrace"
          ];

          const techTenants = [
            "Telangana State Ind. Infra Corp (TSIIC Reception)",
            "Oracle Financial Services Software Limited",
            "Qualcomm India Private Limited",
            "Infosys Technologies Global Delivery Unit",
            "Tata Consultancy Services (TCS) Innovation Lab",
            "Cognizant Technology Solutions India",
            "Wipro Digital & Cloud Transformation",
            "National Cyber Security Operations Center (CERT-In)",
            "Cyient Global Engineering Design Hub",
            "T-Hub Cloud Incubation Accelerator & Sky Deck"
          ];

          const numFloors = 10;
          for (let f = 0; f < numFloors; f++) {{
            const zMin = f * 3.6;
            const zMax = zMin + 3.6;
            const lvl = f === 0 ? "G00" : `F0${{f}}`;
            const flrTitle = floorNames[f] || `IT Enterprise Level ${{f}}`;
            const flrOwner = techTenants[f] || `Tech Enterprise Tenant (Tier ${{f}})`;

            // Central Cylindrical Glass Drum Core (Diameter 15m)
            createCylinderPrism(`COM_${{lvl}}_DRUM`, 7.5, 7.5, zMin, zMax, 32, 0x0284c7, 0.7, "COM", f, {{
              name: `Cyber Towers Central Glass Drum (${{flrTitle}})`,
              ulpin: `${{data.base_ulpin}}-COM-${{lvl}}-DR01-C`,
              z: `${{zMin.toFixed(1)}}m to ${{zMax.toFixed(1)}}m`,
              area: "176 m²",
              vol: "633 m³",
              owner: f === 0 ? "Telangana State Ind. Infra Corp (TSIIC)" : flrOwner,
              val: "₹ 1.20 Cr"
            }});

            // 4 Radial Quadrant Wings with Distinct Geometry
            const wings = [
              {{ id: "NW", name: "North-West Wing (FinTech Quadrant)", poly: [[16, 25], [24, 25], [24, 38], [16, 38]], clr: 0x0369a1 }},
              {{ id: "SW", name: "South-West Wing (AI & Cognitive Quadrant)", poly: [[16, 2], [24, 2], [24, 15], [16, 15]], clr: 0x0284c7 }},
              {{ id: "EW", name: "East Wing (Cloud Enterprise Quadrant)", poly: [[25, 16], [38, 16], [38, 24], [25, 24]], clr: 0x38bdf8 }},
              {{ id: "WW", name: "West Wing (Incubation & Research Quadrant)", poly: [[2, 16], [15, 16], [15, 24], [2, 24]], clr: 0x0ea5e9 }}
            ];

            wings.forEach((w, wi) => {{
              const wingTenantList = [
                ["Oracle Financial Services Software", "Qualcomm India R&D", "Infosys Global Delivery", "Tata Consultancy Services"],
                ["Cognizant Digital Works", "Wipro Cloud Engineering", "Cyient Aerospace Hub", "Virtusa Global Solutions"],
                ["Microsoft Azure Innovation", "ServiceNow India Hub", "Hitachi Vantara Labs", "T-Hub DeepTech Accelerator"]
              ];
              const specificWingOwner = (wingTenantList[f % wingTenantList.length] || [])[wi] || flrOwner;
              createPrism(`BLD_${{lvl}}_${{w.id}}`, w.poly, zMin, zMax, w.clr, 0.88, "BLD", f, {{
                name: `${{w.name}} - ${{flrTitle}}`,
                ulpin: `${{data.base_ulpin}}-BLD-${{lvl}}-${{w.id}}01-H`,
                z: `${{zMin.toFixed(1)}}m to ${{zMax.toFixed(1)}}m`,
                area: "104 m²",
                vol: "374 m³",
                owner: specificWingOwner,
                val: "₹ 2.45 Cr"
              }});
            }});
          }}

          // Rooftop Circular Helipad with Markings
          const hGeo = new THREE.CylinderGeometry(8.5, 8.5, 0.4, 32);
          hGeo.rotateX(Math.PI / 2);
          const hMat = new THREE.MeshStandardMaterial({{ color: 0x1e293b, roughness: 0.8 }});
          const hMesh = new THREE.Mesh(hGeo, hMat);
          hMesh.position.set(20, 20, 36.2);
          groups.AIR.add(hMesh);

          const rGeo = new THREE.RingGeometry(5.0, 5.8, 32);
          const rMat = new THREE.MeshBasicMaterial({{ color: 0xfacc15, side: THREE.DoubleSide }});
          const rMesh = new THREE.Mesh(rGeo, rMat);
          rMesh.position.set(20, 20, 36.45);
          groups.AIR.add(rMesh);

          // White "H" Helipad Marking
          const hSymbolMat = new THREE.MeshBasicMaterial({{ color: 0xffffff }});
          const bar1 = new THREE.Mesh(new THREE.BoxGeometry(0.7, 3.4, 0.05), hSymbolMat);
          bar1.position.set(18.6, 20, 36.5);
          groups.AIR.add(bar1);
          const bar2 = new THREE.Mesh(new THREE.BoxGeometry(0.7, 3.4, 0.05), hSymbolMat);
          bar2.position.set(21.4, 20, 36.5);
          groups.AIR.add(bar2);
          const barCross = new THREE.Mesh(new THREE.BoxGeometry(2.8, 0.7, 0.05), hSymbolMat);
          barCross.position.set(20, 20, 36.5);
          groups.AIR.add(barCross);

          // Rooftop Communications Mast Spire & Flashing Aviation Light
          const mastGeo = new THREE.CylinderGeometry(0.2, 0.6, 12, 12);
          mastGeo.rotateX(Math.PI / 2);
          const mastMat = new THREE.MeshStandardMaterial({{ color: 0xe2e8f0, metalness: 0.8, roughness: 0.2 }});
          const mastMesh = new THREE.Mesh(mastGeo, mastMat);
          mastMesh.position.set(20, 20, 42.5);
          groups.AIR.add(mastMesh);

          const bcnGeo = new THREE.SphereGeometry(0.5, 12, 12);
          const bcnMat = new THREE.MeshBasicMaterial({{ color: 0xef4444 }});
          const bcnMesh = new THREE.Mesh(bcnGeo, bcnMat);
          bcnMesh.position.set(20, 20, 48.6);
          groups.AIR.add(bcnMesh);

          // Subsurface Tier-IV Data Vault & Power Grid (SUB)
          createPrism("SUB_DATA", [[5,5],[35,5],[35,35],[5,35]], -16, 0, 0xf59e0b, 0.85, "SUB", -1, {{
            name: "Cyberabad Subsurface Tier-IV Data Vault & Dual Power Substation",
            ulpin: `${{data.base_ulpin}}-SUB-B02-DV01-9`,
            z: "-16.0m to 0.0m",
            area: "900 m²",
            vol: "14400 m³",
            owner: "National Data Grid Infrastructure SPV",
            val: "₹ 620 Cr"
          }});
        }}

        // ARCHETYPE 2: Worli Sea-Facing Super-Tower (Mumbai) - Lodha World One (Pei Cobb Freed 3-Winged Cloverleaf)
        function buildSupertallTiered(data) {{
          // Real-World Pei Cobb Freed & Partners (PCF&P) "The World Towers" Architecture:
          // A soaring, aerodynamic 3-petal cloverleaf/trefoil supertall tower (280.2m MSL)
          // wrapped in signature continuous gleaming white horizontal ribbon balconies on EVERY floor,
          // with sculpted cascading setbacks, sovereign sky penthouse with ocean infinity pool,
          // glowing crystalline crown, grand arrival fountain roundabout, and companion curved towers!

          // Helper: Generates smooth 48-point 3-petal cloverleaf polygon
          function getCloverleafPolygon(cx, cy, R, lobePurity = 0.38) {{
            const pts = [];
            for (let i = 0; i < 48; i++) {{
              const theta = (Math.PI * 2 * i) / 48;
              const r = R * (1 + lobePurity * Math.cos(3 * (theta - Math.PI / 2)));
              pts.push([
                Math.round((cx + r * Math.cos(theta)) * 100) / 100,
                Math.round((cy + r * Math.sin(theta)) * 100) / 100
              ]);
            }}
            return pts;
          }}

          // Helper: Creates smooth 3D curved white wrap-around balcony ribbon
          const whiteBalconyMat = new THREE.MeshStandardMaterial({{
            color: 0xf8fafc,
            metalness: 0.85,
            roughness: 0.25
          }});

          function createBalconyRibbon(cx, cy, R, zHeight) {{
            const pts2D = getCloverleafPolygon(cx, cy, R * 1.02);
            const pts3D = pts2D.map(p => new THREE.Vector3(p[0], p[1], zHeight));
            const curve = new THREE.CatmullRomCurve3(pts3D, true);
            const tubeGeo = new THREE.TubeGeometry(curve, 48, 0.28, 8, true);
            const tubeMesh = new THREE.Mesh(tubeGeo, whiteBalconyMat);
            groups.BLD.add(tubeMesh);

            // Subtle floor slab underside trim
            const trimGeo = new THREE.TubeGeometry(curve, 48, 0.12, 6, true);
            const trimMesh = new THREE.Mesh(trimGeo, new THREE.MeshBasicMaterial({{ color: 0xe2e8f0 }}));
            trimMesh.position.z = -0.15;
            groups.BLD.add(trimMesh);
          }}

          // 1. Grand Landscaped Arrival Plaza & Water Fountain (Z = 0.0 to 1.5m)
          const plazaGeo = new THREE.BoxGeometry(40, 40, 0.2);
          const plazaMat = new THREE.MeshStandardMaterial({{ color: 0x1e293b, roughness: 0.85 }});
          const plaza = new THREE.Mesh(plazaGeo, plazaMat);
          plaza.position.set(20, 20, 0.1);
          groups.SUR.add(plaza);

          // Central Circular Stepped Water Fountain
          const fPoolGeo = new THREE.CylinderGeometry(5.2, 5.2, 0.4, 32);
          fPoolGeo.rotateX(Math.PI / 2);
          const fPoolMat = new THREE.MeshStandardMaterial({{ color: 0x0284c7, roughness: 0.08, transparent: true, opacity: 0.85 }});
          const fPool = new THREE.Mesh(fPoolGeo, fPoolMat);
          fPool.position.set(20, 5.5, 0.3);
          groups.SUR.add(fPool);

          const fRimGeo = new THREE.RingGeometry(4.8, 5.4, 32);
          const fRim = new THREE.Mesh(fRimGeo, new THREE.MeshStandardMaterial({{ color: 0x94a3b8, roughness: 0.8 }}));
          fRim.position.set(20, 5.5, 0.52);
          groups.SUR.add(fRim);

          // Fountain Central Spray Jet
          const fJetGeo = new THREE.CylinderGeometry(0.8, 1.8, 1.2, 16);
          fJetGeo.rotateX(Math.PI / 2);
          const fJet = new THREE.Mesh(fJetGeo, new THREE.MeshBasicMaterial({{ color: 0xe0f2fe }}));
          fJet.position.set(20, 5.5, 0.9);
          groups.SUR.add(fJet);

          // Ring of Royal Palm Trees around arrival roundabout
          for (let pi = 0; pi < 8; pi++) {{
            const pAngle = (Math.PI * 2 * pi) / 8;
            const px = 20 + 8.5 * Math.cos(pAngle);
            const py = 5.5 + 8.5 * Math.sin(pAngle);
            if (py > 0 && py < 12) {{
              const trunk = new THREE.Mesh(new THREE.CylinderGeometry(0.18, 0.22, 3.8, 8), new THREE.MeshStandardMaterial({{ color: 0x78350f }}));
              trunk.rotateX(Math.PI / 2);
              trunk.position.set(px, py, 1.9);
              groups.SUR.add(trunk);

              const fronds = new THREE.Mesh(new THREE.SphereGeometry(1.2, 8, 8), new THREE.MeshStandardMaterial({{ color: 0x15803d }}));
              fronds.position.set(px, py, 4.0);
              groups.SUR.add(fronds);
            }}
          }}

          // 3D Entrance Totem Monolith
          const totem = new THREE.Mesh(new THREE.BoxGeometry(1.4, 0.4, 3.2), new THREE.MeshStandardMaterial({{ color: 0x0f172a, metalness: 0.8 }}));
          totem.position.set(11, 2.5, 1.6);
          groups.SUR.add(totem);

          // 2. Triple-Height Concierge Port Cochère & Lifestyle Podium (Floors G00 - L02, Z = 0.0m to 10.0m)
          const polyG00 = getCloverleafPolygon(20, 20, 15.5);
          createPrism("BLD_PODIUM_G00", polyG00, 0, 10.0, 0x0284c7, 0.88, "BLD", 1, {{
            name: "World One Triple-Height Concierge Grand Port Cochère & Club W Podium",
            ulpin: `${{data.base_ulpin}}-BLD-P01-GR01-7`,
            z: "0.0m to +10.0m",
            area: "1080 m²",
            vol: "10800 m³",
            owner: "World One Grand Concierge & Reception Trust",
            val: "₹ 520 Cr"
          }});
          createBalconyRibbon(20, 20, 15.5, 5.0);
          createBalconyRibbon(20, 20, 15.5, 9.8);

          // Sweeping Aerodynamic Glass Canopy over Driveway
          const canopyGeo = new THREE.CylinderGeometry(9.0, 9.0, 0.35, 24, 1, false, 0, Math.PI);
          canopyGeo.rotateX(Math.PI / 2);
          const canopyMat = new THREE.MeshStandardMaterial({{ color: 0x38bdf8, roughness: 0.1, transparent: true, opacity: 0.85 }});
          const canopy = new THREE.Mesh(canopyGeo, canopyMat);
          canopy.position.set(20, 7.5, 5.8);
          groups.BLD.add(canopy);

          // HNI Resident Registry
          const residentRoster = [
            "Sh. Vikramaditya & Shweta Singhania (Industrialist Sky Villa)",
            "Dr. Radhika & Amitav Oberoi (Worli Sea Face Residence)",
            "Smt. Ananya & Rohit Narang (Arabian Sea Suite)",
            "Capt. Devendra K. Bakshi (Retd. Naval Commander)",
            "Sh. Rajeshwar & Meenakshi Sundaram (FinTech Director)",
            "Dr. Rohan & Nandini Mehta (Bandra Sea Link View)",
            "Smt. Sunita & Siddharth Agarwal (Luxury Suite)",
            "Sh. Harishchandra V. Rao (Corporate Chambers)",
            "Smt. Priya & Sanjay Nambiar (Marine Vista Residence)",
            "Sh. Jaideep & Vandana Munjal (Panoramic Sky Mansion)",
            "Sh. K. V. Subramanian (Global Equity Fund Executive)"
          ];

          // 3. Low-Rise 3-Petal Luxury Residences (Floors L03 - L06, Z = 10.0m to 28.4m, R = 14.0m)
          for (let f = 3; f <= 6; f++) {{
            const zMin = 10.0 + (f - 3) * 4.6;
            const zMax = zMin + 4.6;
            const lvl = `L0${{f}}`;
            const poly = getCloverleafPolygon(20, 20, 14.0);
            createPrism(`BLD_${{lvl}}_RESIDENCES`, poly, zMin, zMax, 0x0284c7, 0.88, "BLD", f, {{
              name: `World One 3-Petal Luxury Residences (${{lvl}})`,
              ulpin: `${{data.base_ulpin}}-BLD-${{lvl}}-TR01-A`,
              z: `+${{zMin.toFixed(1)}}m to +${{zMax.toFixed(1)}}m`,
              area: "860 m²",
              vol: "3956 m³",
              owner: residentRoster[f - 3] || `World One Title Holder (${{lvl}})`,
              val: "₹ 68.0 Cr"
            }});
            createBalconyRibbon(20, 20, 14.0, zMin + 0.2);
          }}

          // 4. Mid-Rise Tier & 1st Cascading Setback (Floors L07 - L10, Z = 28.4m to 46.8m, R = 12.2m)
          // Setback: West petal steps back into an open-air sky garden
          for (let f = 7; f <= 10; f++) {{
            const zMin = 28.4 + (f - 7) * 4.6;
            const zMax = zMin + 4.6;
            const lvl = f < 10 ? `L0${{f}}` : `L${{f}}`;
            const poly = getCloverleafPolygon(20, 20, 12.2);
            createPrism(`BLD_${{lvl}}_SIGNATURE`, poly, zMin, zMax, 0x0369a1, 0.88, "BLD", f, {{
              name: `World One Signature Panoramic Residences (${{lvl}})`,
              ulpin: `${{data.base_ulpin}}-BLD-${{lvl}}-SG01-B`,
              z: `+${{zMin.toFixed(1)}}m to +${{zMax.toFixed(1)}}m`,
              area: "650 m²",
              vol: "2990 m³",
              owner: residentRoster[f - 3] || `World One Title Holder (${{lvl}})`,
              val: "₹ 82.0 Cr"
            }});
            createBalconyRibbon(20, 20, 12.2, zMin + 0.2);
          }}

          // Sky Garden Terrace at Floor L07 Setback
          const terraceMat = new THREE.MeshStandardMaterial({{ color: 0x15803d, roughness: 0.9 }});
          const terrace = new THREE.Mesh(new THREE.BoxGeometry(4.2, 4.2, 0.2), terraceMat);
          terrace.position.set(10.5, 14.5, 28.5);
          groups.BLD.add(terrace);

          // 5. High-Rise Sky Mansions & 2nd Cascading Setback (Floors L11 - L13, Z = 46.8m to 60.6m, R = 10.4m)
          // Setback: South-East petal steps back into cantilevered sky duplexes
          for (let f = 11; f <= 13; f++) {{
            const zMin = 46.8 + (f - 11) * 4.6;
            const zMax = zMin + 4.6;
            const lvl = `L${{f}}`;
            const poly = getCloverleafPolygon(20, 20, 10.4);
            createPrism(`BLD_${{lvl}}_DUPLEX`, poly, zMin, zMax, 0x0ea5e9, 0.88, "BLD", f, {{
              name: `World One High-Rise Sky Duplex Suites (${{lvl}})`,
              ulpin: `${{data.base_ulpin}}-BLD-${{lvl}}-DX01-C`,
              z: `+${{zMin.toFixed(1)}}m to +${{zMax.toFixed(1)}}m`,
              area: "480 m²",
              vol: "2208 m³",
              owner: residentRoster[f - 3] || `World One Sky Duplex Custodian (${{lvl}})`,
              val: "₹ 110 Cr"
            }});
            createBalconyRibbon(20, 20, 10.4, zMin + 0.2);
          }}

          // 6. Sovereign Triplex Sky Palace & Penthouse with Private Ocean Plunge Pool (Floors L14 - L16, Z = 60.6m to 76.0m, R = 8.6m)
          const polyPH = getCloverleafPolygon(20, 20, 8.6);
          createPrism("BLD_SOVEREIGN_PENTHOUSE", polyPH, 60.6, 76.0, 0x06b6d4, 0.94, "BLD", 14, {{
            name: "World One Sovereign Triplex Sky Palace & Penthouse (Floors L14-L16)",
            ulpin: `${{data.base_ulpin}}-BLD-L16-PH01-P`,
            z: "+60.6m to +76.0m",
            area: "340 m²",
            vol: "5236 m³",
            owner: "Sovereign Sky Palace Family Trust (Chairman Suite)",
            val: "₹ 240 Cr"
          }});
          createBalconyRibbon(20, 20, 8.6, 65.2);
          createBalconyRibbon(20, 20, 8.6, 70.6);

          // Cantilevered Ocean Infinity Plunge Pool on North Petal
          const poolWater = new THREE.Mesh(
            new THREE.BoxGeometry(5.2, 4.2, 1.2),
            new THREE.MeshStandardMaterial({{ color: 0x0284c7, roughness: 0.05, transparent: true, opacity: 0.85 }})
          );
          poolWater.position.set(20, 28.5, 72.0);
          groups.BLD.add(poolWater);

          const poolGlass = new THREE.Mesh(
            new THREE.BoxGeometry(5.6, 0.15, 1.6),
            new THREE.MeshStandardMaterial({{ color: 0x38bdf8, transparent: true, opacity: 0.55 }})
          );
          poolGlass.position.set(20, 30.6, 72.2);
          groups.BLD.add(poolGlass);

          // 7. Sculpted Aerodynamic Crown Fins & Stainless Steel Spire (Z = 76.0m to 96.0m, 280.2m MSL)
          // Crown Tapering Fins
          const crownMat = new THREE.MeshStandardMaterial({{
            color: 0xfbbf24,
            emissive: 0xd97706,
            roughness: 0.2,
            metalness: 0.8
          }});
          for (let fi = 0; fi < 6; fi++) {{
            const fAngle = (Math.PI * 2 * fi) / 6;
            const finGeo = new THREE.BoxGeometry(0.3, 2.2, 8.0);
            const fin = new THREE.Mesh(finGeo, crownMat);
            fin.position.set(20 + 3.2 * Math.cos(fAngle), 20 + 3.2 * Math.sin(fAngle), 80.0);
            fin.rotation.z = fAngle;
            groups.AIR.add(fin);
          }}

          // Crown Spire Cone
          const spGeo = new THREE.ConeGeometry(2.4, 12, 16);
          spGeo.rotateX(Math.PI / 2);
          const spMesh = new THREE.Mesh(spGeo, crownMat);
          spMesh.position.set(20, 20, 82.0);
          groups.AIR.add(spMesh);

          // Stainless Steel Needle Mast
          const mastGeo = new THREE.CylinderGeometry(0.12, 0.35, 10, 8);
          mastGeo.rotateX(Math.PI / 2);
          const mast = new THREE.Mesh(mastGeo, new THREE.MeshStandardMaterial({{ color: 0xf8fafc, metalness: 0.95 }}));
          mast.position.set(20, 20, 91.0);
          groups.AIR.add(mast);

          // Aircraft Obstruction Warning Beacon
          const beacon = new THREE.Mesh(new THREE.SphereGeometry(0.45, 12, 12), new THREE.MeshBasicMaterial({{ color: 0xef4444 }}));
          beacon.position.set(20, 20, 96.2);
          groups.AIR.add(beacon);

          // 8. Companion Curved Towers (The World Towers Triad: World View & World Crest)
          // World Crest (South-West companion curved tower, 223m)
          const crestGeo = new THREE.CylinderGeometry(4.2, 4.8, 38, 24, 1, false, 0, Math.PI * 1.5);
          crestGeo.rotateX(Math.PI / 2);
          const compMat = new THREE.MeshStandardMaterial({{
            color: 0x0369a1,
            metalness: 0.75,
            roughness: 0.25,
            transparent: true,
            opacity: 0.85
          }});
          const crest = new THREE.Mesh(crestGeo, compMat);
          crest.position.set(5.5, 30.5, 19.0);
          groups.BLD.add(crest);

          // World Crest crown ring
          const crestCrown = new THREE.Mesh(new THREE.TorusGeometry(4.3, 0.3, 8, 24), whiteBalconyMat);
          crestCrown.position.set(5.5, 30.5, 38.0);
          groups.BLD.add(crestCrown);

          // World View (South-East companion curved tower, 277m)
          const viewGeo = new THREE.CylinderGeometry(4.5, 5.0, 52, 24, 1, false, 0, Math.PI * 1.5);
          viewGeo.rotateX(Math.PI / 2);
          const viewMesh = new THREE.Mesh(viewGeo, compMat);
          viewMesh.position.set(34.5, 30.5, 26.0);
          groups.BLD.add(viewMesh);

          // World View crown ring
          const viewCrown = new THREE.Mesh(new THREE.TorusGeometry(4.6, 0.3, 8, 24), whiteBalconyMat);
          viewCrown.position.set(34.5, 30.5, 52.0);
          groups.BLD.add(viewCrown);

          // 9. Subsurface 4-Tier Automated Robotic Valet Vault (-20m to 0m)
          createPrism("SUB_VAULT", [[4, 4], [36, 4], [36, 36], [4, 36]], -20, 0, 0xf59e0b, 0.88, "SUB", -1, {{
            name: "Worli 4-Tier Automated Robotic Valet Vault (1200 Vehicle Bays & MEP Vault)",
            ulpin: `${{data.base_ulpin}}-SUB-B04-RP01-3`,
            z: "-20.0m to 0.0m",
            area: "1024 m²",
            vol: "20480 m³",
            owner: "World One Resident Automated Valet Trust",
            val: "₹ 160 Cr"
          }});
        }}

        // ARCHETYPE 3: UB City & Kingfisher Towers (Bengaluru) - Neo-Classical Roman Galleria & White House Penthouse
        function buildUBcitySteppedSpire(data) {{
          // 1. Neoclassical Luxury Retail Galleria (The Collection, 0 to 8m)
          createPrism("BLD_GALLERIA", [[4,4],[36,4],[36,36],[4,36]], 0, 8, 0x059669, 0.86, "BLD", 1, {{
            name: "The Collection Luxury Galleria & Roman Arched Piazza",
            ulpin: `${{data.base_ulpin}}-BLD-P01-GL01-B`,
            z: "0.0m to +8.0m",
            area: "1024 m²",
            vol: "8192 m³",
            owner: "The Collection Luxury Galleria Piazza Trust",
            val: "₹ 520 Cr"
          }});

          // Central Roman Amphitheater & Piazza Water Fountain (at X = 20, Y = 20)
          const pFountain = new THREE.Mesh(new THREE.CylinderGeometry(3.5, 3.8, 0.4, 24), new THREE.MeshStandardMaterial({{ color: 0x64748b, roughness: 0.8 }}));
          pFountain.rotateX(Math.PI / 2);
          pFountain.position.set(20, 20, 8.2);
          groups.BLD.add(pFountain);

          const pWater = new THREE.Mesh(new THREE.CylinderGeometry(3.2, 3.2, 0.3, 24), new THREE.MeshStandardMaterial({{ color: 0x0284c7, roughness: 0.1, transparent: true, opacity: 0.85 }}));
          pWater.rotateX(Math.PI / 2);
          pWater.position.set(20, 20, 8.3);
          groups.BLD.add(pWater);

          const ubCorporateTenants = [
            "KKR & Co. India Private Equity Advisors",
            "Morgan Stanley Advantage Services India",
            "United Breweries Holdings Ltd (Corporate HQ)",
            "Blackstone India Real Estate Advisory",
            "Cisco Systems Global Innovation Studio"
          ];

          // 2. Structure A: Corporate UB Tower (West Wing: X = 6-18, Y = 8-32, 8 to 28m)
          for (let f = 3; f <= 7; f++) {{
            const zMin = 8 + (f - 3) * 4.0;
            const zMax = zMin + 4.0;
            const lvl = `F0${{f}}`;
            createPrism(`BLD_UB_${{lvl}}`, [[6,8],[18,8],[18,32],[6,32]], zMin, zMax, 0x10b981, 0.86, "BLD", f, {{
              name: `UB Corporate Tower Executive Offices (Level 0${{f}})`,
              ulpin: `${{data.base_ulpin}}-BLD-${{lvl}}-UB01-U`,
              z: `+${{zMin.toFixed(1)}}m to +${{zMax.toFixed(1)}}m`,
              area: "288 m²",
              vol: "1152 m³",
              owner: ubCorporateTenants[f - 3] || "UBHL Corporate Holdings",
              val: "₹ 34.0 Cr"
            }});
          }}

          // Elevated Helipad on Stilt Columns atop UB Tower (Z = 28.5m)
          const ubHeliGeo = new THREE.CylinderGeometry(5.8, 5.8, 0.4, 24);
          ubHeliGeo.rotateX(Math.PI / 2);
          const ubHeli = new THREE.Mesh(ubHeliGeo, new THREE.MeshStandardMaterial({{ color: 0x1e293b, roughness: 0.85 }}));
          ubHeli.position.set(12, 20, 28.5);
          groups.AIR.add(ubHeli);

          // Soaring Gilded Needle Spire atop UB Tower (Z = 29m to 48m)
          const spGeo = new THREE.CylinderGeometry(0.12, 1.2, 19, 16);
          spGeo.rotateX(Math.PI / 2);
          const spMat = new THREE.MeshStandardMaterial({{ color: 0xf59e0b, metalness: 0.85, roughness: 0.2 }});
          const spMesh = new THREE.Mesh(spGeo, spMat);
          spMesh.position.set(12, 20, 38.5);
          groups.AIR.add(spMesh);

          const kfResidents = [
            "Sh. Kiran Mazumdar-Shaw & Family Trust",
            "Dr. Devi Prasad & Alaknanda Shetty",
            "Sh. Nandan & Rohini Nilekani Family Trust",
            "Sh. Kris & Sudha Gopalakrishnan"
          ];

          // 3. Structure B: Prestige Kingfisher Towers (East Wing: X = 22-34, Y = 8-32, 8 to 28m)
          for (let f = 3; f <= 6; f++) {{
            const zMin = 8 + (f - 3) * 5.0;
            const zMax = zMin + 5.0;
            const lvl = `F0${{f}}`;
            createPrism(`BLD_KF_${{lvl}}`, [[22,8],[34,8],[34,32],[22,32]], zMin, zMax, 0x0284c7, 0.86, "BLD", f, {{
              name: `Prestige Kingfisher Ultra-Luxury Residences (Level 0${{f}})`,
              ulpin: `${{data.base_ulpin}}-BLD-${{lvl}}-KF01-K`,
              z: `+${{zMin.toFixed(1)}}m to +${{zMax.toFixed(1)}}m`,
              area: "288 m²",
              vol: "1440 m³",
              owner: kfResidents[f - 3] || "Prestige Luxury Living",
              val: "₹ 42.0 Cr"
            }});
          }}

          // 4. THE FAMOUS CANTILEVERED "WHITE HOUSE IN THE SKY" MANSION (Z = 28 to 38m)
          createPrism("BLD_WHITE_HOUSE_BASE", [[19,6],[37,6],[37,34],[19,34]], 28, 29.5, 0xf8fafc, 0.95, "BLD", 7, {{
            name: "Prestige Cantilevered Steel Transfer Deck (White House Base)",
            ulpin: `${{data.base_ulpin}}-BLD-F07-DK01-W`,
            z: "+28.0m to +29.5m",
            area: "504 m²",
            vol: "756 m³",
            owner: "Sovereign Sky Mansion Trust",
            val: "₹ 45.0 Cr"
          }});

          createPrism("BLD_SKY_MANSION", [[21,8],[35,8],[35,32],[21,32]], 29.5, 37.0, 0xf1f5f9, 0.96, "BLD", 8, {{
            name: "Prestige Kingfisher 'White House in the Sky' Luxury Penthouse (40,000 sq ft)",
            ulpin: `${{data.base_ulpin}}-BLD-F08-WH01-M`,
            z: "+29.5m to +37.0m",
            area: "336 m²",
            vol: "2520 m³",
            owner: "Sovereign Sky Mansion Trust (Cantilevered White House)",
            val: "₹ 195 Cr"
          }});

          const roofGeo = new THREE.ConeGeometry(9, 4.5, 4);
          roofGeo.rotateX(Math.PI / 2);
          roofGeo.rotateZ(Math.PI / 4);
          const roofMesh = new THREE.Mesh(roofGeo, new THREE.MeshStandardMaterial({{ color: 0x64748b, roughness: 0.4 }}));
          roofMesh.position.set(28, 20, 39.2);
          groups.AIR.add(roofMesh);

          const kfPool = new THREE.Mesh(new THREE.BoxGeometry(16, 3, 0.8), new THREE.MeshStandardMaterial({{ color: 0x06b6d4, roughness: 0.05, transparent: true, opacity: 0.9 }}));
          kfPool.position.set(28, 6.8, 29.8);
          groups.BLD.add(kfPool);

          createPrism("SUB_UB", [[5,5],[35,5],[35,35],[5,35]], -14, 0, 0xf59e0b, 0.85, "SUB", -1, {{
            name: "UB City Supercar Concierge Basements (B1-B2)",
            ulpin: `${{data.base_ulpin}}-SUB-B02-UB01-5`,
            z: "-14.0m to 0.0m",
            area: "900 m²",
            vol: "12600 m³",
            owner: "UB City Supercar Concierge & Security Operations",
            val: "₹ 75.0 Cr"
          }});
        }}

        // ARCHETYPE 4: GIFT Diamond Tower & BKC Diamond Tower - Crystalline Faceted Skyscraper
        function buildDiamondTower(data) {{
          const isGIFT = data.city && data.city.includes("GIFT");
          const towerName = isGIFT ? "GIFT Diamond Tower Pinnacle" : "BKC Bharat Diamond Bourse Tower";

          const diamondPoly = [[14,5],[26,5],[35,14],[35,26],[26,35],[14,35],[5,26],[5,14]];
          
          const bourseTenants = [
            "Bharat Diamond Bourse / International Bullion Exchange",
            "Gemological Institute of America (GIA) India",
            "Rosy Blue India Private Limited (Diamond Trading Wing)",
            "Kiran Gems Private Limited (Global Export Center)",
            "State Bank of India International Bullion Branch",
            "NSE International Exchange (NSE IX FinTech Center)",
            "International Financial Services Centres Authority (IFSCA)",
            "Global Diamond Trading & Vault Custodian"
          ];

          for (let f = 0; f <= 7; f++) {{
            const zMin = f * 4.5;
            const zMax = zMin + 4.5;
            const lvl = f === 0 ? "G00" : `F0${{f}}`;
            
            createPrism(`BLD_${{lvl}}_DIAMOND`, diamondPoly, zMin, zMax, 0x06b6d4, 0.88, "BLD", f, {{
              name: `${{towerName}} Trading Floor (${{lvl}})`,
              ulpin: `${{data.base_ulpin}}-BLD-${{lvl}}-DM01-D`,
              z: `+${{zMin.toFixed(1)}}m to +${{zMax.toFixed(1)}}m`,
              area: "650 m²",
              vol: "2925 m³",
              owner: bourseTenants[f] || "Global Diamond Bourse Custodian",
              val: `₹ ${{(65.0 + f * 4.0).toFixed(1)}} Cr`
            }});

            [-1, 1].forEach(dx => {{
              [-1, 1].forEach(dy => {{
                const cornerFacet = new THREE.Mesh(new THREE.ConeGeometry(2.0, 4.4, 4), new THREE.MeshStandardMaterial({{ color: 0x38bdf8, roughness: 0.1, metalness: 0.8, transparent: true, opacity: 0.7 }}));
                cornerFacet.position.set(20 + dx * 13, 20 + dy * 13, zMin + 2.2);
                cornerFacet.rotation.z = Math.PI / 4;
                groups.BLD.add(cornerFacet);
              }});
            }});
          }}

          const crownGeo = new THREE.ConeGeometry(9.0, 16, 8);
          crownGeo.rotateX(Math.PI / 2);
          const crownMat = new THREE.MeshStandardMaterial({{ color: 0x0ea5e9, roughness: 0.1, metalness: 0.85, transparent: true, opacity: 0.85 }});
          const crownMesh = new THREE.Mesh(crownGeo, crownMat);
          crownMesh.position.set(20, 20, 44.0);
          groups.AIR.add(crownMesh);

          const hGeo = new THREE.CylinderGeometry(5.2, 5.2, 0.35, 24);
          hGeo.rotateX(Math.PI / 2);
          const hMesh = new THREE.Mesh(hGeo, new THREE.MeshStandardMaterial({{ color: 0x1e293b, roughness: 0.85 }}));
          hMesh.position.set(20, 14, 46.0);
          groups.AIR.add(hMesh);

          const hRing = new THREE.Mesh(new THREE.RingGeometry(3.2, 3.8, 24), new THREE.MeshBasicMaterial({{ color: 0xfacc15, side: THREE.DoubleSide }}));
          hRing.position.set(20, 14, 46.2);
          groups.AIR.add(hRing);

          createPrism("SUB_VAULT", [[6,6],[34,6],[34,34],[6,34]], -16, 0, 0xf59e0b, 0.88, "SUB", -1, {{
            name: "High-Security Bullion & Diamond Vault (B1-B3 Fortress)",
            ulpin: `${{data.base_ulpin}}-SUB-B03-BV01-9`,
            z: "-16.0m to 0.0m",
            area: "784 m²",
            vol: "12544 m³",
            owner: "Reserve Bank of India & Customs High-Security Depository",
            val: "₹ 520 Cr"
          }});

          const tubeGeo = new THREE.CylinderGeometry(1.4, 1.4, 42, 16);
          tubeGeo.rotateZ(Math.PI / 2);
          const tubeMesh = new THREE.Mesh(tubeGeo, new THREE.MeshStandardMaterial({{ color: 0xa855f7, transparent: true, opacity: 0.9 }}));
          tubeMesh.position.set(20, 10, -8);
          groups.UTL.add(tubeMesh);
          meshMap.set("UTL_TUM", tubeMesh);
        }}

        // ARCHETYPE 5: Connaught Place Heritage Colonnade (New Delhi) - Concentric Colonnades & National Flag
        function buildHeritageRotunda(data) {{
          // 1. Outer Georgian Palladian Colonnade Arcade (Ground to +6.5m, Radius 18.5m)
          createCylinderPrism("BLD_OUTER_COLONNADE", 18.5, 18.5, 0, 6.5, 48, 0xf8fafc, 0.92, "BLD", 0, {{
            name: "Lutyens Georgian Heritage Colonnade Arcade (Outer Circle / Connaught Circus)",
            ulpin: `${{data.base_ulpin}}-BLD-G00-OC01-1`,
            z: "0.0m to +6.5m",
            area: "1075 m²",
            vol: "6988 m³",
            owner: "New Delhi Municipal Council (Colonnade Heritage Custodian)",
            val: "₹ 380 Cr"
          }});

          const colMat = new THREE.MeshStandardMaterial({{ color: 0xf1f5f9, roughness: 0.7 }});
          for (let a = 0; a < Math.PI * 2; a += Math.PI / 12) {{
            const isAvenue = Math.abs(a % (Math.PI / 4)) < 0.15;
            if (!isAvenue) {{
              const dCol = new THREE.Mesh(new THREE.CylinderGeometry(0.22, 0.25, 6.2, 12), colMat);
              dCol.rotateX(Math.PI / 2);
              dCol.position.set(20 + Math.cos(a) * 18.5, 20 + Math.sin(a) * 18.5, 3.1);
              groups.SUR.add(dCol);
            }}
          }}

          // 2. Inner Circular Georgian Colonnade (Ground to +6.5m, Radius 12.5m)
          createCylinderPrism("BLD_INNER_COLONNADE", 12.5, 12.5, 0, 6.5, 36, 0xf8fafc, 0.92, "BLD", 0, {{
            name: "Connaught Place Inner Circle Heritage Colonnade & Verandas",
            ulpin: `${{data.base_ulpin}}-BLD-G00-IC01-2`,
            z: "0.0m to +6.5m",
            area: "490 m²",
            vol: "3185 m³",
            owner: "NDMC Heritage & Commercial Properties Wing",
            val: "₹ 320 Cr"
          }});

          for (let a = 0; a < Math.PI * 2; a += Math.PI / 10) {{
            const isAvenue = Math.abs(a % (Math.PI / 4)) < 0.15;
            if (!isAvenue) {{
              const dCol = new THREE.Mesh(new THREE.CylinderGeometry(0.2, 0.22, 6.2, 12), colMat);
              dCol.rotateX(Math.PI / 2);
              dCol.position.set(20 + Math.cos(a) * 12.5, 20 + Math.sin(a) * 12.5, 3.1);
              groups.SUR.add(dCol);
            }}
          }}

          // 3. Central Park Circular Green Lawn (Radius 8.5m)
          const parkGeo = new THREE.CylinderGeometry(8.5, 8.5, 0.35, 36);
          parkGeo.rotateX(Math.PI / 2);
          const parkMat = new THREE.MeshStandardMaterial({{ color: 0x15803d, roughness: 0.9 }});
          const parkMesh = new THREE.Mesh(parkGeo, parkMat);
          parkMesh.position.set(20, 20, 0.18);
          groups.SUR.add(parkMesh);

          const walkGeo = new THREE.RingGeometry(5.5, 6.8, 36);
          const walkMat = new THREE.MeshStandardMaterial({{ color: 0xcbd5e1, roughness: 0.8 }});
          const walkMesh = new THREE.Mesh(walkGeo, walkMat);
          walkMesh.position.set(20, 20, 0.38);
          groups.SUR.add(walkMesh);

          // 4. MONUMENTAL 207-FOOT CENTRAL INDIAN NATIONAL FLAG (TIRANGA)
          const flagPole = new THREE.Mesh(new THREE.CylinderGeometry(0.12, 0.32, 20, 16), new THREE.MeshStandardMaterial({{ color: 0xe2e8f0, metalness: 0.9 }}));
          flagPole.rotateX(Math.PI / 2);
          flagPole.position.set(20, 20, 10.0);
          groups.SUR.add(flagPole);

          const finial = new THREE.Mesh(new THREE.SphereGeometry(0.35, 12, 12), new THREE.MeshStandardMaterial({{ color: 0xfacc15, metalness: 0.9, roughness: 0.1 }}));
          finial.position.set(20, 20, 20.2);
          groups.SUR.add(finial);

          const flagCanvas = document.createElement('canvas');
          flagCanvas.width = 256; flagCanvas.height = 160;
          const fctx = flagCanvas.getContext('2d');
          fctx.fillStyle = '#ff9933'; fctx.fillRect(0, 0, 256, 53);
          fctx.fillStyle = '#ffffff'; fctx.fillRect(0, 53, 256, 54);
          fctx.fillStyle = '#138808'; fctx.fillRect(0, 107, 256, 53);
          fctx.strokeStyle = '#000080'; fctx.lineWidth = 3;
          fctx.beginPath(); fctx.arc(128, 80, 20, 0, Math.PI * 2); fctx.stroke();
          for (let s = 0; s < 24; s++) {{
            const rad = (s / 24) * Math.PI * 2;
            fctx.beginPath(); fctx.moveTo(128, 80); fctx.lineTo(128 + Math.cos(rad) * 19, 80 + Math.sin(rad) * 19); fctx.stroke();
          }}
          const flagTex = new THREE.CanvasTexture(flagCanvas);
          const flagMesh = new THREE.Mesh(new THREE.PlaneGeometry(6.4, 4.0), new THREE.MeshStandardMaterial({{ map: flagTex, side: THREE.DoubleSide }}));
          flagMesh.position.set(23.2, 20, 18.0);
          groups.SUR.add(flagMesh);

          // 5. Commercial Ring Storeys (Z = 6.5m to 20m)
          const cpLeaseholders = [
            "Standard Chartered Bank Heritage Flagship Branch",
            "Oxford University Press & Legal Chambers",
            "Lutyens Heritage Trust & Rotunda Observatory",
            "Central Business District Corporate Chambers"
          ];

          for (let f = 1; f <= 3; f++) {{
            const zMin = 6.5 + (f - 1) * 4.5;
            const zMax = zMin + 4.5;
            createCylinderPrism(`BLD_F0${{f}}_ROTUNDA`, 12.5, 12.5, zMin, zMax, 32, 0xd97706, 0.85, "BLD", f, {{
              name: `Connaught Place Central Business Suites (Tier ${{f}})`,
              ulpin: `${{data.base_ulpin}}-BLD-F0${{f}}-RT01-N`,
              z: `+${{zMin.toFixed(1)}}m to +${{zMax.toFixed(1)}}m`,
              area: "490 m²",
              vol: "2205 m³",
              owner: cpLeaseholders[f - 1] || "NDMC Authorized Commercial Leaseholder",
              val: `₹ ${{(50.0 + f * 5.0).toFixed(1)}} Cr`
            }});
          }}

          // 6. Multi-Level Rajiv Chowk Underground Metro Hub & Palika Bazaar
          createPrism("SUB_CONCOURSE", [[4,4],[36,4],[36,36],[4,36]], -6, 0, 0xf59e0b, 0.88, "SUB", -1, {{
            name: "Rajiv Chowk Metro Concourse & Palika Bazaar Underground Market",
            ulpin: `${{data.base_ulpin}}-SUB-B01-RC01-4`,
            z: "-6.0m to 0.0m",
            area: "1024 m²",
            vol: "6144 m³",
            owner: "Delhi Metro Rail Corp & Palika Bazaar Traders Association",
            val: "₹ 480 Cr"
          }});

          createPrism("SUB_YELLOW_LINE", [[13,2],[27,2],[27,38],[13,38]], -13, -6, 0xeab308, 0.9, "UTL", -2, {{
            name: "Yellow Line Dual Island Platforms 1 & 2 (Samaypur Badli - Millennium City Centre)",
            ulpin: `${{data.base_ulpin}}-UTL-B02-YL01-Y`,
            z: "-13.0m to -6.0m",
            area: "504 m²",
            vol: "3528 m³",
            owner: "DMRC Yellow Line Operations Directorate",
            val: "₹ 410 Cr"
          }});

          createPrism("SUB_BLUE_LINE", [[2,13],[38,13],[38,27],[2,27]], -21, -13, 0x0284c7, 0.9, "UTL", -3, {{
            name: "Blue Line Deep Platform 3 & 4 (Dwarka Sector 21 - Noida Electronic City)",
            ulpin: `${{data.base_ulpin}}-UTL-B03-BL01-B`,
            z: "-21.0m to -13.0m",
            area: "504 m²",
            vol: "4032 m³",
            owner: "DMRC Blue Line Operations Directorate",
            val: "₹ 440 Cr"
          }});
        }}

        // ARCHETYPE 6: Seawoods Grand Central (Navi Mumbai) - Transit-Oriented Development (TOD)
        function buildSeawoodsQuadPodium(data) {{
          // -----------------------------------------------------------------
          // 1. GRAND RETAIL PODIUM: NEXUS GRAND CENTRAL MALL (Z = 0 to 12.0m)
          // -----------------------------------------------------------------
          // Level G00: Hypermarket, Station Concourse & Grand Retail (Z = 0.0 to 4.2m)
          const polyPodiumG00 = [
            [4, 4.5], [10, 2.2], [16, 1.0], [20, 0.6], [24, 1.0], [30, 2.2], [36, 4.5],
            [38, 12], [38, 37], [35, 39], [5, 39], [2, 37], [2, 12]
          ];
          createPrism("BLD_PODIUM_G00", polyPodiumG00, 0, 4.2, 0x0284c7, 0.88, "BLD", 0, {{
            name: "Nexus Grand Central Retail Atrium & Transit Concourse (Ground Floor)",
            ulpin: `${{data.base_ulpin}}-BLD-G00-POD1-8`,
            z: "0.0m to +4.2m",
            area: "1240 m²",
            vol: "5208 m³",
            owner: "Nexus Select Trust (Retail Anchors & Central Transit Concourse)",
            val: "₹ 680 Cr"
          }});

          // Level L01: International Brands & Fashion Galleria (Z = 4.2 to 8.2m)
          const polyPodiumL01 = [
            [4.5, 5.5], [11, 3.2], [20, 2.0], [29, 3.2], [35.5, 5.5],
            [37.5, 13], [37.5, 36.5], [34.5, 38.5], [5.5, 38.5], [2.5, 36.5], [2.5, 13]
          ];
          createPrism("BLD_PODIUM_L01", polyPodiumL01, 4.2, 8.2, 0x0369a1, 0.88, "BLD", 1, {{
            name: "Nexus Grand Central Fashion Galleria & Central Atrium (Level 01)",
            ulpin: `${{data.base_ulpin}}-BLD-L01-POD2-9`,
            z: "+4.2m to +8.2m",
            area: "1150 m²",
            vol: "4600 m³",
            owner: "Nexus Select Trust (International Retail Tenants)",
            val: "₹ 540 Cr"
          }});

          // Level L02: PVR INOX Multiplex, Food Court & Sky Dining (Z = 8.2 to 12.0m)
          const polyPodiumL02 = [
            [5, 6.5], [12, 4.5], [20, 3.5], [28, 4.5], [35, 6.5],
            [37, 14], [37, 36], [34, 38], [6, 38], [3, 36], [3, 14]
          ];
          createPrism("BLD_PODIUM_L02", polyPodiumL02, 8.2, 12.0, 0x0284c7, 0.88, "BLD", 2, {{
            name: "PVR INOX 11-Screen Multiplex & Sky Dining Terrace (Level 02)",
            ulpin: `${{data.base_ulpin}}-BLD-L02-POD3-1`,
            z: "+8.2m to +12.0m",
            area: "1080 m²",
            vol: "4104 m³",
            owner: "PVR INOX Limited & Nexus Gourmet Dining SPV",
            val: "₹ 490 Cr"
          }});

          // Stepped Terrace Outdoor Dining Decks & Planter Greenery (Z = 12.0m)
          const deckMat = new THREE.MeshStandardMaterial({{ color: 0x78350f, roughness: 0.85 }});
          const deckWest = new THREE.Mesh(new THREE.BoxGeometry(6, 12, 0.1), deckMat);
          deckWest.position.set(6, 14, 12.05);
          groups.BLD.add(deckWest);
          const deckEast = new THREE.Mesh(new THREE.BoxGeometry(6, 12, 0.1), deckMat);
          deckEast.position.set(34, 14, 12.05);
          groups.BLD.add(deckEast);

          // Green Planter Hedges around Terraces
          const hedgeMat = new THREE.MeshStandardMaterial({{ color: 0x166534, roughness: 0.9 }});
          [[6, 8], [34, 8], [2.8, 14], [37.2, 14]].forEach(([hx, hy]) => {{
            const hedge = new THREE.Mesh(new THREE.BoxGeometry(5.2, 0.8, 0.8), hedgeMat);
            hedge.position.set(hx, hy, 12.4);
            groups.BLD.add(hedge);
          }});

          // Grand Main Entrance Glass Canopy & Portico (South Facade, Z = 4.0 to 6.2m)
          const canopyTex = getCurvedCanopyTexture();
          const canopyMat = new THREE.MeshStandardMaterial({{
            map: canopyTex,
            color: 0xffffff,
            roughness: 0.2,
            transparent: true,
            opacity: 0.88,
            side: THREE.DoubleSide
          }});
          const canopyGeo = new THREE.BoxGeometry(16, 6, 0.3);
          const canopyMesh = new THREE.Mesh(canopyGeo, canopyMat);
          canopyMesh.position.set(20, -1.2, 5.0);
          canopyMesh.rotation.x = 0.08;
          groups.BLD.add(canopyMesh);

          // White steel tubular pylons supporting entrance canopy
          const pylonMat = new THREE.MeshStandardMaterial({{ color: 0xe2e8f0, metalness: 0.8, roughness: 0.2 }});
          [-6.5, 6.5].forEach(px => {{
            const pyl = new THREE.Mesh(new THREE.CylinderGeometry(0.18, 0.18, 5.2, 12), pylonMat);
            pyl.rotateX(Math.PI / 2);
            pyl.position.set(20 + px, -3.8, 2.6);
            groups.SUR.add(pyl);
          }});

          // 3D Entrance Signboard Banner over Canopy
          const signCanvas = document.createElement('canvas');
          signCanvas.width = 512; signCanvas.height = 64;
          const sctx = signCanvas.getContext('2d');
          sctx.fillStyle = '#0b3c5d'; sctx.fillRect(0, 0, 512, 64);
          sctx.strokeStyle = '#38bdf8'; sctx.lineWidth = 4; sctx.strokeRect(2, 2, 508, 60);
          sctx.fillStyle = '#f8fafc'; sctx.font = 'bold 22px sans-serif'; sctx.textAlign = 'center';
          sctx.fillText('NEXUS SEAWOODS • GRAND CENTRAL TOD', 256, 40);
          const sTex = new THREE.CanvasTexture(signCanvas);
          const sMesh = new THREE.Mesh(new THREE.BoxGeometry(13, 0.2, 1.2), new THREE.MeshStandardMaterial({{ map: sTex }}));
          sMesh.position.set(20, 0.8, 6.2);
          groups.BLD.add(sMesh);

          // Longitudinal Curvilinear Glass Barrel-Vault Skylight Spine (Z = 12.0m to 14.5m)
          const skylightGeo = new THREE.CylinderGeometry(2.8, 2.8, 24, 24, 1, false, 0, Math.PI);
          skylightGeo.rotateZ(Math.PI / 2);
          skylightGeo.rotateX(Math.PI / 2);
          const skylightMat = new THREE.MeshStandardMaterial({{
            color: 0x38bdf8,
            roughness: 0.1,
            metalness: 0.3,
            transparent: true,
            opacity: 0.8,
            side: THREE.DoubleSide
          }});
          const skylightMesh = new THREE.Mesh(skylightGeo, skylightMat);
          skylightMesh.position.set(20, 22, 12.0);
          groups.BLD.add(skylightMesh);

          // Steel Arch Ribs along Skylight Spine
          const ribMat = new THREE.MeshStandardMaterial({{ color: 0x0f172a, metalness: 0.8 }});
          for (let ry = 11; ry <= 33; ry += 3) {{
            const ribGeo = new THREE.TorusGeometry(2.85, 0.08, 8, 24, Math.PI);
            ribGeo.rotateZ(Math.PI);
            ribGeo.rotateY(Math.PI / 2);
            const ribMesh = new THREE.Mesh(ribGeo, ribMat);
            ribMesh.position.set(20, ry, 12.0);
            groups.BLD.add(ribMesh);
          }}

          // -----------------------------------------------------------------
          // 2. INTEGRATED SEAWOODS-DARAVE RAILWAY STATION & LOCAL EMU TRAIN
          // -----------------------------------------------------------------
          // Ballasted Gravel Trackbed Corridor (Z = 0.05m)
          const ballastMat = new THREE.MeshStandardMaterial({{ color: 0x334155, roughness: 0.95 }});
          const ballastMesh = new THREE.Mesh(new THREE.BoxGeometry(8.4, 56, 0.2), ballastMat);
          ballastMesh.position.set(20, 19, 0.1);
          groups.SUR.add(ballastMesh);

          // Dual Railway Tracks: Track 1 (Up Harbour) at X = 18.2, Track 2 (Down Harbour) at X = 21.8
          const sleeperMat = new THREE.MeshStandardMaterial({{ color: 0x475569, roughness: 0.85 }});
          const railMat = new THREE.MeshStandardMaterial({{ color: 0xe2e8f0, metalness: 0.95, roughness: 0.15 }});

          [18.2, 21.8].forEach(trackX => {{
            // Concrete sleepers along corridor
            for (let sy = -7; sy <= 45; sy += 1.4) {{
              const sleeper = new THREE.Mesh(new THREE.BoxGeometry(2.4, 0.3, 0.15), sleeperMat);
              sleeper.position.set(trackX, sy, 0.22);
              groups.SUR.add(sleeper);
            }}
            // Dual steel rails
            [-0.7, 0.7].forEach(rx => {{
              const rail = new THREE.Mesh(new THREE.BoxGeometry(0.12, 56, 0.22), railMat);
              rail.position.set(trackX + rx, 19, 0.38);
              groups.SUR.add(rail);
            }});
          }});

          // Covered Passenger Island Platforms (Z = 0.0 to 1.1m)
          const yellowEdgeMat = new THREE.MeshBasicMaterial({{ color: 0xfacc15 }});

          // West Platform (X = 14 to 17) & East Platform (X = 23 to 26)
          [
            {{ x: 15.2, name: "Seawoods-Darave Platform 1 & 2 (Harbour Line)", ulpin: `${{data.base_ulpin}}-SUR-PF01-P1` }},
            {{ x: 24.8, name: "Seawoods-Darave Platform 3 & 4 (Trans-Harbour Line)", ulpin: `${{data.base_ulpin}}-SUR-PF02-P2` }}
          ].forEach(p => {{
            createPrism(`SUR_PLAT_${{p.x < 20 ? "W" : "E"}}`, [
              [p.x - 1.4, 0], [p.x + 1.4, 0], [p.x + 1.4, 38], [p.x - 1.4, 38]
            ], 0, 1.1, 0x64748b, 0.95, "SUR", 0, {{
              name: p.name,
              ulpin: p.ulpin,
              z: "0.0m to +1.1m",
              area: "106 m²",
              vol: "116 m³",
              owner: "Central Railway (Mumbai Suburban Division)",
              val: "₹ 180 Cr"
            }});

            // Yellow tactile safety line along platform edge
            const tactileEdge = new THREE.Mesh(new THREE.BoxGeometry(0.25, 38, 0.02), yellowEdgeMat);
            tactileEdge.position.set(p.x + (p.x < 20 ? 1.3 : -1.3), 19, 1.11);
            groups.SUR.add(tactileEdge);

            // Platform Roof Canopy on tubular steel stanchions
            const canopyRoof = new THREE.Mesh(new THREE.BoxGeometry(3.0, 36, 0.15), new THREE.MeshStandardMaterial({{ color: 0x0284c7, metalness: 0.5, roughness: 0.3 }}));
            canopyRoof.position.set(p.x, 19, 3.8);
            groups.SUR.add(canopyRoof);

            for (let cy = 4; cy <= 34; cy += 6) {{
              const col = new THREE.Mesh(new THREE.CylinderGeometry(0.08, 0.08, 2.7, 8), pylonMat);
              col.rotateX(Math.PI / 2);
              col.position.set(p.x, cy, 2.45);
              groups.SUR.add(col);
            }}

            // Multilingual Indian Railways Station Nameboards
            createStationSignboard("सीवूड्स - दारावे", "SEAWOODS - DARAVE", p.x, 6, 2.6, 0);
            createStationSignboard("सीवूड्स - दारावे", "SEAWOODS - DARAVE", p.x, 32, 2.6, 0);

            // Escalators leading to Mall Concourse
            const escMat = new THREE.MeshStandardMaterial({{ color: 0x94a3b8, metalness: 0.8 }});
            const esc = new THREE.Mesh(new THREE.BoxGeometry(1.2, 5.0, 0.3), escMat);
            esc.position.set(p.x, 20, 2.6);
            esc.rotation.x = -Math.PI / 6;
            groups.SUR.add(esc);
          }});

          // Overhead Electrification (OHE) Catenary Gantries & Contact Wires
          const oheGantryMat = new THREE.MeshStandardMaterial({{ color: 0x475569, metalness: 0.85 }});
          [-3, 11, 25, 41].forEach(gy => {{
            // Vertical portal masts
            [-4.8, 4.8].forEach(gx => {{
              const mast = new THREE.Mesh(new THREE.BoxGeometry(0.25, 0.25, 5.4), oheGantryMat);
              mast.position.set(20 + gx, gy, 2.7);
              groups.SUR.add(mast);
            }});
            // Horizontal portal boom spanning across tracks
            const boom = new THREE.Mesh(new THREE.BoxGeometry(10.2, 0.22, 0.25), oheGantryMat);
            boom.position.set(20, gy, 5.3);
            groups.SUR.add(boom);

            // Drop arms and porcelain insulators
            [18.2, 21.8].forEach(wx => {{
              const dropArm = new THREE.Mesh(new THREE.CylinderGeometry(0.03, 0.03, 0.6, 6), pylonMat);
              dropArm.rotateX(Math.PI / 2);
              dropArm.position.set(wx, gy, 5.0);
              groups.SUR.add(dropArm);
            }});
          }});

          // Continuous overhead copper contact wire (Z = 4.8m)
          const wireMat = new THREE.MeshStandardMaterial({{ color: 0xb45309, metalness: 0.9, roughness: 0.2 }});
          [18.2, 21.8].forEach(wx => {{
            const oheWire = new THREE.Mesh(new THREE.CylinderGeometry(0.02, 0.02, 54, 6), wireMat);
            oheWire.rotateZ(Math.PI / 2);
            oheWire.position.set(wx, 19, 4.8);
            groups.SUR.add(oheWire);
          }});

          // High-Fidelity 12-Car Mumbai Suburban Local EMU Train (stopped at Platform on Track 1)
          const emuBodyMat = new THREE.MeshStandardMaterial({{ color: 0x6b21a8, roughness: 0.3 }});
          const emuWhiteMat = new THREE.MeshStandardMaterial({{ color: 0xf8fafc, roughness: 0.4 }});
          const emuGlassMat = new THREE.MeshStandardMaterial({{ color: 0x0284c7, roughness: 0.1, metalness: 0.8 }});
          const emuBogieMat = new THREE.MeshStandardMaterial({{ color: 0x0f172a, roughness: 0.9 }});

          const coaches = [
            {{ y: 11, isCab: false }},
            {{ y: 19, isCab: false }},
            {{ y: 27, isCab: true }}
          ];

          coaches.forEach(c => {{
            const coachMesh = new THREE.Mesh(new THREE.BoxGeometry(2.3, 7.2, 2.4), emuBodyMat);
            coachMesh.position.set(18.2, c.y, 1.8);
            groups.SUR.add(coachMesh);

            const stripeMesh = new THREE.Mesh(new THREE.BoxGeometry(2.32, 7.2, 1.1), emuWhiteMat);
            stripeMesh.position.set(18.2, c.y, 2.3);
            groups.SUR.add(stripeMesh);

            [-1.17, 1.17].forEach(wx => {{
              const win = new THREE.Mesh(new THREE.BoxGeometry(0.04, 6.2, 0.65), emuGlassMat);
              win.position.set(18.2 + wx, c.y, 2.3);
              groups.SUR.add(win);
            }});

            [-2.4, 2.4].forEach(by => {{
              const bogie = new THREE.Mesh(new THREE.BoxGeometry(2.1, 1.6, 0.45), emuBogieMat);
              bogie.position.set(18.2, c.y + by, 0.6);
              groups.SUR.add(bogie);
            }});

            if (c.isCab) {{
              const cabNose = new THREE.Mesh(new THREE.BoxGeometry(2.28, 0.8, 2.1), emuWhiteMat);
              cabNose.position.set(18.2, c.y + 3.8, 1.7);
              groups.SUR.add(cabNose);

              const cabGlass = new THREE.Mesh(new THREE.BoxGeometry(1.9, 0.1, 0.8), emuGlassMat);
              cabGlass.position.set(18.2, c.y + 4.22, 2.2);
              cabGlass.rotation.x = -0.2;
              groups.SUR.add(cabGlass);

              const headMat = new THREE.MeshBasicMaterial({{ color: 0xfef08a }});
              [-0.6, 0.6].forEach(hx => {{
                const hl = new THREE.Mesh(new THREE.SphereGeometry(0.12, 8, 8), headMat);
                hl.position.set(18.2 + hx, c.y + 4.25, 1.3);
                groups.SUR.add(hl);
              }});

              // Raised Diamond Pantograph touching OHE contact wire
              const pantoMat = new THREE.MeshStandardMaterial({{ color: 0xef4444, metalness: 0.9 }});
              const pantoBase = new THREE.Mesh(new THREE.BoxGeometry(1.2, 1.2, 0.1), pantoMat);
              pantoBase.position.set(18.2, c.y + 1.5, 3.05);
              groups.SUR.add(pantoBase);

              const pantoArm1 = new THREE.Mesh(new THREE.CylinderGeometry(0.03, 0.03, 1.8, 6), pantoMat);
              pantoArm1.position.set(18.2, c.y + 1.2, 3.8);
              pantoArm1.rotation.x = 0.45;
              groups.SUR.add(pantoArm1);

              const pantoArm2 = new THREE.Mesh(new THREE.CylinderGeometry(0.03, 0.03, 1.8, 6), pantoMat);
              pantoArm2.position.set(18.2, c.y + 1.8, 4.4);
              pantoArm2.rotation.x = -0.45;
              groups.SUR.add(pantoArm2);

              const pantoHead = new THREE.Mesh(new THREE.BoxGeometry(1.6, 0.2, 0.06), pantoMat);
              pantoHead.position.set(18.2, c.y + 1.5, 4.8);
              groups.SUR.add(pantoHead);
            }}
          }});

          // -----------------------------------------------------------------
          // 3. FOUR ARTICULATED COMMERCIAL OFFICE TOWERS (Z = 12.0m to 40.8m)
          // -----------------------------------------------------------------
          const polyT1 = [[4, 23], [15, 23], [17, 25], [17, 36.5], [15, 38], [4, 38]];
          const polyT2 = [[23, 25], [25, 23], [36, 23], [36, 38], [25, 38], [23, 36.5]];
          const polyT3 = [[4, 6], [15, 6], [17, 8], [17, 19], [15, 21], [4, 21]];
          const polyT4 = [[23, 8], [25, 6], [36, 6], [36, 21], [25, 21], [23, 19]];

          const towers = [
            {{
              id: "T1",
              name: "Grand Central Tower 1 (Airspace IT Hub)",
              poly: polyT1,
              clr: 0x0369a1,
              tenants: [
                "LTIMindtree Cloud Innovation Hub",
                "LTIMindtree Enterprise Solutions & R&D",
                "Cognizant Digital Business Operations",
                "Tech Mahindra AI & Autonomous Systems",
                "Cisco Systems Cloud Networking Center",
                "Executive Boardrooms & Panoramic Sky Suite"
              ]
            }},
            {{
              id: "T2",
              name: "Grand Central Tower 2 (Engineering & Infrastructure)",
              poly: polyT2,
              clr: 0x38bdf8,
              tenants: [
                "Jacobs Engineering Global Delivery Unit",
                "Jacobs Infrastructure Design Studio",
                "Mott MacDonald Engineering Consultants",
                "Arup Sustainable Technologies Hub",
                "Fluor Daniel EPC Projects Center",
                "Executive C-Suite & Helipad Lounge"
              ]
            }},
            {{
              id: "T3",
              name: "Grand Central Tower 3 (Global Financial Services)",
              poly: polyT3,
              clr: 0x0284c7,
              tenants: [
                "BNP Paribas India Solutions (Retail Banking)",
                "BNP Paribas Global Securities & Custody",
                "SBI Capital Markets Investment Banking",
                "HDFC Bank Corporate Treasury Center",
                "Barclays Global Shared Services",
                "Private Wealth Client Suites & Sky Deck"
              ]
            }},
            {{
              id: "T4",
              name: "Grand Central Tower 4 (Multinational Headquarters)",
              poly: polyT4,
              clr: 0x0ea5e9,
              tenants: [
                "Siemens Smart Infrastructure India HQ",
                "Siemens Healthcare Diagnostics Labs",
                "Tata AIG General Insurance Corporate HQ",
                "Philips Healthcare Innovation Hub",
                "Schneider Electric Digital Energy",
                "Corporate Auditorium & Panoramic Lounge"
              ]
            }}
          ];

          // Build 6 Storeys per Tower (Floors 3 to 8, from 12.0m to 40.8m)
          towers.forEach(t => {{
            for (let f = 3; f <= 8; f++) {{
              const zMin = 12.0 + (f - 3) * 4.8;
              const zMax = zMin + 4.8;
              const lvl = `F0${{f}}`;
              const tenantName = t.tenants[f - 3] || `${{t.name}} Level ${{f}}`;

              createPrism(`BLD_${{t.id}}_${{lvl}}`, t.poly, zMin, zMax, t.clr, 0.88, "BLD", f, {{
                name: `${{t.name}} - ${{tenantName}} (${{lvl}})`,
                ulpin: `${{data.base_ulpin}}-BLD-${{lvl}}-${{t.id}}01-M`,
                z: `+${{zMin.toFixed(1)}}m to +${{zMax.toFixed(1)}}m`,
                area: "148 m²",
                vol: "710 m³",
                owner: tenantName,
                val: `₹ ${{(32.0 + f * 2.5).toFixed(1)}} Cr`
              }});

              // Horizontal Aluminum Spandrel Band at each floor slab
              const spandrelMat = new THREE.MeshStandardMaterial({{ color: 0x94a3b8, metalness: 0.85, roughness: 0.2 }});
              const tCenter = t.id === "T1" ? [10.5, 30.5] : t.id === "T2" ? [29.5, 30.5] : t.id === "T3" ? [10.5, 13.5] : [29.5, 13.5];
              const spandrel = new THREE.Mesh(new THREE.BoxGeometry(12.8, 14.8, 0.35), spandrelMat);
              spandrel.position.set(tCenter[0], tCenter[1], zMin + 0.2);
              groups.BLD.add(spandrel);
            }}
          }});

          // -----------------------------------------------------------------
          // 4. SUSPENDED STRUCTURAL STEEL-TRUSS SKYBRIDGES (Z = 22.0m to 26.5m)
          // -----------------------------------------------------------------
          createPrism("BLD_SKYWALK_NORTH", [[17, 28], [23, 28], [23, 32], [17, 32]], 22.0, 26.5, 0x38bdf8, 0.82, "COM", 5, {{
            name: "Connecting Skybridge Galleria North (Tower 1 to Tower 2)",
            ulpin: `${{data.base_ulpin}}-COM-F05-SBN1-6`,
            z: "+22.0m to +26.5m",
            area: "24 m²",
            vol: "108 m³",
            owner: "Seawoods Grand Central Common Facilities Custodian",
            val: "₹ 18.0 Cr"
          }});

          createPrism("BLD_SKYWALK_SOUTH", [[17, 11], [23, 11], [23, 15], [17, 15]], 22.0, 26.5, 0x38bdf8, 0.82, "COM", 5, {{
            name: "Connecting Skybridge Galleria South (Tower 3 to Tower 4)",
            ulpin: `${{data.base_ulpin}}-COM-F05-SBS1-7`,
            z: "+22.0m to +26.5m",
            area: "24 m²",
            vol: "108 m³",
            owner: "Seawoods Grand Central Common Facilities Custodian",
            val: "₹ 18.0 Cr"
          }});

          // Exposed Warren Diagonal Steel Truss Framing on Skybridges
          const trussMat = new THREE.MeshStandardMaterial({{ color: 0x0f172a, metalness: 0.9, roughness: 0.2 }});
          [13, 30].forEach(bridgeY => {{
            for (let tx = 17.5; tx <= 22.5; tx += 1.5) {{
              const diag1 = new THREE.Mesh(new THREE.CylinderGeometry(0.06, 0.06, 4.6, 6), trussMat);
              diag1.position.set(tx, bridgeY - 1.95, 24.25);
              diag1.rotation.z = 0.65;
              groups.BLD.add(diag1);

              const diag2 = new THREE.Mesh(new THREE.CylinderGeometry(0.06, 0.06, 4.6, 6), trussMat);
              diag2.position.set(tx, bridgeY + 1.95, 24.25);
              diag2.rotation.z = -0.65;
              groups.BLD.add(diag2);
            }}
          }});

          // -----------------------------------------------------------------
          // 5. ROOFTOP ARCHITECTURAL MEP, HELIPAD & GREEN TECH (Z = 40.8m to 52m)
          // -----------------------------------------------------------------
          // Tower 1 Roof: Industrial HVAC Cooling Towers & BMU Crane
          const ctMat = new THREE.MeshStandardMaterial({{ color: 0x334155, roughness: 0.7 }});
          [[8.5, 28], [12.5, 28]].forEach(([cx, cy]) => {{
            const ct = new THREE.Mesh(new THREE.CylinderGeometry(1.4, 1.4, 2.2, 16), ctMat);
            ct.rotateX(Math.PI / 2);
            ct.position.set(cx, cy, 41.9);
            groups.AIR.add(ct);
          }});
          const bmuBase = new THREE.Mesh(new THREE.BoxGeometry(1.2, 1.2, 1.2), new THREE.MeshStandardMaterial({{ color: 0x475569 }}));
          bmuBase.position.set(10.5, 34, 41.4);
          groups.AIR.add(bmuBase);
          const bmuBoom = new THREE.Mesh(new THREE.BoxGeometry(6.2, 0.25, 0.25), new THREE.MeshStandardMaterial({{ color: 0xfacc15 }}));
          bmuBoom.position.set(8.5, 34, 42.2);
          groups.AIR.add(bmuBoom);

          // Tower 2 Roof: Official Corporate Helipad (13m diameter)
          const heliBase = new THREE.Mesh(new THREE.CylinderGeometry(6.2, 6.2, 0.4, 32), new THREE.MeshStandardMaterial({{ color: 0x1e293b, roughness: 0.9 }}));
          heliBase.rotateX(Math.PI / 2);
          heliBase.position.set(29.5, 30.5, 41.0);
          groups.AIR.add(heliBase);

          const ringMesh = new THREE.Mesh(new THREE.RingGeometry(3.8, 4.4, 32), new THREE.MeshBasicMaterial({{ color: 0xfacc15, side: THREE.DoubleSide }}));
          ringMesh.position.set(29.5, 30.5, 41.22);
          groups.AIR.add(ringMesh);

          const hMat = new THREE.MeshBasicMaterial({{ color: 0xffffff }});
          const hBar1 = new THREE.Mesh(new THREE.BoxGeometry(0.5, 2.8, 0.04), hMat);
          hBar1.position.set(28.4, 30.5, 41.25);
          groups.AIR.add(hBar1);
          const hBar2 = new THREE.Mesh(new THREE.BoxGeometry(0.5, 2.8, 0.04), hMat);
          hBar2.position.set(30.6, 30.5, 41.25);
          groups.AIR.add(hBar2);
          const hCross = new THREE.Mesh(new THREE.BoxGeometry(2.2, 0.5, 0.04), hMat);
          hCross.position.set(29.5, 30.5, 41.25);
          groups.AIR.add(hCross);

          for (let ha = 0; ha < Math.PI * 2; ha += Math.PI / 6) {{
            const hDot = new THREE.Mesh(new THREE.SphereGeometry(0.12, 6, 6), new THREE.MeshBasicMaterial({{ color: 0x22c55e }}));
            hDot.position.set(29.5 + Math.cos(ha) * 5.9, 30.5 + Math.sin(ha) * 5.9, 41.25);
            groups.AIR.add(hDot);
          }}

          // Tower 3 Roof: Heavy-Duty Telecommunications Spire Mast (Z = 41m to 54m)
          const mastMat = new THREE.MeshStandardMaterial({{ color: 0xe2e8f0, metalness: 0.9, roughness: 0.2 }});
          const commMast = new THREE.Mesh(new THREE.CylinderGeometry(0.15, 0.55, 13, 12), mastMat);
          commMast.rotateX(Math.PI / 2);
          commMast.position.set(10.5, 13.5, 47.3);
          groups.AIR.add(commMast);

          const dish = new THREE.Mesh(new THREE.SphereGeometry(1.1, 16, 8, 0, Math.PI * 2, 0, Math.PI / 2), new THREE.MeshStandardMaterial({{ color: 0xffffff, metalness: 0.6 }}));
          dish.position.set(10.5, 12.8, 48.5);
          dish.rotation.x = Math.PI / 3;
          groups.AIR.add(dish);

          const bcn1 = new THREE.Mesh(new THREE.SphereGeometry(0.35, 10, 10), new THREE.MeshBasicMaterial({{ color: 0xef4444 }}));
          bcn1.position.set(10.5, 13.5, 53.8);
          groups.AIR.add(bcn1);

          // Tower 4 Roof: Solar Photovoltaic Array (4 rows tilted towards South)
          const solarTex = getSolarPanelTexture();
          const solarMat = new THREE.MeshStandardMaterial({{ map: solarTex, roughness: 0.2, metalness: 0.8 }});
          for (let sy = 9.5; sy <= 17.5; sy += 2.5) {{
            const panelRow = new THREE.Mesh(new THREE.BoxGeometry(10.5, 1.8, 0.12), solarMat);
            panelRow.position.set(29.5, sy, 41.5);
            panelRow.rotation.x = 0.32;
            groups.AIR.add(panelRow);
          }}

          // -----------------------------------------------------------------
          // 6. GRAND ENTRANCE PLAZA, ROUNDABOUT & WATER FOUNTAIN (Ground Z = 0)
          // -----------------------------------------------------------------
          const roadMat = new THREE.MeshStandardMaterial({{ color: 0x1e293b, roughness: 0.95 }});
          const roadLoop = new THREE.Mesh(new THREE.RingGeometry(5.5, 11.5, 32, 1, 0, Math.PI), roadMat);
          roadLoop.rotation.z = Math.PI;
          roadLoop.position.set(20, -1.5, 0.02);
          groups.SUR.add(roadLoop);

          const fRim = new THREE.Mesh(new THREE.CylinderGeometry(3.6, 3.8, 0.45, 32), new THREE.MeshStandardMaterial({{ color: 0x64748b, roughness: 0.8 }}));
          fRim.rotateX(Math.PI / 2);
          fRim.position.set(20, -2.5, 0.22);
          groups.SUR.add(fRim);

          const fWater = new THREE.Mesh(new THREE.CylinderGeometry(3.2, 3.2, 0.35, 32), new THREE.MeshStandardMaterial({{ color: 0x0284c7, roughness: 0.05, transparent: true, opacity: 0.85 }}));
          fWater.rotateX(Math.PI / 2);
          fWater.position.set(20, -2.5, 0.3);
          groups.SUR.add(fWater);

          const fSpray = new THREE.Mesh(new THREE.ConeGeometry(0.6, 2.4, 16), new THREE.MeshBasicMaterial({{ color: 0xe0f2fe, transparent: true, opacity: 0.75 }}));
          fSpray.position.set(20, -2.5, 1.4);
          fSpray.rotation.x = Math.PI;
          groups.SUR.add(fSpray);

          [[7, -2], [12, -4], [28, -4], [33, -2], [3, 8], [37, 8]].forEach(([tx, ty]) => {{
            createPalmTree(tx, ty, 0);
          }});

          const totemCanvas = document.createElement('canvas');
          totemCanvas.width = 128; totemCanvas.height = 256;
          const tctx = totemCanvas.getContext('2d');
          tctx.fillStyle = '#0f172a'; tctx.fillRect(0, 0, 128, 256);
          tctx.fillStyle = '#facc15'; tctx.font = 'bold 16px sans-serif'; tctx.textAlign = 'center';
          tctx.fillText('L&T REALTY', 64, 50);
          tctx.fillStyle = '#ffffff'; tctx.font = 'bold 18px sans-serif';
          tctx.fillText('SEAWOODS', 64, 100);
          tctx.fillText('GRAND', 64, 130);
          tctx.fillText('CENTRAL', 64, 160);
          tctx.fillStyle = '#38bdf8'; tctx.font = 'bold 14px sans-serif';
          tctx.fillText('TOD STATION', 64, 210);
          const totemTex = new THREE.CanvasTexture(totemCanvas);
          const totemMesh = new THREE.Mesh(new THREE.BoxGeometry(1.6, 0.4, 4.2), new THREE.MeshStandardMaterial({{ map: totemTex }}));
          totemMesh.position.set(13, -1.0, 2.1);
          groups.SUR.add(totemMesh);

          // -----------------------------------------------------------------
          // 7. MULTI-LEVEL SUBSURFACE COMMUTER BASEMENTS (Z = -15m to 0m)
          // -----------------------------------------------------------------
          createPrism("SUB_B1_CONCOURSE", [[3, 3], [37, 3], [37, 37], [3, 37]], -5, 0, 0xf59e0b, 0.88, "SUB", -1, {{
            name: "Seawoods Commuter Ticket Concourse, Smart AFC Gates & Station Portals (Level B1)",
            ulpin: `${{data.base_ulpin}}-SUB-B01-TC01-M`,
            z: "-5.0m to 0.0m",
            area: "1156 m²",
            vol: "5780 m³",
            owner: "CIDCO & Central Railway Joint Concourse SPV",
            val: "₹ 340 Cr"
          }});

          createPrism("SUB_B2_PARKING", [[3, 3], [37, 3], [37, 37], [3, 37]], -10, -5, 0xd97706, 0.88, "SUB", -2, {{
            name: "CIDCO 1500-Vehicle Commuter Park-and-Ride Automated Facility (Level B2)",
            ulpin: `${{data.base_ulpin}}-SUB-B02-PR01-8`,
            z: "-10.0m to -5.0m",
            area: "1156 m²",
            vol: "5780 m³",
            owner: "CIDCO Urban Infrastructure Authority (Park-and-Ride)",
            val: "₹ 260 Cr"
          }});

          const pillarMat = new THREE.MeshStandardMaterial({{ color: 0x94a3b8, roughness: 0.9 }});
          for (let px = 7; px <= 33; px += 6.5) {{
            for (let py = 7; py <= 33; py += 6.5) {{
              const pillar = new THREE.Mesh(new THREE.BoxGeometry(0.8, 0.8, 5.0), pillarMat);
              pillar.position.set(px, py, -7.5);
              groups.SUB.add(pillar);
            }}
          }}

          createPrism("SUB_B3_UTILITY", [[3, 3], [37, 3], [37, 37], [3, 37]], -15, -10, 0xb45309, 0.92, "SUB", -3, {{
            name: "Central Railway Traction Substation & District Chilled Water Plant (Level B3)",
            ulpin: `${{data.base_ulpin}}-SUB-B03-UT01-4`,
            z: "-15.0m to -10.0m",
            area: "1156 m²",
            vol: "5780 m³",
            owner: "Central Railway Electrification & CIDCO MEP Directorate",
            val: "₹ 410 Cr"
          }});
        }}

        // ARCHETYPE 7: DLF Cyber City Building 10 (Gurugram) - Curved Chevron Twin Towers, Skybridge & Rapid Metro
        function buildSkybridgeTwin(data) {{
          // Real-World DLF Cyber City Building 10 Architecture:
          // Two iconic curved chevron / boomerang towers facing each other across an open landscaped plaza,
          // connected by a 2-storey suspended steel truss glass skybridge, with the Gurugram Rapid Metro viaduct & train!

          const tenantsAlpha = [
            "DLF Cyber Hub Executive Reception & Portals",
            "Google India Pvt. Ltd. (Digital Marketing & Ads Hub)",
            "KPMG Global Services Private Limited",
            "Deloitte Shared Services India LLP",
            "Boston Consulting Group (BCG) India",
            "American Express India Private Limited",
            "McKinsey & Company (NCR Strategic Consulting Unit)"
          ];

          const tenantsBeta = [
            "DLF Corporate Client Services & Executive Concierge",
            "Microsoft Corporation (India) Pvt. Ltd.",
            "Ernst & Young (EY) Global Delivery Services",
            "Amazon Web Services (AWS) India Cloud Tech",
            "Cisco Systems India Private Limited",
            "Cognizant Technology Solutions India",
            "IBM India Client Innovation Center"
          ];

          // 1. Tower 10A (West Curved Chevron Wing)
          const polyA = [[4, 8], [9, 7], [16, 9], [17, 18], [15, 27], [10, 34], [4, 34], [6, 26], [8, 18], [4, 12]];
          for (let f = 0; f <= 6; f++) {{
            const zMin = f * 4.8;
            const zMax = zMin + 4.8;
            const lvl = f === 0 ? "G00" : `F0${{f}}`;
            createPrism(`BLD_T1_F0${{f}}`, polyA, zMin, zMax, 0x1e40af, 0.88, "BLD", f, {{
              name: `DLF CyberCity Epitome Tower 10A (${{lvl}})`,
              ulpin: `${{data.base_ulpin}}-BLD-${{lvl}}-T10A-G`,
              z: `${{zMin.toFixed(1)}}m to ${{zMax.toFixed(1)}}m`,
              area: "310 m²",
              vol: "1488 m³",
              owner: tenantsAlpha[f] || "Fortune 500 Enterprise Tenant",
              val: "₹ 46.0 Cr"
            }});

            // Silver metallic horizontal spandrel louvers at slab
            const spMesh = new THREE.Mesh(new THREE.BoxGeometry(13, 0.4, 0.45), new THREE.MeshStandardMaterial({{ color: 0x94a3b8, metalness: 0.85, roughness: 0.2 }}));
            spMesh.position.set(10, 18, zMin + 0.2);
            groups.BLD.add(spMesh);
          }}

          // 2. Tower 10B (East Curved Chevron Wing)
          const polyB = [[36, 8], [31, 7], [24, 9], [23, 18], [25, 27], [30, 34], [36, 34], [34, 26], [32, 18], [36, 12]];
          for (let f = 0; f <= 6; f++) {{
            const zMin = f * 4.8;
            const zMax = zMin + 4.8;
            const lvl = f === 0 ? "G00" : `F0${{f}}`;
            createPrism(`BLD_T2_F0${{f}}`, polyB, zMin, zMax, 0x2563eb, 0.88, "BLD", f, {{
              name: `DLF CyberCity Epitome Tower 10B (${{lvl}})`,
              ulpin: `${{data.base_ulpin}}-BLD-${{lvl}}-T10B-H`,
              z: `${{zMin.toFixed(1)}}m to ${{zMax.toFixed(1)}}m`,
              area: "310 m²",
              vol: "1488 m³",
              owner: tenantsBeta[f] || "Fortune 500 Enterprise Tenant",
              val: "₹ 46.0 Cr"
            }});

            // Silver metallic horizontal spandrel louvers at slab
            const spMeshB = new THREE.Mesh(new THREE.BoxGeometry(13, 0.4, 0.45), new THREE.MeshStandardMaterial({{ color: 0x94a3b8, metalness: 0.85, roughness: 0.2 }}));
            spMeshB.position.set(30, 18, zMin + 0.2);
            groups.BLD.add(spMeshB);
          }}

          // 3. Suspended 2-Storey High-Rise Curved Glass Skybridge (Floors 4-5, 19.2 to 25.6m)
          createPrism("BLD_SKYBRIDGE", [[16, 16], [24, 16], [24, 26], [16, 26]], 19.2, 25.6, 0x38bdf8, 0.82, "COM", 4, {{
            name: "DLF CyberCity Suspended Executive Skybridge & Collaboration Deck",
            ulpin: `${{data.base_ulpin}}-COM-F04-SB02-K`,
            z: "+19.2m to +25.6m",
            area: "128 m²",
            vol: "819 m³",
            owner: "DLF Executive Collaboration Center (Shared Tenant Facility)",
            val: "₹ 48.0 Cr"
          }});

          // Diamond Structural Steel Truss Bracing on Skybridge sides
          const trussMat = new THREE.LineBasicMaterial({{ color: 0xe2e8f0, linewidth: 2 }});
          const trussGeo = new THREE.BufferGeometry();
          const tPts = [];
          for (let tx = 16; tx <= 22; tx += 2) {{
            tPts.push(new THREE.Vector3(tx, 16.05, 19.2), new THREE.Vector3(tx + 1, 16.05, 25.6));
            tPts.push(new THREE.Vector3(tx + 1, 16.05, 25.6), new THREE.Vector3(tx + 2, 16.05, 19.2));
            tPts.push(new THREE.Vector3(tx, 25.95, 19.2), new THREE.Vector3(tx + 1, 25.95, 25.6));
            tPts.push(new THREE.Vector3(tx + 1, 25.95, 25.6), new THREE.Vector3(tx + 2, 25.95, 19.2));
          }}
          trussGeo.setFromPoints(tPts);
          groups.COM.add(new THREE.LineSegments(trussGeo, trussMat));

          // Skybridge Interior Warm Lighting Slab
          const glowBox = new THREE.Mesh(new THREE.BoxGeometry(7.6, 9.6, 6.0), new THREE.MeshBasicMaterial({{ color: 0xfef08a, transparent: true, opacity: 0.28 }}));
          glowBox.position.set(20, 21, 22.4);
          groups.COM.add(glowBox);

          // 4. Ground Level Plazas, Cyber Hub Connector & Portes-Cochères
          const courtyardGeo = new THREE.BoxGeometry(12, 28, 0.15);
          const courtyardMat = new THREE.MeshStandardMaterial({{ color: 0x1e293b, roughness: 0.8 }});
          const courtyard = new THREE.Mesh(courtyardGeo, courtyardMat);
          courtyard.position.set(20, 21, 0.1);
          groups.SUR.add(courtyard);

          // Cantilevered Entrance Canopies (Portes-Cochères)
          const canopyMat = new THREE.MeshStandardMaterial({{ color: 0x475569, metalness: 0.7, roughness: 0.2 }});
          const c1 = new THREE.Mesh(new THREE.BoxGeometry(7, 4.5, 0.35), canopyMat);
          c1.position.set(9, 6.2, 4.2);
          groups.BLD.add(c1);
          const c2 = new THREE.Mesh(new THREE.BoxGeometry(7, 4.5, 0.35), canopyMat);
          c2.position.set(31, 6.2, 4.2);
          groups.BLD.add(c2);

          // 5. Authentic Gurugram Rapid Metro Viaduct & Detailed 3-Car Rolling Stock
          // Concrete Segmental Box-Girder Guideway
          createPrism("AIR_METRO", [[-6, 1.5], [46, 1.5], [46, 5.0], [-6, 5.0]], 7.4, 8.6, 0x64748b, 0.95, "AIR", 2, {{
            name: "Gurugram Rapid Metro Elevated Segmental Concrete Guideway",
            ulpin: `${{data.base_ulpin}}-AIR-E01-RM01-R`,
            z: "+7.4m to +8.6m",
            area: "182 m²",
            vol: "218 m³",
            owner: "Haryana Mass Rapid Transport Corp (Rapid Metro SPV)",
            val: "₹ 95.0 Cr"
          }});

          // Parapet Crash Barriers
          const parapetMat = new THREE.MeshStandardMaterial({{ color: 0x475569, roughness: 0.9 }});
          const p1 = new THREE.Mesh(new THREE.BoxGeometry(52, 0.3, 0.8), parapetMat);
          p1.position.set(20, 1.65, 9.0);
          groups.AIR.add(p1);
          const p2 = new THREE.Mesh(new THREE.BoxGeometry(52, 0.3, 0.8), parapetMat);
          p2.position.set(20, 4.85, 9.0);
          groups.AIR.add(p2);

          // Concrete Cylindrical Piers with Inverted Trapezoid Crossheads
          [-2, 10, 20, 30, 42].forEach(px => {{
            const pierGeo = new THREE.CylinderGeometry(0.55, 0.65, 7.4, 16);
            pierGeo.rotateX(Math.PI / 2);
            const pierMesh = new THREE.Mesh(pierGeo, new THREE.MeshStandardMaterial({{ color: 0x64748b, roughness: 0.8 }}));
            pierMesh.position.set(px, 3.25, 3.7);
            groups.AIR.add(pierMesh);

            const crosshead = new THREE.Mesh(new THREE.BoxGeometry(2.4, 3.8, 0.8), new THREE.MeshStandardMaterial({{ color: 0x475569, roughness: 0.8 }}));
            crosshead.position.set(px, 3.25, 7.0);
            groups.AIR.add(crosshead);
          }});

          // Twin Steel Running Rails & 750V DC Conductor Rail
          const railMat = new THREE.MeshStandardMaterial({{ color: 0x334155, metalness: 0.9, roughness: 0.2 }});
          [2.6, 3.9].forEach(ry => {{
            const rail = new THREE.Mesh(new THREE.BoxGeometry(52, 0.15, 0.2), railMat);
            rail.position.set(20, ry, 8.7);
            groups.AIR.add(rail);
          }});

          // 3-Car Rapid Metro Train Model (Silver & Electric Blue CSR Zhuzhou trainset)
          const carBodyMat = new THREE.MeshStandardMaterial({{ color: 0xe2e8f0, metalness: 0.8, roughness: 0.25 }});
          const blueStripeMat = new THREE.MeshBasicMaterial({{ color: 0x2563eb }});
          const windowMat = new THREE.MeshStandardMaterial({{ color: 0x0f172a, roughness: 0.1 }});
          const cabGlassMat = new THREE.MeshStandardMaterial({{ color: 0x1e293b, roughness: 0.1 }});
          const hvacMat = new THREE.MeshStandardMaterial({{ color: 0x475569, roughness: 0.6 }});

          const trainCars = [
            {{ x: 14.5, isCab: "west" }},
            {{ x: 21.0, isCab: false }},
            {{ x: 27.5, isCab: "east" }}
          ];

          trainCars.forEach(tc => {{
            // Coach body
            const coach = new THREE.Mesh(new THREE.BoxGeometry(6.0, 2.0, 1.8), carBodyMat);
            coach.position.set(tc.x, 3.25, 9.8);
            groups.AIR.add(coach);

            // Electric Blue Livery Stripe
            const stripe = new THREE.Mesh(new THREE.BoxGeometry(6.05, 2.05, 0.35), blueStripeMat);
            stripe.position.set(tc.x, 3.25, 9.55);
            groups.AIR.add(stripe);

            // Side Windows
            const wL = new THREE.Mesh(new THREE.BoxGeometry(5.2, 0.05, 0.65), windowMat);
            wL.position.set(tc.x, 2.22, 9.9);
            groups.AIR.add(wL);
            const wR = new THREE.Mesh(new THREE.BoxGeometry(5.2, 0.05, 0.65), windowMat);
            wR.position.set(tc.x, 4.28, 9.9);
            groups.AIR.add(wR);

            // Roof HVAC Unit
            const hvac = new THREE.Mesh(new THREE.BoxGeometry(2.4, 1.2, 0.3), hvacMat);
            hvac.position.set(tc.x, 3.25, 10.85);
            groups.AIR.add(hvac);

            // Aerodynamic nose for driving motor cabs
            if (tc.isCab === "west") {{
              const cabW = new THREE.Mesh(new THREE.BoxGeometry(0.8, 1.8, 1.4), cabGlassMat);
              cabW.position.set(tc.x - 3.2, 3.25, 9.7);
              groups.AIR.add(cabW);
            }} else if (tc.isCab === "east") {{
              const cabE = new THREE.Mesh(new THREE.BoxGeometry(0.8, 1.8, 1.4), cabGlassMat);
              cabE.position.set(tc.x + 3.2, 3.25, 9.7);
              groups.AIR.add(cabE);
            }}
          }});

          // 6. Rooftop Industrial MEP Plants (Tower 10A & 10B)
          // Cooling towers
          [10, 30].forEach(cx => {{
            const ctGeo = new THREE.CylinderGeometry(1.6, 1.6, 2.2, 20);
            ctGeo.rotateX(Math.PI / 2);
            const ctMesh = new THREE.Mesh(ctGeo, new THREE.MeshStandardMaterial({{ color: 0x334155, roughness: 0.7 }}));
            ctMesh.position.set(cx, 26, 34.7);
            groups.AIR.add(ctMesh);
          }});

          // Heavy-duty BMU window washing crane rig
          const bmuBase = new THREE.Mesh(new THREE.BoxGeometry(1.2, 1.2, 1.5), new THREE.MeshStandardMaterial({{ color: 0x475569 }}));
          bmuBase.position.set(10, 14, 34.4);
          groups.AIR.add(bmuBase);
          const bmuArm = new THREE.Mesh(new THREE.BoxGeometry(5.0, 0.3, 0.3), new THREE.MeshStandardMaterial({{ color: 0xfacc15 }}));
          bmuArm.position.set(8.0, 14, 35.3);
          groups.AIR.add(bmuArm);

          // Rooftop Communications Mast with dual blinking obstruction lights
          const mastGeo = new THREE.CylinderGeometry(0.15, 0.4, 12, 12);
          mastGeo.rotateX(Math.PI / 2);
          const mast = new THREE.Mesh(mastGeo, new THREE.MeshStandardMaterial({{ color: 0xe2e8f0, metalness: 0.8 }}));
          mast.position.set(30, 20, 39.6);
          groups.AIR.add(mast);

          const redBcn = new THREE.Mesh(new THREE.SphereGeometry(0.4, 12, 12), new THREE.MeshBasicMaterial({{ color: 0xef4444 }}));
          redBcn.position.set(30, 20, 45.8);
          groups.AIR.add(redBcn);

          // 7. Corporate Subsurface Basements
          createPrism("SUB_CYBER_B1", [[4,7],[36,7],[36,34],[4,34]], -7, 0, 0xf59e0b, 0.85, "SUB", -1, {{
            name: "DLF CyberCity Subsurface Transit Shuttle Terminal & Delivery Docks (B1)",
            ulpin: `${{data.base_ulpin}}-SUB-B01-CC01-5`,
            z: "-7.0m to 0.0m",
            area: "864 m²",
            vol: "6048 m³",
            owner: "Gurugram Rapid Metro Shuttle Terminal & Delivery Docks",
            val: "₹ 85.0 Cr"
          }});

          createPrism("SUB_CYBER_B2", [[4,7],[36,7],[36,34],[4,34]], -14, -7, 0xd97706, 0.85, "SUB", -2, {{
            name: "DLF CyberCity Corporate Subsurface Security & Energy Substation (B2)",
            ulpin: `${{data.base_ulpin}}-SUB-B02-CC02-6`,
            z: "-14.0m to -7.0m",
            area: "864 m²",
            vol: "6048 m³",
            owner: "DLF Corporate Subsurface Security & Central Energy Plant",
            val: "₹ 110 Cr"
          }});
        }}

        // ARCHETYPE 8: Subterranean Multilevel Cavern (Rajiv Chowk, BKC Metro-3, Cubbon Park, Chennai Central)
        function buildSubterraneanCavern(data) {{
          // 1. Surface Level Plaza & Iconic Metro Glass Pyramid / Pavilion (Z = 0.0 to 4.5m)
          // Surface Plaza Granite Pavement
          const plazaGeo = new THREE.BoxGeometry(36, 36, 0.2);
          const plazaMat = new THREE.MeshStandardMaterial({{ color: 0x334155, roughness: 0.85 }});
          const plaza = new THREE.Mesh(plazaGeo, plazaMat);
          plaza.position.set(20, 20, 0.1);
          groups.SUR.add(plaza);

          // Surface Metro Entry Pavilion (Steel Frame & High-Translucency Glass)
          createPrism("SUR_ENTRANCE", [[12, 12], [28, 12], [28, 28], [12, 28]], 0, 4.5, 0x38bdf8, 0.72, "BLD", 0, {{
            name: `Surface Metro Transit Pavilion & Entry Portals (${{data.name}})`,
            ulpin: `${{data.base_ulpin}}-SUR-G00-EN01-2`,
            z: "0.0m to +4.5m",
            area: "256 m²",
            vol: "1152 m³",
            owner: data.owner,
            val: "₹ 55.0 Cr"
          }});

          // Angular Space-Frame Steel Roof Truss on Entrance Pavilion
          const pRoofGeo = new THREE.ConeGeometry(12, 3.2, 4);
          pRoofGeo.rotateZ(Math.PI / 4);
          pRoofGeo.rotateX(Math.PI / 2);
          const pRoofMat = new THREE.MeshStandardMaterial({{ color: 0x0284c7, transparent: true, opacity: 0.65, roughness: 0.2 }});
          const pRoof = new THREE.Mesh(pRoofGeo, pRoofMat);
          pRoof.position.set(20, 20, 5.8);
          groups.BLD.add(pRoof);

          // Station Identification Totem Monolith (Bilingual Station Signage)
          const isDelhi = data.name && data.name.includes("Rajiv");
          const isMumbai = data.name && data.name.includes("BKC");
          const stationHi = isDelhi ? "राजीव चौक" : (isMumbai ? "बीकेसी मेट्रो" : "मेट्रो स्थानक");
          const stationEn = isDelhi ? "RAJIV CHOWK • INTERCHANGE" : (isMumbai ? "BKC METRO-3 • AQUA LINE" : (data.name.toUpperCase()));
          createStationSignboard(stationHi, stationEn, 20, 9.5, 2.2, 0);

          // Surface Escalator Portal Descent Ramp (Angled Void into B1)
          const escMat = new THREE.MeshStandardMaterial({{ color: 0x64748b, metalness: 0.8, roughness: 0.3 }});
          const esc1 = new THREE.Mesh(new THREE.BoxGeometry(3.2, 7.5, 0.3), escMat);
          esc1.rotation.x = Math.PI / 6;
          esc1.position.set(16.5, 16.5, 1.2);
          groups.BLD.add(esc1);
          const esc2 = new THREE.Mesh(new THREE.BoxGeometry(3.2, 7.5, 0.3), escMat);
          esc2.rotation.x = Math.PI / 6;
          esc2.position.set(23.5, 16.5, 1.2);
          groups.BLD.add(esc2);

          // Surface Ventilation & Smoke Extraction Shafts (Dual Louvered Concrete Towers)
          [6, 34].forEach(vx => {{
            const vGeo = new THREE.BoxGeometry(3.2, 3.2, 3.8);
            const vMat = new THREE.MeshStandardMaterial({{ color: 0x475569, roughness: 0.7 }});
            const vMesh = new THREE.Mesh(vGeo, vMat);
            vMesh.position.set(vx, 32, 1.9);
            groups.AIR.add(vMesh);

            // Louver grill texture lines
            const grill = new THREE.Mesh(new THREE.BoxGeometry(3.3, 0.1, 2.2), new THREE.MeshBasicMaterial({{ color: 0x0f172a }}));
            grill.position.set(vx, 30.3, 2.0);
            groups.AIR.add(grill);
          }});

          // Public Plaza Amenities: Bike Racks, Bollards & Trees
          const bMat = new THREE.MeshStandardMaterial({{ color: 0x94a3b8, metalness: 0.9 }});
          for (let bx = 8; bx <= 32; bx += 4) {{
            const bol = new THREE.Mesh(new THREE.CylinderGeometry(0.12, 0.12, 0.9, 12), bMat);
            bol.position.set(bx, 5.5, 0.45);
            bol.rotation.x = Math.PI / 2;
            groups.SUR.add(bol);
          }}

          // 2. Level B1: Grand Ticketing Concourse, Retail Arcade & Smart AFC Flap Gates (Z = -7.0m to 0.0m)
          createPrism("SUB_B1_CONCOURSE", [[4, 4], [36, 4], [36, 36], [4, 36]], -7, 0, 0xf59e0b, 0.85, "SUB", -1, {{
            name: "Subsurface Concourse, AFC Smart Gates & Retail Arcade (Level B1)",
            ulpin: `${{data.base_ulpin}}-SUB-B01-TC01-M`,
            z: "-7.0m to 0.0m",
            area: "1024 m²",
            vol: "7168 m³",
            owner: data.owner,
            val: "₹ 290 Cr"
          }});

          // Row of Smart Automatic Fare Collection (AFC) Flap Turnstiles (8 Gates)
          const afcMat = new THREE.MeshStandardMaterial({{ color: 0x0284c7, metalness: 0.7, roughness: 0.3 }});
          const flapGreen = new THREE.MeshBasicMaterial({{ color: 0x22c55e }});
          for (let gx = 10; gx <= 30; gx += 2.8) {{
            const afcGate = new THREE.Mesh(new THREE.BoxGeometry(0.35, 1.8, 1.2), afcMat);
            afcGate.position.set(gx, 20, -3.5);
            groups.SUB.add(afcGate);

            const flap = new THREE.Mesh(new THREE.BoxGeometry(0.1, 0.6, 0.45), flapGreen);
            flap.position.set(gx, 20, -3.2);
            groups.SUB.add(flap);
          }}

          // Security Baggage X-Ray Scanner & Walk-Through Metal Detector (DFMD)
          const xrayBox = new THREE.Mesh(new THREE.BoxGeometry(3.5, 1.2, 1.4), new THREE.MeshStandardMaterial({{ color: 0x334155 }}));
          xrayBox.position.set(12, 14, -3.5);
          groups.SUB.add(xrayBox);
          const dfmd = new THREE.Mesh(new THREE.BoxGeometry(0.3, 1.2, 2.2), new THREE.MeshStandardMaterial({{ color: 0x475569 }}));
          dfmd.position.set(14.2, 14, -3.2);
          groups.SUB.add(dfmd);

          // Customer Care & Token Recharge Booth
          const booth = new THREE.Mesh(new THREE.BoxGeometry(4.5, 2.5, 2.2), new THREE.MeshStandardMaterial({{ color: 0x0f172a, roughness: 0.5 }}));
          booth.position.set(28, 14, -3.5);
          groups.SUB.add(booth);
          const boothWin = new THREE.Mesh(new THREE.BoxGeometry(3.8, 0.1, 1.0), new THREE.MeshBasicMaterial({{ color: 0x7dd3fc }}));
          boothWin.position.set(28, 12.7, -3.2);
          groups.SUB.add(boothWin);

          // Overhead Directional Line Signage
          const signCanvas = document.createElement('canvas');
          signCanvas.width = 512; signCanvas.height = 64;
          const sctx = signCanvas.getContext('2d');
          sctx.fillStyle = '#0f172a'; sctx.fillRect(0, 0, 512, 64);
          sctx.fillStyle = '#eab308'; sctx.font = 'bold 20px sans-serif';
          sctx.fillText('◀ LINE 1: YELLOW LINE', 30, 40);
          sctx.fillStyle = '#38bdf8';
          sctx.fillText('LINE 2: BLUE LINE ▶', 310, 40);
          const sTex = new THREE.CanvasTexture(signCanvas);
          const oSign = new THREE.Mesh(new THREE.BoxGeometry(16, 0.2, 1.2), new THREE.MeshBasicMaterial({{ map: sTex }}));
          oSign.position.set(20, 24, -1.8);
          groups.SUB.add(oSign);

          // Structural Heavy Concrete Columns
          const colMat = new THREE.MeshStandardMaterial({{ color: 0x64748b, roughness: 0.9 }});
          [9, 20, 31].forEach(cx => {{
            [9, 31].forEach(cy => {{
              const col = new THREE.Mesh(new THREE.BoxGeometry(1.2, 1.2, 7.0), colMat);
              col.position.set(cx, cy, -3.5);
              groups.SUB.add(col);
            }});
          }});

          // 3. Level B2: Environmental Control, Traction Substation & Telemetry Vault (Z = -15.0m to -7.0m)
          createPrism("SUB_B2_PLANT", [[6, 6], [34, 6], [34, 34], [6, 34]], -15, -7, 0xd97706, 0.88, "SUB", -2, {{
            name: "Environmental Control, Traction Power & Signal Interlocking Vault (Level B2)",
            ulpin: `${{data.base_ulpin}}-SUB-B02-PL01-8`,
            z: "-15.0m to -7.0m",
            area: "784 m²",
            vol: "6272 m³",
            owner: data.owner,
            val: "₹ 230 Cr"
          }});

          // Large Industrial Tunnel Ventilation Fans (TVF - Dual Ducted Axial Fans)
          [13, 27].forEach(fx => {{
            const fanGeo = new THREE.CylinderGeometry(1.6, 1.6, 4.5, 24);
            fanGeo.rotateZ(Math.PI / 2);
            const fan = new THREE.Mesh(fanGeo, new THREE.MeshStandardMaterial({{ color: 0x334155, metalness: 0.8, roughness: 0.3 }}));
            fan.position.set(fx, 30, -11.0);
            groups.SUB.add(fan);

            const fanHub = new THREE.Mesh(new THREE.CylinderGeometry(0.5, 0.5, 4.6, 16), new THREE.MeshBasicMaterial({{ color: 0xfacc15 }}));
            fanHub.rotateZ(Math.PI / 2);
            fanHub.position.set(fx, 30, -11.0);
            groups.SUB.add(fanHub);
          }});

          // 25kV Traction Power Transformer Units with Safety Enclosures
          const tr1 = new THREE.Mesh(new THREE.BoxGeometry(5.0, 3.5, 3.2), new THREE.MeshStandardMaterial({{ color: 0x475569, roughness: 0.6 }}));
          tr1.position.set(12, 12, -11.0);
          groups.SUB.add(tr1);
          const trWarn = new THREE.Mesh(new THREE.BoxGeometry(1.5, 0.1, 0.8), new THREE.MeshBasicMaterial({{ color: 0xef4444 }}));
          trWarn.position.set(12, 10.2, -11.0);
          groups.SUB.add(trWarn);

          // SCADA Telemetry & Signal Interlocking Server Racks
          for (let rx = 22; rx <= 30; rx += 2.2) {{
            const rack = new THREE.Mesh(new THREE.BoxGeometry(1.4, 2.8, 4.0), new THREE.MeshStandardMaterial({{ color: 0x0f172a, roughness: 0.4 }}));
            rack.position.set(rx, 12, -11.0);
            groups.SUB.add(rack);

            const leds = new THREE.Mesh(new THREE.BoxGeometry(1.2, 0.1, 0.3), new THREE.MeshBasicMaterial({{ color: 0x22c55e }}));
            leds.position.set(rx, 10.55, -10.0);
            groups.SUB.add(leds);
          }}

          // 4. Level B3: Deep Passenger Island Platform & Dual Running Tracks (Z = -24.0m to -15.0m)
          createPrism("SUB_B3_PLATFORM", [[13, 4], [27, 4], [27, 36], [13, 36]], -24, -15, 0xb45309, 0.94, "SUB", -3, {{
            name: "Underground Passenger Island Platform & Dual Track Slabs (Level B3)",
            ulpin: `${{data.base_ulpin}}-SUB-B03-PF01-4`,
            z: "-24.0m to -15.0m",
            area: "448 m²",
            vol: "4032 m³",
            owner: data.owner,
            val: "₹ 380 Cr"
          }});

          // Platform Yellow Tactile Edge Warning Strips
          const tacMat = new THREE.MeshBasicMaterial({{ color: 0xfacc15 }});
          const tacW = new THREE.Mesh(new THREE.BoxGeometry(0.35, 32, 0.1), tacMat);
          tacW.position.set(13.2, 20, -18.9);
          groups.SUB.add(tacW);
          const tacE = new THREE.Mesh(new THREE.BoxGeometry(0.35, 32, 0.1), tacMat);
          tacE.position.set(26.8, 20, -18.9);
          groups.SUB.add(tacE);

          // Platform Screen Doors (PSDs - Full-Height Glazed Safety Wall)
          const psdMat = new THREE.MeshStandardMaterial({{ color: 0x38bdf8, transparent: true, opacity: 0.45, roughness: 0.1 }});
          const psdW = new THREE.Mesh(new THREE.BoxGeometry(0.15, 32, 2.6), psdMat);
          psdW.position.set(13.0, 20, -17.6);
          groups.SUB.add(psdW);
          const psdE = new THREE.Mesh(new THREE.BoxGeometry(0.15, 32, 2.6), psdMat);
          psdE.position.set(27.0, 20, -17.6);
          groups.SUB.add(psdE);

          // Dual Running Tunnels with Concrete Trackbed & Steel Rails
          const trackX = [8.5, 31.5];
          trackX.forEach((tx, idx) => {{
            // Circular bored tunnel sleeve
            const tGeo = new THREE.CylinderGeometry(3.6, 3.6, 44, 28);
            tGeo.rotateX(Math.PI / 2);
            const tMat = new THREE.MeshStandardMaterial({{ color: 0xec4899, roughness: 0.4, transparent: true, opacity: 0.75 }});
            const tMesh = new THREE.Mesh(tGeo, tMat);
            tMesh.position.set(tx, 20, -20.2);
            groups.UTL.add(tMesh);
            meshMap.set(`UTL_TUBE_${{idx}}`, tMesh);

            // Concrete trackbed slab
            const bed = new THREE.Mesh(new THREE.BoxGeometry(3.2, 42, 0.4), new THREE.MeshStandardMaterial({{ color: 0x475569 }}));
            bed.position.set(tx, 20, -22.5);
            groups.UTL.add(bed);

            // Steel running rails
            const rMat = new THREE.MeshStandardMaterial({{ color: 0xe2e8f0, metalness: 0.95, roughness: 0.2 }});
            const r1 = new THREE.Mesh(new THREE.BoxGeometry(0.12, 42, 0.2), rMat);
            r1.position.set(tx - 0.72, 20, -22.2);
            groups.UTL.add(r1);
            const r2 = new THREE.Mesh(new THREE.BoxGeometry(0.12, 42, 0.2), rMat);
            r2.position.set(tx + 0.72, 20, -22.2);
            groups.UTL.add(r2);

            // 25kV Overhead Rigid Catenary Conductor Rail (ROCS) on Ceiling
            const rocs = new THREE.Mesh(new THREE.BoxGeometry(0.25, 42, 0.3), new THREE.MeshStandardMaterial({{ color: 0xf59e0b, metalness: 0.8 }}));
            rocs.position.set(tx, 20, -16.8);
            groups.UTL.add(rocs);
          }});

          // Detailed 4-Coach Modern Underground Metro Train on West Track
          const trainX = 8.5;
          const coachMat = new THREE.MeshStandardMaterial({{ color: 0xf1f5f9, metalness: 0.85, roughness: 0.25 }});
          const lineStripeMat = new THREE.MeshBasicMaterial({{ color: isDelhi ? 0xeab308 : (isMumbai ? 0x06b6d4 : 0xa855f7) }});
          const winMat = new THREE.MeshStandardMaterial({{ color: 0x0284c7, roughness: 0.1 }});

          [-12, -4, 4, 12].forEach((cy, cIdx) => {{
            // Main Coach Body
            const coach = new THREE.Mesh(new THREE.BoxGeometry(2.6, 7.2, 2.5), coachMat);
            coach.position.set(trainX, 20 + cy, -20.2);
            groups.UTL.add(coach);

            // Route Colour Livery Band
            const stripe = new THREE.Mesh(new THREE.BoxGeometry(2.64, 7.25, 0.4), lineStripeMat);
            stripe.position.set(trainX, 20 + cy, -20.6);
            groups.UTL.add(stripe);

            // Windows
            const wL = new THREE.Mesh(new THREE.BoxGeometry(0.1, 6.2, 0.8), winMat);
            wL.position.set(trainX - 1.32, 20 + cy, -19.8);
            groups.UTL.add(wL);
            const wR = new THREE.Mesh(new THREE.BoxGeometry(0.1, 6.2, 0.8), winMat);
            wR.position.set(trainX + 1.32, 20 + cy, -19.8);
            groups.UTL.add(wR);

            // Roof HVAC Pod
            const hvac = new THREE.Mesh(new THREE.BoxGeometry(1.6, 2.8, 0.35), new THREE.MeshStandardMaterial({{ color: 0x64748b }}));
            hvac.position.set(trainX, 20 + cy, -18.8);
            groups.UTL.add(hvac);

            // Front driving cab nose & headlights on lead coach
            if (cIdx === 3) {{
              const cabNose = new THREE.Mesh(new THREE.BoxGeometry(2.4, 0.8, 1.8), new THREE.MeshStandardMaterial({{ color: 0x0f172a }}));
              cabNose.position.set(trainX, 20 + cy + 3.8, -20.2);
              groups.UTL.add(cabNose);

              const hl1 = new THREE.Mesh(new THREE.SphereGeometry(0.2, 8, 8), new THREE.MeshBasicMaterial({{ color: 0xfef08a }}));
              hl1.position.set(trainX - 0.7, 20 + cy + 4.2, -20.8);
              groups.UTL.add(hl1);
              const hl2 = hl1.clone();
              hl2.position.set(trainX + 0.7, 20 + cy + 4.2, -20.8);
              groups.UTL.add(hl2);
            }}
          }});
        }}

        // ARCHETYPE 9: Hooghly Underwater Subsurface Corridor (Kolkata) - India's 1st Under-River Metro
        function buildUnderwaterShieldTunnel(data) {{
          // 1. Translucent Navigable Hooghly River Water Surface (Z = -2.0m to 0.0m)
          const wGeo = new THREE.PlaneGeometry(64, 64);
          const wMat = new THREE.MeshStandardMaterial({{
            color: 0x0284c7,
            transparent: true,
            opacity: 0.5,
            roughness: 0.08,
            metalness: 0.3
          }});
          const wMesh = new THREE.Mesh(wGeo, wMat);
          wMesh.position.set(20, 20, -1.0);
          groups.SUR.add(wMesh);

          // River Channel Fairway Marker Buoys (Starboard Green & Port Red)
          const buoyData = [
            {{ x: 8, y: 20, clr: 0x22c55e, name: "Starboard Channel Fairway Buoy" }},
            {{ x: 32, y: 20, clr: 0xef4444, name: "Port Channel Fairway Buoy" }}
          ];
          buoyData.forEach(b => {{
            const bGeo = new THREE.CylinderGeometry(0.6, 0.8, 1.4, 16);
            bGeo.rotateX(Math.PI / 2);
            const bMesh = new THREE.Mesh(bGeo, new THREE.MeshStandardMaterial({{ color: b.clr, roughness: 0.4 }}));
            bMesh.position.set(b.x, b.y, 0.1);
            groups.SUR.add(bMesh);

            // Solar flashing LED lantern on top
            const lGeo = new THREE.SphereGeometry(0.2, 8, 8);
            const lMesh = new THREE.Mesh(lGeo, new THREE.MeshBasicMaterial({{ color: b.clr }}));
            lMesh.position.set(b.x, b.y, 1.1);
            groups.SUR.add(lMesh);
          }});

          // Historic Hooghly Passenger Ferry / River Launch Boat cruising on water surface
          const boatHull = new THREE.Mesh(new THREE.BoxGeometry(4.2, 10.0, 1.4), new THREE.MeshStandardMaterial({{ color: 0xf8fafc, roughness: 0.4 }}));
          boatHull.position.set(20, 20, 0.2);
          groups.SUR.add(boatHull);

          const boatCabin = new THREE.Mesh(new THREE.BoxGeometry(3.2, 5.5, 1.2), new THREE.MeshStandardMaterial({{ color: 0x1e293b, roughness: 0.2 }}));
          boatCabin.position.set(20, 19.5, 1.3);
          groups.SUR.add(boatCabin);

          // Indian National Flag at Stern of Ferry
          const mastPole = new THREE.Mesh(new THREE.CylinderGeometry(0.04, 0.04, 2.0, 8), new THREE.MeshStandardMaterial({{ color: 0x94a3b8 }}));
          mastPole.position.set(20, 15.2, 1.8);
          mastPole.rotateX(Math.PI / 2);
          groups.SUR.add(mastPole);
          const flagMesh = new THREE.Mesh(new THREE.BoxGeometry(0.04, 0.8, 0.5), new THREE.MeshBasicMaterial({{ color: 0xf97316 }}));
          flagMesh.position.set(20, 15.6, 2.4);
          groups.SUR.add(flagMesh);

          // 2. Subaqueous Stratified Geological Strata
          // Layer 1: Top Alluvial Silt Strata (-12m to -2m)
          createPrism("GEO_SILT", [[-2, -2], [42, -2], [42, 42], [-2, 42]], -12, -2, 0x475569, 0.38, "SUR", 0, {{
            name: "Hooghly Alluvial Silt Strata & Riverbed Surcharge Sediment",
            ulpin: `${{data.base_ulpin}}-GEO-G01-ST01-R`,
            z: "-12.0m to -2.0m",
            area: "1936 m²",
            vol: "19360 m³",
            owner: "Kolkata Port Trust & Inland Waterways Authority of India",
            val: "₹ 75.0 Cr"
          }});

          // Layer 2: Stiff Impermeable Marine Clay Strata (-20m to -12m)
          createPrism("GEO_CLAY", [[-2, -2], [42, -2], [42, 42], [-2, 42]], -20, -12, 0x334155, 0.45, "SUB", -1, {{
            name: "Stiff Impermeable Silty Clay Geological Barrier Zone",
            ulpin: `${{data.base_ulpin}}-GEO-G02-CL01-C`,
            z: "-20.0m to -12.0m",
            area: "1936 m²",
            vol: "15488 m³",
            owner: "Kolkata Metro Rail Corporation (Geotechnical Reserve)",
            val: "₹ 95.0 Cr"
          }});

          // 3. Deep Riverbank Ventilation & Emergency Escape Shaft (-28m to +3m)
          createPrism("UTL_SHAFT", [[15, 1], [25, 1], [25, 8], [15, 8]], -28, 3, 0x0ea5e9, 0.88, "UTL", -2, {{
            name: "Howrah-Mahakaran Riverbank Deep Ventilation & Evacuation Shaft",
            ulpin: `${{data.base_ulpin}}-UTL-U02-SH01-M`,
            z: "-28.0m to +3.0m",
            area: "70 m²",
            vol: "2170 m³",
            owner: "Kolkata Metro Rail Corporation (KMRCL)",
            val: "₹ 140 Cr"
          }});

          // 4. Twin Circular Bored Shield Tunnels under Riverbed (-28m to -20m, Depth 24m MSL)
          [-1, 1].forEach(side => {{
            const ty = 20 + (side * 9);
            const isEast = side > 0;
            const tGeo = new THREE.CylinderGeometry(3.2, 3.2, 52, 32);
            tGeo.rotateZ(Math.PI / 2);
            const tMat = new THREE.MeshStandardMaterial({{
              color: 0x06b6d4,
              roughness: 0.25,
              metalness: 0.4,
              transparent: true,
              opacity: 0.92
            }});
            const tMesh = new THREE.Mesh(tGeo, tMat);
            tMesh.position.set(20, ty, -24.0);
            tMesh.userData = {{
              id: `UTL_HOOGHLY_${{isEast ? "EAST" : "WEST"}}`,
              stratum: "UTL",
              originalZ: -24.0,
              floorIdx: -3,
              baseOpacity: 0.92,
              info: {{
                name: `Hooghly Subaqueous Shield Tunnel (${{isEast ? "Eastbound Track: Howrah Maidan to Esplanade" : "Westbound Track: Esplanade to Howrah Maidan"}})`,
                ulpin: `${{data.base_ulpin}}-UTL-U03-HT0${{isEast ? 1 : 2}}-K`,
                z: "-27.2m to -20.8m (Depth 24m MSL)",
                area: "340 m²",
                vol: "1520 m³",
                owner: "Kolkata Metro Rail Corporation (KMRCL)",
                val: "₹ 650 Cr"
              }}
            }};
            groups.UTL.add(tMesh);
            meshMap.set(`UTL_HOOGHLY_${{isEast ? "EAST" : "WEST"}}`, tMesh);

            // Bolted Precast Concrete Segmental Lining Rings
            const ringMat = new THREE.MeshStandardMaterial({{ color: 0x1e293b, roughness: 0.8 }});
            for (let rx = 2; rx <= 38; rx += 4.5) {{
              const ringGeo = new THREE.TorusGeometry(3.25, 0.12, 8, 28);
              ringGeo.rotateY(Math.PI / 2);
              const rMesh = new THREE.Mesh(ringGeo, ringMat);
              rMesh.position.set(rx, ty, -24.0);
              groups.UTL.add(rMesh);
            }}

            // Signature 520m Subaqueous Cyan/Aquamarine LED Ceiling Strip
            const ledGeo = new THREE.BoxGeometry(50, 0.35, 0.2);
            const ledMat = new THREE.MeshBasicMaterial({{ color: isEast ? 0x38bdf8 : 0x34d399 }});
            const ledMesh = new THREE.Mesh(ledGeo, ledMat);
            ledMesh.position.set(20, ty, -21.1);
            groups.UTL.add(ledMesh);

            // Concrete Invert Track Slab & Dual Steel Running Rails
            const slab = new THREE.Mesh(new THREE.BoxGeometry(50, 2.8, 0.35), new THREE.MeshStandardMaterial({{ color: 0x334155 }}));
            slab.position.set(20, ty, -26.3);
            groups.UTL.add(slab);

            const rMat = new THREE.MeshStandardMaterial({{ color: 0xf1f5f9, metalness: 0.9 }});
            const r1 = new THREE.Mesh(new THREE.BoxGeometry(50, 0.12, 0.2), rMat);
            r1.position.set(20, ty - 0.72, -26.0);
            groups.UTL.add(r1);
            const r2 = new THREE.Mesh(new THREE.BoxGeometry(50, 0.12, 0.2), rMat);
            r2.position.set(20, ty + 0.72, -26.0);
            groups.UTL.add(r2);
          }});

          // 5. Realistic 4-Coach Kolkata Metro BEML Stainless Steel Trainset (Eastbound Tunnel)
          const kTrainY = 29.0;
          const kCoachMat = new THREE.MeshStandardMaterial({{ color: 0xe2e8f0, metalness: 0.85, roughness: 0.2 }});
          const kGreenStripe = new THREE.MeshBasicMaterial({{ color: 0x15803d }});
          const kYellowStripe = new THREE.MeshBasicMaterial({{ color: 0xfacc15 }});
          const kWinMat = new THREE.MeshStandardMaterial({{ color: 0x0284c7, roughness: 0.1 }});

          [-12, -4, 4, 12].forEach((cx, idx) => {{
            const coach = new THREE.Mesh(new THREE.BoxGeometry(7.0, 2.4, 2.4), kCoachMat);
            coach.position.set(20 + cx, kTrainY, -24.2);
            groups.UTL.add(coach);

            // Signature Green & Yellow Double Stripe Livery
            const sG = new THREE.Mesh(new THREE.BoxGeometry(7.05, 2.45, 0.25), kGreenStripe);
            sG.position.set(20 + cx, kTrainY, -24.5);
            groups.UTL.add(sG);
            const sY = new THREE.Mesh(new THREE.BoxGeometry(7.05, 2.45, 0.12), kYellowStripe);
            sY.position.set(20 + cx, kTrainY, -24.75);
            groups.UTL.add(sY);

            // Windows
            const wN = new THREE.Mesh(new THREE.BoxGeometry(6.2, 0.08, 0.75), kWinMat);
            wN.position.set(20 + cx, kTrainY + 1.22, -23.8);
            groups.UTL.add(wN);
            const wS = new THREE.Mesh(new THREE.BoxGeometry(6.2, 0.08, 0.75), kWinMat);
            wS.position.set(20 + cx, kTrainY - 1.22, -23.8);
            groups.UTL.add(wS);

            // Lead Driving Cab with Headlights
            if (idx === 3) {{
              const cab = new THREE.Mesh(new THREE.BoxGeometry(0.8, 2.2, 1.8), new THREE.MeshStandardMaterial({{ color: 0x0f172a }}));
              cab.position.set(20 + cx + 3.8, kTrainY, -24.2);
              groups.UTL.add(cab);

              const hl1 = new THREE.Mesh(new THREE.SphereGeometry(0.18, 8, 8), new THREE.MeshBasicMaterial({{ color: 0xfef08a }}));
              hl1.position.set(20 + cx + 4.2, kTrainY - 0.6, -24.7);
              groups.UTL.add(hl1);
              const hl2 = hl1.clone();
              hl2.position.set(20 + cx + 4.2, kTrainY + 0.6, -24.7);
              groups.UTL.add(hl2);
            }}
          }});

          // 6. Cross-Passage Escape Chamber with Heavy Marine Pressure Bulkheads
          createPrism("UTL_CROSS_PASS", [[17, 11], [23, 11], [23, 29], [17, 29]], -26.0, -22.0, 0x10b981, 0.94, "UTL", -3, {{
            name: "Subaqueous Emergency Cross-Passage, Pressure Bulkheads & Sump Drainage Vault",
            ulpin: `${{data.base_ulpin}}-UTL-U03-CP01-E`,
            z: "-26.0m to -22.0m",
            area: "108 m²",
            vol: "432 m³",
            owner: "KMRCL Safety & Disaster Management Directorate",
            val: "₹ 55.0 Cr"
          }});

          // Circular Watertight Pressure Bulkhead Doors
          [-1, 1].forEach(side => {{
            const bhGeo = new THREE.CylinderGeometry(1.2, 1.2, 0.4, 20);
            bhGeo.rotateZ(Math.PI / 2);
            const bhMat = new THREE.MeshStandardMaterial({{ color: 0xef4444, metalness: 0.8, roughness: 0.3 }});
            const bh = new THREE.Mesh(bhGeo, bhMat);
            bh.position.set(20, 20 + (side * 7.5), -24.0);
            groups.UTL.add(bh);
          }});
        }}

        // ARCHETYPE 10: GIFT Subsurface Utility Tunnel (TUM) - Multi-Utility Conduit System
        function buildUtilityTunnelTrench(data) {{
          // 1. Walk-Through Reinforced Concrete Utility Trench (-16m to 0m)
          createPrism("SUB_TRENCH", [[8, 2], [32, 2], [32, 38], [8, 38]], -16, 0, 0x334155, 0.82, "SUB", -1, {{
            name: "GIFT City Walk-Through Utility Tunnel (TUM Trench Corridor)",
            ulpin: `${{data.base_ulpin}}-SUB-B01-TM01-G`,
            z: "-16.0m to 0.0m",
            area: "864 m²",
            vol: "13824 m³",
            owner: "GIFT Urban Infrastructure Ltd (Smart Utility SPV)",
            val: "₹ 920 Cr"
          }});

          // Precast Concrete Structural Ribs along Trench Walls
          const ribMat = new THREE.MeshStandardMaterial({{ color: 0x1e293b, roughness: 0.9 }});
          for (let ry = 4; ry <= 36; ry += 4) {{
            const ribL = new THREE.Mesh(new THREE.BoxGeometry(0.8, 0.8, 15.5), ribMat);
            ribL.position.set(8.4, ry, -8);
            groups.SUB.add(ribL);
            const ribR = new THREE.Mesh(new THREE.BoxGeometry(0.8, 0.8, 15.5), ribMat);
            ribR.position.set(31.6, ry, -8);
            groups.SUB.add(ribR);
          }}

          // Central Longitudinal Floor Drainage Invert Channel
          const drain = new THREE.Mesh(new THREE.BoxGeometry(2.0, 36, 0.4), new THREE.MeshStandardMaterial({{ color: 0x0f172a }}));
          drain.position.set(20, 20, -15.8);
          groups.SUB.add(drain);

          // 2. Elevated Galvanized Steel Catwalk & Walkway System (Z = -9.0m)
          // Anti-slip walkway grating
          const catwalkMat = new THREE.MeshStandardMaterial({{ color: 0x94a3b8, metalness: 0.85, roughness: 0.3 }});
          const catwalk = new THREE.Mesh(new THREE.BoxGeometry(2.6, 36, 0.15), catwalkMat);
          catwalk.position.set(20, 20, -9.0);
          groups.SUB.add(catwalk);

          // Yellow Industrial Safety Handrails on Catwalk
          const railMat = new THREE.MeshStandardMaterial({{ color: 0xfacc15, roughness: 0.4 }});
          const railL = new THREE.Mesh(new THREE.BoxGeometry(0.08, 36, 1.1), railMat);
          railL.position.set(18.7, 20, -8.45);
          groups.SUB.add(railL);
          const railR = new THREE.Mesh(new THREE.BoxGeometry(0.08, 36, 1.1), railMat);
          railR.position.set(21.3, 20, -8.45);
          groups.SUB.add(railR);

          // Vertical Steel Access Ladder with Round Safety Cage (North Portal)
          const ladMat = new THREE.MeshStandardMaterial({{ color: 0xe2e8f0, metalness: 0.9 }});
          const lad = new THREE.Mesh(new THREE.BoxGeometry(0.6, 0.1, 15.0), ladMat);
          lad.position.set(20, 3.2, -7.5);
          groups.SUB.add(lad);

          // 3. Five Color-Coded Conduit Systems on Heavy Cantilevered Steel Brackets
          const conduitLayers = [
            {{
              id: "COOLING",
              name: "District Cooling Chilled Water 900mm Insulated Pipelines",
              clr: 0x06b6d4,
              z: -4.5,
              dia: 0.9,
              xOffsets: [13.2, 26.8],
              ulpinSuffix: "DC01-C",
              val: "₹ 340 Cr",
              area: "144 m²",
              vol: "1296 m³"
            }},
            {{
              id: "WASTE",
              name: "Automated Vacuum Waste Collection (AVWC) Pneumatic Steel Tubes",
              clr: 0xa855f7,
              z: -7.2,
              dia: 0.55,
              xOffsets: [14.0, 26.0],
              ulpinSuffix: "VW01-P",
              val: "₹ 180 Cr",
              area: "90 m²",
              vol: "540 m³"
            }},
            {{
              id: "POWER",
              name: "66kV Extra High Voltage Underground Transmission Cable Trays",
              clr: 0xf59e0b,
              z: -10.5,
              dia: 0.4,
              isTray: true,
              xOffsets: [13.8, 26.2],
              ulpinSuffix: "HV01-E",
              val: "₹ 260 Cr",
              area: "120 m²",
              vol: "720 m³"
            }},
            {{
              id: "WATER",
              name: "Dual Potable Water & Recycled Tertiary Irrigation Conduits",
              clr: 0x10b981,
              z: -13.5,
              dia: 0.65,
              xOffsets: [13.5, 26.5],
              ulpinSuffix: "WT01-W",
              val: "₹ 140 Cr",
              area: "105 m²",
              vol: "630 m³"
            }},
            {{
              id: "TELECOM",
              name: "Smart City SCADA & Redundant Fiber Optic Backbone Trays",
              clr: 0x38bdf8,
              z: -2.2,
              dia: 0.35,
              isTray: true,
              xOffsets: [14.2, 25.8],
              ulpinSuffix: "TC01-S",
              val: "₹ 80 Cr",
              area: "75 m²",
              vol: "300 m³"
            }}
          ];

          conduitLayers.forEach(c => {{
            c.xOffsets.forEach((cx, idx) => {{
              let pipeMesh;
              if (c.isTray) {{
                // Cable ladder tray
                const tGeo = new THREE.BoxGeometry(1.2, 36, 0.25);
                const tMat = new THREE.MeshStandardMaterial({{ color: c.clr, metalness: 0.7, roughness: 0.3 }});
                pipeMesh = new THREE.Mesh(tGeo, tMat);
                pipeMesh.position.set(cx, 20, c.z);
              }} else {{
                // Cylindrical pipe with insulated casing
                const pGeo = new THREE.CylinderGeometry(c.dia, c.dia, 36, 20);
                pGeo.rotateX(Math.PI / 2);
                const pMat = new THREE.MeshStandardMaterial({{ color: c.clr, roughness: 0.25, metalness: 0.4, transparent: true, opacity: 0.92 }});
                pipeMesh = new THREE.Mesh(pGeo, pMat);
                pipeMesh.position.set(cx, 20, c.z);

                // Flanged expansion joint rings at intervals
                for (let fy = 6; fy <= 34; fy += 8) {{
                  const flGeo = new THREE.CylinderGeometry(c.dia * 1.25, c.dia * 1.25, 0.35, 16);
                  flGeo.rotateX(Math.PI / 2);
                  const flMesh = new THREE.Mesh(flGeo, new THREE.MeshStandardMaterial({{ color: 0x475569, metalness: 0.8 }}));
                  flMesh.position.set(cx, fy, c.z);
                  groups.UTL.add(flMesh);
                }}
              }}

              // Structural Cantilever Support Brackets from Wall
              const brkGeo = new THREE.BoxGeometry(Math.abs(cx > 20 ? (31.6 - cx + 0.6) : (cx - 8.4 + 0.6)), 0.2, 0.2);
              const brkMat = new THREE.MeshStandardMaterial({{ color: 0x64748b, metalness: 0.8 }});
              for (let by = 4; by <= 36; by += 8) {{
                const brk = new THREE.Mesh(brkGeo, brkMat);
                brk.position.set(cx > 20 ? (cx + (31.6 - cx) / 2) : (cx - (cx - 8.4) / 2), by, c.z - 0.35);
                groups.UTL.add(brk);
              }}

              pipeMesh.userData = {{
                id: `UTL_${{c.id}}_${{idx}}`,
                stratum: "UTL",
                originalZ: c.z,
                floorIdx: Math.round(c.z / 4),
                baseOpacity: 0.92,
                info: {{
                  name: `${{c.name}} (${{idx === 0 ? "Bank A - West" : "Bank B - East"}})`,
                  ulpin: `${{data.base_ulpin}}-UTL-U01-${{c.ulpinSuffix}}`,
                  z: `${{(c.z - 0.5).toFixed(1)}}m to ${{(c.z + 0.5).toFixed(1)}}m`,
                  area: c.area,
                  vol: c.vol,
                  owner: "GIFT Multi-Services Utility SPV",
                  val: c.val
                }}
              }};

              groups.UTL.add(pipeMesh);
              if (idx === 0) meshMap.set(`UTL_${{c.id}}`, pipeMesh);
            }});
          }});

          // 4. Overhead Continuous LED Strip Lighting & SCADA Sensors
          const ledGeo = new THREE.BoxGeometry(0.3, 36, 0.1);
          const ledMat = new THREE.MeshBasicMaterial({{ color: 0xffffff }});
          const led = new THREE.Mesh(ledGeo, ledMat);
          led.position.set(20, 20, -1.0);
          groups.UTL.add(led);

          // Surface Access Kiosk & Ventilation Cowl
          const hatchGeo = new THREE.BoxGeometry(4.0, 4.0, 1.4);
          const hatchMat = new THREE.MeshStandardMaterial({{ color: 0x475569, metalness: 0.7, roughness: 0.4 }});
          const hatch = new THREE.Mesh(hatchGeo, hatchMat);
          hatch.position.set(20, 4, 0.7);
          groups.SUR.add(hatch);
        }}

        // ARCHETYPE 11: TIDEL Park IT Expressway (Chennai) - Linear Monolith with Spinal Glass Atrium
        function buildLinearITSpine(data) {{
          const tidelTenants = [
            "TIDEL Park Common Grand Atrium & Visitor Reception",
            "Tata Consultancy Services (Global BFSI Delivery Center)",
            "Cisco Systems India (Advanced Cloud Networking Lab)",
            "HCL Technologies (AI & Digital Engineering Hub)",
            "Cognizant Technology Solutions (Digital Business Solutions)",
            "Sify Technologies Cloud Data & Executive Penthouse Suites"
          ];

          // 1. Linear IT Monolith (Floors G00 to F05, Footprint 36m x 28m)
          for (let f = 0; f <= 5; f++) {{
            const zMin = f * 4.6;
            const zMax = zMin + 4.6;
            const lvl = f === 0 ? "G00" : `F0${{f}}`;
            const flrOwner = tidelTenants[f] || "TIDEL OMR Tech Enterprise Tenant";

            // North IT Office Wing (polygon [2,22] to [38,32])
            createPrism(`BLD_${{lvl}}_NORTH`, [[2, 22], [38, 22], [38, 32], [2, 32]], zMin, zMax, 0x0284c7, 0.88, "BLD", f, {{
              name: `TIDEL Park North Wing Block (${{lvl}})`,
              ulpin: `${{data.base_ulpin}}-BLD-${{lvl}}-NB01-C`,
              z: `${{zMin.toFixed(1)}}m to ${{zMax.toFixed(1)}}m`,
              area: "360 m²",
              vol: "1656 m³",
              owner: flrOwner,
              val: "₹ 45.0 Cr"
            }});

            // Central Soaring Spinal Glass Canyon Atrium (polygon [2,16] to [38,22])
            createPrism(`COM_${{lvl}}_SPINE`, [[2, 16], [38, 16], [38, 22], [2, 22]], zMin, zMax, 0x38bdf8, 0.58, "COM", f, {{
              name: `TIDEL Central Spinal Glass Canyon & Aerial Concourse (${{lvl}})`,
              ulpin: `${{data.base_ulpin}}-COM-${{lvl}}-SP01-S`,
              z: `${{zMin.toFixed(1)}}m to ${{zMax.toFixed(1)}}m`,
              area: "216 m²",
              vol: "993 m³",
              owner: "TIDEL Park Ltd (Shared Corporate Facilities)",
              val: "₹ 16.0 Cr"
            }});

            // South IT Office Wing (polygon [2,6] to [38,16])
            createPrism(`BLD_${{lvl}}_SOUTH`, [[2, 6], [38, 6], [38, 16], [2, 16]], zMin, zMax, 0x0369a1, 0.88, "BLD", f, {{
              name: `TIDEL Park South Wing Block (${{lvl}})`,
              ulpin: `${{data.base_ulpin}}-BLD-${{lvl}}-SB01-T`,
              z: `${{zMin.toFixed(1)}}m to ${{zMax.toFixed(1)}}m`,
              area: "360 m²",
              vol: "1656 m³",
              owner: flrOwner,
              val: "₹ 45.0 Cr"
            }});

            // Horizontal Architectural Brise-Soleil (Silver Metallic Sunshades)
            const louverMat = new THREE.MeshStandardMaterial({{ color: 0xe2e8f0, metalness: 0.85, roughness: 0.2 }});
            const louverN = new THREE.Mesh(new THREE.BoxGeometry(36, 0.4, 0.25), louverMat);
            louverN.position.set(20, 32.2, zMin + 2.3);
            groups.BLD.add(louverN);
            const louverS = new THREE.Mesh(new THREE.BoxGeometry(36, 0.4, 0.25), louverMat);
            louverS.position.set(20, 5.8, zMin + 2.3);
            groups.BLD.add(louverS);
          }}

          // 2. Suspended Aerial Skywalk Bridges across the Atrium Canyon (Floors 2, 4, 5)
          [2, 4, 5].forEach(flr => {{
            const szMin = flr * 4.6;
            const skybridge = new THREE.Mesh(
              new THREE.BoxGeometry(3.6, 6.0, 3.2),
              new THREE.MeshStandardMaterial({{ color: 0x7dd3fc, transparent: true, opacity: 0.75, roughness: 0.2 }})
            );
            skybridge.position.set(20, 19, szMin + 1.8);
            groups.COM.add(skybridge);

            // Steel truss framing around skybridge
            const frameMat = new THREE.MeshStandardMaterial({{ color: 0x334155, metalness: 0.9 }});
            const f1 = new THREE.Mesh(new THREE.BoxGeometry(3.8, 0.2, 3.4), frameMat);
            f1.position.set(20, 16.0, szMin + 1.8);
            groups.COM.add(f1);
            const f2 = new THREE.Mesh(new THREE.BoxGeometry(3.8, 0.2, 3.4), frameMat);
            f2.position.set(20, 22.0, szMin + 1.8);
            groups.COM.add(f2);
          }});

          // 3. Grand Triple-Height Space-Frame Entrance Portico
          const porticoGeo = new THREE.BoxGeometry(10, 6, 0.4);
          const porticoMat = new THREE.MeshStandardMaterial({{ color: 0x475569, metalness: 0.8, roughness: 0.3 }});
          const portico = new THREE.Mesh(porticoGeo, porticoMat);
          portico.position.set(20, 3, 5.2);
          groups.BLD.add(portico);

          // Support Columns for Portico
          [-4, 4].forEach(px => {{
            const col = new THREE.Mesh(new THREE.CylinderGeometry(0.35, 0.35, 5.2, 16), porticoMat);
            col.rotateX(Math.PI / 2);
            col.position.set(20 + px, 3, 2.6);
            groups.BLD.add(col);
          }});

          // 4. Landscaped Rajiv Gandhi Salai (OMR) Frontage & Reflecting Water Feature
          const waterGeo = new THREE.BoxGeometry(18, 2.5, 0.3);
          const waterMat = new THREE.MeshStandardMaterial({{ color: 0x0284c7, roughness: 0.1, transparent: true, opacity: 0.85 }});
          const water = new THREE.Mesh(waterGeo, waterMat);
          water.position.set(20, 1.2, 0.15);
          groups.SUR.add(water);

          // Tropical Palm Trees along Boulevard
          for (let px = 5; px <= 35; px += 7.5) {{
            const trunk = new THREE.Mesh(new THREE.CylinderGeometry(0.18, 0.22, 3.8, 8), new THREE.MeshStandardMaterial({{ color: 0x78350f }}));
            trunk.rotateX(Math.PI / 2);
            trunk.position.set(px, 1.2, 1.9);
            groups.SUR.add(trunk);

            const crown = new THREE.Mesh(new THREE.SphereGeometry(1.1, 8, 8), new THREE.MeshStandardMaterial({{ color: 0x15803d }}));
            crown.position.set(px, 1.2, 4.0);
            groups.SUR.add(crown);
          }}

          // TIDEL Corporate Entrance Totem
          const totem = new THREE.Mesh(new THREE.BoxGeometry(1.2, 0.4, 3.2), new THREE.MeshStandardMaterial({{ color: 0x0f172a }}));
          totem.position.set(6, 3.0, 1.6);
          groups.SUR.add(totem);

          // 5. Rooftop Industrial HVAC Chillers, BMU Crane & Executive Helipad
          // 6 Cooling Towers on North Roof
          for (let cx = 8; cx <= 32; cx += 5) {{
            const ct = new THREE.Mesh(new THREE.CylinderGeometry(1.3, 1.3, 2.4, 16), new THREE.MeshStandardMaterial({{ color: 0x334155, roughness: 0.6 }}));
            ct.rotateX(Math.PI / 2);
            ct.position.set(cx, 27, 28.8);
            groups.AIR.add(ct);
          }}

          // Dedicated Executive Helipad on South Wing Roof
          const padGeo = new THREE.BoxGeometry(12, 8, 0.4);
          const padMat = new THREE.MeshStandardMaterial({{ color: 0x1e293b, roughness: 0.9 }});
          const pad = new THREE.Mesh(padGeo, padMat);
          pad.position.set(20, 11, 27.8);
          groups.AIR.add(pad);

          // Yellow Touchdown Circle & "H" Marking
          const hCanvas = document.createElement('canvas');
          hCanvas.width = 128; hCanvas.height = 128;
          const hctx = hCanvas.getContext('2d');
          hctx.fillStyle = '#1e293b'; hctx.fillRect(0, 0, 128, 128);
          hctx.strokeStyle = '#facc15'; hctx.lineWidth = 8;
          hctx.beginPath(); hctx.arc(64, 64, 48, 0, Math.PI * 2); hctx.stroke();
          hctx.fillStyle = '#facc15'; hctx.font = 'bold 56px sans-serif';
          hctx.textAlign = 'center'; hctx.textBaseline = 'middle';
          hctx.fillText('H', 64, 64);
          const hTex = new THREE.CanvasTexture(hCanvas);
          const hMesh = new THREE.Mesh(new THREE.PlaneGeometry(9, 7), new THREE.MeshBasicMaterial({{ map: hTex, transparent: true }}));
          hMesh.position.set(20, 11, 28.05);
          groups.AIR.add(hMesh);

          // Facade Maintenance BMU Crane Rig
          const bmuBase = new THREE.Mesh(new THREE.BoxGeometry(1.6, 1.6, 1.8), new THREE.MeshStandardMaterial({{ color: 0x475569 }}));
          bmuBase.position.set(34, 11, 28.5);
          groups.AIR.add(bmuBase);
          const bmuArm = new THREE.Mesh(new THREE.BoxGeometry(6.5, 0.4, 0.4), new THREE.MeshStandardMaterial({{ color: 0xfacc15 }}));
          bmuArm.position.set(31, 11, 29.8);
          groups.AIR.add(bmuArm);

          // Communications Satellite Radome & Obstruction Beacon Mast
          const radome = new THREE.Mesh(new THREE.SphereGeometry(1.4, 16, 16), new THREE.MeshStandardMaterial({{ color: 0xf8fafc, roughness: 0.3 }}));
          radome.position.set(6, 11, 28.8);
          groups.AIR.add(radome);

          const mast = new THREE.Mesh(new THREE.CylinderGeometry(0.1, 0.3, 10, 8), new THREE.MeshStandardMaterial({{ color: 0xe2e8f0, metalness: 0.9 }}));
          mast.rotateX(Math.PI / 2);
          mast.position.set(20, 19, 32.6);
          groups.AIR.add(mast);

          const redBcn = new THREE.Mesh(new THREE.SphereGeometry(0.35, 8, 8), new THREE.MeshBasicMaterial({{ color: 0xef4444 }}));
          redBcn.position.set(20, 19, 37.8);
          groups.AIR.add(redBcn);

          // 6. Subsurface Dual Basements (Z = -14.0m to 0.0m)
          createPrism("SUB_TIDEL_B1", [[2, 6], [38, 6], [38, 32], [2, 32]], -7, 0, 0xf59e0b, 0.85, "SUB", -1, {{
            name: "TIDEL Automated Employee Parking & Logistics Docks (Level B1)",
            ulpin: `${{data.base_ulpin}}-SUB-B01-TD01-A`,
            z: "-7.0m to 0.0m",
            area: "936 m²",
            vol: "6552 m³",
            owner: "TIDEL Park Ltd (Parking & Logistics)",
            val: "₹ 80.0 Cr"
          }});

          createPrism("SUB_TIDEL_B2", [[2, 6], [38, 6], [38, 32], [2, 32]], -14, -7, 0xd97706, 0.88, "SUB", -2, {{
            name: "100% Redundant Diesel Power Generator Bank & 110kV Substation (Level B2)",
            ulpin: `${{data.base_ulpin}}-SUB-B02-TD02-B`,
            z: "-14.0m to -7.0m",
            area: "936 m²",
            vol: "6552 m³",
            owner: "TIDEL Energy & Critical Utilities SPV",
            val: "₹ 110 Cr"
          }});
        }}

        // ARCHETYPE 12: Transit Terminal Canopy (Seawoods Transit, Durgam Cheruvu Hub)
        function buildTransitTerminalCanopy(data) {{
          // Real-World Multi-Modal Transit Terminal & Cable-Stayed Bridge Pylon Hub
          // 1. Signature Structural Concrete Cable-Stayed Pylon Tower (Z = 0.0m to 42.0m)
          // Pylon A-Frame Legs
          const pylonMat = new THREE.MeshStandardMaterial({{ color: 0x64748b, roughness: 0.7, metalness: 0.2 }});
          
          // West Leg
          const legW = new THREE.Mesh(new THREE.BoxGeometry(1.6, 2.2, 40), pylonMat);
          legW.position.set(15.5, 20, 20);
          legW.rotation.y = 0.12;
          groups.AIR.add(legW);

          // East Leg
          const legE = new THREE.Mesh(new THREE.BoxGeometry(1.6, 2.2, 40), pylonMat);
          legE.position.set(24.5, 20, 20);
          legE.rotation.y = -0.12;
          groups.AIR.add(legE);

          // Pylon Head Apex & Crossbeams
          const pylonHead = new THREE.Mesh(new THREE.BoxGeometry(3.6, 2.6, 6), pylonMat);
          pylonHead.position.set(20, 20, 40);
          groups.AIR.add(pylonHead);

          const crossBeam = new THREE.Mesh(new THREE.BoxGeometry(10.5, 2.0, 1.6), pylonMat);
          crossBeam.position.set(20, 20, 19);
          groups.AIR.add(crossBeam);

          // Aircraft Obstruction Warning Light on Apex
          const beacon = new THREE.Mesh(new THREE.SphereGeometry(0.4, 12, 12), new THREE.MeshBasicMaterial({{ color: 0xef4444 }}));
          beacon.position.set(20, 20, 43.4);
          groups.AIR.add(beacon);

          // 2. High-Tensile Steel Stay Cables (Semi-Harp Fan Array)
          const cableMat = new THREE.LineBasicMaterial({{ color: 0xf1f5f9, linewidth: 2 }});
          const cableGeo = new THREE.BufferGeometry();
          const cPts = [];
          for (let cy = 2; cy <= 38; cy += 4.5) {{
            // Cables to West deck edge
            cPts.push(new THREE.Vector3(19.2, 20, 39.5), new THREE.Vector3(7.5, cy, 9.2));
            // Cables to East deck edge
            cPts.push(new THREE.Vector3(20.8, 20, 39.5), new THREE.Vector3(32.5, cy, 9.2));
          }}
          cableGeo.setFromPoints(cPts);
          groups.AIR.add(new THREE.LineSegments(cableGeo, cableMat));

          // 3. Elevated Roadway Viaduct Deck (Z = 8.0m to 10.0m)
          createPrism("AIR_VIADUCT", [[6, 0], [34, 0], [34, 40], [6, 40]], 8.0, 9.4, 0x475569, 0.95, "AIR", 2, {{
            name: "Elevated Cable-Stayed 4-Lane Rapid Transit Deck",
            ulpin: `${{data.base_ulpin}}-AIR-E01-CS01-T`,
            z: "+8.0m to +9.4m",
            area: "1120 m²",
            vol: "1568 m³",
            owner: "State Road Development & Urban Transit Corporation",
            val: "₹ 180 Cr"
          }});

          // Aerodynamic Concrete Parapet Crash Barriers
          const barMat = new THREE.MeshStandardMaterial({{ color: 0x94a3b8, roughness: 0.8 }});
          const barL = new THREE.Mesh(new THREE.BoxGeometry(0.35, 40, 0.8), barMat);
          barL.position.set(6.2, 20, 9.8);
          groups.AIR.add(barL);
          const barR = new THREE.Mesh(new THREE.BoxGeometry(0.35, 40, 0.8), barMat);
          barR.position.set(33.8, 20, 9.8);
          groups.AIR.add(barR);

          // LED Street Lighting Masts on Viaduct
          for (let ly = 4; ly <= 36; ly += 8) {{
            const mastGeo = new THREE.CylinderGeometry(0.08, 0.12, 3.2, 8);
            mastGeo.rotateX(Math.PI / 2);
            const mastMesh = new THREE.Mesh(mastGeo, new THREE.MeshStandardMaterial({{ color: 0xe2e8f0 }}));
            mastMesh.position.set(20, ly, 11.0);
            groups.AIR.add(mastMesh);

            const lamp = new THREE.Mesh(new THREE.BoxGeometry(0.4, 0.2, 0.1), new THREE.MeshBasicMaterial({{ color: 0xfef08a }}));
            lamp.position.set(20, ly, 12.6);
            groups.AIR.add(lamp);
          }}

          // 4. Sweeping Tensile Fabric Terminal Canopy Structure (Z = 0.0m to 7.0m)
          // Curved space-frame arches
          const archGeo = new THREE.TorusGeometry(15, 0.6, 12, 32, Math.PI);
          archGeo.rotateY(Math.PI / 2);
          const archMat = new THREE.MeshStandardMaterial({{ color: 0x0284c7, metalness: 0.7, roughness: 0.3 }});
          
          [-10, 0, 10].forEach(pos => {{
            const arch = new THREE.Mesh(archGeo, archMat);
            arch.position.set(20, 20 + pos, 0);
            groups.BLD.add(arch);
          }});

          // White Tensile Fabric Canopy Membrane
          const canopyTex = getCurvedCanopyTexture();
          const canopyGeo = new THREE.CylinderGeometry(15.2, 15.2, 26, 32, 1, true, 0, Math.PI);
          canopyGeo.rotateZ(Math.PI / 2);
          const canopyMat = new THREE.MeshStandardMaterial({{
            map: canopyTex,
            color: 0xf8fafc,
            side: THREE.DoubleSide,
            transparent: true,
            opacity: 0.88,
            roughness: 0.4
          }});
          const canopy = new THREE.Mesh(canopyGeo, canopyMat);
          canopy.position.set(20, 20, 0);
          groups.BLD.add(canopy);

          // 5. Central Ground-Level Transit Concourse & Platform Hall (0.0m to 6.0m)
          createPrism("BLD_CONCOURSE", [[8, 8], [32, 8], [32, 32], [8, 32]], 0, 6.0, 0x38bdf8, 0.82, "BLD", 0, {{
            name: "High-Capacity Multi-Modal Transit Concourse & Ticketing Terminal",
            ulpin: `${{data.base_ulpin}}-BLD-G00-TT01-4`,
            z: "0.0m to +6.0m",
            area: "576 m²",
            vol: "3456 m³",
            owner: "State Multi-Modal Transit Authority & Central Railway",
            val: "₹ 190 Cr"
          }});

          // 6. Bus Rapid Transit (BRT) Bays & 2 Detailed Modern Electric Transit Buses
          // Asphalt Bus Bays on East and West sides
          const bayMat = new THREE.MeshStandardMaterial({{ color: 0x1e293b, roughness: 0.95 }});
          const bayW = new THREE.Mesh(new THREE.BoxGeometry(4.5, 34, 0.15), bayMat);
          bayW.position.set(4, 20, 0.1);
          groups.SUR.add(bayW);
          const bayE = new THREE.Mesh(new THREE.BoxGeometry(4.5, 34, 0.15), bayMat);
          bayE.position.set(36, 20, 0.1);
          groups.SUR.add(bayE);

          // Tactile Boarding Kerbs
          const kerbMat = new THREE.MeshBasicMaterial({{ color: 0xfacc15 }});
          const kerbW = new THREE.Mesh(new THREE.BoxGeometry(0.3, 34, 0.2), kerbMat);
          kerbW.position.set(6.3, 20, 0.2);
          groups.SUR.add(kerbW);
          const kerbE = new THREE.Mesh(new THREE.BoxGeometry(0.3, 34, 0.2), kerbMat);
          kerbE.position.set(33.7, 20, 0.2);
          groups.SUR.add(kerbE);

          // 2 Electric Transit Buses (Olectra / JBM Green Zero-Emission E-Buses)
          const busBodyMat = new THREE.MeshStandardMaterial({{ color: 0xf8fafc, roughness: 0.3 }});
          const busGreenMat = new THREE.MeshBasicMaterial({{ color: 0x15803d }});
          const busGlassMat = new THREE.MeshStandardMaterial({{ color: 0x0284c7, roughness: 0.1 }});

          [
            {{ x: 4.0, y: 15, rot: 0, route: "AIRPORT EXPRESS" }},
            {{ x: 36.0, y: 25, rot: Math.PI, route: "METRO FEEDER" }}
          ].forEach(b => {{
            // Chassis
            const bus = new THREE.Mesh(new THREE.BoxGeometry(2.4, 7.5, 2.2), busBodyMat);
            bus.position.set(b.x, b.y, 1.3);
            bus.rotation.z = b.rot;
            groups.SUR.add(bus);

            // Green livery bottom skirt
            const skirt = new THREE.Mesh(new THREE.BoxGeometry(2.45, 7.55, 0.5), busGreenMat);
            skirt.position.set(b.x, b.y, 0.45);
            skirt.rotation.z = b.rot;
            groups.SUR.add(skirt);

            // Panoramic side windows
            const win = new THREE.Mesh(new THREE.BoxGeometry(2.48, 6.2, 0.8), busGlassMat);
            win.position.set(b.x, b.y, 1.6);
            win.rotation.z = b.rot;
            groups.SUR.add(win);

            // Roof Battery Pack
            const batt = new THREE.Mesh(new THREE.BoxGeometry(1.8, 3.2, 0.3), new THREE.MeshStandardMaterial({{ color: 0x475569 }}));
            batt.position.set(b.x, b.y, 2.55);
            batt.rotation.z = b.rot;
            groups.SUR.add(batt);
          }});

          // 7. Subsurface Pedestrian Metro/Rail Transfer Link (Z = -6.0m to 0.0m)
          createPrism("SUB_PED_LINK", [[8, 8], [32, 8], [32, 32], [8, 32]], -6.0, 0, 0xf59e0b, 0.85, "SUB", -1, {{
            name: "Subsurface Multi-Modal Commuter Subway & Escalator Transfer Vault",
            ulpin: `${{data.base_ulpin}}-SUB-B01-PL01-M`,
            z: "-6.0m to 0.0m",
            area: "576 m²",
            vol: "3456 m³",
            owner: "State Multi-Modal Transit Directorate",
            val: "₹ 75.0 Cr"
          }});
        }}

        // DEFAULT PARAMETRIC TOWER (For Any Other Property)
        function buildModernParametricTower(data) {{
          const isRes = (data.building_type === 'Apartment') || (data.name && data.name.includes('Residency'));
          const resNames = [
            "Sh. Vikramaditya & Shweta Singhania",
            "Dr. Radhika & Amitav Oberoi",
            "Smt. Ananya & Rohit Narang",
            "Capt. Devendra K. Bakshi (Retd.)",
            "Sh. Rajeshwar & Meenakshi Sundaram",
            "Dr. Rohan & Nandini Mehta",
            "Smt. Sunita & Siddharth Agarwal",
            "Sh. Harishchandra V. Rao",
            "Smt. Priya & Sanjay Nambiar",
            "Sh. K. V. Subramanian (Equity Fund Director)"
          ];

          const h = Math.abs(data.total_height) || 60;
          const numFloors = Math.min(10, Math.max(4, Math.floor(h / 10)));
          const floorH = h / numFloors;

          for (let f = 0; f < numFloors; f++) {{
            const zMin = f * floorH * 0.35;
            const zMax = zMin + (floorH * 0.35);
            const lvl = f === 0 ? "G00" : `F0${{f}}`;
            const unitOwner = isRes ? resNames[f % resNames.length] : `${{data.name}} Corporate Tenant (Floor ${{lvl}})`;

            createPrism(`BLD_${{lvl}}`, [[8,8],[32,8],[32,32],[8,32]], zMin, zMax, 0x0284c7, 0.85, "BLD", f, {{
              name: `${{data.name}} - Volumetric Unit ${{lvl}}`,
              ulpin: `${{data.base_ulpin}}-BLD-${{lvl}}-U01-K`,
              z: `${{zMin.toFixed(1)}}m to ${{zMax.toFixed(1)}}m`,
              area: "576 m²",
              vol: `${{Math.round(576 * (zMax - zMin))}} m³`,
              owner: unitOwner,
              val: `₹ ${{Math.round(data.valuation_cr / numFloors)}} Cr`
            }});
          }}

          // Basements
          createPrism("SUB_BASE", [[8,8],[32,8],[32,32],[8,32]], -12, 0, 0xf59e0b, 0.85, "SUB", -1, {{
            name: `${{data.name}} - Subsurface Foundation & Parking`,
            ulpin: `${{data.base_ulpin}}-SUB-B01-PK01-7`,
            z: "-12.0m to 0.0m",
            area: "576 m²",
            vol: "6912 m³",
            owner: `${{data.owner}} Facilities SPV`,
            val: "₹ 35.0 Cr"
          }});
        }}

        // Surrounding Urban Context Masses (Disabled to ensure unobstructed view of the actual model)
        function addSurroundingUrbanContext() {{
          // Contextual massing blocks removed per user request for clear viewing
        }}

        // Procedural Architectural Curtain Wall & Spandrel Texture Generator
        const materialCache = new Map();
        function getArchitecturalTexture(colorHex) {{
          const hex = typeof colorHex === 'number' ? '#' + colorHex.toString(16).padStart(6, '0') : colorHex;
          if (materialCache.has(hex)) return materialCache.get(hex);

          const canvas = document.createElement('canvas');
          canvas.width = 128;
          canvas.height = 128;
          const ctx = canvas.getContext('2d');

          const grad = ctx.createLinearGradient(0, 0, 0, 128);
          grad.addColorStop(0, hex);
          grad.addColorStop(0.5, '#0284c7');
          grad.addColorStop(1, '#0f172a');
          ctx.fillStyle = grad;
          ctx.fillRect(0, 0, 128, 128);

          ctx.fillStyle = 'rgba(15, 23, 42, 0.85)';
          ctx.fillRect(0, 114, 128, 14);
          ctx.fillStyle = 'rgba(255, 255, 255, 0.4)';
          ctx.fillRect(0, 112, 128, 2);

          ctx.strokeStyle = 'rgba(255, 255, 255, 0.3)';
          ctx.lineWidth = 2;
          for (let x = 16; x < 128; x += 32) {{
            ctx.beginPath();
            ctx.moveTo(x, 0);
            ctx.lineTo(x, 112);
            ctx.stroke();
          }}

          ctx.fillStyle = 'rgba(254, 240, 138, 0.08)';
          ctx.fillRect(18, 16, 26, 80);
          ctx.fillRect(82, 20, 26, 75);

          const tex = new THREE.CanvasTexture(canvas);
          tex.wrapS = THREE.RepeatWrapping;
          tex.wrapT = THREE.RepeatWrapping;
          tex.repeat.set(2, 1);
          materialCache.set(hex, tex);
          return tex;
        }}

        function getCurvedCanopyTexture() {{
          const canvas = document.createElement('canvas');
          canvas.width = 128;
          canvas.height = 128;
          const ctx = canvas.getContext('2d');
          ctx.fillStyle = 'rgba(240, 249, 255, 0.85)';
          ctx.fillRect(0, 0, 128, 128);
          ctx.strokeStyle = '#0284c7';
          ctx.lineWidth = 3;
          for (let i = -128; i < 256; i += 32) {{
            ctx.beginPath(); ctx.moveTo(i, 0); ctx.lineTo(i + 128, 128); ctx.stroke();
            ctx.beginPath(); ctx.moveTo(i + 128, 0); ctx.lineTo(i, 128); ctx.stroke();
          }}
          const tex = new THREE.CanvasTexture(canvas);
          tex.wrapS = THREE.RepeatWrapping;
          tex.wrapT = THREE.RepeatWrapping;
          tex.repeat.set(4, 4);
          return tex;
        }}

        function getSolarPanelTexture() {{
          const canvas = document.createElement('canvas');
          canvas.width = 128;
          canvas.height = 128;
          const ctx = canvas.getContext('2d');
          ctx.fillStyle = '#0f172a';
          ctx.fillRect(0, 0, 128, 128);
          ctx.fillStyle = '#1e3a8a';
          for (let x = 4; x < 128; x += 30) {{
            for (let y = 4; y < 128; y += 30) {{
              ctx.fillRect(x, y, 26, 26);
            }}
          }}
          ctx.strokeStyle = '#94a3b8';
          ctx.lineWidth = 1;
          for (let x = 17; x < 128; x += 30) {{
            ctx.beginPath(); ctx.moveTo(x, 0); ctx.lineTo(x, 128); ctx.stroke();
          }}
          const tex = new THREE.CanvasTexture(canvas);
          tex.wrapS = THREE.RepeatWrapping;
          tex.wrapT = THREE.RepeatWrapping;
          tex.repeat.set(3, 3);
          return tex;
        }}

        function createStationSignboard(textHindi, textEng, x, y, z, rotZ) {{
          const canvas = document.createElement('canvas');
          canvas.width = 256;
          canvas.height = 64;
          const ctx = canvas.getContext('2d');
          ctx.fillStyle = '#0b3c5d';
          ctx.fillRect(0, 0, 256, 64);
          ctx.strokeStyle = '#facc15';
          ctx.lineWidth = 4;
          ctx.strokeRect(2, 2, 252, 60);

          ctx.fillStyle = '#facc15';
          ctx.font = 'bold 16px sans-serif';
          ctx.textAlign = 'center';
          ctx.fillText(textHindi, 128, 24);

          ctx.fillStyle = '#ffffff';
          ctx.font = 'bold 18px sans-serif';
          ctx.fillText(textEng, 128, 50);

          const tex = new THREE.CanvasTexture(canvas);
          const boardGeo = new THREE.BoxGeometry(4.4, 0.12, 1.1);
          const boardMat = new THREE.MeshStandardMaterial({{ map: tex, roughness: 0.4 }});
          const boardMesh = new THREE.Mesh(boardGeo, boardMat);
          boardMesh.position.set(x, y, z);
          boardMesh.rotation.z = rotZ || 0;

          // Steel support posts
          const postMat = new THREE.MeshStandardMaterial({{ color: 0x64748b, metalness: 0.7 }});
          [-1.6, 1.6].forEach(px => {{
            const pGeo = new THREE.CylinderGeometry(0.06, 0.06, z, 8);
            pGeo.rotateX(Math.PI / 2);
            const pMesh = new THREE.Mesh(pGeo, postMat);
            pMesh.position.set(x + (Math.cos(rotZ || 0) * px), y + (Math.sin(rotZ || 0) * px), z / 2);
            groups.SUR.add(pMesh);
          }});

          groups.SUR.add(boardMesh);
        }}

        function createPalmTree(x, y, zBase) {{
          const treeGroup = new THREE.Group();
          const trunkMat = new THREE.MeshStandardMaterial({{ color: 0x78350f, roughness: 0.9 }});
          const trunk = new THREE.Mesh(new THREE.CylinderGeometry(0.18, 0.32, 4.2, 8), trunkMat);
          trunk.position.set(0, 0, 2.1);
          trunk.rotation.x = Math.PI / 2;
          treeGroup.add(trunk);

          const frondMat = new THREE.MeshStandardMaterial({{ color: 0x15803d, roughness: 0.7, side: THREE.DoubleSide }});
          for (let i = 0; i < 7; i++) {{
            const angle = (i / 7) * Math.PI * 2;
            const frondGeo = new THREE.ConeGeometry(0.8, 2.8, 4);
            frondGeo.rotateX(Math.PI / 3);
            const frond = new THREE.Mesh(frondGeo, frondMat);
            frond.position.set(Math.cos(angle) * 0.4, Math.sin(angle) * 0.4, 4.1);
            frond.rotation.z = angle;
            treeGroup.add(frond);
          }}
          treeGroup.position.set(x, y, zBase || 0);
          groups.SUR.add(treeGroup);
        }}

        // -------------------------------------------------------------
        // THREE.JS GEOMETRY HELPERS
        // -------------------------------------------------------------
        function createPrism(id, coords, zMin, zMax, color, opacity, stratum, floorIdx, info) {{
          const shape = new THREE.Shape();
          shape.moveTo(coords[0][0], coords[0][1]);
          for (let i = 1; i < coords.length; i++) {{ shape.lineTo(coords[i][0], coords[i][1]); }}
          shape.closePath();

          const geo = new THREE.ExtrudeGeometry(shape, {{ steps: 1, depth: zMax - zMin, bevelEnabled: false }});
          
          let mat;
          if (stratum === "BLD" || stratum === "COM") {{
            const archTex = getArchitecturalTexture(color);
            mat = new THREE.MeshStandardMaterial({{
              color: color,
              map: archTex,
              roughness: 0.22,
              metalness: 0.65,
              transparent: true,
              opacity: Math.max(0.78, opacity),
              side: THREE.DoubleSide
            }});
          }} else if (stratum === "SUB" || stratum === "UTL") {{
            mat = new THREE.MeshStandardMaterial({{
              color: color,
              roughness: 0.8,
              metalness: 0.2,
              transparent: true,
              opacity: opacity,
              side: THREE.DoubleSide
            }});
          }} else {{
            mat = new THREE.MeshStandardMaterial({{
              color: color,
              roughness: 0.35,
              metalness: 0.15,
              transparent: true,
              opacity: opacity,
              side: THREE.DoubleSide
            }});
          }}

          const mesh = new THREE.Mesh(geo, mat);
          mesh.position.set(0, 0, zMin);
          mesh.userData = {{ id, originalZ: zMin, stratum, floorIdx, baseOpacity: opacity, baseColor: color, info }};

          // Edge Wireframe
          const wire = new THREE.LineSegments(new THREE.EdgesGeometry(geo), new THREE.LineBasicMaterial({{ color: 0xffffff, opacity: 0.3, transparent: true }}));
          mesh.add(wire);

          groups[stratum].add(mesh);
          meshMap.set(id, mesh);
          return mesh;
        }}

        function createCylinderPrism(id, radiusTop, radiusBottom, zMin, zMax, radialSegments, color, opacity, stratum, floorIdx, info) {{
          const height = zMax - zMin;
          const geo = new THREE.CylinderGeometry(radiusTop, radiusBottom, height, radialSegments);
          geo.rotateX(Math.PI / 2);

          let mat;
          if (stratum === "BLD" || stratum === "COM") {{
            const archTex = getArchitecturalTexture(color);
            archTex.repeat.set(4, 1);
            mat = new THREE.MeshStandardMaterial({{
              color: color,
              map: archTex,
              roughness: 0.2,
              metalness: 0.7,
              transparent: true,
              opacity: Math.max(0.78, opacity),
              side: THREE.DoubleSide
            }});
          }} else {{
            mat = new THREE.MeshStandardMaterial({{
              color: color,
              roughness: 0.6,
              metalness: 0.2,
              transparent: true,
              opacity: opacity,
              side: THREE.DoubleSide
            }});
          }}

          const mesh = new THREE.Mesh(geo, mat);
          const midZ = zMin + height / 2;
          mesh.position.set(20, 20, midZ);
          mesh.userData = {{ id, originalZ: midZ, stratum, floorIdx, baseOpacity: opacity, baseColor: color, info }};

          const wire = new THREE.LineSegments(new THREE.EdgesGeometry(geo), new THREE.LineBasicMaterial({{ color: 0xffffff, opacity: 0.25, transparent: true }}));
          mesh.add(wire);

          groups[stratum].add(mesh);
          meshMap.set(id, mesh);
          return mesh;
        }}

        function applyExplode(factor) {{
          const sp = 7.5 * factor;
          meshMap.forEach(m => {{
            const f = m.userData.floorIdx || 0;
            if (f > 0) m.position.z = m.userData.originalZ + (f * sp);
            else if (f < 0) m.position.z = m.userData.originalZ - (Math.abs(f) * sp * 0.75);
          }});
        }}

        function applyXRay(val) {{
          meshMap.forEach(m => {{
            const s = m.userData.stratum;
            if (s === "SUR" || s === "BLD" || s === "COM") m.material.opacity = Math.max(0.06, m.userData.baseOpacity * val);
            else if (s === "SUB" || s === "UTL") m.material.opacity = Math.min(1.0, 0.95);
          }});
        }}

        function toggleLayer(stratum, visible) {{
          if (groups[stratum]) groups[stratum].visible = visible;
        }}

        function setCam(mode) {{
          if (!controls) return;
          const isSub = BUILDING_DATA.base_elevation < 0;
          const bH = BUILDING_DATA.total_height;
          const midZ = isSub ? -8 : (bH > 150 ? 25 : 14);

          if (mode === 'iso') {{
            if (isSub) camera.position.set(48, -40, -10);
            else if (bH > 150) camera.position.set(70, -65, 75);
            else camera.position.set(52, -48, 50);
            controls.target.set(20, 20, midZ);
          }} else if (mode === 'top') {{
            camera.position.set(20, 20, bH > 150 ? 130 : 92);
            controls.target.set(20, 20, 0);
          }} else if (mode === 'sub') {{
            camera.position.set(38, -28, -18);
            controls.target.set(20, 20, -8);
            applyXRay(0.18);
            document.getElementById('rng-xray').value = 0.18;
            document.getElementById('lbl-xray').textContent = '18%';
          }} else if (mode === 'front') {{
            camera.position.set(20, -60, midZ);
            controls.target.set(20, 20, midZ);
          }}
          controls.update();
        }}

        function onPointerDown(e) {{
          const rect = renderer.domElement.getBoundingClientRect();
          const mouse = new THREE.Vector2(
            ((e.clientX - rect.left) / rect.width) * 2 - 1,
            -((e.clientY - rect.top) / rect.height) * 2 + 1
          );
          const raycaster = new THREE.Raycaster();
          raycaster.setFromCamera(mouse, camera);
          
          const visibleMeshes = Array.from(meshMap.values()).filter(m => groups[m.userData.stratum].visible);
          const hits = raycaster.intersectObjects(visibleMeshes);
          if (hits.length > 0) {{
            selectUnit(hits[0].object);
          }}
        }}

        function selectUnit(mesh) {{
          if (selectedMesh) selectedMesh.material.emissive.setHex(0x000000);
          selectedMesh = mesh;
          mesh.material.emissive.setHex(0x38bdf8);

          // Open right drawer
          document.getElementById('right-drawer').style.display = 'flex';

          const info = mesh.userData.info;
          if (info) {{
            document.getElementById('card-title').textContent = info.name;
            document.getElementById('card-ulpin').textContent = info.ulpin;
            document.getElementById('card-z').textContent = info.z;
            document.getElementById('card-vol').textContent = info.vol;
            document.getElementById('card-area').textContent = info.area;
            document.getElementById('card-owner').textContent = info.owner;
            document.getElementById('card-val').textContent = info.val;
            document.getElementById('card-lvl').textContent = `${{mesh.userData.stratum}} (Tier ${{mesh.userData.floorIdx}})`;

            // Modal sync
            document.getElementById('m-ulpin').textContent = info.ulpin;
            document.getElementById('m-name').textContent = info.name;
            document.getElementById('m-z').textContent = info.z;
            document.getElementById('m-area').textContent = info.area;
            document.getElementById('m-vol').textContent = info.vol;
            document.getElementById('m-owner').textContent = info.owner;
          }}
        }}

        function closeRightDrawer() {{
          document.getElementById('right-drawer').style.display = 'none';
          if (selectedMesh) {{
            selectedMesh.material.emissive.setHex(0x000000);
            selectedMesh = null;
          }}
        }}

        function toggleLeftControls() {{
          const sidebar = document.getElementById('left-sidebar');
          const btnShow = document.getElementById('btn-show-controls');
          const isCollapsed = sidebar.classList.toggle('collapsed');
          if (isCollapsed) {{
            btnShow.classList.add('visible');
          }} else {{
            btnShow.classList.remove('visible');
          }}
        }}

        function searchParcel() {{
          const q = document.getElementById('inp-search').value.trim().toUpperCase();
          if (!q) return;
          for (let [id, m] of meshMap.entries()) {{
            const info = m.userData.info;
            if (id.includes(q) || (info && (info.name.toUpperCase().includes(q) || info.ulpin.toUpperCase().includes(q)))) {{
              selectUnit(m);
              controls.target.set(m.position.x || 20, m.position.y || 20, m.position.z || 20);
              return;
            }}
          }}
          alert(`No 3D spatial unit matched query: "${{q}}"`);
        }}

        function switchView(tab) {{
          document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
          document.getElementById('tab-' + tab).classList.add('active');

          // Ensure left sidebar is visible when switching tabs
          const sidebar = document.getElementById('left-sidebar');
          const btnShow = document.getElementById('btn-show-controls');
          sidebar.classList.remove('collapsed');
          btnShow.classList.remove('visible');

          document.getElementById('ctrl-twin-group').style.display = tab === 'twin' ? 'flex' : 'none';
          document.getElementById('ctrl-gen-group').style.display = tab === 'gen' ? 'flex' : 'none';
          document.getElementById('ctrl-ai-group').style.display = tab === 'ai' ? 'flex' : 'none';
          document.getElementById('ctrl-topo-group').style.display = tab === 'topo' ? 'flex' : 'none';
        }}

        function executeGenerateULPIN() {{
          const strat = document.getElementById('gen-strat').value;
          const lvl = document.getElementById('gen-lvl').value.trim();
          const uid = document.getElementById('gen-uid').value.trim();
          const core = `{base_ulpin}-${{strat}}-${{lvl}}-${{uid}}`;
          
          // Modulo 36 check digit
          let sum = 0;
          for (let i = 0; i < core.length; i++) {{ sum += core.charCodeAt(i) * (i + 1); }}
          const chars = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ";
          const chk = chars[sum % 36];
          const full = `${{core}}-${{chk}}`;

          document.getElementById('gen-res').style.display = 'flex';
          document.getElementById('gen-out').textContent = full;
          document.getElementById('gen-chk').textContent = chk;
        }}

        function toggleClashHighlight() {{
          isClashActive = !isClashActive;
          meshMap.forEach(m => {{
            if (m.userData.id.includes("402") || m.userData.id.includes("AIR")) {{
              if (isClashActive) {{
                m.material.color.setHex(0xef4444);
                m.material.emissive.setHex(0xb91c1c);
              }} else {{
                m.material.color.setHex(m.userData.baseColor);
                m.material.emissive.setHex(0x000000);
              }}
            }}
          }});
        }}

        function generateLidarProfile() {{
          const bElev = BUILDING_DATA.base_elevation || 0;
          const tH = Math.abs(BUILDING_DATA.total_height) || 40;
          const zStart = bElev < 0 ? bElev - 3 : -6;
          const zEnd = bElev < 0 ? (bElev + tH + 4) : (tH + 6);
          const step = Math.max(1, Math.round((zEnd - zStart) / 12));

          const labels = [];
          const data = [];
          for (let z = zStart; z <= zEnd; z += step) {{
            labels.push(`${{Math.round(z)}}m`);
            const isFloorSlab = Math.abs(z % 3.5) < 1.2 || Math.abs(z) < 1.0;
            const density = isFloorSlab ? (360 + Math.floor(Math.random() * 110)) : (45 + Math.floor(Math.random() * 45));
            data.push(density);
          }}
          return {{ labels, data }};
        }}

        function initChart() {{
          const ctx = document.getElementById('lidar-chart');
          if (!ctx) return;
          const profile = generateLidarProfile();
          currentChart = new Chart(ctx, {{
            type: 'line',
            data: {{
              labels: profile.labels,
              datasets: [{{
                label: 'Points / 0.5m Bin',
                data: profile.data,
                borderColor: '#38bdf8',
                backgroundColor: 'rgba(56, 189, 248, 0.2)',
                fill: true,
                tension: 0.35,
                pointRadius: 2
              }}]
            }},
            options: {{
              responsive: true,
              maintainAspectRatio: false,
              plugins: {{ legend: {{ display: false }} }},
              scales: {{
                x: {{ ticks: {{ color: '#64748b', font: {{ size: 9 }} }} }},
                y: {{ ticks: {{ color: '#64748b', font: {{ size: 9 }} }} }}
              }}
            }}
          }});
        }}

        function recalculateAI() {{
          if (currentChart) {{
            const profile = generateLidarProfile();
            currentChart.data.labels = profile.labels;
            currentChart.data.datasets[0].data = profile.data;
            currentChart.update();
          }}
        }}

        function openDeedModal() {{ document.getElementById('deed-modal').classList.add('open'); }}
        function closeDeedModal() {{ document.getElementById('deed-modal').classList.remove('open'); }}

        function onResize() {{
          const w = container.clientWidth;
          const h = container.clientHeight;
          camera.aspect = w / h;
          camera.updateProjectionMatrix();
          renderer.setSize(w, h);
        }}

        function animate() {{
          requestAnimationFrame(animate);
          if (controls) controls.update();
          renderer.render(scene, camera);
        }}

        let isExplodedState = false;
        function toggleExplodedCompact() {{
          isExplodedState = !isExplodedState;
          const rng = document.getElementById('rng-explode');
          if (rng) {{
            rng.value = isExplodedState ? "0.65" : "0";
            rng.dispatchEvent(new Event('input'));
          }}
          const btn = document.getElementById('btn-tb-explode');
          if (btn) btn.classList.toggle('active', isExplodedState);
        }}

        let isXrayState = false;
        function toggleXrayMode() {{
          isXrayState = !isXrayState;
          const rng = document.getElementById('rng-xray');
          if (rng) {{
            rng.value = isXrayState ? "0.2" : "1";
            rng.dispatchEvent(new Event('input'));
          }}
          const btn = document.getElementById('btn-tb-xray');
          if (btn) btn.classList.toggle('active', isXrayState);
        }}

        function resetCamGov() {{
          setCam('iso');
          const rng1 = document.getElementById('rng-explode');
          if (rng1) {{ rng1.value = "0"; rng1.dispatchEvent(new Event('input')); }}
          const rng2 = document.getElementById('rng-xray');
          if (rng2) {{ rng2.value = "1"; rng2.dispatchEvent(new Event('input')); }}
          isExplodedState = false;
          isXrayState = false;
          const b1 = document.getElementById('btn-tb-explode');
          if (b1) b1.classList.remove('active');
          const b2 = document.getElementById('btn-tb-xray');
          if (b2) b2.classList.remove('active');
        }}

        function exportModelGLB() {{
          if (!THREE.GLTFExporter) {{
            alert("GLTFExporter is loading. Please try again in a moment.");
            return;
          }}
          const exporter = new THREE.GLTFExporter();
          const exportGroup = new THREE.Group();
          Object.values(groups).forEach(g => {{
            if (g.visible) {{
              exportGroup.add(g.clone(true));
            }}
          }});

          exporter.parse(
            exportGroup,
            function (result) {{
              let blob;
              if (result instanceof ArrayBuffer) {{
                blob = new Blob([result], {{ type: 'application/octet-stream' }});
              }} else {{
                const output = JSON.stringify(result, null, 2);
                blob = new Blob([output], {{ type: 'application/json' }});
              }}
              const link = document.createElement('a');
              link.href = URL.createObjectURL(blob);
              link.download = `${{BUILDING_DATA.name.replace(/[^a-zA-Z0-9]/g, '_')}}_3D_Digital_Twin.glb`;
              link.click();
              URL.revokeObjectURL(link.href);
            }},
            function (error) {{
              console.error('An error happened during GLTF export:', error);
              alert('Export error: ' + error.message);
            }},
            {{ binary: true }}
          );
        }}

        function loadCustom3DModel(event) {{
          const file = event.target.files[0];
          if (!file) return;
          const fileName = file.name.toLowerCase();
          const reader = new FileReader();

          if (fileName.endsWith('.glb') || fileName.endsWith('.gltf')) {{
            reader.readAsArrayBuffer(file);
            reader.onload = function (e) {{
              const contents = e.target.result;
              const loader = new THREE.GLTFLoader();
              loader.parse(contents, '', function (gltf) {{
                const model = gltf.scene;
                const box = new THREE.Box3().setFromObject(model);
                const size = box.getSize(new THREE.Vector3());
                const center = box.getCenter(new THREE.Vector3());
                const maxDim = Math.max(size.x, size.y, size.z) || 1;
                const targetScale = 38.0 / maxDim;
                model.scale.set(targetScale, targetScale, targetScale);
                model.position.set(20 - center.x * targetScale, 20 - center.y * targetScale, -box.min.z * targetScale);

                groups.BLD.clear();
                groups.BLD.add(model);
                alert(`Successfully loaded 3D Model: ${{file.name}}`);
              }}, function (err) {{
                console.error(err);
                alert('Error parsing 3D file: ' + err.message);
              }});
            }};
          }} else if (fileName.endsWith('.obj')) {{
            reader.readAsText(file);
            reader.onload = function (e) {{
              const contents = e.target.result;
              const loader = new THREE.OBJLoader();
              const obj = loader.parse(contents);
              const box = new THREE.Box3().setFromObject(obj);
              const size = box.getSize(new THREE.Vector3());
              const center = box.getCenter(new THREE.Vector3());
              const maxDim = Math.max(size.x, size.y, size.z) || 1;
              const targetScale = 38.0 / maxDim;
              obj.scale.set(targetScale, targetScale, targetScale);
              obj.position.set(20 - center.x * targetScale, 20 - center.y * targetScale, -box.min.z * targetScale);

              groups.BLD.clear();
              groups.BLD.add(obj);
              alert(`Successfully loaded OBJ Model: ${{file.name}}`);
            }};
          }}
        }}

        init();
      </script>
    </body>
    </html>
    """
    components.html(html_code, height=height, scrolling=False)
