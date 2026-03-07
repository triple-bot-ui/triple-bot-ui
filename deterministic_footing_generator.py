# ============================================================
# TRIPLE BOT – DETERMINISTIC FOOTING GENERATOR
# V2 ADAPTIVE FOUNDATION SIZING ENGINE
# ============================================================

import math


def generate_square_footing(validation_result):

    # --------------------------------------------------------
    # INPUT
    # --------------------------------------------------------

    applied_load = validation_result["load"]
    soil_capacity = validation_result["soil_capacity"]
    required_area = validation_result["required_area"]


    # --------------------------------------------------------
    # ADAPTIVE FOOTING SEARCH
    # --------------------------------------------------------

    area = required_area

    step = 0.01

    while True:

        pressure = applied_load / area

        if pressure <= soil_capacity:
            break

        area += step


    # --------------------------------------------------------
    # CONVERT AREA TO SQUARE FOOTING
    # --------------------------------------------------------

    width = math.sqrt(area)
    width = round(width, 2)

    length = width


    # --------------------------------------------------------
    # THICKNESS DESIGN
    # --------------------------------------------------------

    thickness = width * 0.25

    thickness = round(thickness, 2)


    # --------------------------------------------------------
    # OUTPUT
    # --------------------------------------------------------

    return {

        "width": width,
        "length": length,
        "thickness": thickness,
        "area": area
    }