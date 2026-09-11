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
      <!-- Three.js & OrbitControls -->
      <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
      <script src="https://cdn.jsdelivr.net/npm/three@0.128.0/examples/js/controls/OrbitControls.js"></script>
      <!-- Chart.js for LiDAR Histogram -->
      <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>

      <style>
        :root {{
          --primary: #2563eb;
          --primary-hover: #1d4ed8;
          --dark-bg: #0b1120;
          --card-bg: rgba(15, 23, 42, 0.85);
          --border-color: rgba(255, 255, 255, 0.12);
        }}
        * {{ margin: 0; padding: 0; box-sizing: border-box; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; }}
        body {{ background: var(--dark-bg); color: #f8fafc; overflow: hidden; height: 100vh; width: 100vw; display: flex; flex-direction: column; }}
        
        .glass {{
          background: var(--card-bg);
          backdrop-filter: blur(12px);
          -webkit-backdrop-filter: blur(12px);
          border: 1px solid var(--border-color);
        }}

        /* Top App Header */
        header {{
          display: flex;
          align-items: center;
          justify-content: space-between;
          padding: 6px 14px;
          height: 46px;
          background: rgba(11, 17, 32, 0.96);
          border-bottom: 1px solid var(--border-color);
          z-index: 50;
          gap: 8px;
          overflow: hidden;
          white-space: nowrap;
        }}
        .emblem-badge {{
          background: linear-gradient(135deg, #f59e0b 0%, #10b981 100%);
          color: #0f172a;
          font-weight: 800;
          font-size: 11px;
          padding: 4px 7px;
          border-radius: 6px;
          letter-spacing: 0.5px;
          flex-shrink: 0;
        }}
        .nav-tabs {{
          display: flex;
          gap: 4px;
          background: rgba(15, 23, 42, 0.7);
          padding: 3px;
          border-radius: 8px;
          border: 1px solid var(--border-color);
          flex-shrink: 1;
        }}
        .tab-btn {{
          background: transparent;
          border: none;
          color: #94a3b8;
          padding: 4px 10px;
          border-radius: 5px;
          font-size: 11px;
          font-weight: 600;
          cursor: pointer;
          transition: all 0.2s;
          display: flex;
          align-items: center;
          gap: 4px;
          white-space: nowrap;
        }}
        .tab-btn:hover {{ color: #ffffff; background: rgba(255, 255, 255, 0.05); }}
        .tab-btn.active {{ background: var(--primary); color: #ffffff; box-shadow: 0 2px 8px rgba(37, 99, 235, 0.4); }}
        
        .badge-cors {{
          display: flex;
          align-items: center;
          gap: 5px;
          font-size: 10px;
          background: rgba(16, 185, 129, 0.15);
          color: #10b981;
          padding: 3px 8px;
          border-radius: 16px;
          border: 1px solid rgba(16, 185, 129, 0.3);
          flex-shrink: 0;
        }}
        .pulse-dot {{
          width: 6px;
          height: 6px;
          background-color: #10b981;
          border-radius: 50%;
          box-shadow: 0 0 6px #10b981;
          animation: pulse 1.8s infinite;
        }}
        @keyframes pulse {{
          0% {{ transform: scale(0.95); opacity: 0.8; }}
          50% {{ transform: scale(1.3); opacity: 1; }}
          100% {{ transform: scale(0.95); opacity: 0.8; }}
        }}

        /* Workspace */
        .workspace {{ display: flex; flex: 1; position: relative; overflow: hidden; }}
        #webgl-container {{ flex: 1; width: 100%; height: 100%; position: relative; outline: none; }}

        /* Floating Left Sidebar */
        .left-controls {{
          position: absolute;
          top: 10px;
          left: 10px;
          width: 240px;
          max-height: calc(100vh - 68px);
          overflow-y: auto;
          border-radius: 10px;
          padding: 12px;
          z-index: 20;
          display: flex;
          flex-direction: column;
          gap: 10px;
          box-shadow: 0 8px 32px rgba(0, 0, 0, 0.5);
          transition: transform 0.25s cubic-bezier(0.4, 0, 0.2, 1), opacity 0.2s;
        }}
        .left-controls::-webkit-scrollbar {{ width: 3px; }}
        .left-controls::-webkit-scrollbar-thumb {{ background: rgba(255, 255, 255, 0.2); border-radius: 3px; }}
        .left-controls.collapsed {{
          transform: translateX(-115%);
          opacity: 0;
          pointer-events: none;
        }}

        /* Floating Button to re-open Controls when collapsed */
        .btn-toggle-left {{
          position: absolute;
          top: 10px;
          left: 10px;
          z-index: 22;
          background: rgba(15, 23, 42, 0.88);
          backdrop-filter: blur(8px);
          border: 1px solid rgba(56, 189, 248, 0.4);
          color: #38bdf8;
          padding: 5px 10px;
          border-radius: 8px;
          font-size: 11px;
          font-weight: 700;
          cursor: pointer;
          display: none;
          align-items: center;
          gap: 5px;
          box-shadow: 0 4px 16px rgba(0,0,0,0.5);
          transition: all 0.2s;
        }}
        .btn-toggle-left:hover {{
          background: #0284c7;
          color: #ffffff;
        }}
        .btn-toggle-left.visible {{
          display: flex;
        }}

        .panel-title {{
          font-size: 11px;
          font-weight: 700;
          text-transform: uppercase;
          letter-spacing: 0.6px;
          color: #94a3b8;
          display: flex;
          justify-content: space-between;
          align-items: center;
        }}

        input[type="range"] {{
          -webkit-appearance: none;
          width: 100%;
          height: 6px;
          border-radius: 4px;
          background: rgba(255, 255, 255, 0.15);
          outline: none;
        }}
        input[type="range"]::-webkit-slider-thumb {{
          -webkit-appearance: none;
          width: 15px;
          height: 15px;
          border-radius: 50%;
          background: var(--primary);
          cursor: pointer;
        }}

        .camera-grid {{
          display: grid;
          grid-template-columns: 1fr 1fr;
          gap: 6px;
        }}
        .camera-btn {{
          background: rgba(255, 255, 255, 0.05);
          border: 1px solid var(--border-color);
          color: #f8fafc;
          padding: 6px 8px;
          border-radius: 6px;
          font-size: 11px;
          cursor: pointer;
          transition: all 0.2s;
          text-align: center;
        }}
        .camera-btn:hover {{ background: rgba(255, 255, 255, 0.15); border-color: #38bdf8; }}

        .strata-item {{
          display: flex;
          align-items: center;
          justify-content: space-between;
          font-size: 12px;
          padding: 5px 6px;
          border-radius: 6px;
          background: rgba(255, 255, 255, 0.03);
          cursor: pointer;
        }}
        .strata-item:hover {{ background: rgba(255, 255, 255, 0.08); }}

        /* Floating Right Inspection Card */
        .right-drawer {{
          position: absolute;
          top: 10px;
          right: 10px;
          width: 260px;
          max-height: calc(100vh - 68px);
          overflow-y: auto;
          border-radius: 10px;
          padding: 12px;
          z-index: 25;
          display: none; /* Hidden by default so 3D model is completely unobstructed */
          flex-direction: column;
          gap: 10px;
          box-shadow: 0 12px 36px rgba(0, 0, 0, 0.6);
          animation: slideInRight 0.2s ease-out;
        }}
        .right-drawer::-webkit-scrollbar {{ width: 3px; }}
        .right-drawer::-webkit-scrollbar-thumb {{ background: rgba(255, 255, 255, 0.2); border-radius: 3px; }}
        @keyframes slideInRight {{
          from {{ transform: translateX(20px); opacity: 0; }}
          to {{ transform: translateX(0); opacity: 1; }}
        }}

        .ulpin-box {{
          background: rgba(15, 23, 42, 0.7);
          border: 1px solid rgba(59, 130, 246, 0.4);
          border-radius: 8px;
          padding: 10px;
          display: flex;
          flex-direction: column;
          gap: 4px;
        }}
        .ulpin-code {{
          font-family: monospace;
          font-weight: 700;
          font-size: 12px;
          color: #60a5fa;
          word-break: break-all;
        }}

        .metrics-grid {{
          display: grid;
          grid-template-columns: 1fr 1fr;
          gap: 6px;
          font-size: 11px;
        }}
        .metric-tile {{
          background: rgba(255, 255, 255, 0.04);
          padding: 6px;
          border-radius: 6px;
        }}
        .metric-tile .lbl {{ font-size: 9px; color: #94a3b8; text-transform: uppercase; }}
        .metric-tile .val {{ font-size: 12px; font-weight: 700; color: #f8fafc; }}

        .btn-primary {{
          background: var(--primary);
          color: #ffffff;
          border: none;
          padding: 8px 12px;
          border-radius: 8px;
          font-size: 12px;
          font-weight: 600;
          cursor: pointer;
          transition: all 0.2s;
          display: flex;
          align-items: center;
          justify-content: center;
          gap: 6px;
        }}
        .btn-primary:hover {{ background: var(--primary-hover); }}

        /* Modal */
        .modal-overlay {{
          position: fixed;
          top: 0; left: 0; width: 100vw; height: 100vh;
          background: rgba(0,0,0,0.75);
          backdrop-filter: blur(8px);
          display: none;
          align-items: center;
          justify-content: center;
          z-index: 100;
        }}
        .modal-overlay.open {{ display: flex; }}
        .cert-sheet {{
          background: #ffffff;
          color: #1e293b;
          border: 10px double #0284c7;
          border-radius: 12px;
          padding: 24px;
          max-width: 750px;
          width: 90%;
          max-height: 85vh;
          overflow-y: auto;
        }}
      </style>
    </head>
    <body>
      <!-- Header -->
      <header>
        <div class="flex items-center gap-2 min-w-0">
          <div class="emblem-badge">IN 3D-ULPIN</div>
          <div class="truncate">
            <div class="flex items-center gap-1.5">
              <h1 class="font-bold text-xs tracking-tight text-white truncate max-w-[150px]" title="{property_name}">{property_name}</h1>
              <span class="text-[9px] text-amber-400 font-mono font-bold hidden sm:inline">[{building_type} &bull; {archetype_title}]</span>
            </div>
            <p class="text-[9px] text-slate-400 truncate hidden md:block">{city} • {zone} &bull; {elev_str}</p>
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
            <span class="font-mono text-[9px] font-bold">RTK ACTIVE</span>
          </div>
        </div>
      </header>

      <!-- Main Workspace -->
      <div class="workspace">
        
        <!-- Toggle button to restore left sidebar when collapsed -->
        <button id="btn-show-controls" class="btn-toggle-left" onclick="toggleLeftControls()" title="Open Controls Menu">
          <i data-lucide="sliders" class="w-3.5 h-3.5"></i>
          <span>Controls</span>
        </button>

        <!-- Left Sidebar Controls -->
        <aside class="left-controls glass" id="left-sidebar">
          
          <!-- Top bar with Collapse button -->
          <div class="flex items-center justify-between pb-1 border-b border-white/10">
            <span class="text-[10px] font-bold text-sky-400 uppercase tracking-wider flex items-center gap-1.5">
              <i data-lucide="sliders" class="w-3 h-3"></i> Controls Panel
            </span>
            <button onclick="toggleLeftControls()" class="text-slate-400 hover:text-white px-1.5 py-0.5 rounded hover:bg-white/10 text-[10px] flex items-center gap-1 border border-white/10" title="Collapse Menu to clear 3D view">
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
          scene.background = new THREE.Color(0x0b1120);
          scene.fog = new THREE.FogExp2(0x0b1120, 0.0032);

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

          // Surrounding Urban Context Blocks
          addSurroundingUrbanContext();

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

        // ARCHETYPE 2: Worli Sea-Facing Super-Tower (Mumbai) - Pei Cobb Freed 3-Winged Cloverleaf 280m Skyscraper
        function buildSupertallTiered(data) {{
          // Authentic Pei Cobb Freed & Partners Curvilinear Cloverleaf Architecture:
          // 3 curved petal wings radiating outward at 0°, 120°, and 240° around a central core

          // Tier 1: Grand Port Cochère & Club W Lifestyle Podium (0 to 12m)
          createPrism("BLD_PODIUM", [[5,5],[35,5],[35,35],[5,35]], 0, 12, 0xd97706, 0.88, "BLD", 1, {{
            name: "Triple-Height Concierge Port Cochère & Club W Lifestyle Podium",
            ulpin: `${{data.base_ulpin}}-BLD-P01-GR01-7`,
            z: "0.0m to +12.0m",
            area: "900 m²",
            vol: "10800 m³",
            owner: "World One Grand Concierge & Reception Trust",
            val: "₹ 420 Cr"
          }});

          // Unique Authentic HNI Resident Registry by Wing and Floor
          const residentRegistry = {{
            3: [
              "Sh. Vikramaditya & Shweta Singhania",
              "Dr. Radhika & Amitav Oberoi",
              "Smt. Ananya & Rohit Narang"
            ],
            4: [
              "Capt. Devendra K. Bakshi (Retd. Naval Commander)",
              "Sh. Rajeshwar & Meenakshi Sundaram",
              "Dr. Rohan & Nandini Mehta"
            ],
            5: [
              "Smt. Sunita & Siddharth Agarwal",
              "Sh. Harishchandra V. Rao",
              "Smt. Priya & Sanjay Nambiar"
            ]
          }};

          // Tier 2: Mid-Rise 3-Winged Cloverleaf Petals (12 to 26m)
          for (let f = 3; f <= 5; f++) {{
            const zMin = 12 + (f - 3) * 4.6;
            const zMax = zMin + 4.6;
            const lvl = `L0${{f}}`;
            const wingOwners = residentRegistry[f] || residentRegistry[3];

            // Central Core
            createCylinderPrism(`BLD_CORE_${{lvl}}`, 6.0, 6.0, zMin, zMax, 24, 0x0284c7, 0.7, "COM", f, {{
              name: `World One Elevator Core & Service Spine (${{lvl}})`,
              ulpin: `${{data.base_ulpin}}-COM-${{lvl}}-CR01-1`,
              z: `${{zMin.toFixed(1)}}m to ${{zMax.toFixed(1)}}m`,
              area: "113 m²",
              vol: "520 m³",
              owner: "World One Common Strata Facilities Association",
              val: "₹ 15.0 Cr"
            }});

            // Wing 1 (North - Arabian Sea Panorama)
            createPrism(`BLD_W1_${{lvl}}`, [[15, 20], [25, 20], [24, 36], [16, 36]], zMin, zMax, 0x0284c7, 0.85, "BLD", f, {{
              name: `Signature Arabian Sea-Facing Luxury Residence ${{lvl}}01`,
              ulpin: `${{data.base_ulpin}}-BLD-${{lvl}}-W101-A`,
              z: `${{zMin.toFixed(1)}}m to ${{zMax.toFixed(1)}}m`,
              area: "135 m²",
              vol: "621 m³",
              owner: wingOwners[0],
              val: "₹ 48.0 Cr"
            }});

            // Wing 2 (South-East - Worli Sea Face)
            createPrism(`BLD_W2_${{lvl}}`, [[20, 15], [20, 25], [34, 17], [30, 9]], zMin, zMax, 0x0369a1, 0.85, "BLD", f, {{
              name: `Worli Sea Face Luxury Panorama Residence ${{lvl}}02`,
              ulpin: `${{data.base_ulpin}}-BLD-${{lvl}}-W201-B`,
              z: `${{zMin.toFixed(1)}}m to ${{zMax.toFixed(1)}}m`,
              area: "130 m²",
              vol: "598 m³",
              owner: wingOwners[1],
              val: "₹ 46.5 Cr"
            }});

            // Wing 3 (South-West - Bandra Sea Link Overlook)
            createPrism(`BLD_W3_${{lvl}}`, [[20, 15], [20, 25], [10, 9], [6, 17]], zMin, zMax, 0x0ea5e9, 0.85, "BLD", f, {{
              name: `Sea Link Sunset Sky Villa ${{lvl}}03`,
              ulpin: `${{data.base_ulpin}}-BLD-${{lvl}}-W301-C`,
              z: `${{zMin.toFixed(1)}}m to ${{zMax.toFixed(1)}}m`,
              area: "130 m²",
              vol: "598 m³",
              owner: wingOwners[2],
              val: "₹ 46.5 Cr"
            }});

            // Curved cantilevered balcony slab bands (Pei Cobb Freed styling)
            const balconyMat = new THREE.MeshStandardMaterial({{ color: 0xf8fafc, roughness: 0.3, metalness: 0.2 }});
            const b1 = new THREE.Mesh(new THREE.BoxGeometry(10, 1, 0.35), balconyMat);
            b1.position.set(20, 36.2, zMin + 0.2);
            groups.BLD.add(b1);
            const b2 = new THREE.Mesh(new THREE.BoxGeometry(8, 1, 0.35), balconyMat);
            b2.rotation.z = Math.PI / 3;
            b2.position.set(32, 13, zMin + 0.2);
            groups.BLD.add(b2);
            const b3 = new THREE.Mesh(new THREE.BoxGeometry(8, 1, 0.35), balconyMat);
            b3.rotation.z = -Math.PI / 3;
            b3.position.set(8, 13, zMin + 0.2);
            groups.BLD.add(b3);
          }}

          // Tier 3: High-Rise Setback Sky Mansions (26 to 38m)
          const duplexOwners = [
            "Sh. K. V. Subramanian (Global Equity Fund Director)",
            "Smt. Divya & Gautam Chopra (Logistics Pioneers)",
            "Sh. Jaideep & Vandana Munjal (Industrialist)"
          ];

          for (let f = 6; f <= 8; f++) {{
            const zMin = 26 + (f - 6) * 4.0;
            const zMax = zMin + 4.0;
            const lvl = `L0${{f}}`;
            createPrism(`BLD_SKY_${{lvl}}`, [[11,11],[29,11],[29,29],[11,29]], zMin, zMax, 0x38bdf8, 0.88, "BLD", f, {{
              name: `High-Rise Panoramic Sky Duplex Suite (${{lvl}})`,
              ulpin: `${{data.base_ulpin}}-BLD-${{lvl}}-SD01-S`,
              z: `${{zMin.toFixed(1)}}m to ${{zMax.toFixed(1)}}m`,
              area: "324 m²",
              vol: "1296 m³",
              owner: duplexOwners[f - 6] || `Exclusive Duplex Title Holder (${{lvl}})`,
              val: "₹ 72.0 Cr"
            }});
          }}

          // Tier 4: Sovereign Triplex Penthouse & Sky Plunge Pool (38 to 48m)
          createPrism("BLD_PENTHOUSE", [[14,14],[26,14],[26,26],[14,26]], 38, 48, 0x06b6d4, 0.92, "BLD", 9, {{
            name: "World One Sovereign Triplex Penthouse with Private Infinity Plunge Pool",
            ulpin: `${{data.base_ulpin}}-BLD-L16-PH01-P`,
            z: "+38.0m to +48.0m",
            area: "144 m²",
            vol: "1440 m³",
            owner: "Sovereign Sky Palace Family Trust (Chairman Suite)",
            val: "₹ 165 Cr"
          }});

          // Architectural Crystalline Crown Spire & Flashing Beacon (48 to 62m)
          const spGeo = new THREE.ConeGeometry(3.0, 14, 12);
          spGeo.rotateX(Math.PI / 2);
          const spMat = new THREE.MeshStandardMaterial({{ color: 0xfbbf24, emissive: 0xd97706, roughness: 0.15, metalness: 0.6 }});
          const spMesh = new THREE.Mesh(spGeo, spMat);
          spMesh.position.set(20, 20, 55);
          groups.AIR.add(spMesh);

          const mastTopGeo = new THREE.CylinderGeometry(0.12, 0.35, 8, 8);
          mastTopGeo.rotateX(Math.PI / 2);
          const mastTop = new THREE.Mesh(mastTopGeo, new THREE.MeshBasicMaterial({{ color: 0xffffff }}));
          mastTop.position.set(20, 20, 62);
          groups.AIR.add(mastTop);

          // 4-Tier Automated Robotic Valet Vault (-18m to 0m)
          createPrism("SUB_VAULT", [[6,6],[34,6],[34,34],[6,34]], -18, 0, 0xf59e0b, 0.85, "SUB", -1, {{
            name: "Worli 4-Tier Automated Robotic Valet Vault & HVAC Plant",
            ulpin: `${{data.base_ulpin}}-SUB-B04-RP01-3`,
            z: "-18.0m to 0.0m",
            area: "784 m²",
            vol: "14112 m³",
            owner: "World One Resident Automated Valet Trust",
            val: "₹ 110 Cr"
          }});
        }}

        // ARCHETYPE 3: UB City & Kingfisher Towers (Bengaluru) - Dual Tower with Cantilevered Sky Mansion
        function buildUBcitySteppedSpire(data) {{
          // 1. Neoclassical Luxury Retail Galleria Podium (The Collection, 0 to 8m)
          createPrism("BLD_GALLERIA", [[5,5],[35,5],[35,35],[5,35]], 0, 8, 0x059669, 0.86, "BLD", 1, {{
            name: "The Collection Luxury Galleria & Roman Arched Piazza",
            ulpin: `${{data.base_ulpin}}-BLD-P01-GL01-B`,
            z: "0.0m to +8.0m",
            area: "900 m²",
            vol: "7200 m³",
            owner: "The Collection Luxury Galleria Piazza Trust",
            val: "₹ 480 Cr"
          }});

          const ubCorporateTenants = [
            "KKR & Co. India Private Equity Advisors",
            "Morgan Stanley Advantage Services India",
            "United Breweries Holdings Ltd (Corporate Headquarters)",
            "Blackstone India Real Estate Advisory"
          ];

          // 2. Structure A: Corporate UB Tower (West Wing: x 7-19, y 9-31, 8 to 26m)
          for (let f = 3; f <= 6; f++) {{
            const zMin = 8 + (f - 3) * 4.5;
            const zMax = zMin + 4.5;
            createPrism(`BLD_UB_F0${{f}}`, [[7,9],[19,9],[19,31],[7,31]], zMin, zMax, 0x10b981, 0.85, "BLD", f, {{
              name: `UB Corporate Tower Executive Offices (Level 0${{f}})`,
              ulpin: `${{data.base_ulpin}}-BLD-F0${{f}}-UB01-U`,
              z: `${{zMin.toFixed(1)}}m to ${{zMax.toFixed(1)}}m`,
              area: "264 m²",
              vol: "1188 m³",
              owner: ubCorporateTenants[f - 3] || "UBHL Corporate Holdings",
              val: "₹ 28.0 Cr"
            }});
          }}

          // Elevated Helipad on Stilt Columns atop UB Tower (Z = 28m)
          const ubHeliGeo = new THREE.CylinderGeometry(5.5, 5.5, 0.4, 24);
          ubHeliGeo.rotateX(Math.PI / 2);
          const ubHeli = new THREE.Mesh(ubHeliGeo, new THREE.MeshStandardMaterial({{ color: 0x1e293b, roughness: 0.8 }}));
          ubHeli.position.set(13, 20, 27);
          groups.AIR.add(ubHeli);

          // Gilded Needle Spire atop UB Tower
          const spGeo = new THREE.CylinderGeometry(0.15, 1.2, 14, 16);
          spGeo.rotateX(Math.PI / 2);
          const spMat = new THREE.MeshStandardMaterial({{ color: 0xf59e0b, metalness: 0.8, roughness: 0.2 }});
          const spMesh = new THREE.Mesh(spGeo, spMat);
          spMesh.position.set(13, 20, 34);
          groups.AIR.add(spMesh);

          const kfResidents = [
            "Sh. Kiran Mazumdar-Shaw & Family Trust",
            "Dr. Devi Prasad & Alaknanda Shetty",
            "Sh. Nandan & Rohini Nilekani Family Trust",
            "Sh. Kris & Sudha Gopalakrishnan"
          ];

          // 3. Structure B: Prestige Kingfisher Towers (East Wing: x 21-33, y 9-31, 8 to 28m)
          for (let f = 3; f <= 6; f++) {{
            const zMin = 8 + (f - 3) * 4.8;
            const zMax = zMin + 4.8;
            createPrism(`BLD_KF_F0${{f}}`, [[21,9],[33,9],[33,31],[21,31]], zMin, zMax, 0x0284c7, 0.85, "BLD", f, {{
              name: `Prestige Kingfisher Ultra-Luxury Residences (Level 0${{f}})`,
              ulpin: `${{data.base_ulpin}}-BLD-F0${{f}}-KF01-K`,
              z: `${{zMin.toFixed(1)}}m to ${{zMax.toFixed(1)}}m`,
              area: "264 m²",
              vol: "1267 m³",
              owner: kfResidents[f - 3] || "Prestige Luxury Living",
              val: "₹ 36.0 Cr"
            }});
          }}

          // 4. THE FAMOUS CANTILEVERED "WHITE HOUSE IN THE SKY" MANSION (Z = 28 to 36m)
          // Cantilever platform jutting out 2m over the tower edge
          createPrism("BLD_WHITE_HOUSE_BASE", [[19,7],[35,7],[35,33],[19,33]], 28, 29, 0xf8fafc, 0.95, "BLD", 7, {{
            name: "Prestige Cantilevered Steel Transfer Deck",
            ulpin: `${{data.base_ulpin}}-BLD-F07-DK01-W`,
            z: "+28.0m to +29.0m",
            area: "416 m²",
            vol: "416 m³",
            owner: "Private Sky Mansion Trust",
            val: "₹ 35.0 Cr"
          }});

          // Neoclassical 2-Storey White Mansion & Infinity Pool
          createPrism("BLD_SKY_MANSION", [[20,8],[34,8],[34,32],[20,32]], 29, 36, 0xf1f5f9, 0.95, "BLD", 8, {{
            name: "Prestige Kingfisher 'White House in the Sky' Luxury Penthouse (40,000 sq ft)",
            ulpin: `${{data.base_ulpin}}-BLD-F08-WH01-M`,
            z: "+29.0m to +36.0m",
            area: "336 m²",
            vol: "2352 m³",
            owner: "Sovereign Sky Mansion Trust (Cantilevered White House)",
            val: "₹ 175 Cr"
          }});

          // Mansion Classical Pitched Roof
          const roofGeo = new THREE.ConeGeometry(8, 4.5, 4);
          roofGeo.rotateX(Math.PI / 2);
          roofGeo.rotateZ(Math.PI / 4);
          const roofMesh = new THREE.Mesh(roofGeo, new THREE.MeshStandardMaterial({{ color: 0x94a3b8, roughness: 0.3 }}));
          roofMesh.position.set(27, 20, 38.2);
          groups.AIR.add(roofMesh);

          // Subsurface Luxury Supercar Parking
          createPrism("SUB_UB", [[6,6],[34,6],[34,34],[6,34]], -14, 0, 0xf59e0b, 0.85, "SUB", -1, {{
            name: "UB City Supercar Concierge Basements (B1-B2)",
            ulpin: `${{data.base_ulpin}}-SUB-B02-UB01-5`,
            z: "-14.0m to 0.0m",
            area: "784 m²",
            vol: "10976 m³",
            owner: "UB City Supercar Concierge & Security Operations",
            val: "₹ 65.0 Cr"
          }});
        }}

        // ARCHETYPE 4: GIFT Diamond Tower & BKC Diamond Tower - Crystalline Faceted Skyscraper
        function buildDiamondTower(data) {{
          const diamondPoly = [[14,6],[26,6],[34,14],[34,26],[26,34],[14,34],[6,26],[6,14]];
          
          const bourseTenants = [
            "Bharat Diamond Bourse / International Bullion Exchange",
            "Gemological Institute of America (GIA) India",
            "Rosy Blue India Private Limited (Diamond Trading Wing)",
            "Kiran Gems Private Limited",
            "State Bank of India International Banking Branch",
            "NSE International Exchange (NSE IX)",
            "International Financial Services Centres Authority (IFSCA)",
            "Global Diamond Bourse Custodian"
          ];

          for (let f = 0; f <= 7; f++) {{
            const zMin = f * 4.5;
            const zMax = zMin + 4.5;
            const lvl = f === 0 ? "G00" : `F0${{f}}`;
            
            createPrism(`BLD_${{lvl}}_DIAMOND`, diamondPoly, zMin, zMax, 0x06b6d4, 0.85, "BLD", f, {{
              name: `Diamond Bourse International Trading Floor (${{lvl}})`,
              ulpin: `${{data.base_ulpin}}-BLD-${{lvl}}-DM01-D`,
              z: `${{zMin.toFixed(1)}}m to ${{zMax.toFixed(1)}}m`,
              area: "624 m²",
              vol: "2808 m³",
              owner: bourseTenants[f] || "Global Diamond Bourse Custodian",
              val: "₹ 62.0 Cr"
            }});
          }}

          // Angular Sky Atrium Cut
          const aGeo = new THREE.ConeGeometry(5, 8, 4);
          aGeo.rotateX(Math.PI / 2);
          const aMat = new THREE.MeshStandardMaterial({{ color: 0x38bdf8, transparent: true, opacity: 0.9 }});
          const aMesh = new THREE.Mesh(aGeo, aMat);
          aMesh.position.set(20, 20, 39);
          groups.AIR.add(aMesh);

          // Subsurface Utility Tunnel (TUM) Connection
          const pGeo = new THREE.CylinderGeometry(1.2, 1.2, 44, 16);
          pGeo.rotateZ(Math.PI / 2);
          const pMat = new THREE.MeshStandardMaterial({{ color: 0xa855f7, transparent: true, opacity: 0.9 }});
          const pMesh = new THREE.Mesh(pGeo, pMat);
          pMesh.position.set(20, 10, -8);
          groups.UTL.add(pMesh);
          meshMap.set("UTL_TUM", pMesh);

          createPrism("SUB_VAULT", [[8,8],[32,8],[32,32],[8,32]], -16, 0, 0xf59e0b, 0.85, "SUB", -1, {{
            name: "High-Security Diamond & Bullion Vault (B1-B3)",
            ulpin: `${{data.base_ulpin}}-SUB-B03-BV01-9`,
            z: "-16.0m to 0.0m",
            area: "576 m²",
            vol: "9216 m³",
            owner: "Reserve Bank of India & Customs High-Security Depository",
            val: "₹ 480 Cr"
          }});
        }}

        // ARCHETYPE 5: Connaught Outer Circle & Rajiv Chowk Metro (New Delhi) - Concentric Colonnade & Subterranean Hub
        function buildHeritageRotunda(data) {{
          // 1. Outer Georgian Doric Colonnade Arcade (Ground to +6m, Radius 18m)
          createCylinderPrism("BLD_COLONNADE", 18, 18, 0, 6, 36, 0xf8fafc, 0.9, "BLD", 0, {{
            name: "Lutyens Heritage Colonnade Arcade & Doric Portico (Outer Circle)",
            ulpin: `${{data.base_ulpin}}-BLD-G00-HD01-1`,
            z: "0.0m to +6.0m",
            area: "1017 m²",
            vol: "6102 m³",
            owner: "New Delhi Municipal Council (Colonnade Heritage Custodian)",
            val: "₹ 340 Cr"
          }});

          // 2. Central Park Circular Green Lawn & Inner Circle Ring
          const parkGeo = new THREE.CylinderGeometry(11, 11, 0.3, 32);
          parkGeo.rotateX(Math.PI / 2);
          const parkMat = new THREE.MeshStandardMaterial({{ color: 0x15803d, roughness: 0.9 }});
          const parkMesh = new THREE.Mesh(parkGeo, parkMat);
          parkMesh.position.set(20, 20, 0.15);
          groups.SUR.add(parkMesh);

          // Central Monumental National Flag Mast (Height 16m)
          const flagMastGeo = new THREE.CylinderGeometry(0.12, 0.3, 16, 12);
          flagMastGeo.rotateX(Math.PI / 2);
          const flagMast = new THREE.Mesh(flagMastGeo, new THREE.MeshStandardMaterial({{ color: 0xe2e8f0, metalness: 0.8 }}));
          flagMast.position.set(20, 20, 8.0);
          groups.SUR.add(flagMast);

          const cpLeaseholders = [
            "Standard Chartered Bank Heritage Flagship Branch",
            "Oxford University Press & Legal Chambers",
            "Lutyens Heritage Trust & Rotunda Observatory",
            "Central Business District Corporate Chambers"
          ];

          // 3. Middle Commercial Ring Storeys (6 to 24m)
          for (let f = 1; f <= 4; f++) {{
            const zMin = 6 + (f - 1) * 4.5;
            const zMax = zMin + 4.5;
            createCylinderPrism(`BLD_F0${{f}}_ROTUNDA`, 13, 13, zMin, zMax, 28, 0xd97706, 0.82, "BLD", f, {{
              name: `Connaught Place Central Business Suites (Tier ${{f}})`,
              ulpin: `${{data.base_ulpin}}-BLD-F0${{f}}-RT01-N`,
              z: `${{zMin.toFixed(1)}}m to ${{zMax.toFixed(1)}}m`,
              area: "530 m²",
              vol: "2385 m³",
              owner: cpLeaseholders[f - 1] || "NDMC Authorized Commercial Leaseholder",
              val: "₹ 48.0 Cr"
            }});
          }}

          // 4. Stepped Rotunda Dome Lantern (24 to 32m)
          const dGeo = new THREE.SphereGeometry(6.5, 24, 16, 0, Math.PI * 2, 0, Math.PI / 2);
          dGeo.rotateX(Math.PI / 2);
          const dMat = new THREE.MeshStandardMaterial({{ color: 0x9a3412, roughness: 0.5 }});
          const dMesh = new THREE.Mesh(dGeo, dMat);
          dMesh.position.set(20, 20, 24);
          groups.AIR.add(dMesh);

          // 5. Multi-Level Rajiv Chowk Underground Metro Cavern
          // B1: Concourse & Palika Bazaar Link (-7 to 0m)
          createPrism("SUB_CONCOURSE", [[5,5],[35,5],[35,35],[5,35]], -7, 0, 0xf59e0b, 0.85, "SUB", -1, {{
            name: "Rajiv Chowk Metro Concourse & Palika Underground Link",
            ulpin: `${{data.base_ulpin}}-SUB-B01-RC01-4`,
            z: "-7.0m to 0.0m",
            area: "900 m²",
            vol: "6300 m³",
            owner: "Delhi Metro Rail Corp (DMRC Station Operations)",
            val: "₹ 420 Cr"
          }});

          // B2: Yellow Line (North-South) Dual Island Platforms (-14 to -7m)
          createPrism("SUB_YELLOW_LINE", [[13,2],[27,2],[27,38],[13,38]], -14, -7, 0xeab308, 0.88, "UTL", -2, {{
            name: "Yellow Line Dual Island Platform 1 & 2 (North-South Rapid Transit)",
            ulpin: `${{data.base_ulpin}}-UTL-B02-YL01-Y`,
            z: "-14.0m to -7.0m",
            area: "504 m²",
            vol: "3528 m³",
            owner: "DMRC Yellow Line Operations Directorate",
            val: "₹ 380 Cr"
          }});

          // B3: Blue Line (East-West) Deep Platform & Shield Tunnels (-22 to -14m)
          createPrism("SUB_BLUE_LINE", [[2,13],[38,13],[38,27],[2,27]], -22, -14, 0x0284c7, 0.9, "UTL", -3, {{
            name: "Blue Line Deep Platform 3 & 4 (East-West Metro Corridor)",
            ulpin: `${{data.base_ulpin}}-UTL-B03-BL01-B`,
            z: "-22.0m to -14.0m",
            area: "504 m²",
            vol: "4032 m³",
            owner: "DMRC Blue Line Operations Directorate",
            val: "₹ 410 Cr"
          }});
        }}

        // ARCHETYPE 6: Seawoods Grand Central (Navi Mumbai) - Transit-Oriented Development (TOD)
        function buildSeawoodsQuadPodium(data) {{
          // 1. Nexus Grand Central 3-Storey Retail Mall Podium (0 to 10m)
          createPrism("BLD_PODIUM", [[3,3],[37,3],[37,37],[3,37]], 0, 10, 0x0284c7, 0.85, "BLD", 0, {{
            name: "Nexus Grand Central Retail & Multiplex Podium (Floors G00-L02)",
            ulpin: `${{data.base_ulpin}}-BLD-G00-POD1-8`,
            z: "0.0m to +10.0m",
            area: "1156 m²",
            vol: "11560 m³",
            owner: "Nexus Select Trust (Nexus Grand Central Mall Retailers)",
            val: "₹ 620 Cr"
          }});

          // 2. Active Railway Track Corridor with Dual Tracks cutting through Ground Level
          const trkCorridor = new THREE.Mesh(new THREE.BoxGeometry(44, 5, 0.3), new THREE.MeshStandardMaterial({{ color: 0x1e293b, roughness: 0.9 }}));
          trkCorridor.position.set(20, 20, 0.15);
          groups.SUR.add(trkCorridor);

          [-1.5, 1.5].forEach(offsetY => {{
            const railMesh = new THREE.Mesh(new THREE.BoxGeometry(44, 0.35, 0.25), new THREE.MeshStandardMaterial({{ color: 0x94a3b8, metalness: 0.9, roughness: 0.2 }}));
            railMesh.position.set(20, 20 + offsetY, 0.35);
            groups.SUR.add(railMesh);
          }});

          // 3. Five Elliptical Skylights on the Podium Roof Terrace (Z = 10m)
          const mainDome = new THREE.Mesh(new THREE.SphereGeometry(4.6, 24, 14, 0, Math.PI * 2, 0, Math.PI / 2), new THREE.MeshStandardMaterial({{ color: 0x38bdf8, transparent: true, opacity: 0.82, roughness: 0.1 }}));
          mainDome.position.set(20, 20, 10);
          groups.AIR.add(mainDome);

          const domeLocs = [[11, 11], [29, 11], [11, 29], [29, 29]];
          domeLocs.forEach(([dx, dy]) => {{
            const sDome = new THREE.Mesh(new THREE.SphereGeometry(2.3, 16, 10, 0, Math.PI * 2, 0, Math.PI / 2), new THREE.MeshStandardMaterial({{ color: 0x06b6d4, transparent: true, opacity: 0.8, roughness: 0.1 }}));
            sDome.position.set(dx, dy, 10);
            groups.AIR.add(sDome);
          }});

          // 4. Four Distinct Quad Towers (Floors 3 to 7, 10 to 34m)
          const quads = [
            {{ id: "T1", name: "Quad Tower 1 (Fintech & Cloud Hub)", poly: [[5,22],[17,22],[17,35],[5,35]], clr: 0x0369a1, owner: "Larsen & Toubro Infotech (LTIMindtree Cloud Center)" }},
            {{ id: "T2", name: "Quad Tower 2 (Engineering & R&D)", poly: [[23,22],[35,22],[35,35],[23,35]], clr: 0x38bdf8, owner: "Jacobs Engineering India Private Limited" }},
            {{ id: "T3", name: "Quad Tower 3 (Global Business Services)", poly: [[5,5],[17,5],[17,18],[5,18]], clr: 0x0284c7, owner: "BNP Paribas India Solutions Private Limited" }},
            {{ id: "T4", name: "Quad Tower 4 (Multinational Headquarters)", poly: [[23,5],[35,5],[35,18],[23,18]], clr: 0x0ea5e9, owner: "Siemens Healthcare & Smart Infrastructure HQ" }}
          ];

          quads.forEach(q => {{
            for (let f = 3; f <= 7; f++) {{
              const zMin = 10 + (f - 3) * 4.8;
              const zMax = zMin + 4.8;
              createPrism(`BLD_${{q.id}}_F0${{f}}`, q.poly, zMin, zMax, q.clr, 0.86, "BLD", f, {{
                name: `${{q.name}} (Level 0${{f}})`,
                ulpin: `${{data.base_ulpin}}-BLD-F0${{f}}-${{q.id}}01-M`,
                z: `${{zMin.toFixed(1)}}m to ${{zMax.toFixed(1)}}m`,
                area: "144 m²",
                vol: "691 m³",
                owner: q.owner,
                val: "₹ 24.5 Cr"
              }});
            }}
          }});

          // 5. Connecting Elevated Glass Skybridges between Towers
          createPrism("BLD_SKYWALK_NORTH", [[17,26],[23,26],[23,30],[17,30]], 20, 24, 0x38bdf8, 0.8, "COM", 5, {{
            name: "Connecting Skybridge Galleria North (Tower 1 to 2)",
            ulpin: `${{data.base_ulpin}}-COM-F05-SBN1-6`,
            z: "+20.0m to +24.0m",
            area: "24 m²",
            vol: "96 m³",
            owner: "Seawoods Common Facilities Custodian",
            val: "₹ 12.0 Cr"
          }});

          createPrism("BLD_SKYWALK_SOUTH", [[17,10],[23,10],[23,14],[17,14]], 20, 24, 0x38bdf8, 0.8, "COM", 5, {{
            name: "Connecting Skybridge Galleria South (Tower 3 to 4)",
            ulpin: `${{data.base_ulpin}}-COM-F05-SBS1-7`,
            z: "+20.0m to +24.0m",
            area: "24 m²",
            vol: "96 m³",
            owner: "Seawoods Common Facilities Custodian",
            val: "₹ 12.0 Cr"
          }});

          // 6. Subsurface Commuter Park-and-Ride Basements (-15m to 0m)
          createPrism("SUB_BASE", [[5,5],[35,5],[35,35],[5,35]], -15, 0, 0xf59e0b, 0.85, "SUB", -1, {{
            name: "Seawoods Commuter Park-and-Ride & Infrastructure Vault",
            ulpin: `${{data.base_ulpin}}-SUB-B02-SW01-7`,
            z: "-15.0m to 0.0m",
            area: "900 m²",
            vol: "13500 m³",
            owner: "CIDCO Urban Infrastructure Authority (Park-and-Ride)",
            val: "₹ 210 Cr"
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

        // ARCHETYPE 8: Subterranean Multilevel Cavern (Rajiv Chowk, BKC Metro-3, Chennai Central, Cubbon Park)
        function buildSubterraneanCavern(data) {{
          // Street Level Minimalist Glass Pavilion (0 to 4m)
          createPrism("SUR_ENTRANCE", [[14,14],[26,14],[26,26],[14,26]], 0, 4, 0x38bdf8, 0.7, "BLD", 0, {{
            name: "Surface Metro Entry Pavilion & Escalator Plazas",
            ulpin: `${{data.base_ulpin}}-SUR-G00-EN01-2`,
            z: "0.0m to +4.0m",
            area: "144 m²",
            vol: "576 m³",
            owner: data.owner,
            val: "₹ 45.0 Cr"
          }});

          // Level B1: Ticket Hall, Smart AFC Gates & Retail Concourse (-7 to 0m)
          createPrism("SUB_B1_CONCOURSE", [[5,5],[35,5],[35,35],[5,35]], -7, 0, 0xf59e0b, 0.85, "SUB", -1, {{
            name: "Subsurface Concourse, AFC Smart Gates & Ticketing Hall (Level B1)",
            ulpin: `${{data.base_ulpin}}-SUB-B01-TC01-M`,
            z: "-7.0m to 0.0m",
            area: "900 m²",
            vol: "6300 m³",
            owner: data.owner,
            val: "₹ 280 Cr"
          }});

          // Level B2: Traction Power, Ventilation & Signal Interlocking (-15 to -7m)
          createPrism("SUB_B2_PLANT", [[7,7],[33,7],[33,33],[7,33]], -15, -7, 0xd97706, 0.85, "SUB", -2, {{
            name: "Environmental Control, Traction Power & Signal Interlocking Vault (Level B2)",
            ulpin: `${{data.base_ulpin}}-SUB-B02-PL01-8`,
            z: "-15.0m to -7.0m",
            area: "676 m²",
            vol: "5408 m³",
            owner: data.owner,
            val: "₹ 210 Cr"
          }});

          // Level B3: Island Passenger Platform & Running Tracks (-24 to -15m)
          createPrism("SUB_B3_PLATFORM", [[13,5],[27,5],[27,35],[13,35]], -24, -15, 0xb45309, 0.92, "SUB", -3, {{
            name: "Underground Passenger Island Platform & Dual Track Slabs (Level B3)",
            ulpin: `${{data.base_ulpin}}-SUB-B03-PF01-4`,
            z: "-24.0m to -15.0m",
            area: "420 m²",
            vol: "3780 m³",
            owner: data.owner,
            val: "₹ 350 Cr"
          }});

          // Twin Metro Running Tunnels with Railway Tracks
          [-1, 1].forEach(side => {{
            const tGeo = new THREE.CylinderGeometry(2.8, 2.8, 52, 24);
            tGeo.rotateZ(Math.PI / 2);
            const tMat = new THREE.MeshStandardMaterial({{ color: 0xec4899, roughness: 0.3, transparent: true, opacity: 0.9 }});
            const tMesh = new THREE.Mesh(tGeo, tMat);
            tMesh.position.set(20, 20 + (side * 14), -19.5);
            groups.UTL.add(tMesh);
            meshMap.set(`UTL_TUBE_${{side}}`, tMesh);

            // Internal Rails
            const rGeo = new THREE.BoxGeometry(50, 0.25, 0.2);
            const rMat = new THREE.MeshStandardMaterial({{ color: 0x94a3b8, metalness: 0.8 }});
            const rMesh = new THREE.Mesh(rGeo, rMat);
            rMesh.position.set(20, 20 + (side * 14), -21.0);
            groups.UTL.add(rMesh);
          }});
        }}

        // ARCHETYPE 9: Hooghly Underwater Subsurface Corridor (Kolkata) - India's 1st Under-River Metro
        function buildUnderwaterShieldTunnel(data) {{
          // 1. Translucent Navigable River Water Surface (-2m to 0m)
          const wGeo = new THREE.PlaneGeometry(64, 64);
          const wMat = new THREE.MeshStandardMaterial({{ color: 0x0284c7, transparent: true, opacity: 0.45, roughness: 0.05 }});
          const wMesh = new THREE.Mesh(wGeo, wMat);
          wMesh.position.set(20, 20, -1.0);
          groups.SUR.add(wMesh);

          // River Channel Fairway Marker Buoys
          [-12, 12].forEach(bx => {{
            const bGeo = new THREE.CylinderGeometry(0.6, 0.6, 1.2, 12);
            bGeo.rotateX(Math.PI / 2);
            const bMesh = new THREE.Mesh(bGeo, new THREE.MeshStandardMaterial({{ color: 0x10b981 }}));
            bMesh.position.set(20 + bx, 20, 0.2);
            groups.SUR.add(bMesh);
          }});

          // 2. Subaqueous Alluvial Silt Strata (Riverbed Sediment, -14m to -2m)
          createPrism("GEO_SEDIMENT", [[-2,-2],[42,-2],[42,42],[-2,42]], -14, -2, 0x475569, 0.35, "SUR", 0, {{
            name: "Subaqueous Alluvial Silt Strata & Geotechnical Surcharge Bed",
            ulpin: `${{data.base_ulpin}}-GEO-G01-ST01-R`,
            z: "-14.0m to -2.0m",
            area: "1936 m²",
            vol: "23232 m³",
            owner: "Kolkata Port Trust & Inland Waterways Authority",
            val: "₹ 75.0 Cr"
          }});

          // 3. Deep Mahakaran Station Ventilation & Evacuation Shaft (-28m to +3m)
          createPrism("UTL_SHAFT", [[15,1],[25,1],[25,8],[15,8]], -28, 3, 0x0ea5e9, 0.85, "UTL", -2, {{
            name: "Howrah-Mahakaran Riverbank Deep Ventilation & Access Shaft",
            ulpin: `${{data.base_ulpin}}-UTL-U02-SH01-M`,
            z: "-28.0m to +3.0m",
            area: "70 m²",
            vol: "2170 m³",
            owner: "Kolkata Metro Rail Corporation (KMRCL)",
            val: "₹ 120 Cr"
          }});

          // 4. Twin Circular Bored Shield Tunnels under Riverbed (-28m to -21m, Depth 24m)
          [-1, 1].forEach(side => {{
            const tGeo = new THREE.CylinderGeometry(3.0, 3.0, 52, 28);
            tGeo.rotateZ(Math.PI / 2);
            const tMat = new THREE.MeshStandardMaterial({{ color: 0x06b6d4, roughness: 0.2, transparent: true, opacity: 0.92 }});
            const tMesh = new THREE.Mesh(tGeo, tMat);
            tMesh.position.set(20, 20 + (side * 8), -24.0);
            tMesh.userData = {{
              id: `UTL_HOOGHLY_${{side > 0 ? "EAST" : "WEST"}}`,
              stratum: "UTL",
              originalZ: -24.0,
              floorIdx: -3,
              baseOpacity: 0.92,
              info: {{
                name: `Hooghly Subaqueous Shield Tunnel Bore (${{side > 0 ? "Eastbound Track - Howrah to Esplanade" : "Westbound Track - Esplanade to Howrah"}})`,
                ulpin: `${{data.base_ulpin}}-UTL-U03-HT0${{side > 0 ? 1 : 2}}-K`,
                z: "-27.0m to -21.0m (Depth 24m MSL)",
                area: "340 m²",
                vol: "1480 m³",
                owner: "Kolkata Metro Rail Corporation (KMRCL)",
                val: "₹ 620 Cr"
              }}
            }};
            groups.UTL.add(tMesh);
            meshMap.set(`UTL_HOOGHLY_${{side > 0 ? "EAST" : "WEST"}}`, tMesh);

            // Subaqueous Blue/Green LED Ceiling Light Strip (Signature 520m Under-River Feature)
            const ledGeo = new THREE.BoxGeometry(50, 0.3, 0.2);
            const ledMat = new THREE.MeshBasicMaterial({{ color: side > 0 ? 0x38bdf8 : 0x34d399 }});
            const ledMesh = new THREE.Mesh(ledGeo, ledMat);
            ledMesh.position.set(20, 20 + (side * 8), -21.3);
            groups.UTL.add(ledMesh);
          }});

          // 5. Cross-Passage Escape Chamber & Sump Pump Vault
          createPrism("UTL_CROSS_PASS", [[17,12],[23,12],[23,28],[17,28]], -26.0, -22.0, 0x10b981, 0.92, "UTL", -3, {{
            name: "Underwater Evacuation Cross-Passage, Pressure Bulkhead & Sump Vault",
            ulpin: `${{data.base_ulpin}}-UTL-U03-CP01-E`,
            z: "-26.0m to -22.0m",
            area: "96 m²",
            vol: "384 m³",
            owner: "KMRCL Safety & Disaster Management Directorate",
            val: "₹ 48.0 Cr"
          }});
        }}

        // ARCHETYPE 10: GIFT Subsurface Utility Tunnel (TUM) - Multi-Utility Conduit System
        function buildUtilityTunnelTrench(data) {{
          // Walk-Through Utility Trench (-16 to 0m)
          createPrism("SUB_TRENCH", [[10,2],[30,2],[30,38],[10,38]], -16, 0, 0x334155, 0.8, "SUB", -1, {{
            name: "GIFT City Walk-Through Utility Tunnel (TUM Trench)",
            ulpin: `${{data.base_ulpin}}-SUB-B01-TM01-G`,
            z: "-16.0m to 0.0m",
            area: "720 m²",
            vol: "11520 m³",
            owner: "GIFT Urban Infrastructure Ltd",
            val: "₹ 890 Cr"
          }});

          // 4 Conduits: District Cooling (Cyan), Vacuum Waste (Purple), Power (Amber), Water (Emerald)
          const conduits = [
            {{ id: "COOLING", clr: 0x06b6d4, z: -4, name: "District Cooling Chilled Water 900mm Pipes" }},
            {{ id: "WASTE", clr: 0xa855f7, z: -8, name: "Automated Vacuum Waste Collection (AVWC) Tubes" }},
            {{ id: "POWER", clr: 0xf59e0b, z: -11, name: "66kV Extra High Voltage Underground Power Trays" }},
            {{ id: "WATER", clr: 0x10b981, z: -14, name: "Dual Potable & Recycled Irrigation Water Conduits" }}
          ];

          conduits.forEach(c => {{
            const pGeo = new THREE.CylinderGeometry(0.8, 0.8, 38, 16);
            const pMat = new THREE.MeshStandardMaterial({{ color: c.clr, roughness: 0.3, transparent: true, opacity: 0.95 }});
            const pMesh = new THREE.Mesh(pGeo, pMat);
            pMesh.position.set(16, 20, c.z);
            groups.UTL.add(pMesh);

            const pMesh2 = pMesh.clone();
            pMesh2.position.set(24, 20, c.z);
            groups.UTL.add(pMesh2);

            meshMap.set(`UTL_${{c.id}}`, pMesh);
          }});
        }}

        // ARCHETYPE 11: TIDEL Park IT Expressway (Chennai) - Linear Monolith with Spinal Glass Atrium
        function buildLinearITSpine(data) {{
          const tidelTenants = [
            "TIDEL Park Common Atrium & Visitor Reception",
            "Cisco Systems India Private Limited",
            "Tata Consultancy Services (Global Delivery Unit)",
            "HCL Technologies Software Engineering Hub",
            "Sify Technologies Cloud Data Services",
            "TIDEL Park Ltd (Executive Corporate Suites)"
          ];

          // Linear IT Block (0 to 28m)
          for (let f = 0; f <= 5; f++) {{
            const zMin = f * 4.6;
            const zMax = zMin + 4.6;
            const lvl = f === 0 ? "G00" : `F0${{f}}`;
            const flrOwner = tidelTenants[f] || "OMR IT Enterprise Tenant";

            // North Wing
            createPrism(`BLD_${{lvl}}_NORTH`, [[4,21],[36,21],[36,31],[4,31]], zMin, zMax, 0x0284c7, 0.85, "BLD", f, {{
              name: `TIDEL Park IT North Block (${{lvl}})`,
              ulpin: `${{data.base_ulpin}}-BLD-${{lvl}}-NB01-C`,
              z: `${{zMin.toFixed(1)}}m to ${{zMax.toFixed(1)}}m`,
              area: "320 m²",
              vol: "1472 m³",
              owner: flrOwner,
              val: "₹ 38.0 Cr"
            }});

            // Central Spinal Glass Canyon
            createPrism(`COM_${{lvl}}_SPINE`, [[4,17],[36,17],[36,21],[4,21]], zMin, zMax, 0x38bdf8, 0.6, "COM", f, {{
              name: `TIDEL Central Spinal Atrium & Skywalks (${{lvl}})`,
              ulpin: `${{data.base_ulpin}}-COM-${{lvl}}-SP01-S`,
              z: `${{zMin.toFixed(1)}}m to ${{zMax.toFixed(1)}}m`,
              area: "128 m²",
              vol: "588 m³",
              owner: "TIDEL Park Common Strata Facility",
              val: "₹ 12.0 Cr"
            }});

            // South Wing
            createPrism(`BLD_${{lvl}}_SOUTH`, [[4,7],[36,7],[36,17],[4,17]], zMin, zMax, 0x0369a1, 0.85, "BLD", f, {{
              name: `TIDEL Park IT South Block (${{lvl}})`,
              ulpin: `${{data.base_ulpin}}-BLD-${{lvl}}-SB01-T`,
              z: `${{zMin.toFixed(1)}}m to ${{zMax.toFixed(1)}}m`,
              area: "320 m²",
              vol: "1472 m³",
              owner: flrOwner,
              val: "₹ 38.0 Cr"
            }});
          }}

          // Subsurface
          createPrism("SUB_TIDEL", [[4,7],[36,7],[36,31],[4,31]], -12, 0, 0xf59e0b, 0.85, "SUB", -1, {{
            name: "TIDEL Basement Parking & Storm Reservoir",
            ulpin: `${{data.base_ulpin}}-SUB-B02-TD01-8`,
            z: "-12.0m to 0.0m",
            area: "768 m²",
            vol: "9216 m³",
            owner: "TIDEL Park Ltd & Infrastructure Operations",
            val: "₹ 95.0 Cr"
          }});
        }}

        // ARCHETYPE 12: Transit Terminal Canopy (Seawoods Transit, Durgam Cheruvu Hub)
        function buildTransitTerminalCanopy(data) {{
          // Aerodynamic Tubular Canopy Arches
          const archGeo = new THREE.TorusGeometry(16, 1.8, 12, 32, Math.PI);
          archGeo.rotateY(Math.PI / 2);
          const archMat = new THREE.MeshStandardMaterial({{ color: 0x0284c7, roughness: 0.3, transparent: true, opacity: 0.85 }});
          
          [-8, 8].forEach(pos => {{
            const arch = new THREE.Mesh(archGeo, archMat);
            arch.position.set(20, 20 + pos, 0);
            groups.BLD.add(arch);
          }});

          // Concourse Deck (0 to 6m)
          createPrism("BLD_CONCOURSE", [[6,8],[34,8],[34,32],[6,32]], 0, 6, 0x38bdf8, 0.8, "BLD", 0, {{
            name: "High-Capacity Transit Concourse & Platform Hall",
            ulpin: `${{data.base_ulpin}}-BLD-G00-TT01-4`,
            z: "0.0m to +6.0m",
            area: "672 m²",
            vol: "4032 m³",
            owner: "State Multi-Modal Transit Authority & Rail Concessionaire",
            val: "₹ 160 Cr"
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

        // Surrounding Urban Context Masses (Low-poly contextual blocks on perimeter)
        function addSurroundingUrbanContext() {{
          const ctxMat = new THREE.MeshStandardMaterial({{ color: 0x334155, roughness: 0.7, metalness: 0.3 }});
          const ctxBlocks = [
            {{ x: -32, y: 20, w: 22, d: 28, h: 25 }},
            {{ x: 72, y: 20, w: 24, d: 26, h: 32 }},
            {{ x: 20, y: -34, w: 32, d: 18, h: 18 }},
            {{ x: 20, y: 74, w: 30, d: 20, h: 22 }},
            {{ x: -28, y: -28, w: 18, d: 18, h: 15 }},
            {{ x: 68, y: 68, w: 20, d: 20, h: 28 }}
          ];

          ctxBlocks.forEach(b => {{
            const geo = new THREE.BoxGeometry(b.w, b.d, b.h);
            const m = new THREE.Mesh(geo, ctxMat);
            m.position.set(b.x, b.y, b.h / 2);
            m.receiveShadow = true;
            m.castShadow = true;
            
            const wire = new THREE.LineSegments(new THREE.EdgesGeometry(geo), new THREE.LineBasicMaterial({{ color: 0x64748b, transparent: true, opacity: 0.35 }}));
            m.add(wire);
            
            groups.SUR.add(m);
          }});
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

        init();
      </script>
    </body>
    </html>
    """
    components.html(html_code, height=height, scrolling=False)
