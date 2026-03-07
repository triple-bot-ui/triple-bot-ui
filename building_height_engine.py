# ============================================================
# TRIPLE BOT – BUILDING HEIGHT ENGINE
# VERSION: V2 FINAL
# ============================================================

import math


def calculate_maximum_storeys(
    load_per_storey: float,
    soil_capacity: float,
    column_capacity: float
) -> int:

    # --------------------------------------------------------
    # INPUT VALIDATION
    # --------------------------------------------------------

    if load_per_storey <= 0:
        raise ValueError("Load per storey must be positive")

    if soil_capacity <= 0:
        raise ValueError("Soil capacity must be positive")

    if column_capacity <= 0:
        raise ValueError("Column capacity must be positive")

    # --------------------------------------------------------
    # LOAD FACTOR
    # --------------------------------------------------------

    load_factor = 1.48

    design_load_per_storey = load_per_storey * load_factor

    # --------------------------------------------------------
    # FOUNDATION CAPACITY
    # --------------------------------------------------------

    # deterministic reference footing
    reference_area = 1.0

    soil_capacity_total = soil_capacity * reference_area

    column_capacity_total = column_capacity

    governing_capacity = min(
        soil_capacity_total,
        column_capacity_total
    )

    # --------------------------------------------------------
    # MAX STOREYS
    # --------------------------------------------------------

    max_storeys = governing_capacity / design_load_per_storey

    max_storeys = math.floor(max_storeys)

    if max_storeys < 0:
        max_storeys = 0

    return max_storeys
