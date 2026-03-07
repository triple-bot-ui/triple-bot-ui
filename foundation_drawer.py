# ============================================================
# TRIPLE BOT – FOUNDATION PLAN DRAWER
# VERSION: V2 FINAL
# ============================================================

import matplotlib.pyplot as plt
import io


def draw_foundation_plan(width, length):

    fig, ax = plt.subplots()

    # Draw square foundation
    x = [0, width, width, 0, 0]
    y = [0, 0, length, length, 0]

    ax.plot(x, y, linewidth=4)

    # center lines
    ax.axvline(width / 2, linestyle="--")
    ax.axhline(length / 2, linestyle="--")

    # center point
    ax.plot(width / 2, length / 2, "ro")

    ax.set_aspect("equal")

    ax.set_xlim(-0.2, width + 0.2)
    ax.set_ylim(-0.2, length + 0.2)

    ax.axis("off")

    # ------------------------------------------------
    # convert matplotlib figure -> PNG
    # ------------------------------------------------

    buf = io.BytesIO()

    plt.savefig(buf, format="png", bbox_inches="tight")

    buf.seek(0)

    plt.close(fig)

    return buf
