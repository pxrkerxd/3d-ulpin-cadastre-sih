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
        
        # Header (pages after cover)
        if self._pageNumber > 1:
            self.drawString(50, letter[1] - 34, "BHU-AADHAAR 3D | Comprehensive Technical & Architectural Specification")
            self.drawRightString(letter[0] - 50, letter[1] - 34, "ISO 19152 Cadastre | SIH 2026")
            self.setStrokeColor(colors.HexColor("#cbd5e1"))
            self.setLineWidth(0.75)
            self.line(50, letter[1] - 38, letter[0] - 50, letter[1] - 38)

        # Footer (all pages)
        self.setStrokeColor(colors.HexColor("#cbd5e1"))
        self.setLineWidth(0.75)
        self.line(50, 42, letter[0] - 50, 42)
        
        self.setFont("Helvetica", 8)
        self.drawString(50, 30, "Confidential • National Land Records Modernization Programme (DILRMP) / SIH 2026")
        page_str = f"Page {self._pageNumber} of {page_count}"
        self.drawRightString(letter[0] - 50, 30, page_str)
        self.restoreState()


def build_technical_pdf(filename="Bhu_Aadhaar_3D_Complete_Technical_Specification.pdf"):
    doc = SimpleDocTemplate(
        filename,
        pagesize=letter,
        leftMargin=50,
        rightMargin=50,
        topMargin=48,
        bottomMargin=48
    )

    styles = getSampleStyleSheet()

    # Typography Styles
    doc_title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=23,
        leading=27,
        textColor=colors.HexColor('#0f172a'),
        spaceAfter=4
    )

    subtitle_style = ParagraphStyle(
        'DocSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=11,
        leading=15,
        textColor=colors.HexColor('#0284c7'),
        spaceAfter=10
    )

    meta_style = ParagraphStyle(
        'DocMeta',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.5,
        leading=12,
        textColor=colors.HexColor('#475569')
    )

    h1_style = ParagraphStyle(
        'H1',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=13,
        leading=16,
        textColor=colors.HexColor('#0f172a'),
        spaceBefore=12,
        spaceAfter=6,
        keepWithNext=True
    )

    h2_style = ParagraphStyle(
        'H2',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=10.5,
        leading=14,
        textColor=colors.HexColor('#0369a1'),
        spaceBefore=9,
        spaceAfter=5,
        keepWithNext=True
    )

    body_style = ParagraphStyle(
        'Body',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9,
        leading=13,
        textColor=colors.HexColor('#1e293b'),
        spaceAfter=6
    )

    bullet_style = ParagraphStyle(
        'Bullet',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.5,
        leading=12.5,
        textColor=colors.HexColor('#334155'),
        leftIndent=12,
        firstLineIndent=-8,
        spaceAfter=3
    )

    code_style = ParagraphStyle(
        'CodeSnippet',
        parent=styles['Normal'],
        fontName='Courier',
        fontSize=8,
        leading=10.5,
        textColor=colors.HexColor('#0f172a')
    )

    table_th_style = ParagraphStyle(
        'TableTH',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8,
        leading=10,
        textColor=colors.white
    )

    table_td_style = ParagraphStyle(
        'TableTD',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8,
        leading=10.5,
        textColor=colors.HexColor('#1e293b')
    )

    callout_box_style = ParagraphStyle(
        'Callout',
        parent=styles['Normal'],
        fontName='Helvetica-Oblique',
        fontSize=8.5,
        leading=12,
        textColor=colors.HexColor('#0369a1')
    )

    story = []

    # =========================================================================
    # COVER / TOP BANNER
    # =========================================================================
    badge_table = Table([[
        Paragraph("<b>SMART INDIA HACKATHON 2026</b>", ParagraphStyle('B1', fontName='Helvetica-Bold', fontSize=7.5, textColor=colors.HexColor('#0284c7'))),
        Paragraph("<b>ISO 19152 LADM COMPLIANT</b>", ParagraphStyle('B2', fontName='Helvetica-Bold', fontSize=7.5, textColor=colors.HexColor('#059669'))),
        Paragraph("<b>MINISTRY OF RURAL DEV / DILRMP</b>", ParagraphStyle('B3', fontName='Helvetica-Bold', fontSize=7.5, textColor=colors.HexColor('#7e22ce')))
    ]], colWidths=[165, 175, 172])
    badge_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (0,0), colors.HexColor('#e0f2fe')),
        ('BACKGROUND', (1,0), (1,0), colors.HexColor('#dcfce7')),
        ('BACKGROUND', (2,0), (2,0), colors.HexColor('#f3e8ff')),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOX', (0,0), (0,0), 0.5, colors.HexColor('#38bdf8')),
        ('BOX', (1,0), (1,0), 0.5, colors.HexColor('#4ade80')),
        ('BOX', (2,0), (2,0), 0.5, colors.HexColor('#c084fc')),
    ]))
    story.append(badge_table)
    story.append(Spacer(1, 8))

    story.append(Paragraph("BHU-AADHAAR 3D: MASTER TECHNICAL SPECIFICATION", doc_title_style))
    story.append(Paragraph("Next-Generation 3D Spatial Cadastre, Subsurface Collision Engine, AI Slicing & Vertical Land Registry", subtitle_style))
    story.append(Paragraph("<b>System Lead:</b> Parijat Sharma &bull; <b>Ecosystem:</b> Smart India Hackathon 2026 &bull; <b>Standard:</b> ISO 19152 (LADM Edition II)", meta_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor("#0284c7"), spaceAfter=10, spaceBefore=6))

    # =========================================================================
    # 1. EXECUTIVE SUMMARY & PROBLEM STATEMENT
    # =========================================================================
    story.append(Paragraph("1. Executive Summary & Problem Context", h1_style))
    story.append(Paragraph(
        "India's urban economy is experiencing rapid vertical densification. In commercial and residential hubs such as Mumbai MMR, Delhi NCR, Bengaluru, Hyderabad, and GIFT City, high-rise superstructures are intricately integrated with multi-level subterranean basements, deep-bore metro tunnels, and dense underground utility corridors. "
        "However, current land administration across India (governed under DILRMP and Bhu-Naksha) remains strictly <b>two-dimensional (2D)</b>. Parcels are registered purely as flat surface polygons on a 2D plane (Latitude, Longitude), assuming a single titleholder owns the land from the center of the earth to the sky.",
        body_style
    ))
    story.append(Paragraph(
        "This structural deficiency creates systemic real estate, municipal, and legal hazards:",
        body_style
    ))
    story.append(Paragraph("&bull; <b>Airspace & Unit Demarcation Failure:</b> In a 50-storey high-rise, hundreds of flat buyers share identical 2D coordinates. Existing land registries cannot legally demarcate individual volumetric units in 3D.", bullet_style))
    story.append(Paragraph("&bull; <b>Subsurface Utility Breaches:</b> Deep private foundation piling and basement excavation frequently collide with underground metro tunnels, water mains, and high-voltage power conduits due to the lack of a 3D subsurface cadastre.", bullet_style))
    story.append(Paragraph("&bull; <b>Title Ambiguity & Double Financing:</b> Without immutable, vertical parcel IDs, fraudulent developers can double-mortgage air-rights or transfer overlapping units.", bullet_style))
    story.append(Paragraph(
        "<b>Bhu-Aadhaar 3D</b> solves this by delivering an ISO 19152 compliant 3D cadastral platform with procedural WebGL digital twins, automated AI LiDAR floor slicing, subterranean clash audits, Modulo-36 check-digit vertical ULPINs, and tamper-proof SHA-256 PDF title deeds.",
        body_style
    ))
    story.append(Spacer(1, 6))

    # =========================================================================
    # 2. DATASET & VALUATION METHODOLOGY
    # =========================================================================
    story.append(Paragraph("2. Cadastral Dataset Architecture & Structure Valuation", h1_style))
    story.append(Paragraph(
        "The cadastral data architecture operates across three persistent, synchronized layers designed for high-performance spatial querying and national interoperability:",
        body_style
    ))
    story.append(Paragraph("&bull; <b>Relational SQLite Storage (<code>database/spatial_records.db</code>):</b> Primary transactional database containing parcel geometry, LGD geographical hierarchy, elevation datums, height bounds, owner identities, zones, and valuations.", bullet_style))
    story.append(Paragraph("&bull; <b>Master JSON Specification (<code>data/master_cadastre_dataset.json</code>):</b> Machine-readable canonical dataset containing system-wide metadata, ISO 19152 compliance flags, and 25 benchmark multi-strata landmark properties.", bullet_style))
    story.append(Paragraph("&bull; <b>Tabular CSV Interoperability Layer (<code>data/mock_city_data.csv</code>):</b> Standard tabular export used for GIS desktop tooling (QGIS, ArcGIS) and fallback synchronization.", bullet_style))
    
    story.append(Paragraph("2.1 Valuation Derivation Methodology", h2_style))
    story.append(Paragraph(
        "Property and structure valuations in Bhu-Aadhaar 3D are modeled on realistic Indian municipal circle rates and market capitalizations:",
        body_style
    ))
    story.append(Paragraph("&bull; <b>Cadastral Base Capitalization (<code>valuation_cr</code>):</b> Stored in ₹ Crores, calibrated against Ready Reckoner Rates (Maharashtra), Circle Rates (Delhi/NCR), Guidance Values (Karnataka), and jantri rates (Gujarat). Tier-1 financial bourses (e.g. BKC Diamond Tower at ₹2,400 Cr, GIFT Diamond Tower at ₹2,800 Cr) reflect real capital valuations.", bullet_style))
    story.append(Paragraph("&bull; <b>Dynamic Volumetric Floor Apportionment:</b> Individual floor and unit values are dynamically derived in the WebGL Digital Twin component via the formula:", bullet_style))
    
    # Formula Box
    f_table = Table([[
        Paragraph("<b>Volumetric Stratum Valuation Formula:</b><br/>"
                  "<code>Floor Valuation (₹ Cr) = Total Building Valuation (valuation_cr) / Total Slices (numFloors)</code><br/>"
                  "<i>Subsurface basements are allocated dedicated utility values (e.g. ₹35.0 Cr to ₹180.0 Cr) reflecting specialized geotechnical construction costs.</i>", callout_box_style)
    ]], colWidths=[512])
    f_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#f0f9ff')),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#0284c7')),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('LEFTPADDING', (0,0), (-1,-1), 10),
        ('RIGHTPADDING', (0,0), (-1,-1), 10),
    ]))
    story.append(f_table)
    story.append(Spacer(1, 5))

    story.append(Paragraph("&bull; <b>Statutory State Stamp Duty Calculation:</b> In Sub-Registrar Mode, the platform automatically computes legal state stamp duty for individual airspace conveyances at 6% of the cadastral valuation: <code>Stamp Duty = valuation_cr * 0.06</code>.", bullet_style))
    story.append(Paragraph("&bull; <b>Cryptographic Title Binding:</b> The cadastral valuation is cryptographically fused into the SHA-256 title hash printed on the Bhu-Aadhaar certificate, preventing fraudulent undervaluation during bank mortgage audits.", bullet_style))

    story.append(Paragraph("2.2 Benchmark Pan-India Cadastral Dataset (Sample)", h2_style))
    
    # Dataset Table
    ds_headers = [
        Paragraph("<b>ID</b>", table_th_style),
        Paragraph("<b>Landmark Name</b>", table_th_style),
        Paragraph("<b>City / State</b>", table_th_style),
        Paragraph("<b>LGD</b>", table_th_style),
        Paragraph("<b>Type</b>", table_th_style),
        Paragraph("<b>Z Bounds</b>", table_th_style),
        Paragraph("<b>Valuation</b>", table_th_style)
    ]
    ds_rows = [
        ds_headers,
        [Paragraph("101", table_td_style), Paragraph("Seawoods Grand Central TOD", table_td_style), Paragraph("Navi Mumbai, MH", table_td_style), Paragraph("27-21", table_td_style), Paragraph("Commercial", table_td_style), Paragraph("0 to +120m", table_td_style), Paragraph("₹ 850 Cr", table_td_style)],
        [Paragraph("102", table_td_style), Paragraph("Grand Central Subsurface Concourse", table_td_style), Paragraph("Navi Mumbai, MH", table_td_style), Paragraph("27-21", table_td_style), Paragraph("Underground Parking", table_td_style), Paragraph("-15 to 0m", table_td_style), Paragraph("₹ 180 Cr", table_td_style)],
        [Paragraph("105", table_td_style), Paragraph("BKC Diamond Tower", table_td_style), Paragraph("Mumbai, MH", table_td_style), Paragraph("27-22", table_td_style), Paragraph("Commercial", table_td_style), Paragraph("0 to +160m", table_td_style), Paragraph("₹ 2,400 Cr", table_td_style)],
        [Paragraph("106", table_td_style), Paragraph("BKC Metro-3 Underground Vault", table_td_style), Paragraph("Mumbai, MH", table_td_style), Paragraph("27-22", table_td_style), Paragraph("Subsurface Utility", table_td_style), Paragraph("-24 to 0m", table_td_style), Paragraph("₹ 680 Cr", table_td_style)],
        [Paragraph("107", table_td_style), Paragraph("Lodha World One (Worli)", table_td_style), Paragraph("Mumbai, MH", table_td_style), Paragraph("27-22", table_td_style), Paragraph("Apartment", table_td_style), Paragraph("0 to +240m", table_td_style), Paragraph("₹ 1,850 Cr", table_td_style)],
        [Paragraph("201", table_td_style), Paragraph("Connaught Outer Circle Rotunda", table_td_style), Paragraph("New Delhi, DL", table_td_style), Paragraph("07-01", table_td_style), Paragraph("Commercial", table_td_style), Paragraph("0 to +75m", table_td_style), Paragraph("₹ 950 Cr", table_td_style)],
        [Paragraph("202", table_td_style), Paragraph("Rajiv Chowk Subsurface Metro Terminal", table_td_style), Paragraph("New Delhi, DL", table_td_style), Paragraph("07-01", table_td_style), Paragraph("Subsurface Utility", table_td_style), Paragraph("-18 to 0m", table_td_style), Paragraph("₹ 780 Cr", table_td_style)],
        [Paragraph("204", table_td_style), Paragraph("DLF Cyber City Building 10", table_td_style), Paragraph("Gurugram, HR", table_td_style), Paragraph("06-18", table_td_style), Paragraph("Commercial", table_td_style), Paragraph("0 to +140m", table_td_style), Paragraph("₹ 2,100 Cr", table_td_style)],
        [Paragraph("301", table_td_style), Paragraph("Manyata Embassy High-Tech Park", table_td_style), Paragraph("Bengaluru, KA", table_td_style), Paragraph("29-20", table_td_style), Paragraph("Commercial", table_td_style), Paragraph("0 to +110m", table_td_style), Paragraph("₹ 1,750 Cr", table_td_style)],
        [Paragraph("401", table_td_style), Paragraph("GIFT Diamond Tower Pinnacle", table_td_style), Paragraph("GIFT City, GJ", table_td_style), Paragraph("24-07", table_td_style), Paragraph("Commercial", table_td_style), Paragraph("0 to +180m", table_td_style), Paragraph("₹ 2,800 Cr", table_td_style)],
        [Paragraph("402", table_td_style), Paragraph("GIFT Subsurface Utility Tunnel (TUM)", table_td_style), Paragraph("GIFT City, GJ", table_td_style), Paragraph("24-07", table_td_style), Paragraph("Subsurface Utility", table_td_style), Paragraph("-16 to 0m", table_td_style), Paragraph("₹ 890 Cr", table_td_style)],
        [Paragraph("501", table_td_style), Paragraph("HITEC Cyber Towers (Cyberabad)", table_td_style), Paragraph("Hyderabad, TS", table_td_style), Paragraph("36-12", table_td_style), Paragraph("Commercial", table_td_style), Paragraph("0 to +135m", table_td_style), Paragraph("₹ 1,600 Cr", table_td_style)],
        [Paragraph("702", table_td_style), Paragraph("Hooghly Underwater Metro Corridor", table_td_style), Paragraph("Kolkata, WB", table_td_style), Paragraph("19-11", table_td_style), Paragraph("Subsurface Utility", table_td_style), Paragraph("-32 to 0m", table_td_style), Paragraph("₹ 1,150 Cr", table_td_style)]
    ]
    ds_table = Table(ds_rows, colWidths=[24, 150, 95, 45, 80, 60, 58])
    ds_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#0f172a')),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#cbd5e1')),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.HexColor('#ffffff'), colors.HexColor('#f8fafc')]),
    ]))
    story.append(ds_table)
    story.append(Spacer(1, 10))

    # =========================================================================
    # 3. 3D ULPIN NUMBERING LOGIC & STANDARDS
    # =========================================================================
    story.append(Paragraph("3. Building ULPIN (Bhu-Aadhaar 3D) Numbering Logic", h1_style))
    story.append(Paragraph(
        "India's Ministry of Rural Development prescribes the 14-digit Unique Land Parcel Identification Number (ULPIN). Bhu-Aadhaar 3D extends this into a full volumetric cadastre under ISO 19152 (LADM Edition II):",
        body_style
    ))
    
    story.append(Paragraph("3.1 14-Digit Base ULPIN Structure (LGD Compliant)", h2_style))
    story.append(Paragraph(
        "The base 14 digits are deterministically generated from official Census and Local Government Directory (LGD) codes:",
        body_style
    ))
    
    ulpin_struct = [
        [Paragraph("<b>Component</b>", table_th_style), Paragraph("<b>Digits</b>", table_th_style), Paragraph("<b>Description</b>", table_th_style), Paragraph("<b>Sample Value</b>", table_th_style)],
        [Paragraph("State Code (SS)", table_td_style), Paragraph("2 Digits", table_td_style), Paragraph("LGD Indian State / UT code", table_td_style), Paragraph("<code>27</code> (Maharashtra)", table_td_style)],
        [Paragraph("District Code (DD)", table_td_style), Paragraph("2 Digits", table_td_style), Paragraph("LGD District identifier", table_td_style), Paragraph("<code>21</code> (Thane / Navi Mumbai)", table_td_style)],
        [Paragraph("Sub-District (SSS)", table_td_style), Paragraph("3 Digits", table_td_style), Paragraph("Taluk / Tehsil / Ward number", table_td_style), Paragraph("<code>101</code>", table_td_style)],
        [Paragraph("Village / Ward (VVV)", table_td_style), Paragraph("3 Digits", table_td_style), Paragraph("Revenue Village / Municipal Ward", table_td_style), Paragraph("<code>050</code>", table_td_style)],
        [Paragraph("Plot ID (PPPP)", table_td_style), Paragraph("4 Digits", table_td_style), Paragraph("Cadastral plot / building envelope", table_td_style), Paragraph("<code>0101</code>", table_td_style)],
        [Paragraph("Base ULPIN", ParagraphStyle('TB', parent=table_td_style, fontName='Helvetica-Bold')), Paragraph("14 Digits", table_td_style), Paragraph("Permanent ground parcel identifier", table_td_style), Paragraph("<b><code>27211010500101</code></b>", table_td_style)]
    ]
    u_table = Table(ulpin_struct, colWidths=[115, 65, 202, 130])
    u_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#0f172a')),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#cbd5e1')),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.HexColor('#ffffff'), colors.HexColor('#f8fafc')]),
    ]))
    story.append(u_table)
    story.append(Spacer(1, 6))

    story.append(Paragraph("3.2 3D Vertical Cadastral Extension & Modulo-36 Checksum", h2_style))
    story.append(Paragraph(
        "To establish legal ownership of vertical airspace and subsurface caverns, the system appends vertical strata designators:",
        body_style
    ))
    story.append(Paragraph("&bull; <b>Standard Vertical Suffix (<code>core/ulpin_logic.py</code>):</b> Appends <code>-FFF</code> for above-ground storeys (e.g. <code>-004</code> for Floor 4, <code>-000</code> for Ground) and <code>-UXX</code> for subterranean basements (e.g. <code>-U02</code> for Basement Level 2).", bullet_style))
    story.append(Paragraph("&bull; <b>Enhanced ISO 19152 Format (<code>core/ulpin_enhanced.py</code>):</b><br/>"
                           "<code>[LGD]-[BASE_2D]-[STRATUM]-[LEVEL]-[UNIT]-[CHECKSUM]</code><br/>"
                           "Example: <b><code>2721-27211010500101-BLD-F04-U01-K</code></b>", bullet_style))
    story.append(Paragraph("&bull; <b>Modulo-36 Weighted Check Character:</b> A cryptographic Modulo-36 checksum character is calculated over prime weights $[3, 7, 11, 13, 17, 19, 23, 29]$ against character set <code>0-9, A-Z</code> to guarantee human transcription integrity during land deed registration.", bullet_style))
    story.append(Paragraph("&bull; <b>Strata Classification Standard:</b>", bullet_style))

    strata_data = [
        [Paragraph("<b>Stratum</b>", table_th_style), Paragraph("<b>Full Name</b>", table_th_style), Paragraph("<b>Hex Theme</b>", table_th_style), Paragraph("<b>Legal Definition & Cadastral Application</b>", table_th_style)],
        [Paragraph("<code>SUR</code>", table_td_style), Paragraph("Surface Land Parcel", table_td_style), Paragraph("<code>#10B981</code>", table_td_style), Paragraph("Ground datum terrain, roadways, surface courtyards", table_td_style)],
        [Paragraph("<code>BLD</code>", table_td_style), Paragraph("Multi-Storey Building Unit", table_td_style), Paragraph("<code>#3B82F6</code>", table_td_style), Paragraph("Private residential apartments, corporate office units", table_td_style)],
        [Paragraph("<code>COM</code>", table_td_style), Paragraph("Common Condominium Property", table_td_style), Paragraph("<code>#8B5CF6</code>", table_td_style), Paragraph("Elevated skybridges, shared atriums, clubhouse podiums", table_td_style)],
        [Paragraph("<code>SUB</code>", table_td_style), Paragraph("Subterranean Basement Unit", table_td_style), Paragraph("<code>#F59E0B</code>", table_td_style), Paragraph("Underground car parking, HVAC chiller plant vaults", table_td_style)],
        [Paragraph("<code>UTL</code>", table_td_style), Paragraph("Subsurface Utility Corridor", table_td_style), Paragraph("<code>#EC4899</code>", table_td_style), Paragraph("Metro tunnels, municipal water mains, electrical busways", table_td_style)],
        [Paragraph("<code>AIR</code>", table_td_style), Paragraph("Elevated Air-Rights Parcel", table_td_style), Paragraph("<code>#06B6D4</code>", table_td_style), Paragraph("Rooftop helipads, solar PV decks, telecomm arrays, spires", table_td_style)],
    ]
    st_table = Table(strata_data, colWidths=[45, 125, 60, 282])
    st_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#0f172a')),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#cbd5e1')),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.HexColor('#ffffff'), colors.HexColor('#f8fafc')]),
    ]))
    story.append(st_table)
    story.append(Spacer(1, 10))

    # =========================================================================
    # 4. THE AI, 3D & COMPUTATIONAL MODELS
    # =========================================================================
    story.append(Paragraph("4. The AI, 3D & Computational Models", h1_style))
    story.append(Paragraph(
        "Bhu-Aadhaar 3D incorporates four distinct mathematical and artificial intelligence engines:",
        body_style
    ))

    story.append(Paragraph("4.1 AI Point Cloud Floor Slicing Engine (<code>core/ai_floor_segmentation.py</code>)", h2_style))
    story.append(Paragraph(
        "Processes high-density drone LiDAR point clouds and photogrammetry point elevations (synthesized via <code>data/mock_lidar.py</code>) to automatically detect floor slabs without manual CAD blueprints:",
        body_style
    ))
    story.append(Paragraph("&bull; <b>Vertical Density Histogramming:</b> Computes point frequencies across vertical bins of $\\Delta Z = 0.1\\text{m}$. Concrete ceiling and floor slabs produce distinct horizontal reflective point spikes.", bullet_style))
    story.append(Paragraph("&bull; <b>Moving-Average Signal Smoothing:</b> Applies a 5-point moving average window to eliminate sensor noise and multipath foliage scatter.", bullet_style))
    story.append(Paragraph("&bull; <b>Peak Prominence Detection:</b> Enforces a minimum storey threshold ($h_{min} \\ge 2.7\\text{m}$) and relative peak prominence ($>25\\%$ of maximum density) to locate true structural floors, classifying them as Basements (<code>B01-B04</code>), Ground (<code>G00</code>), or Upper Storeys (<code>F01-F16</code>).", bullet_style))

    story.append(Paragraph("4.2 3D Subsurface Collision & Clash Engine (<code>core/collision_engine.py</code>)", h2_style))
    story.append(Paragraph(
        "Protects critical subsurface infrastructure (e.g. underground metro tunnels, water aqueducts, gas conduits) from deep piling and foundation encroachment:",
        body_style
    ))
    story.append(Paragraph("&bull; <b>Geodesic Proximity (Haversine Formula):</b> Computes exact surface distance $D$ over Earth mean radius $R = 6,371,000\\text{m}$:<br/>"
                           "$$a = \\sin^2\\left(\\frac{\\Delta \\phi}{2}\\right) + \\cos(\\phi_1)\\cos(\\phi_2)\\sin^2\\left(\\frac{\\Delta \\lambda}{2}\\right), \\quad D = 2R \\cdot \\arctan2\\left(\\sqrt{a}, \\sqrt{1-a}\\right)$$", bullet_style))
    story.append(Paragraph("&bull; <b>1D/3D Vertical Interval Overlap:</b> Evaluates vertical overlap: $\\Delta Z = \\min(Z_{top1}, Z_{top2}) - \\max(Z_{base1}, Z_{base2})$.", bullet_style))
    story.append(Paragraph("&bull; <b>Automated Severity Classification:</b><br/>"
                           "- <b>CRITICAL COLLISION (Direct 3D Encroachment):</b> $D \\le 2 \\times R_{footprint}$ and $\\Delta Z > 0\\text{m}$. Physical overlap of volume.<br/>"
                           "- <b>SAFETY BUFFER VIOLATION:</b> $D \\le 2 \\times R_{footprint} + S_{buffer}$ and $\\Delta Z > -10\\text{m}$. Threatens structural integrity.", bullet_style))

    story.append(Paragraph("4.3 3D Cadastral Topology & Volumetric Delineation (<code>core/topology_3d.py</code>)", h2_style))
    story.append(Paragraph(
        "Validates that 3D volumetric parcels conform to ISO 19152 watertightness and non-overlap standards:",
        body_style
    ))
    story.append(Paragraph("&bull; <b>Shoelace Formula:</b> Computes exact 2D planar gross floor area: $Area = \\frac{1}{2} \\left| \\sum_{i=0}^{n-1} (x_i y_{i+1} - x_{i+1} y_i) \\right|$.", bullet_style))
    story.append(Paragraph("&bull; <b>Enclosed Volume & Centroid:</b> Calculates 3D prismatic volume ($V = Area \\times \\Delta Z$) and 3D centroid coordinates $(C_x, C_y, C_z)$.", bullet_style))
    story.append(Paragraph("&bull; <b>3D AABB Intersection Volume:</b> Computes axis-aligned bounding box intersection volumes to verify unit containment and parent boundary setback compliance.", bullet_style))

    story.append(Paragraph("4.4 Procedural 3D WebGL Digital Twin Models (<code>frontend/digital_twin_component.py</code>)", h2_style))
    story.append(Paragraph(
        "Features over <b>2,500 lines of custom Three.js</b> WebGL code rendering realistic procedural architectural archetypes:",
        body_style
    ))
    story.append(Paragraph("&bull; <b>20 Procedural Archetypes:</b> Includes <code>transit_quad_podium</code>, <code>crystalline_diamond</code>, <code>supertall_tiered</code>, <code>subterranean_multilevel_cavern</code>, <code>skybridge_twin</code>, and <code>underwater_subaqueous_tunnel</code>.", bullet_style))
    story.append(Paragraph("&bull; <b>Dynamic Interaction Shaders:</b> Exploded floor slider (vertically expands storeys for inspection), Subsurface X-Ray slider (transparent ground plane revealing underground tunnels and train networks), and satellite terrain mapping.", bullet_style))
    story.append(Spacer(1, 10))

    # =========================================================================
    # 5. COMPLETE TECHNOLOGY STACK
    # =========================================================================
    story.append(Paragraph("5. Complete Full-Stack Technology Architecture", h1_style))
    story.append(Paragraph(
        "The system is built on a resilient, high-performance tech stack combining Python data science backends with interactive WebGL and GIS rendering:",
        body_style
    ))

    stack_data = [
        [Paragraph("<b>Category</b>", table_th_style), Paragraph("<b>Technology / Library</b>", table_th_style), Paragraph("<b>Version</b>", table_th_style), Paragraph("<b>Core Function & Implementation Role</b>", table_th_style)],
        
        [Paragraph("<b>Frontend Framework</b>", table_td_style), Paragraph("Streamlit", table_td_style), Paragraph(">=1.30.0", table_td_style), Paragraph("Core reactive web application container, state management, role routing", table_td_style)],
        [Paragraph("<b>3D WebGL Graphics</b>", table_td_style), Paragraph("Three.js + OrbitControls", table_td_style), Paragraph("r128", table_td_style), Paragraph("Interactive procedural 3D digital twins, exploded views, subsurface X-Ray", table_td_style)],
        [Paragraph("<b>GIS 3D Mapping</b>", table_td_style), Paragraph("PyDeck (Deck.gl)", table_td_style), Paragraph(">=0.8.0", table_td_style), Paragraph("Geospatial visualization: extruded ColumnLayer, ScatterplotLayer halos", table_td_style)],
        [Paragraph("<b>Cartography / Tiles</b>", table_td_style), Paragraph("ESRI / CartoDB / MapLibre", table_td_style), Paragraph("Raster/GL", table_td_style), Paragraph("Satellite imagery, Dark Matter, Positron Light, and Voyager basemaps", table_td_style)],
        [Paragraph("<b>Styling & UX</b>", table_td_style), Paragraph("Tailwind CSS + Vanilla CSS", table_td_style), Paragraph("3.x / CSS3", table_td_style), Paragraph("Figma glassmorphic design system, persistent dark/light theme switcher", table_td_style)],
        [Paragraph("<b>UI Iconography</b>", table_td_style), Paragraph("Lucide Icons", table_td_style), Paragraph("Latest", table_td_style), Paragraph("Modern iconography across top navigation, control bars, and dossiers", table_td_style)],
        [Paragraph("<b>Analytics Charts</b>", table_td_style), Paragraph("Chart.js + Streamlit Charts", table_td_style), Paragraph("Latest", table_td_style), Paragraph("LiDAR vertical Z-density curves, metro-wise valuation aggregations", table_td_style)],
        [Paragraph("<b>Database Layer</b>", table_td_style), Paragraph("SQLite3 (Embedded SQL)", table_td_style), Paragraph("3.x (Built-in)", table_td_style), Paragraph("Persistent relational spatial database (<code>spatial_records.db</code>)", table_td_style)],
        [Paragraph("<b>Data Processing</b>", table_td_style), Paragraph("Pandas", table_td_style), Paragraph(">=2.0.0", table_td_style), Paragraph("DataFrame filtering, spatial tabular analysis, and CSV interoperability", table_td_style)],
        [Paragraph("<b>Certificate Engine</b>", table_td_style), Paragraph("ReportLab", table_td_style), Paragraph(">=4.0.0", table_td_style), Paragraph("Precision vector PDF generation for official 3D Bhu-Aadhaar Title Deeds", table_td_style)],
        [Paragraph("<b>Cryptographic QR</b>", table_td_style), Paragraph("qrcode + Pillow", table_td_style), Paragraph("Latest", table_td_style), Paragraph("Generates scannable SVG and PNG QR verification payloads", table_td_style)],
        [Paragraph("<b>Schema Validation</b>", table_td_style), Paragraph("Pydantic", table_td_style), Paragraph(">=2.0.0", table_td_style), Paragraph("Strict typing and JSON schema enforcement across cadastre APIs", table_td_style)],
        [Paragraph("<b>Runtime / Env</b>", table_td_style), Paragraph("Python", table_td_style), Paragraph("3.10 / 3.11+", table_td_style), Paragraph("Core backend execution environment running on Windows / Linux", table_td_style)]
    ]
    stk_table = Table(stack_data, colWidths=[95, 115, 55, 247])
    stk_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#0f172a')),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 2.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2.5),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#cbd5e1')),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.HexColor('#ffffff'), colors.HexColor('#f8fafc')]),
    ]))
    story.append(stk_table)
    story.append(Spacer(1, 10))

    # =========================================================================
    # 6. OPERATIONAL WORKFLOWS & PERSONAS
    # =========================================================================
    story.append(Paragraph("6. Operational Personas & Role-Based Workflows", h1_style))
    story.append(Paragraph(
        "To serve India's diverse cadastral stakeholders, the system provides dedicated operational personas with instantaneous session state switching:",
        body_style
    ))

    persona_specs = [
        [Paragraph("<b>Persona Mode</b>", table_th_style), Paragraph("<b>Target Stakeholders</b>", table_th_style), Paragraph("<b>Core Functionalities & Operational Capabilities</b>", table_th_style)],
        
        [Paragraph("<b>🏠 Citizen / Homebuyer Mode</b>", table_td_style),
         Paragraph("Flat buyers, real estate investors, mortgage banks", table_td_style),
         Paragraph("&bull; Instant title verification and RERA registration audit.<br/>"
                   "&bull; Interactive floor-by-floor dropdown displaying exact elevation bounds.<br/>"
                   "&bull; Live 3D Bhu-Aadhaar certificate card preview.<br/>"
                   "&bull; 1-Click official PDF title certificate generation with cryptographic QR code.", table_td_style)],

        [Paragraph("<b>📐 Government Surveyor Mode</b>", table_td_style),
         Paragraph("Municipal engineers, GIS surveyors, urban planners", table_td_style),
         Paragraph("&bull; Volumetric architectural metrics: Gross Volume ($m^3$), Built-up Area ($m^2$), FSI.<br/>"
                   "&bull; Automated subsurface 3D clash audit against metro tunnels and utility conduits.<br/>"
                   "&bull; AI LiDAR Point Cloud floor slab detection with interactive histogram charts.<br/>"
                   "&bull; Direct 3D parcel coordinate ingestion into the SQLite cadastral database.", table_td_style)],

        [Paragraph("<b>🏛️ Sub-Registrar Mode</b>", table_td_style),
         Paragraph("Revenue officers, land registrars, stamp duty authorities", table_td_style),
         Paragraph("&bull; Individual vertical airspace deed conveyance simulation.<br/>"
                   "&bull; Automated 6% state stamp duty calculation based on cadastral valuation.<br/>"
                   "&bull; Immutable ownership record updates directly in <code>spatial_records.db</code>.<br/>"
                   "&bull; Audit trail verification preventing double-mortgaging and title conflicts.", table_td_style)],
    ]
    p_table = Table(persona_specs, colWidths=[120, 115, 277])
    p_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#0f172a')),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#cbd5e1')),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.HexColor('#ffffff'), colors.HexColor('#f8fafc')]),
    ]))
    story.append(p_table)
    story.append(Spacer(1, 10))

    # =========================================================================
    # 7. CRYPTOGRAPHIC TITLE DEED & QR VERIFICATION
    # =========================================================================
    story.append(Paragraph("7. Cryptographic Title Security & QR Verification", h1_style))
    story.append(Paragraph(
        "To prevent document forgery and fraudulent double-sales, Bhu-Aadhaar 3D implements end-to-end cryptographic sealing:",
        body_style
    ))
    story.append(Paragraph("&bull; <b>SHA-256 Title Hash:</b> The vertical deed is sealed via an immutable SHA-256 hash incorporating all physical and legal attributes:", bullet_style))
    
    hash_box = Table([[
        Paragraph("<b>Cryptographic Hash Construction (<code>core/certificate_generator.py</code>):</b><br/>"
                  "<code>Title Hash = SHA-256( ULPIN | Legal Owner | Latitude | Longitude | Z-Range (MSL) | Valuation )</code><br/>"
                  "<i>Any post-issuance tampering with floor height, ownership, or valuation instantly invalidates the hash.</i>", callout_box_style)
    ]], colWidths=[512])
    hash_box.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#f8fafc')),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#64748b')),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('LEFTPADDING', (0,0), (-1,-1), 10),
        ('RIGHTPADDING', (0,0), (-1,-1), 10),
    ]))
    story.append(hash_box)
    story.append(Spacer(1, 5))

    story.append(Paragraph("&bull; <b>Scannable Digital QR Payload:</b> Encodes a structured JSON payload directly into the certificate:", bullet_style))
    story.append(Paragraph("<code>{\"ulpin\": \"27211010500101-004\", \"owner\": \"Sh. Singhania\", \"z_bounds\": \"+12.8m to +16.0m\", \"valuation\": \"₹ 85.0 Cr\", \"hash\": \"7a8e4...\", \"authority\": \"National 3D Cadastre Portal\"}</code>", code_style))
    story.append(Paragraph("&bull; <b>On-Site Mobile Verification:</b> Citizens, commercial lenders, and sub-registrars can scan the QR code using any standard smartphone to instantly verify title validity against the national land registry in real time.", bullet_style))
    story.append(Spacer(1, 8))

    # =========================================================================
    # 8. CONCLUSION & COMPETITIVE ADVANTAGES
    # =========================================================================
    story.append(Paragraph("8. Conclusion & SIH 2026 Competitive Edge", h1_style))
    story.append(Paragraph(
        "Bhu-Aadhaar 3D transitions Indian land administration from historical 2D planar maps into a future-ready, three-dimensional geospatial infrastructure. "
        "Key competitive differentiators include:",
        body_style
    ))
    story.append(Paragraph("&bull; <b>End-to-End Operational Pipeline:</b> From raw drone point clouds to procedural WebGL 3D twins, subsurface safety audits, and downloadable legal PDF deeds.", bullet_style))
    story.append(Paragraph("&bull; <b>Full Standards Compliance:</b> Fully aligned with the ISO 19152 Land Administration Domain Model (LADM) and India's DILRMP ULPIN mandate.", bullet_style))
    story.append(Paragraph("&bull; <b>Zero Proprietary Lock-In:</b> Built entirely on open, accessible technologies—Python, Streamlit, Three.js, SQLite, and ReportLab.", bullet_style))
    story.append(Paragraph("&bull; <b>Economic & Municipal Impact:</b> Prevents billion-rupee subsurface infrastructure collisions, accelerates mortgage underwriting, and unlocks high-density vertical real estate revenues.", bullet_style))

    # Build the document
    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"Technical Specification PDF successfully built: {filename}")

if __name__ == "__main__":
    out_path = os.path.join(os.path.dirname(__file__), "Bhu_Aadhaar_3D_Complete_Technical_Specification.pdf")
    build_technical_pdf(out_path)
