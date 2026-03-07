# ============================================================
# TRIPLE BOT – FOUNDATION DESIGN ENGINE
# VERSION: V2 DEV (CONSERVATIVE ROUNDING FIX)
# ============================================================

import math


def design_foundation(validation_result):

    # --------------------------------------------------------
    # INPUT
    # --------------------------------------------------------

    required_area = validation_result["required_area"]

    # --------------------------------------------------------
    # FOUNDATION SIZE (CONSERVATIVE ROUND UP)
    # --------------------------------------------------------

    width = math.sqrt(required_area)

    # round UP to ensure actual area >= required area
    width = math.ceil(width * 100) / 100

    length = width

    thickness = 0.24

    # --------------------------------------------------------
    # RETURN
    # --------------------------------------------------------

    return {

        "width": width,

        "length": length,

        "thickness": thickness

    }
