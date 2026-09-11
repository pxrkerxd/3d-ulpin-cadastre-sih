import os
import sys
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, KeepTogether, PageBreak, HRFlowable
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfgen import canvas

class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super(NumberedCanvas, self).__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super(NumberedCanvas, self).showPage()
        super(NumberedCanvas, self).save()

    def draw_page_decorations(self, page_count):
        self.saveState()
        self.setFont("Helvetica-Bold", 8)
        self.setFillColor(colors.HexColor("#64748b"))
        
        # Running Header (on pages after cover/first page)
        if self._pageNumber > 1:
            self.drawString(54, letter[1] - 36, "3D ULPIN GENERATOR | Comprehensive Project Technical & Architecture Report")
            self.drawRightString(letter[0] - 54, letter[1] - 36, "SIH 2026 Innovation")
            self.setStrokeColor(colors.HexColor("#e2e8f0"))
            self.setLineWidth(0.75)
            self.line(54, letter[1] - 42, letter[0] - 54, letter[1] - 42)

        # Running Footer
        self.setStrokeColor(colors.HexColor("#e2e8f0"))
        self.setLineWidth(0.75)
        self.line(54, 46, letter[0] - 54, 46)
        
        self.setFont("Helvetica", 8)
        self.drawString(54, 32, "Confidential & Proprietary • Department of Land Resources (DILRMP) / NIC / SIH 2026")
        page_str = f"Page {self._pageNumber} of {page_count}"
        self.drawRightString(letter[0] - 54, 32, page_str)
        self.restoreState()

