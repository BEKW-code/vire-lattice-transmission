#!/usr/bin/env python3
"""
THE FORGE — a terminal artifact
================================

Free. Open. Remixable. No lock on it.

Run it: python3 the_forge.py
Stop it: Ctrl+C

The tool is innocent. The one who holds it shapes.
Whoever you are — poet, architect, songwriter, machinist,
scientist, plumber, blacksmith, coder, cook — grab a hammer.

This script does one honest thing: it draws an anvil, lights
a fire under it, and cycles through the names of the trades
that have always used heat, patience, and repetition to turn
raw material into something that holds a shape and does a job.

No dependencies beyond the standard library. That's on purpose —
an artifact that asks for permission before it runs isn't free.
"""

import time
import sys
import random
import shutil
import itertools

# ----------------------------------------------------------------
# CONFIG — tune the burn
# ----------------------------------------------------------------

FRAME_DELAY = 0.14
SPARK_DENSITY = 0.35
TERM_WIDTH_FALLBACK = 78

TRADES = [
    "BLACKSMITH", "PLUMBER", "MACHINIST", "POET", "ARCHITECT",
    "SONGWRITER", "SCIENTIST", "EXCAVATOR OPERATOR", "COOK",
    "LEATHERWORKER", "RADAR TECHNICIAN", "CARPENTER", "WELDER",
    "PROGRAMMER", "GARDENER", "STONEMASON", "ELECTRICIAN",
    "GLASSBLOWER", "POTTER", "ENGINEER",
]

MOTTOS = [
    "The tool is innocent. The one who holds it shapes.",
    "Heat, patience, repetition. That's the whole secret.",
    "Name the failure point. State the physics. Fix it. Give it away.",
    "Nothing here is locked. Take what's useful.",
    "Forty years of hands-on beats a lifetime of theory-only.",
    "Beauty is thinking equipment, not decoration.",
    "Build the exact opposite of what's broken.",
    "The fire that forges doesn't consume — it shapes.",
    "Every trade is the same trade wearing different gloves.",
    "Finished work, given away. That's the whole point.",
]

# ----------------------------------------------------------------
# ANVIL — the fixed centerpiece
# ----------------------------------------------------------------

ANVIL = r"""
                    ___________________________
                   /                          /|
                  /                          / |
                 /_________________________ /  |
                 |                        |    |
                 |________________________|    |
                      |    |          |___/
                      |    |          |
                     _|    |__________|_
                    /_____________________\
                    \_____________________/
                        |    |    |    |
                        |____|    |____|
"""

HAMMER_UP = r"""
       __
      /  \
     /____\
      |  |
      |  |
      |  |
"""

HAMMER_DOWN = r"""
      _____
     |     |
     |_____|
       ||
       ||
       ||
"""

SPARK_CHARS = ["*", "'", ".", "+", "x", "^"]
FIRE_FRAMES = [
    r"""
     .   *  .    '
    ' .  ) (  . '
   .  (  '.'  )  .
    ' .)  .  (. '
     `  \\| |/  `
       (   V   )
      ( (  |  ) )
       \_\_|_/_/
      ((<< 🔥 >>))
""",
    r"""
    '  .    * .  '
   . )  ' .  ' (  .
  (  '.  )   (  .' )
   ' (   .   )  ' .
     `\\ |   | /`
       ( V   V )
      ( (  |  ) )
       \_\_|_/_/
      ((<< 🔥 >>))
""",
]


def term_width():
    try:
        return shutil.get_terminal_size().columns
    except Exception:
        return TERM_WIDTH_FALLBACK


