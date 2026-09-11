# 🏙️ 3D ULPIN Generator: Pan-India 3D Cadastral System
### ISO 19152 Compliant Next-Generation 3D Spatial Cadastre, Subsurface Collision Engine, AI Slicing & Vertical Land Registry Portal

**Lead Team:** Ctrl Alt Defeat  
**Event:** Smart India Hackathon 2026 (SIH 2026)  
**Standards:** ISO 19152 (LADM Edition II) • Digital India Land Records Modernization Programme (DILRMP) • Survey of India CORS Network  
**Tech Stack:** Python 3.10+, Streamlit, Three.js (WebGL), PyDeck (Deck.gl), SQLite3, ReportLab, Chart.js, Tailwind CSS  

---

## 📌 1. Executive Summary & Problem Statement
Modern Indian urban centers (e.g., Mumbai MMR, Delhi NCR, Bengaluru, Hyderabad, GIFT City) have evolved rapidly into dense, vertically stacked superstructures featuring multi-level subterranean basements, underground metro lines, and dense utility corridors. However, existing land administration systems across India (under DILRMP and Bhu-Naksha) remain fundamentally **two-dimensional (2D)**, treating land parcels purely as flat polygons (Latitude, Longitude). 

This architectural limitation introduces severe systemic risks:
* **Airspace & Floor Ownership Ambiguity:** In a 50-storey high-rise, hundreds of distinct flat owners share the exact same 2D footprint, which traditional 2D cadastres cannot legally demarcate.
* **Catastrophic Subsurface Encroachments:** Deep private foundations and underground parking lots often collide with or breach the safety buffers of underground metro tunnels, high-voltage power conduits, gas lines, and water aqueducts.
* **Title Disputes & Double Mortgaging:** The absence of a unique, immutable vertical parcel identifier allows fraudulent sales or overlapping conveyance of individual floor units.

**The Solution:** **3D ULPIN Generator** provides an ISO 19152 compliant 3D cadastral platform featuring real-time procedural WebGL digital twins, automated AI LiDAR floor slicing, 3D subterranean collision detection, a 14-digit + vertical ULPIN standard with Modulo-36 check digits, role-based workflows, and tamper-proof SHA-256 cryptographic title certificate issuance with mobile QR verification.

---

## 🏗️ 2. System Architecture & End-to-End Pipeline

```
                      ┌───────────────────────────────────────────────┐
                      │            PAN-INDIA DATASET & DB             │
                      │  SQLite (spatial_records.db) / JSON / LiDAR   │
                      └───────────────────────┬───────────────────────┘
                                              │
                    ┌─────────────────────────┴─────────────────────────┐
                    ▼                                                   ▼
     ┌──────────────────────────────┐                    ┌──────────────────────────────┐
     │      CORE MATH ENGINES       │                    │        3D GIS ENGINES        │
     │ • Volumetric Floor Slicing   │                    │ • Three.js WebGL Twin        │
     │ • 14-d + Vertical ULPIN      │                    │ • PyDeck (Deck.gl) GIS       │
     │ • Subsurface Clash Engine    │                    │ • Esri / Carto Basemaps      │
     │ • AI LiDAR Peak Detection    │                    │ • Chart.js LiDAR Analytics   │
     │ • SHA-256 Cryptographic Hash │                    │ • Exploded / X-Ray Shaders   │
     └──────────────┬───────────────┘                    └──────────────┬───────────────┘
                    └─────────────────────────┬─────────────────────────┘
                                              ▼
                              ┌───────────────────────────────┐
                              │     STREAMLIT MAIN PORTAL     │
                              │    Unified Minimal GIS Bar    │
                              │    Figma Dark / Light Token   │
                              └───────────────┬───────────────┘
                 ┌────────────────────────────┼────────────────────────────┐
                 ▼                            ▼                            ▼
       ┌──────────────────┐         ┌──────────────────┐         ┌──────────────────┐
       │  CITIZEN MODE    │         │  SURVEYOR MODE   │         │  REGISTRAR MODE  │
       │ • Title Verify   │         │ • Subsurface Clash│        │ • Deed Transfer  │
       │ • Floor Bounds   │         │ • FSI / GFA Math │         │ • 6% Stamp Duty  │
       │ • PDF Title Deed │         │ • AI LiDAR Slicing│        │ • Immutable Log  │
       └──────────────────┘         └──────────────────┘         └──────────────────┘
```