def build_pdf(filename="Bhu_Aadhaar_3D_Comprehensive_Project_Report.pdf"):
    doc = SimpleDocTemplate(
        filename,
        pagesize=letter,
        leftMargin=54,
        rightMargin=54,
        topMargin=54,
        bottomMargin=54
    )

    styles = getSampleStyleSheet()

    # Custom styles
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=24,
        leading=28,
        textColor=colors.HexColor('#0f172a'),
        spaceAfter=6
    )

    subtitle_style = ParagraphStyle(
        'DocSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=12,
        leading=16,
        textColor=colors.HexColor('#0284c7'),
        spaceAfter=14
    )

    meta_style = ParagraphStyle(
        'DocMeta',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9,
        leading=13,
        textColor=colors.HexColor('#475569')
    )

    h1_style = ParagraphStyle(
        'H1',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=15,
        leading=18,
        textColor=colors.HexColor('#0f172a'),
        spaceBefore=14,
        spaceAfter=8,
        keepWithNext=True
    )

    h2_style = ParagraphStyle(
        'H2',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=12,
        leading=15,
        textColor=colors.HexColor('#0369a1'),
        spaceBefore=10,
        spaceAfter=6,
        keepWithNext=True
    )

    body_style = ParagraphStyle(
        'BodyDark',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9.5,
        leading=14,
        textColor=colors.HexColor('#1e293b'),
        spaceAfter=8
    )

    bullet_style = ParagraphStyle(
        'BulletText',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9,
        leading=13,
        textColor=colors.HexColor('#334155'),
        leftIndent=14,
        firstLineIndent=-10,
        spaceAfter=4
    )

    code_style = ParagraphStyle(
        'CodeSnippet',
        parent=styles['Normal'],
        fontName='Courier',
        fontSize=8,
        leading=11,
        textColor=colors.HexColor('#0f172a')
    )

    callout_style = ParagraphStyle(
        'CalloutText',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9,
        leading=13,
        textColor=colors.HexColor('#0369a1')
    )

    story = []

    # -------------------------------------------------------------
    # COVER / HEADER BANNER
    # -------------------------------------------------------------
    badge_table = Table([[
        Paragraph("<b>SMART INDIA HACKATHON 2026</b>", ParagraphStyle('B1', fontName='Helvetica-Bold', fontSize=8, textColor=colors.HexColor('#0284c7'))),
        Paragraph("<b>PAN-INDIA 3D CADASTRAL SYSTEM</b>", ParagraphStyle('B2', fontName='Helvetica-Bold', fontSize=8, textColor=colors.HexColor('#059669'))),
        Paragraph("<b>ISO 19152 COMPLIANT</b>", ParagraphStyle('B3', fontName='Helvetica-Bold', fontSize=8, textColor=colors.HexColor('#7e22ce')))
    ]], colWidths=[160, 200, 144])
    badge_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (0,0), colors.HexColor('#e0f2fe')),
        ('BACKGROUND', (1,0), (1,0), colors.HexColor('#dcfce7')),
        ('BACKGROUND', (2,0), (2,0), colors.HexColor('#f3e8ff')),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOX', (0,0), (0,0), 0.5, colors.HexColor('#38bdf8')),
        ('BOX', (1,0), (1,0), 0.5, colors.HexColor('#4ade80')),
        ('BOX', (2,0), (2,0), 0.5, colors.HexColor('#c084fc')),
    ]))
    story.append(badge_table)
    story.append(Spacer(1, 10))

    story.append(Paragraph("3D ULPIN GENERATOR", title_style))
    story.append(Paragraph("Next-Generation 3D Spatial Cadastre, Subsurface Collision Engine & Vertical Land Registry Portal", subtitle_style))
    story.append(Paragraph("<b>Author / Lead:</b> Parijat Sharma &bull; <b>Project:</b> SIH 2026 National Innovation &bull; <b>Framework:</b> Python, Streamlit, PyDeck (Deck.gl), SQLite, ReportLab", meta_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor("#0284c7"), spaceAfter=14, spaceBefore=6))

    # -------------------------------------------------------------
    # 1. EXECUTIVE SUMMARY & PROBLEM STATEMENT
    # -------------------------------------------------------------
    story.append(Paragraph("1. Executive Summary & Problem Statement", h1_style))
    story.append(Paragraph(
        "Modern Indian urban centers (e.g. Mumbai MMR, Delhi NCR, Bengaluru, GIFT City) have evolved rapidly into dense, vertically stacked superstructures with deep multi-level subterranean basements, subterranean metro lines, and underground utility corridors. "
        "However, existing land administration systems across India (under DILRMP and Bhu-Naksha) remain fundamentally <b>two-dimensional (2D)</b>. Traditional cadastres treat land parcels purely as flat polygons (Latitude, Longitude), assuming a single owner owns the land down to the center of the earth and up to the heavens.",
        body_style
    ))
    story.append(Paragraph(
        "This architectural mismatch creates severe systemic risks:",
        body_style
    ))
    story.append(Paragraph("&bull; <b>Airspace & Floor Ownership Ambiguity:</b> In a 40-storey high-rise, dozens of distinct owners share the exact same 2D footprint. Traditional cadastres cannot legally demarcate individual volumetric rights.", bullet_style))
    story.append(Paragraph("&bull; <b>Catastrophic Subsurface Encroachments:</b> Deep private foundations and underground parking lots often collide with or breach safety buffers of underground metro tunnels, gas conduits, water mains, and optic fiber networks.", bullet_style))
    story.append(Paragraph("&bull; <b>Title Disputes & Double Mortgaging:</b> Absence of a unique, immutable vertical parcel identifier allows fraudulent sale or overlapping conveyance of individual floor units.", bullet_style))
    story.append(Paragraph(
        "<b>The Solution:</b> <i>3D ULPIN Generator</i> provides an ISO 19152 compliant 3D cadastral platform featuring real-time volumetric floor slicing, automated 3D subsurface collision detection, a 14-digit + vertical ULPIN standard, cryptographic title certificate issuance with QR verification, and role-based workflows for Citizens, Surveyors, and Sub-Registrars.",
        body_style
    ))
    story.append(Spacer(1, 8))

    # -------------------------------------------------------------
    # 2. SYSTEM ARCHITECTURE & DATA WORKFLOW
    # -------------------------------------------------------------
    story.append(Paragraph("2. System Architecture & End-to-End Pipeline", h1_style))
    story.append(Paragraph(
        "The project is structured around a modular, decoupled architecture consisting of four core mathematical engines, a relational spatial SQLite database, an interactive Deck.gl GIS visualization layer, and role-based operational modules:",
        body_style
    ))

    arch_data = [
        [Paragraph("<b>Component</b>", ParagraphStyle('TH', fontName='Helvetica-Bold', fontSize=9, textColor=colors.white)),
         Paragraph("<b>Module Path</b>", ParagraphStyle('TH', fontName='Helvetica-Bold', fontSize=9, textColor=colors.white)),
         Paragraph("<b>Primary Responsibility & Algorithms</b>", ParagraphStyle('TH', fontName='Helvetica-Bold', fontSize=9, textColor=colors.white))],
        
        [Paragraph("<b>Spatial Math Engine</b>", body_style),
         Paragraph("<code>core/spatial_math.py</code>", code_style),
         Paragraph("Segments total building height and base elevation into discrete volumetric floor blocks. Supports above-ground superstructures and negative subterranean basements.", body_style)],

        [Paragraph("<b>3D ULPIN Engine</b>", body_style),
         Paragraph("<code>core/ulpin_logic.py</code>", code_style),
         Paragraph("Generates 14-digit LGD-compliant base ULPIN + 3-char vertical suffix (e.g. <code>-004</code> for floor 4, <code>-U02</code> for basement 2). Provides bidirectional instant parsing.", body_style)],

        [Paragraph("<b>Collision & Clash Engine</b>", body_style),
         Paragraph("<code>core/collision_engine.py</code>", code_style),
         Paragraph("Performs Haversine surface proximity calculation and 1D vertical overlap checks. Identifies CRITICAL_COLLISION and BUFFER_VIOLATION against metro & utility infrastructure.", body_style)],

        [Paragraph("<b>Digital Certificate Engine</b>", body_style),
         Paragraph("<code>core/certificate_generator.py</code>", code_style),
         Paragraph("Computes immutable SHA-256 cryptographic title hash, generates QR code payload with parcel metadata, and builds downloadable official PDF certificates.", body_style)],

        [Paragraph("<b>PyDeck 3D Map Studio</b>", body_style),
         Paragraph("<code>frontend/map_engine.py</code>", code_style),
         Paragraph("Renders 3D extruded ColumnLayer columns and ground ScatterplotLayer footprints. Features 8 metro viewports, custom camera focus, and theme-adaptive basemaps.", body_style)],

        [Paragraph("<b>UI Components & Theming</b>", body_style),
         Paragraph("<code>frontend/ui_components.py</code>", code_style),
         Paragraph("Injects modern glassmorphic styling, provides persistent Light/Dark mode switcher, KPI metrics row, architectural cross-section, and dossier cards.", body_style)],

        [Paragraph("<b>Database Storage</b>", body_style),
         Paragraph("<code>database/spatial_records.db</code>", code_style),
         Paragraph("Relational SQLite storage storing property IDs, LGD geography, 3D coordinates (lat, lon, base_elevation, total_height), zone, owner, and valuation.", body_style)],
    ]

    arch_table = Table(arch_data, colWidths=[110, 125, 269])
    arch_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#0f172a')),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#cbd5e1')),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.HexColor('#ffffff'), colors.HexColor('#f8fafc')]),
    ]))
    story.append(arch_table)
    story.append(Spacer(1, 10))

    # -------------------------------------------------------------
    # 3. THE 4 MATHEMATICAL & ALGORITHMIC ENGINES
    # -------------------------------------------------------------
    story.append(Paragraph("3. Deep Dive: Mathematical & Algorithmic Engines", h1_style))

    # Engine A
    story.append(Paragraph("3.1 Volumetric 3D Parcel Slicing (<code>core/spatial_math.py</code>)", h2_style))
    story.append(Paragraph(
        "Standard land surveys only record physical footprints. Our spatial segmentation algorithm accepts building base elevation ($Z_{base}$), total height ($H$), and floor height ($h = 3\\text{m}$ default) to generate precise 3D vertical intervals:",
        body_style
    ))
    story.append(Paragraph("&bull; <b>Superstructure (Above Ground, $Z_{base} \\ge 0$):</b> For floor index $f \\in [0, N-1]$, interval is $[Z_{base} + f \\cdot h,\\; Z_{base} + (f+1) \\cdot h]$. Floor number is $f+1$.", bullet_style))
    story.append(Paragraph("&bull; <b>Subsurface (Basements, $Z_{base} < 0$):</b> Extends downwards below surface datum $[-(f \\cdot h),\\; -((f+1) \\cdot h)]$. Floor number is recorded as $-(f+1)$ to denote subterranean depth.", bullet_style))

    # Engine B
    story.append(Paragraph("3.2 14-Digit Base ULPIN + 3D ULPIN Generator Standard (<code>core/ulpin_logic.py</code>)", h2_style))
    story.append(Paragraph(
        "India's Ministry of Rural Development specifies a 14-digit Unique Land Parcel Identification Number (ULPIN) derived from Local Government Directory (LGD) codes: <code>SS-DD-SSS-VVV-PPPP</code> (State 2 digits, District 2 digits, Sub-District 3 digits, Village/Ward 3 digits, Plot ID 4 digits).",
        body_style
    ))
    story.append(Paragraph(
        "<b>Our 3D ISO 19152 Cadastral Extension:</b> We append a hyphenated 3-character vertical suffix: <code>-FFF</code> for above-ground floors (e.g., <code>-004</code> for Level 4) and <code>-UXX</code> for underground basements (e.g., <code>-U02</code> for Basement 2). "
        "The bidirectional decoder instantly unpacks raw ULPIN inputs, validates length and integrity, extracts geographic jurisdiction, and flies the camera to the parcel.",
        body_style
    ))

    # Engine C
    story.append(Paragraph("3.3 Subsurface 3D Clash & Encroachment Detection (<code>core/collision_engine.py</code>)", h2_style))
    story.append(Paragraph(
        "To prevent catastrophic strikes between deep foundations and municipal utility corridors, the collision engine computes both geodesic proximity and vertical intersection:",
        body_style
    ))
    story.append(Paragraph("&bull; <b>Horizontal Ground Distance:</b> Uses the Haversine equation over Earth radius $R = 6,371,000\\text{m}$:<br/>"
                           "$$a = \\sin^2\\left(\\frac{\\Delta \\phi}{2}\\right) + \\cos(\\phi_1)\\cos(\\phi_2)\\sin^2\\left(\\frac{\\Delta \\lambda}{2}\\right), \\quad D = 2R \\cdot \\arctan2\\left(\\sqrt{a}, \\sqrt{1-a}\\right)$$", bullet_style))
    story.append(Paragraph("&bull; <b>Vertical Interval Overlap ($\\Delta Z$):</b><br/>"
                           "$$\\Delta Z = \\min(Z_{top1}, Z_{top2}) - \\max(Z_{base1}, Z_{base2})$$", bullet_style))
    story.append(Paragraph("&bull; <b>Severity Classification:</b> If $D \\le 2 \\times R_{footprint}$ and $\\Delta Z > 0$, flagged as <b>CRITICAL COLLISION (Direct 3D Encroachment)</b>. If $D \\le 2 \\times R_{footprint} + S_{buffer}$ and $\\Delta Z > -10\\text{m}$, flagged as <b>SAFETY BUFFER VIOLATION</b>.", bullet_style))

    # Engine D
    story.append(Paragraph("3.4 Cryptographic SHA-256 Title Certificate & QR Engine (<code>core/certificate_generator.py</code>)", h2_style))
    story.append(Paragraph(
        "Generates an immutable cryptographic fingerprint sealing the vertical airspace parcel: "
        "<code>SHA-256(ULPIN | Owner | Lat | Lon | Z_Range | Valuation)</code>. "
        "Generates a scannable JSON QR payload that any citizen or bank official can scan with a standard smartphone camera to verify title legitimacy on-site.",
        body_style
    ))
    story.append(Spacer(1, 10))

    # -------------------------------------------------------------
    # 4. THREE ROLE-BASED OPERATIONAL PERSONAS
    # -------------------------------------------------------------
    story.append(Paragraph("4. Three Role-Based Operational Workflows", h1_style))
    story.append(Paragraph(
        "To address the diverse stakeholders of the Indian cadastral ecosystem, the platform provides tailored operational personas with 1-click switching:",
        body_style
    ))

    persona_data = [
        [Paragraph("<b>Persona Mode</b>", ParagraphStyle('TH', fontName='Helvetica-Bold', fontSize=9, textColor=colors.white)),
         Paragraph("<b>Primary User</b>", ParagraphStyle('TH', fontName='Helvetica-Bold', fontSize=9, textColor=colors.white)),
         Paragraph("<b>Features & Workflows Enabled</b>", ParagraphStyle('TH', fontName='Helvetica-Bold', fontSize=9, textColor=colors.white))],
        
        [Paragraph("<b>Citizen / Homebuyer Mode</b>", body_style),
         Paragraph("Citizens, Flat Buyers, Real Estate Investors, Banks", body_style),
         Paragraph("&bull; Instant title verification & RERA status check<br/>"
                   "&bull; Unit/Floor level dropdown with height bounds<br/>"
                   "&bull; Live 3D ULPIN Generator certificate card preview<br/>"
                   "&bull; 1-Click official PDF title certificate download", body_style)],

        [Paragraph("<b>Government GIS Surveyor Mode</b>", body_style),
         Paragraph("Municipal Engineers, GIS Officers, Urban Planners", body_style),
         Paragraph("&bull; 3D spatial metrics (Gross Volume $m^3$, Built-up area $m^2$, FSI/FAR)<br/>"
                   "&bull; Automated subsurface 3D clash & buffer violation audit<br/>"
                   "&bull; Interactive vertical architectural cross-section stack<br/>"
                   "&bull; 3D parcel coordinate ingestion into SQLite database", body_style)],

        [Paragraph("<b>Sub-Registrar Mode</b>", body_style),
         Paragraph("Revenue Officers, Land Registrars, Legal Authorities", body_style),
         Paragraph("&bull; Individual vertical airspace deed registration<br/>"
                   "&bull; 6% state stamp duty calculator based on cadastral value<br/>"
                   "&bull; Immutable ownership conveyance in SQLite database<br/>"
                   "&bull; Audit trail logging for pan-India transactions", body_style)],
    ]

    persona_table = Table(persona_data, colWidths=[120, 110, 274])
    persona_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#0f172a')),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#cbd5e1')),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.HexColor('#ffffff'), colors.HexColor('#f8fafc')]),
    ]))
    story.append(persona_table)
    story.append(Spacer(1, 10))

    # -------------------------------------------------------------
    # 5. ALL RECENT CHANGES & UI EVOLUTION
    # -------------------------------------------------------------
    story.append(Paragraph("5. Comprehensive UI/UX Evolution & Recent Changes", h1_style))
    story.append(Paragraph(
        "A major upgrade was executed to transform the prototype into a commercial-grade, multi-theme portal with a dedicated <b>Light Mode / Dark Mode switch button</b>:",
        body_style
    ))
    story.append(Paragraph("&bull; <b>Prominent Theme Switch Button:</b> Added an interactive switch button (<code>☀️ Light Mode</code> / <code>🌙 Dark Mode</code>) embedded in the top portal navbar alongside the Bhu-Naksha Sync pill. Toggling updates <code>st.session_state['theme']</code> with zero page flicker.", bullet_style))
    story.append(Paragraph("&bull; <b>Universal CSS Theming System:</b> Implemented a complete dual-palette design token architecture in <code>frontend/ui_components.py</code> covering Streamlit root canvas, typography, metric cards, inputs, dropdowns, expanders, tabs, radio pills, tables, and scrollbars.", bullet_style))
    story.append(Paragraph("&bull; <b>Theme-Adaptive Custom HTML Blocks:</b> Updated all custom cards—property dossier, vertical architectural cross-section, clash alerts, parsed ULPIN banner, map legend, and digital certificates—to seamlessly adapt background, text contrast, and border glow.", bullet_style))
    story.append(Paragraph("&bull; <b>Basemap Aesthetic Synchronization:</b> Synchronized the 3D PyDeck basemap default to switch between <code>Minimalist Light</code> (in Light Mode) and <code>Dark Matter (Default)</code> (in Dark Mode), with user manual preference persistence.", bullet_style))
    story.append(Paragraph("&bull; <b>High-DPI 3D Rendering:</b> Refined Deck.gl 3D extruded columns with high-contrast neon palettes and glowing footprints to ensure readability under both dark and bright lighting environments.", bullet_style))
    story.append(Spacer(1, 10))

    # -------------------------------------------------------------
    # 6. DATABASE SCHEMA & STORAGE STRUCTURE
    # -------------------------------------------------------------
    story.append(Paragraph("6. Relational Database Schema (SQLite)", h1_style))
    story.append(Paragraph(
        "The system stores all pan-India cadastral parcels in <code>database/spatial_records.db</code> under table <code>property_parcels</code>:",
        body_style
    ))

    schema_data = [
        [Paragraph("<b>Column Name</b>", ParagraphStyle('TH', fontName='Helvetica-Bold', fontSize=8, textColor=colors.white)),
         Paragraph("<b>Type</b>", ParagraphStyle('TH', fontName='Helvetica-Bold', fontSize=8, textColor=colors.white)),
         Paragraph("<b>Cadastral Description</b>", ParagraphStyle('TH', fontName='Helvetica-Bold', fontSize=8, textColor=colors.white))],
        [Paragraph("<code>property_id</code>", code_style), Paragraph("INTEGER PRIMARY KEY", code_style), Paragraph("Unique Cadastral Parcel ID (e.g. 101, 102)", body_style)],
        [Paragraph("<code>name</code>", code_style), Paragraph("TEXT", code_style), Paragraph("Building / Complex Name (e.g. Seawoods Grand Central)", body_style)],
        [Paragraph("<code>city</code> / <code>state</code>", code_style), Paragraph("TEXT", code_style), Paragraph("Municipal city and Indian state name", body_style)],
        [Paragraph("<code>state_code</code> / <code>dist_code</code>", code_style), Paragraph("INTEGER", code_style), Paragraph("LGD State and District codes for 14-digit ULPIN derivation", body_style)],
        [Paragraph("<code>lat</code> / <code>lon</code>", code_style), Paragraph("REAL", code_style), Paragraph("Precise WGS84 GPS decimal coordinates", body_style)],
        [Paragraph("<code>base_elevation</code>", code_style), Paragraph("REAL", code_style), Paragraph("Elevation datum in meters (negative = subterranean)", body_style)],
        [Paragraph("<code>total_height</code>", code_style), Paragraph("REAL", code_style), Paragraph("Vertical structural height in meters (e.g. 50.0m)", body_style)],
        [Paragraph("<code>type</code>", code_style), Paragraph("TEXT", code_style), Paragraph("Commercial, Apartment, Parking, Transit, Utility", body_style)],
        [Paragraph("<code>owner</code>", code_style), Paragraph("TEXT", code_style), Paragraph("Legal title holder / Agency / Developer", body_style)],
        [Paragraph("<code>valuation_cr</code>", code_style), Paragraph("REAL", code_style), Paragraph("Cadastral valuation in Crores INR (for stamp duty)", body_style)],
    ]

    schema_table = Table(schema_data, colWidths=[120, 110, 274])
    schema_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#0f172a')),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#cbd5e1')),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.HexColor('#ffffff'), colors.HexColor('#f8fafc')]),
    ]))
    story.append(schema_table)
    story.append(Spacer(1, 10))

    # -------------------------------------------------------------
    # 7. CONCLUSION & SIH 2026 COMPETITIVE EDGE
    # -------------------------------------------------------------
    story.append(Paragraph("7. SIH 2026 Impact & Competitive Advantages", h1_style))
    story.append(Paragraph(
        "<i>3D ULPIN Generator</i> provides an end-to-end, working implementation addressing the exact needs of modern smart cities and land governance:",
        body_style
    ))
    story.append(Paragraph("&bull; <b>Fully Functional Math & Slicing:</b> Not just mockups—every parcel slices dynamically, computes FSI, and calculates real Haversine & Z-overlap collisions.", bullet_style))
    story.append(Paragraph("&bull; <b>Standards Compliance:</b> Aligned with the ISO 19152 Land Administration Domain Model (LADM) and India's DILRMP ULPIN specification.", bullet_style))
    story.append(Paragraph("&bull; <b>Real Utility:</b> Solves multi-crore utility breach disputes, accelerates homebuyer bank loan approvals, and unlocks vertical deed registration revenues.", bullet_style))
    story.append(Paragraph("&bull; <b>Production-Ready UX:</b> Seamless Dark/Light mode, high-contrast typography, scannable QR codes, and instant vector PDF certificates.", bullet_style))

    # Build document
    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"PDF successfully generated: {filename}")

if __name__ == "__main__":
    out_file = os.path.join(os.path.dirname(__file__), "Bhu_Aadhaar_3D_Comprehensive_Project_Report.pdf")
    build_pdf(out_file)