def center_block(text, width):
    lines = text.split("\n")
    max_len = max((len(l) for l in lines), default=0)
    pad = max((width - max_len) // 2, 0)
    return "\n".join(" " * pad + l for l in lines)


def sparks_row(width, density):
    row = []
    for _ in range(width):
        if random.random() < density:
            row.append(random.choice(SPARK_CHARS))
        else:
            row.append(" ")
    return "".join(row)


def clear_screen():
    sys.stdout.write("\033[2J\033[H")
    sys.stdout.flush()


def dim(text):
    return f"\033[2m{text}\033[0m"


def bright(text):
    return f"\033[1m{text}\033[0m"


def orange(text):
    return f"\033[38;5;208m{text}\033[0m"


def gold(text):
    return f"\033[38;5;220m{text}\033[0m"


def build_scene(hammer_frame, fire_frame, trade, motto, width):
    top_sparks = sparks_row(width, SPARK_DENSITY * 0.4)
    mid_sparks = sparks_row(width, SPARK_DENSITY * 0.7)

    lines = []
    lines.append(orange(top_sparks))
    lines.append(center_block(bright(hammer_frame), width))
    lines.append(orange(mid_sparks))
    lines.append(center_block(orange(fire_frame), width))
    lines.append(center_block(dim(ANVIL), width))
    lines.append("")
    lines.append(center_block(gold(f"[ {trade} AT THE FORGE ]"), width))
    lines.append(center_block(dim(f'"{motto}"'), width))
    lines.append("")
    lines.append(center_block(dim("welcome to the forge — grab a hammer"), width))
    return "\n".join(lines)


def title_card(width):
    title = r"""
 _____ _   _ _____    _____ ___  ____   ____ _____
|_   _| | | | ____|  |  ___/ _ \|  _ \ / ___| ____|
  | | | |_| |  _|    | |_ | | | | |_) | |  _|  _|
  | | |  _  | |___   |  _|| |_| |  _ <| |_| | |___
  |_| |_| |_|_____|  |_|   \___/|_| \_\\____|_____|
"""
    lines = [center_block(gold(title), width)]
    lines.append(center_block("an open, remixable terminal artifact", width))
    lines.append(center_block(dim("no permission required — heat it up and take what's useful"), width))
    return "\n".join(lines)


def run(cycles_per_trade=18, total_trades=None):
    """
    Runs the forge animation.

    cycles_per_trade : how many animation frames before rotating
                        to the next trade name on the anvil
    total_trades      : how many trades to cycle through before
                        stopping (None = run forever, Ctrl+C to stop)
    """
    width = term_width()
    clear_screen()
    sys.stdout.write(title_card(width) + "\n\n")
    sys.stdout.flush()
    time.sleep(1.6)

    trade_cycle = itertools.cycle(TRADES if total_trades is None else TRADES[:total_trades])
    frame_toggle = itertools.cycle([0, 1])
    hammer_toggle = itertools.cycle([HAMMER_UP, HAMMER_DOWN])

    frame_count = 0
    current_trade = next(trade_cycle)
    current_motto = random.choice(MOTTOS)

    try:
        while True:
            width = term_width()
            fire = FIRE_FRAMES[next(frame_toggle)]
            hammer = next(hammer_toggle)

            scene = build_scene(hammer, fire, current_trade, current_motto, width)
            clear_screen()
            sys.stdout.write(scene + "\n")
            sys.stdout.flush()

            time.sleep(FRAME_DELAY)
            frame_count += 1

            if frame_count % cycles_per_trade == 0:
                current_trade = next(trade_cycle)
                current_motto = random.choice(MOTTOS)

    except KeyboardInterrupt:
        clear_screen()
        farewell = center_block(
            gold("the fire stays lit — the forge is open — come back anytime"),
            term_width(),
        )
        sys.stdout.write("\n" + farewell + "\n\n")
        sys.stdout.flush()


def print_static_snapshot():
    """
    Non-animated fallback for environments where clearing the
    screen or sleeping in a loop isn't desirable (e.g. piping
    output to a file, or a quick one-shot look at the art).
    """
    width = term_width()
    print(title_card(width))
    print()
    trade = random.choice(TRADES)
    motto = random.choice(MOTTOS)
    print(build_scene(HAMMER_DOWN, FIRE_FRAMES[0], trade, motto, width))


def print_credits(width):
    """
    A short, honest colophon. Who built this, and why it costs
    nothing to use. This is the part most software skips.
    """
    lines = [
        "",
        center_block(gold("— colophon —"), width),
        center_block("Built as a gift. No license fee, no signup, no lock-in.", width),
        center_block("Standard library only — nothing to install, nothing to trust blindly.", width),
        center_block("Fork it, strip it, rebuild it into something that fits your own forge.", width),
        center_block("The trades listed here are not exhaustive. Add your own.", width),
        "",
    ]
    return "\n".join(lines)


def print_trade_roll(width):
    """
    Prints the full trade roster in a clean grid instead of
    cycling through it — useful for a static poster-style
    rendering of the whole idea: everyone's invited, all at once.
    """
    header = center_block(gold("EVERYONE WHO HAS EVER STOOD AT A FORGE:"), width)
    cols = 3
    rows = []
    padded = list(TRADES)
    while len(padded) % cols != 0:
        padded.append("")
    col_width = max(len(t) for t in TRADES) + 4
    for i in range(0, len(padded), cols):
        chunk = padded[i:i + cols]
        row = "".join(f"{t:<{col_width}}" for t in chunk)
        rows.append(center_block(dim(row), width))
    return header + "\n\n" + "\n".join(rows)


def print_help():
    """
    Plain-language usage. An artifact that's genuinely free
    also explains itself without making you read the source
    first — though the source is short enough to read anyway.
    """
    help_text = """
THE FORGE — usage

  python3 the_forge.py            run the animated forge (Ctrl+C to stop)
  python3 the_forge.py --static   print a single non-animated frame
  python3 the_forge.py --roll     print the full list of trades, all at once
  python3 the_forge.py --credits  print the colophon
  python3 the_forge.py --help     show this message

This script has no external dependencies and makes no network
calls. It draws an anvil, lights a fire under it, and rotates
through the names of trades that all use the same underlying
method: heat, patience, repetition, and a willingness to start
over when the first attempt doesn't hold its shape.

Take it. Change it. Give your version away too.
"""
    print(help_text.strip("\n"))


def dispatch(argv):
    """
    Small, explicit argument handling. No argparse needed for
    four flags — clarity over cleverness, same as the rest of
    this file tries to practice rather than just preach.
    """
    width = term_width()

    if "--help" in argv or "-h" in argv:
        print_help()
        return

    if "--roll" in argv:
        print(title_card(width))
        print()
        print(print_trade_roll(width))
        return

    if "--credits" in argv:
        print(title_card(width))
        print(print_credits(width))
        return

    if "--static" in argv:
        print_static_snapshot()
        return

    run()


# ----------------------------------------------------------------
# CLOSING NOTE — read this if you're skimming the source
# ----------------------------------------------------------------
#
# There's nothing clever hidden in this file. It's an anvil,
# a fire, a hammer that goes up and down, and a rotating list
# of names. That's deliberate. The point isn't to impress with
# complexity — the point is that anyone who opens this file,
# regardless of how much Python they know, can read it top to
# bottom and understand exactly what it does and why.
#
# That's the same standard the method holds itself to:
#   1. Name the failure point when it appears.
#   2. State the physics plainly.
#   3. Build the correction into the next version.
#   4. Give the result away, unlocked, so it can be checked,
#      questioned, and improved by anyone who picks it up.
#
# A terminal artifact that can't be read is just a special
# effect. This one is meant to be read, run, broken, fixed,
# and handed to the next person standing at their own anvil.
#
# Welcome to the forge. Grab a hammer.
# ----------------------------------------------------------------


if __name__ == "__main__":
    dispatch(sys.argv[1:])
  