| Component | Module Path | Primary Responsibility & Algorithms |
| :--- | :--- | :--- |
| **Spatial Math Engine** | `core/spatial_math.py` | Slices building envelopes into discrete volumetric floor blocks for superstructures and subterranean basements. Computes GFA, enclosed volume, and FSI. |
| **3D ULPIN Engine** | `core/ulpin_logic.py` | Generates 14-digit LGD-compliant base ULPIN + 3-character vertical suffix (e.g., `-004` for floor 4, `-U02` for basement 2) with bidirectional parsing. |
| **Enhanced ISO 19152 Engine** | `core/ulpin_enhanced.py` | Generates ISO 19152 (LADM Edition II) format with Modulo-36 weighted checksum and 6-strata classification (`SUR`, `BLD`, `COM`, `SUB`, `UTL`, `AIR`). |
| **AI Floor Slicing Engine** | `core/ai_floor_segmentation.py` | Ingests drone LiDAR / photogrammetry elevation point clouds, builds vertical Z-histograms, and detects concrete slabs via moving-average peak detection. |
| **Collision & Clash Engine** | `core/collision_engine.py` | Performs Haversine surface proximity calculation and 1D vertical overlap checks to identify critical encroachments and safety buffer infringements. |
| **3D Topology Engine** | `core/topology_3d.py` | Computes Shoelace polygon area, 3D centroid coordinates, and 3D Axis-Aligned Bounding Box (AABB) intersection volumes. |
| **Digital Certificate Engine** | `core/certificate_generator.py` | Computes immutable SHA-256 title hashes, generates QR code payloads, and builds downloadable official vector PDF title deeds. |
| **WebGL Digital Twin Studio** | `frontend/digital_twin_component.py` | Over 2,500 lines of custom Three.js WebGL procedural geometry: 20 architectural archetypes, exploded floor sliders, subsurface X-Ray transparency, and animated trains. |
| **PyDeck 3D Map Studio** | `frontend/map_engine.py` | Renders 3D extruded `ColumnLayer` columns, `ScatterplotLayer` halo footprints, 8 metro viewports, and theme-adaptive ESRI/CartoDB basemaps. |
| **UI Components & Theming** | `frontend/ui_components.py` | Injects modern Figma glassmorphic design system, persistent Light/Dark mode switcher, KPI metrics rows, and vertical stack dossiers. |
| **Spatial Database** | `database/spatial_records.db` | Relational SQLite storage for property IDs, LGD geography, 3D coordinates, zones, archetypes, owners, and valuations. |

---

## 🗄️ 3. Master Cadastral Dataset & Structure Valuation

### 3.1 Geographic Scope & Benchmark Portfolio
The system contains a master dataset of **25 multi-strata properties valued at ₹26,770.0 Crores INR** across 8 Indian economic corridors:
* **Navi Mumbai & Mumbai MMR (Maharashtra, LGD 27):** Seawoods Grand Central TOD, Grand Central Subsurface Concourse, BKC Diamond Tower, BKC Metro-3 Underground Vault, Lodha World One (Worli Sea Face).
* **New Delhi NCT & Gurugram NCR (Delhi 07, Haryana 06):** Connaught Outer Circle Heritage Rotunda, Rajiv Chowk Subsurface Metro Terminal, Aerocity Horizon Gateway, DLF Cyber City Building 10.
* **Bengaluru Urban (BBMP, Karnataka 29):** Manyata Embassy High-Tech Park, Cubbon Park Underground Metro Junction, UB City & Kingfisher Towers, Whitefield Tech Park Nexus.
* **GIFT City (Gujarat 24):** GIFT Diamond Tower Pinnacle, GIFT Subsurface Utility Tunnel (TUM), GIFT Aspire Smart Residential.
* **Hyderabad (GHMC, Telangana 36):** HITEC Cyber Towers, Cyberabad Subsurface Data Vault, Durgam Cheruvu Mixed Urban Hub.
* **Chennai (Tamil Nadu 33):** TIDEL Park OMR, Chennai Central Underground Triple-Tier Concourse.
* **Kolkata (West Bengal 19):** New Town EcoSpace IT Hub, Hooghly Riverbed Underwater Metro Line.

### 3.2 Structure Valuation Methodology
1. **Base Cadastral Capitalization (`valuation_cr`):** Derived from official Ready Reckoner / Circle Rates and commercial real estate market valuations across Central Business Districts (e.g., BKC Diamond Tower at ₹2,400 Cr, GIFT Diamond Tower at ₹2,800 Cr, Seawoods TOD at ₹850 Cr).
2. **Volumetric Floor-Level Apportionment:** In the 3D Digital Twin, floor-level valuation is dynamically computed:
   $$\text{Floor Valuation} = \frac{\text{Total Valuation (INR Cr)}}{\text{Total Floor Slices}}$$
   Subterranean parking and infrastructure caverns are assigned dedicated utility valuations (₹35–180 Cr) reflecting specialized geotechnical construction costs.
