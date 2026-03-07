# ============================================================
# TRIPLE BOT – BOQ GENERATOR
# CONTRACT VERSION (STABLE)
# ============================================================

def generate_boq(foundation_result):

    width = foundation_result["width"]
    length = foundation_result["length"]
    thickness = foundation_result["thickness"]

    foundation_type = foundation_result.get("foundation_type", "Square Footing")

    # ------------------------------------------------
    # CONCRETE VOLUME
    # ------------------------------------------------

    concrete_volume = width * length * thickness
    concrete_volume = round(concrete_volume, 3)

    # ------------------------------------------------
    # REINFORCEMENT ESTIMATION
    # ------------------------------------------------

    reinforcement = concrete_volume * 120
    reinforcement = round(reinforcement, 1)

    boq = {

        "foundation_type": foundation_type,

        "foundation_width": width,
        "foundation_length": length,
        "foundation_thickness": thickness,

        "concrete_volume_m3": concrete_volume,

        "reinforcement_kg": reinforcement

    }

    return boq