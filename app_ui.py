import streamlit as st
import hashlib
import json
from datetime import datetime

st.set_page_config(layout="wide")

# =========================================================
# TRIPLE BOT – STRUCTURAL VALIDATION ENGINE
# Version: v1.0 (Deterministic Core Locked)
# Evaluation Build – Partner Review Mode
# =========================================================


# -----------------------------
# CORE ENGINE (LOCKED)
# -----------------------------

def validate_inputs(load, area, fc, phi, gamma):
    errors = []

    if load <= 0:
        errors.append("Axial Load must be > 0 kN")

    if area <= 0:
        errors.append("Section Area must be > 0 mm²")

    if fc <= 0:
        errors.append("Concrete strength must be > 0 MPa")

    if not (0 < phi <= 1):
        errors.append("Strength reduction factor φ must be between 0 and 1")

    if gamma < 1:
        errors.append("Load factor γ should be ≥ 1.0")

    return errors


def structural_engine(load_kN, area_mm2, fc_mpa, phi, gamma):

    Pu = gamma * load_kN
    Pn = 0.85 * fc_mpa * area_mm2 / 1000
    phi_Pn = phi * Pn

    dc_ratio = Pu / phi_Pn
    status = "PASS" if dc_ratio <= 1 else "FAIL"

    return Pu, Pn, phi_Pn, dc_ratio, status


def generate_signature(payload):
    raw = json.dumps(payload, sort_keys=True)
    return hashlib.sha256(raw.encode()).hexdigest()[:20]


# -----------------------------
# HEADER
# -----------------------------

st.title("TRIPLE BOT – Structural Validation Engine")

st.markdown("**Version:** v1.0 – Deterministic Core Locked")
st.markdown("**Execution Mode:** Local Deterministic Evaluation")
st.markdown("**Validation Scope:** Simplified Concrete Axial Compression")

st.markdown("---")

# -----------------------------
# ASSUMPTIONS
# -----------------------------

st.subheader("Model Assumptions")

st.markdown("""
- Short column behavior assumed  
- Concentric axial loading only  
- No slenderness effects included  
- No reinforcement contribution included  
- Strength reduction format (φ-based design)  
""")

st.markdown("---")

# -----------------------------
# INPUT SECTION
# -----------------------------

st.subheader("Demand Parameters")

load = st.number_input("Service Axial Load (kN)", min_value=0.0, value=1000.0)
gamma = st.number_input("Load Combination Factor γ (-)", min_value=1.0, value=1.4)

st.subheader("Resistance Parameters")

area = st.number_input("Gross Section Area (mm²)", min_value=1.0, value=300000.0)
fc = st.number_input("Concrete Compressive Strength f'c (MPa)", min_value=1.0, value=28.0)
phi = st.number_input("Strength Reduction Factor φ (-)", min_value=0.1, max_value=1.0, value=0.65)

run = st.button("Run Structural Validation")

st.markdown("---")

# -----------------------------
# EXECUTION
# -----------------------------

if run:

    errors = validate_inputs(load, area, fc, phi, gamma)

    if errors:
        st.error("Input Validation Error")
        for e in errors:
            st.write(f"- {e}")

    else:

        Pu, Pn, phi_Pn, dc_ratio, status = structural_engine(load, area, fc, phi, gamma)

        result_payload = {
            "Load": load,
            "Gamma": gamma,
            "Area": area,
            "fc": fc,
            "Phi": phi,
            "Pu": Pu,
            "Pn": Pn,
            "phiPn": phi_Pn,
            "DCR": dc_ratio,
            "Status": status
        }

        signature = generate_signature(result_payload)

        # -----------------------------
        # STRUCTURED REPORT
        # -----------------------------

        st.subheader("Validation Report")

        st.markdown("**Demand Side**")
        st.write(f"Factored Load Pu: {round(Pu,3)} kN")

        st.markdown("**Resistance Side**")
        st.write(f"Nominal Capacity Pn: {round(Pn,3)} kN")
        st.write(f"Design Capacity φPn: {round(phi_Pn,3)} kN")

        st.markdown("**Verification**")
        st.write(f"Demand/Capacity Ratio (Pu/φPn): {round(dc_ratio,4)}")

        if status == "PASS":
            st.success("Structural capacity requirement satisfied.")
        else:
            st.error("Structural capacity exceeded.")

        st.markdown("---")

        # -----------------------------
        # EXECUTION CONTROL BLOCK
        # -----------------------------

        st.subheader("Execution Control")

        st.write(f"Execution Timestamp: {datetime.utcnow()} UTC")
        st.write("Deterministic Evaluation: ENABLED")
        st.write("Core Logic State: LOCKED")

        st.markdown("---")

        st.subheader("Deterministic Execution Signature")
        st.code(signature)

        st.markdown("---")

        st.subheader("Formula Reference")

        st.markdown("""
Pn = 0.85 · f'c · Ag  
φPn = φ · Pn  
Demand/Capacity Ratio = Pu / φPn  
""")

        st.markdown("---")

        st.warning("This module represents a simplified axial validation core and is not a substitute for full structural design verification.")