3. **Statutory State Stamp Duty (6%):** Sub-Registrar Mode calculates statutory state stamp duty for individual airspace conveyances:
   $$\text{Stamp Duty} = \text{Cadastral Valuation} \times 0.06$$
4. **Cryptographic Hash Sealing:** Valuations are cryptographically bound into the SHA-256 title hash, preventing fraudulent tax evasion or undervaluation during mortgage underwriting.

---

## 🔏 4. 3D ULPIN Generator Numbering Logic

### 4.1 14-Digit Base ULPIN Structure
Conforming to Ministry of Rural Development & DILRMP standards:
$$\underbrace{\text{SS}}_{\text{State (2d)}} - \underbrace{\text{DD}}_{\text{District (2d)}} - \underbrace{\text{SSS}}_{\text{Sub-District (3d)}} - \underbrace{\text{VVV}}_{\text{Village/Ward (3d)}} - \underbrace{\text{PPPP}}_{\text{Plot ID (4d)}}$$
*Example:* `27211010500101` (Maharashtra `27`, Thane/Navi Mumbai `21`, Belapur Sub-dist `101`, Seawoods Ward `050`, Parcel `0101`).

### 4.2 3D ISO 19152 Vertical Extension
* **Superstructure (Above Ground):** Appends `-FFF` (e.g., `-004` for Floor 4, `-000` for Ground).
* **Subsurface (Basements):** Appends `-UXX` (e.g., `-U02` for Basement Level 2, depth $-6.0\text{m}$ to $-9.0\text{m}$).

### 4.3 Enhanced ISO 19152 (LADM Edition II) Specification
```
[LGD]-[BASE_2D]-[STRATUM]-[LEVEL]-[UNIT]-[CHECKSUM]
```
*Example:* **`2721-27211010500101-BLD-F04-U01-K`**

#### Strata Types
* `SUR`: Surface Land Parcel (roadways, public plazas)
* `BLD`: Multi-Storey Building Unit (residential flats, commercial offices)
* `COM`: Common Condominium Property (lobbies, skybridges, amenities)
* `SUB`: Subterranean Basement Unit (underground parking, plant vaults)
* `UTL`: Subsurface Public Utility Corridor (metro tunnels, water aqueducts)
* `AIR`: Elevated Air-Rights Parcel (rooftop helipads, solar PV arrays, spires)

#### Modulo-36 Weighted Checksum
Calculated over prime weights $[3, 7, 11, 13, 17, 19, 23, 29]$ against the alphanumeric alphabet `0-9, A-Z`:
$$\text{Remainder} = \left(\sum \text{val}(c_i) \times w_i\right) \pmod{36}, \quad \text{CheckVal} = (36 - \text{Remainder}) \pmod{36}$$

---

## 🔬 5. AI, 3D & Computational Models

### 5.1 AI Point Cloud Floor Slicing Engine (`core/ai_floor_segmentation.py`)
* **Input:** Drone photogrammetry / LiDAR point cloud Z-coordinates (`data/mock_lidar.py`).
* **Z-Density Histogram:** Discretizes elevations into $\Delta Z = 0.1\text{m}$ bins. Concrete floor slabs produce high point density spikes due to planar horizontal reflectances.
* **Signal Smoothing:** 5-point moving average filter suppresses airborne noise and foliage scatter.
* **Peak Detection:** Evaluates local maxima with prominence thresholding ($>25\%$ of maximum frequency) and enforces minimum storey clearance ($h \ge 2.7\text{m}$) to classify slabs into basements, ground, and storeys.

### 5.2 3D Subsurface Collision & Clash Engine (`core/collision_engine.py`)
* **Horizontal Ground Proximity (Haversine Formula, Earth $R = 6,371,000\text{m}$):**
  $$a = \sin^2\left(\frac{\Delta \phi}{2}\right) + \cos(\phi_1)\cos(\phi_2)\sin^2\left(\frac{\Delta \lambda}{2}\right), \quad D = 2R \cdot \arctan2\left(\sqrt{a}, \sqrt{1-a}\right)$$
* **Vertical Overlap ($\Delta Z$):**
  $$\Delta Z = \min(Z_{top1}, Z_{top2}) - \max(Z_{base1}, Z_{base2})$$
* **Severity Matrix:**
  * **CRITICAL COLLISION (Direct 3D Encroachment):** $D \le 2 \times R_{footprint}$ and $\Delta Z > 0\text{m}$.
  * **SAFETY BUFFER VIOLATION:** $D \le 2 \times R_{footprint} + S_{buffer}$ and $\Delta Z > -10\text{m}$.

### 5.3 3D Cadastral Topology & Volumetric Delineation (`core/topology_3d.py`)
* **Shoelace Formula:** Calculates exact 2D planar floor area:
  $$Area = \frac{1}{2} \left| \sum_{i=0}^{n-1} (x_i y_{i+1} - x_{i+1} y_i) \right|$$
