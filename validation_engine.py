# ============================================================
# TRIPLE BOT – STRUCTURAL VALIDATION ENGINE
# VERSION: V2 DEV (FINAL LOGIC FIX)
# ============================================================

import math


def validate_structure(
    load_per_storey: float,
    column_capacity: float,
    soil_capacity: float
) -> dict:

    # --------------------------------------------------------
    # INPUT VALIDATION
    # --------------------------------------------------------

    if load_per_storey <= 0:
        raise ValueError("Load per storey must be positive")

    if column_capacity <= 0:
        raise ValueError("Column capacity must be positive")

    if soil_capacity <= 0:
        raise ValueError("Soil capacity must be positive")

    # --------------------------------------------------------
    # LOAD FACTOR
    # --------------------------------------------------------

    load_factor = 1.48

    design_load = load_per_storey * load_factor

    # --------------------------------------------------------
    # REQUIRED FOUNDATION AREA
    # --------------------------------------------------------

    required_area = design_load / soil_capacity

    # --------------------------------------------------------
    # SOIL CHECK (use required area directly)
    # --------------------------------------------------------

    soil_pressure = design_load / required_area

    soil_utilization = soil_pressure / soil_capacity

    # --------------------------------------------------------
    # COLUMN CHECK
    # --------------------------------------------------------

    column_utilization = load_per_storey / column_capacity

    # --------------------------------------------------------
    # GOVERNING MODE
    # --------------------------------------------------------

    if soil_utilization > column_utilization:

        governing_mode = "SOIL"
        utilization = soil_utilization

    else:

        governing_mode = "COLUMN"
        utilization = column_utilization

    # --------------------------------------------------------
    # STATUS
    # --------------------------------------------------------

    status = "SAFE" if utilization <= 1 else "FAIL"

    structural_margin = 1 - utilization

    if abs(structural_margin) < 0.0001:
        structural_margin = 0.0

    # --------------------------------------------------------
    # RETURN PACKAGE
    # --------------------------------------------------------

    return {

        "status": status,

        "governing_mode": governing_mode,

        "governing_ratio": round(utilization, 3),

        "utilization_ratio": round(utilization, 3),

        "structural_margin": round(structural_margin, 3),

        "failure_zone": "SAFE_ZONE" if status == "SAFE" else "FAIL_ZONE",

        "load": round(design_load, 2),

        "load_factor": load_factor,

        "soil_capacity": soil_capacity,

        "required_area": round(required_area, 3)
    }