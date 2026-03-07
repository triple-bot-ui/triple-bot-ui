# ============================================================
# TRIPLE BOT – ENGINEERING REPORT GENERATOR
# VERSION: V2 DEV (RESTORE 15 SECTIONS)
# ============================================================

from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import A4
import datetime
import hashlib


def _v(d, key, default=0):
    return d.get(key, default)


def generate_engineering_report(validation_result, foundation_result, boq_result):

    styles = getSampleStyleSheet()

    report_file = "engineering_report.pdf"

    now = datetime.datetime.now()

    elements = []

    # --------------------------------------------------------
    # SAFE DATA EXTRACTION
    # --------------------------------------------------------

    status = _v(validation_result, "status")
    governing_mode = _v(validation_result, "governing_mode")
    utilization = _v(validation_result, "utilization_ratio")
    margin = _v(validation_result, "structural_margin")
    failure_zone = _v(validation_result, "failure_zone")

    design_load = _v(validation_result, "load")
    load_factor = _v(validation_result, "load_factor")
    soil_capacity = _v(validation_result, "soil_capacity")
    required_area = _v(validation_result, "required_area")

    width = _v(foundation_result, "width")
    length = _v(foundation_result, "length")
    thickness = _v(foundation_result, "thickness")

    concrete = _v(boq_result, "concrete_volume_m3")
    steel = _v(boq_result, "reinforcement_kg")

    foundation_area = width * length if width and length else 1
    soil_pressure = design_load / foundation_area if foundation_area else 0
    soil_utilization = soil_pressure / soil_capacity if soil_capacity else 0

    # --------------------------------------------------------
    # REPORT TITLE
    # --------------------------------------------------------

    elements.append(Paragraph("TRIPLE BOT – Structural Validation Report", styles["Title"]))
    elements.append(Spacer(1,20))

    # 1
    elements.append(Paragraph("1. Project Identification", styles["Heading3"]))
    elements.append(Paragraph(f"Generated: {now}", styles["Normal"]))
    elements.append(Paragraph("Engine Version: Triple Bot V2 FINAL", styles["Normal"]))
    elements.append(Spacer(1,10))

    # 2
    elements.append(Paragraph("2. Design Input", styles["Heading3"]))
    elements.append(Paragraph(f"Design Load: {design_load} kN", styles["Normal"]))
    elements.append(Paragraph(f"Soil Capacity: {soil_capacity} kN/m²", styles["Normal"]))
    elements.append(Spacer(1,10))

    # 3
    elements.append(Paragraph("3. Structural Validation Result", styles["Heading3"]))
    elements.append(Paragraph(f"Status: {status}", styles["Normal"]))
    elements.append(Paragraph(f"Utilization: {utilization}", styles["Normal"]))
    elements.append(Paragraph(f"Structural Margin: {margin}", styles["Normal"]))
    elements.append(Spacer(1,10))

    # 4
    elements.append(Paragraph("4. Governing Failure Mode", styles["Heading3"]))
    elements.append(Paragraph(f"Governing Mode: {governing_mode}", styles["Normal"]))
    elements.append(Paragraph(f"Failure Zone: {failure_zone}", styles["Normal"]))
    elements.append(Spacer(1,10))

    # 5
    elements.append(Paragraph("5. Structural Calculation", styles["Heading3"]))
    elements.append(Paragraph(f"Load Factor: {load_factor}", styles["Normal"]))
    elements.append(Paragraph(f"Required Area: {required_area} m²", styles["Normal"]))
    elements.append(Spacer(1,10))

    # 6
    elements.append(Paragraph("6. Soil Bearing Verification", styles["Heading3"]))
    elements.append(Paragraph(f"Soil Pressure: {round(soil_pressure,2)} kN/m²", styles["Normal"]))
    elements.append(Paragraph(f"Soil Capacity: {soil_capacity} kN/m²", styles["Normal"]))
    elements.append(Spacer(1,10))

    # 7
    elements.append(Paragraph("7. Column Capacity Verification", styles["Heading3"]))
    elements.append(Paragraph("Column check performed in deterministic engine.", styles["Normal"]))
    elements.append(Spacer(1,10))

    # 8
    elements.append(Paragraph("8. Foundation Design", styles["Heading3"]))
    elements.append(Paragraph(f"Width: {width} m", styles["Normal"]))
    elements.append(Paragraph(f"Length: {length} m", styles["Normal"]))
    elements.append(Paragraph(f"Thickness: {thickness} m", styles["Normal"]))
    elements.append(Spacer(1,10))

    # 9
    elements.append(Paragraph("9. Bill of Quantities", styles["Heading3"]))
    elements.append(Paragraph(f"Concrete Volume: {concrete} m³", styles["Normal"]))
    elements.append(Paragraph(f"Reinforcement Steel: {steel} kg", styles["Normal"]))
    elements.append(Spacer(1,10))

    # 10
    elements.append(Paragraph("10. Utilization Breakdown", styles["Heading3"]))
    elements.append(Paragraph(f"Soil Utilization: {round(soil_utilization,3)}", styles["Normal"]))
    elements.append(Spacer(1,10))

    # 11
    elements.append(Paragraph("11. Structural Safety Envelope", styles["Heading3"]))
    elements.append(Paragraph("SAFE if utilization ≤ 1.0", styles["Normal"]))
    elements.append(Spacer(1,10))

    # 12
    elements.append(Paragraph("12. Engineering Note", styles["Heading3"]))

    if status == "SAFE":
        note = "Design is within soil bearing capacity."
    else:
        exceed = round((soil_pressure - soil_capacity) / soil_capacity * 100,2)
        note = f"Soil bearing exceeded by {exceed}%."

    elements.append(Paragraph(note, styles["Normal"]))
    elements.append(Spacer(1,10))

    # 13
    elements.append(Paragraph("13. Deterministic Signature", styles["Heading3"]))

    signature_input = str(validation_result) + str(foundation_result) + str(boq_result)
    signature = hashlib.sha256(signature_input.encode()).hexdigest()

    elements.append(Paragraph(f"Signature: {signature}", styles["Normal"]))
    elements.append(Spacer(1,10))

    # 14
    elements.append(Paragraph("14. System Traceability", styles["Heading3"]))
    elements.append(Paragraph("System: Triple Bot Deterministic Engine", styles["Normal"]))
    elements.append(Spacer(1,10))

    # 15
    elements.append(Paragraph("15. Certification Statement", styles["Heading3"]))
    elements.append(Paragraph("Results must be verified by licensed engineers.", styles["Normal"]))

    doc = SimpleDocTemplate(report_file, pagesize=A4)
    doc.build(elements)

    return report_file, signature