* **Prismatic B-Rep & Centroid:** Calculates 3D volume ($V = Area \times \Delta Z$) and centroid $(C_x, C_y, C_z)$.
* **3D AABB Overlap:** Axis-aligned bounding box intersection volume test verifies unit non-overlap and parent boundary setback compliance.

### 5.4 Procedural 3D WebGL Digital Twin Engine (`frontend/digital_twin_component.py`)
* Interactive Three.js WebGL canvas featuring:
  * 20 procedural architectural archetypes (cantilevered skybridges, diamond bourses, multi-level transit caverns, underwater tunnels).
  * Exploded floor view slider (dynamic vertical storey separation).
  * Subsurface X-Ray transparency slider (renders ground plane semi-transparent to inspect foundations and metro lines).
  * High-res satellite ground textures (ESRI / CartoDB).

---

## 💻 6. Technology Stack Breakdown

| Layer | Technologies | Role & Purpose |
| :--- | :--- | :--- |
| **Frontend Framework** | **Streamlit** (Python) | High-performance reactive web application container and state management |
| **3D WebGL Graphics** | **Three.js (r128)** + **OrbitControls** | Interactive 3D Digital Twin with exploded views, X-ray mode, and strata shaders |
| **GIS Mapping Layer** | **PyDeck (Deck.gl)** + **MapLibre** | Geospatial visualization rendering extruded 3D columns and ground footprints |
| **Basemaps** | **ESRI Satellite**, **CartoDB Dark Matter / Positron** | High-resolution satellite and vector basemaps with automatic theme switching |
| **Styling & Design** | **Tailwind CSS**, **Vanilla CSS**, **Lucide Icons** | Figma glassmorphic design system, light/dark theme switching, KPI metric cards |
| **Data Analytics** | **Chart.js**, **Streamlit Native Charts** | Real-time LiDAR Z-density profiling and metro-wise asset valuation charts |
| **Database & Storage** | **SQLite3** (`spatial_records.db`), **Pandas** | Relational spatial database, SQL querying, tabular inspection, and CSV exports |
| **Certificate Engine** | **ReportLab**, **qrcode**, **Pillow** | Official 3D ULPIN Generator vector PDF certificates and scannable QR payloads |
| **Validation & Schema** | **Pydantic (v2)**, **Python Math** | Data validation schemas, Haversine spatial math, and Shoelace polygon calculations |

---

## 👥 7. Role-Based Operational Workflows

* **🏠 Citizen / Homebuyer Mode:** Unit-level ownership verification, height bounds review, RERA status check, live 3D ULPIN Generator certificate card preview, and 1-click official PDF title certificate download.
* **📐 Government GIS Surveyor Mode:** 3D spatial metrics (Gross Volume $m^3$, Built-up area $m^2$, FSI/FAR), automated subsurface 3D clash audits, interactive vertical cross-section stacks, AI LiDAR point cloud floor segmentation, and SQLite coordinate ingestion.
* **🏛️ Sub-Registrar Mode:** Vertical airspace deed conveyance simulator, automatic 6% state stamp duty calculation, immutable ownership conveyance updates directly in `spatial_records.db`, and audit trail verification.

---

## 📄 8. Documentation & Technical Reports

The repository includes publication-grade documentation:
* **[Bhu_Aadhaar_3D_Complete_Technical_Specification.pdf](Bhu_Aadhaar_3D_Complete_Technical_Specification.pdf):** 6-page comprehensive technical specification covering mathematical equations, database schemas, ULPIN logic, and full-stack architecture.
* **[`generate_system_docs_pdf.py`](generate_system_docs_pdf.py):** Automated ReportLab build script to regenerate the technical specification PDF.
* **[`generate_project_pdf.py`](generate_project_pdf.py):** Project overview PDF generator.
* **[`Bhu_Aadhaar_3D_Comprehensive_Master_Report.docx`](Bhu_Aadhaar_3D_Comprehensive_Master_Report.docx):** Complete master report for submission.

---

## 🚀 9. Getting Started & Installation

### Prerequisites
* Python 3.10+
* Modern WebGL-compatible browser (Chrome, Edge, Firefox, Brave)

### 1. Clone the Repository
```bash
git clone https://github.com/pxrkerxd/3d-ulpin-cadastre-sih.git
cd 3d-ulpin-cadastre-sih
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Initialize the Relational Spatial Database
```bash
python database/db_setup.py
```

### 4. Build the Master Technical Specification PDF (Optional)
```bash
python generate_system_docs_pdf.py
```

### 5. Launch the Streamlit Portal
```bash
streamlit run main.py
```
Open your browser at `http://localhost:8501`.
