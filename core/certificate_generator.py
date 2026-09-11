import io
import hashlib
import json
import qrcode
from PIL import Image

from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image as RLImage, KeepTogether
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

def generate_title_hash(ulpin_str, owner, lat, lon, z_range, valuation):
    """
    Computes an immutable cryptographic SHA-256 seal for the vertical parcel.
    """
    payload = f"{ulpin_str}|{owner}|{lat:.5f}|{lon:.5f}|{z_range}|{valuation}"
    return hashlib.sha256(payload.encode('utf-8')).hexdigest().upper()

def generate_qr_code_image(data_dict):
    """
    Generates a high-resolution QR code image representing the digital title.
    """
    qr_content = json.dumps(data_dict, sort_keys=True)
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_M,
        box_size=8,
        border=2,
    )
    qr.add_data(qr_content)
    qr.make(fit=True)
    img = qr.make_image(fill_color="#0f172a", back_color="#ffffff")
    
    img_byte_arr = io.BytesIO()
    img.save(img_byte_arr, format='PNG')
    img_byte_arr.seek(0)
    return img_byte_arr

def generate_bhu_aadhaar_pdf(prop, floor_dict, ulpin_str):
    """
    Generates an official Government of India 3D ULPIN Generator Property Title Certificate (PDF).
    """
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=letter,
        rightMargin=40,
        leftMargin=40,
        topMargin=40,
        bottomMargin=40
    )

    styles = getSampleStyleSheet()
    
    # Custom styles
    header_title_style = ParagraphStyle(
        'GovHeaderTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=15,
        leading=18,
        alignment=1, # Center
        textColor=colors.HexColor('#0f172a')
    )

    header_sub_style = ParagraphStyle(
        'GovHeaderSub',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=11,
        leading=14,
        alignment=1,
        textColor=colors.HexColor('#0284c7')
    )

    label_style = ParagraphStyle(
        'CellLabel',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=9,
        leading=11,
        textColor=colors.HexColor('#475569')
    )

    val_style = ParagraphStyle(
        'CellValue',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9,
        leading=12,
        textColor=colors.HexColor('#0f172a')
    )

    ulpin_style = ParagraphStyle(
        'UlpinHero',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=12,
        leading=14,
        textColor=colors.HexColor('#0369a1')
    )

    hash_style = ParagraphStyle(
        'HashValue',
        parent=styles['Normal'],
        fontName='Courier',
        fontSize=7,
        leading=9,
        textColor=colors.HexColor('#334155')
    )

    story = []

    # 1. Government Header Banner
    story.append(Paragraph("GOVERNMENT OF INDIA", header_title_style))
    story.append(Paragraph("MINISTRY OF RURAL DEVELOPMENT &bull; DEPARTMENT OF LAND RESOURCES", ParagraphStyle('dept', alignment=1, fontSize=8, textColor=colors.HexColor('#64748b'))))
    story.append(Spacer(1, 4))
    story.append(Paragraph("3D ULPIN GENERATOR SPATIAL PROPERTY CERTIFICATE", header_sub_style))
    story.append(Paragraph("Issued under National Land Records Modernization Programme (DILRMP-3D Cadastre Standard)", ParagraphStyle('std', alignment=1, fontSize=7, textColor=colors.HexColor('#64748b'))))
    story.append(Spacer(1, 14))

    # 2. Cryptographic Security Hash & QR Data
    z_range_str = f"{floor_dict['z_start']}m to {floor_dict['z_end']}m"
    effective_owner = floor_dict.get('owner') or prop.get('owner', 'Government Cadastral Registry')
    prop_lat = float(prop.get('lat', 0.0))
    prop_lon = float(prop.get('lon', 0.0))
    prop_val = float(prop.get('valuation_cr', 0.0))
    prop_plot = int(prop.get('property_id') or prop.get('id', 0))
    prop_name = str(prop.get('name', 'Urban Complex'))
    prop_city = str(prop.get('city', 'National Jurisdiction'))
    prop_state = str(prop.get('state', 'India'))
    prop_state_code = str(prop.get('state_code', '00'))
    prop_base_elev = str(prop.get('base_elevation', '0.0'))

    sha_hash = generate_title_hash(
        ulpin_str,
        effective_owner,
        prop_lat,
        prop_lon,
        z_range_str,
        prop_val
    )

    qr_payload = {
        "portal": "https://dilrmp.gov.in/3d-ulpin-generator",
        "3d_ulpin": ulpin_str,
        "owner": effective_owner,
        "plot": prop_plot,
        "level": floor_dict['floor_number'],
        "z_range": z_range_str,
        "hash_sig": sha_hash[:16]
    }
    qr_img_bytes = generate_qr_code_image(qr_payload)
    rl_qr_image = RLImage(qr_img_bytes, width=1.4*inch, height=1.4*inch)

    # 3. Main Certificate Data Table
    floor_num = floor_dict['floor_number']
    custom_name = floor_dict.get('floor_name')
    if floor_num < 0:
        level_name = custom_name if custom_name else f"Basement {abs(floor_num):02d} (Subsurface Infrastructure)"
        tenure_type = "Subsurface Air/Ground Easement Right"
    else:
        level_name = custom_name if custom_name else f"Floor {floor_num:02d} (Superstructure)"
        tenure_type = "Freehold Vertical Airspace Title"

    table_data = [
        [
            Paragraph("3D ULPIN Generator (ULPIN):", label_style),
            Paragraph(f"<b>{ulpin_str}</b>", ulpin_style),
            rl_qr_image
        ],
        [
            Paragraph("Registered Title Holder:", label_style),
            Paragraph(f"<b>{effective_owner}</b>", val_style),
            ""
        ],
        [
            Paragraph("Property / Complex:", label_style),
            Paragraph(f"{prop_name}", val_style),
            ""
        ],
        [
            Paragraph("Jurisdiction & State:", label_style),
            Paragraph(f"{prop_city}, {prop_state} (LGD: {prop_state_code})", val_style),
            ""
        ],
        [
            Paragraph("Cadastral Plot Ref:", label_style),
            Paragraph(f"Survey Plot #{prop_plot} &bull; Zone: {prop.get('zone', 'Urban Commercial')}", val_style),
            ""
        ],
        [
            Paragraph("Vertical Stratification:", label_style),
            Paragraph(f"<b>{level_name}</b>", val_style),
            ""
        ],
        [
            Paragraph("Absolute Elevation (Z):", label_style),
            Paragraph(f"<b>{z_range_str}</b> (Base Ground: {prop_base_elev}m)", val_style),
            ""
        ],
        [
            Paragraph("Legal Tenure Type:", label_style),
            Paragraph(f"{tenure_type}", val_style),
            ""
        ],
        [
            Paragraph("Cadastral Valuation:", label_style),
            Paragraph(f"₹ {prop.get('valuation_cr', 0):.2f} Crores", val_style),
            ""
        ]
    ]

    t = Table(table_data, colWidths=[1.8*inch, 3.8*inch, 1.6*inch])
    t.setStyle(TableStyle([
        ('SPAN', (2, 0), (2, 4)),
        ('ALIGN', (2, 0), (2, 4), 'CENTER'),
        ('VALIGN', (2, 0), (2, 4), 'MIDDLE'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.HexColor('#0f172a')),
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#f8fafc')),
        ('BOX', (0, 0), (-1, -1), 1, colors.HexColor('#cbd5e1')),
        ('INNERGRID', (0, 0), (1, -1), 0.5, colors.HexColor('#e2e8f0')),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
    ]))
    story.append(t)
    story.append(Spacer(1, 14))

    # 4. Cryptographic Seal Box
    audit_table_data = [
        [
            Paragraph("Cryptographic Title Hash (SHA-256):", label_style),
            Paragraph(f"<code>{sha_hash}</code>", hash_style)
        ],
        [
            Paragraph("Digital Signature & Audit:", label_style),
            Paragraph("Digitally Authenticated by 3D Cadastral Registrar Engine &bull; Timestamped Immutable Record", val_style)
        ]
    ]
    t_audit = Table(audit_table_data, colWidths=[2.2*inch, 5.0*inch])
    t_audit.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#eff6ff')),
        ('BOX', (0, 0), (-1, -1), 1, colors.HexColor('#93c5fd')),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#bfdbfe')),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
    ]))
    story.append(t_audit)
    story.append(Spacer(1, 14))

    # 5. Statutory Footnote & Disclaimer
    footer_text = (
        "<b>STATUTORY NOTICE:</b> This 3D ULPIN Generator Certificate delineates vertical spatial boundaries "
        "pursuant to ISO 19152 (Land Administration Domain Model). Possession or conveyance of this vertical parcel "
        "must be registered in accordance with the Registration Act, 1908 and State Real Estate Regulatory Authority (RERA) norms."
    )
    story.append(Paragraph(footer_text, ParagraphStyle('notice', fontSize=6.5, leading=8.5, textColor=colors.HexColor('#64748b'))))

    doc.build(story)
    buffer.seek(0)
    return buffer.getvalue()

# Alias for backward compatibility & modern naming
generate_3d_ulpin_pdf = generate_bhu_aadhaar_pdf
