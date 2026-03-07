# ============================================================
# TRIPLE BOT – STRUCTURAL VALIDATION SYSTEM UI
# VERSION: V2.1 STABLE
# ============================================================

import streamlit as st
import datetime

from validation_engine import validate_structure
from foundation_design_engine import design_foundation
from boq_generator import generate_boq
from foundation_drawer import draw_foundation_plan
from report_generator import generate_engineering_report
from building_height_engine import calculate_maximum_storeys


# ------------------------------------------------------------
# PAGE CONFIG
# ------------------------------------------------------------

st.set_page_config(
    page_title="TRIPLE BOT",
    layout="wide"
)

st.title("TRIPLE BOT – Structural Validation System")

st.success("Core Engine Loaded")


# ------------------------------------------------------------
# ENGINEERING STANDARD
# ------------------------------------------------------------

engineering_standard = """
Engineering Standard Reference

• Structural Logic: Deterministic Load vs Soil Bearing Validation
• Conceptual Footing Verification inspired by ACI 318
• Load Combination inspired by ASCE structural practice
• Deterministic Structural Engine: Triple Bot Core
"""


# ------------------------------------------------------------
# DESIGN INPUT
# ------------------------------------------------------------

st.header("Design Input")

foundation_area = st.number_input(
    "Foundation Area (m²)",
    min_value=0.5,
    max_value=100.0,
    value=4.0,
    step=0.1
)

column_capacity = st.number_input(
    "Column Capacity (kN)",
    min_value=50.0,
    max_value=5000.0,
    value=500.0,
    step=10.0
)

load_per_storey = st.number_input(
    "Load per Storey (kN)",
    min_value=10.0,
    max_value=1000.0,
    value=120.0,
    step=10.0
)

soil_capacity = st.number_input(
    "Soil Bearing Capacity (kN/m²)",
    min_value=50.0,
    max_value=1000.0,
    value=200.0,
    step=10.0
)

soil_class = st.selectbox(
    "Soil Class",
    ["A", "B", "C", "D"]
)


# ------------------------------------------------------------
# RUN VALIDATION
# ------------------------------------------------------------

if st.button("Run Structural Validation"):

    execution_id = "TB-" + datetime.datetime.now().strftime("%Y%m%d-%H%M%S")

    # --------------------------------------------------------
    # STRUCTURAL VALIDATION
    # --------------------------------------------------------

    validation = validate_structure(
        load_per_storey=load_per_storey,
        column_capacity=column_capacity,
        soil_capacity=soil_capacity
    )

    # --------------------------------------------------------
    # FOUNDATION DESIGN
    # --------------------------------------------------------

    foundation = design_foundation(validation)

    # --------------------------------------------------------
    # BOQ
    # --------------------------------------------------------

    boq = generate_boq(foundation)

    # --------------------------------------------------------
    # MAXIMUM STOREYS
    # --------------------------------------------------------

    max_storeys = calculate_maximum_storeys(
        load_per_storey,
        soil_capacity,
        column_capacity
    )

    # --------------------------------------------------------
    # REPORT
    # --------------------------------------------------------

    report_file, signature = generate_engineering_report(
        validation_result=validation,
        foundation_result=foundation,
        boq_result=boq
    )

    # ========================================================
    # STRUCTURAL RESULT
    # ========================================================

    st.header("Structural Validation Result")

    if validation["status"] == "SAFE":
        st.success("Status: SAFE")
    else:
        st.error("Status: FAIL")

    utilization = validation["utilization_ratio"]

    st.write("Governing Mode:", validation["governing_mode"])
    st.write("Utilization:", utilization)
    st.write("Structural Margin:", validation["structural_margin"])
    st.write("Failure Zone:", validation["failure_zone"])

    # --------------------------------------------------------
    # SAFETY ENVELOPE (FIXED LOGIC)
    # --------------------------------------------------------

    if validation["status"] == "SAFE":
        safety_zone = "SAFE"
        st.success("Safety Envelope: SAFE")
    else:
        safety_zone = "FAIL"
        st.error("Safety Envelope: FAIL")

    # ========================================================
    # FOUNDATION PLAN
    # ========================================================

    st.header("Foundation Plan")

    width = foundation["width"]
    length = foundation["length"]

    st.subheader(f"Foundation Plan {width}m × {length}m")

    foundation_image = draw_foundation_plan(width, length)

    st.image(foundation_image)

    # ========================================================
    # BILL OF QUANTITIES
    # ========================================================

    st.header("Bill of Quantities")

    st.write("Foundation Type: Square Footing")
    st.write("Width (m):", foundation["width"])
    st.write("Length (m):", foundation["length"])
    st.write("Thickness (m):", foundation["thickness"])

    st.write("Concrete Volume (m³):", boq["concrete_volume_m3"])
    st.write("Reinforcement (kg):", boq["reinforcement_kg"])

    # ========================================================
    # MAXIMUM STOREYS
    # ========================================================

    st.header("Maximum Safe Building Height")

    st.success(f"Maximum Safe Storeys: {max_storeys}")

    # ========================================================
    # ENGINEERING STANDARD
    # ========================================================

    st.header("Engineering Standard")

    st.info(engineering_standard)

    # ========================================================
    # ENGINEERING REPORT
    # ========================================================

    st.header("Engineering Report")

    with open(report_file, "rb") as file:

        st.download_button(
            label="Download Engineering Report (PDF)",
            data=file,
            file_name="engineering_report.pdf"
        )

    # ========================================================
    # SIGNATURE
    # ========================================================

    st.header("Deterministic Signature")

    st.code(signature)

    # ========================================================
    # TRACEABILITY
    # ========================================================

    st.header("Execution Traceability")

    st.write("Execution ID:", execution_id)
    st.write("Engine Version: Triple Bot V2.1 STABLE")

    st.caption("Triple Bot System – Deterministic Structural Validation")