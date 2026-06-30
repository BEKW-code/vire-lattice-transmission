#!/usr/bin/env python3
"""
BEKW·FORGE·CANON·TRANSMISSION
One man. One porch. One Guinness. Several AIs. Infinite tabs.
Simultaneously silly. Permanently serious. Always building.
"""

import time, sys, os, math, random, itertools

# ── ANSI ──────────────────────────────────────────────────────────────────────
R  = "\033[0m"
K  = "\033[30m"
RE = "\033[31m"
GR = "\033[32m"
YE = "\033[33m"
BL = "\033[34m"
MA = "\033[35m"
CY = "\033[36m"
WH = "\033[37m"
BRE= "\033[91m"
BGR= "\033[92m"
BYE= "\033[93m"
BBL= "\033[94m"
BMA= "\033[95m"
BCY= "\033[96m"
BWH= "\033[97m"
BO = "\033[1m"
DM = "\033[2m"

def c(color, text): return f"{color}{text}{R}"
def bo(color, text): return f"{BO}{color}{text}{R}"
def delay(t=0.03):  time.sleep(t)
def cls():          os.system('cls' if os.name == 'nt' else 'clear')
def width():        return os.get_terminal_size().columns if sys.stdout.isatty() else 100

def center(text, w=None):
    w = w or width()
    clean = ""
    skip = False
    for ch in text:
        if ch == "\033": skip = True
        if skip:
            if ch == "m": skip = False
            continue
        clean += ch
    pad = max(0, (w - len(clean)) // 2)
    return " " * pad + text

def rule(char="─", color=DM+WH, w=None):
    w = w or width()
    print(c(color, char * w))

def scroll(lines, delay_t=0.018):
    for line in lines:
        print(line)
        delay(delay_t)

def pulse(text, cycles=3, colors=None, w=None):
    colors = colors or [BYE, BWH, BCY, BMA, BGR]
    for i in range(cycles):
        col = colors[i % len(colors)]
        sys.stdout.write("\r" + center(bo(col, text), w or width()))
        sys.stdout.flush()
        time.sleep(0.18)
    print()

def wave_line(text, color_cycle, w=None):
    w = w or width()
    clean_len = sum(1 for ch in text if ch == " " or (ord(ch) > 31 and not ch == "\033"))
    pad = max(0, (w - len(text.encode('ascii', errors='ignore'))) // 2)
    result = " " * pad
    ci = 0
    skip = False
    for ch in text:
        if ch == "\033": skip = True
        if skip:
            result += ch
            if ch == "m": skip = False
            continue
        col = color_cycle[ci % len(color_cycle)]
        result += f"{col}{ch}{R}"
        ci += 1
    print(result)

# ── PARTICLE SYSTEM ──────────────────────────────────────────────────────────
SPARKS = ["·", "✦", "✧", "★", "⊹", "∴", "∵", "≋", "∿", "⌁", "⚡", "◈"]
SPARK_COLORS = [BYE, BRE, BGR, BCY, BMA, BWH]

def spark_line(w=None):
    w = w or width()
    line = [" "] * w
    for _ in range(random.randint(4, 12)):
        pos = random.randint(0, w-1)
        ch  = random.choice(SPARKS)
        col = random.choice(SPARK_COLORS)
        line[pos] = f"{col}{ch}{R}"
    print("".join(line))

def particle_burst(rows=3, w=None):
    for _ in range(rows):
        spark_line(w)
        delay(0.04)

# ── WAVEFORMS ─────────────────────────────────────────────────────────────────
def sine_wave(label, color, freq=1.0, amp=3, offset=0, w=None):
    w = w or min(width(), 120)
    line = [" "] * w
    for x in range(w):
        y = int(amp * math.sin(freq * x * 2 * math.pi / w + offset)) + amp
        if 0 <= y < w:
            line[x] = f"{color}{'▓' if x % 8 == 0 else '─'}{R}"
    print(f"{DM+WH}{label[:6]:>6}{R} " + "".join(line[:w-8]))

def triple_wave(cycles=2):
    for i in range(cycles):
        t = i * 0.4
        sine_wave("HEAT  ", BRE,  freq=1.2, amp=2, offset=t)
        sine_wave("WATER ", BCY,  freq=0.8, amp=3, offset=t+1.0)
        sine_wave("FORGE ", BYE,  freq=1.6, amp=2, offset=t+2.0)
        delay(0.06)

# ── ASCII ART ─────────────────────────────────────────────────────────────────
TOWER = f"""
{DM+WH}                     ╔══════════════╗
{DM+WH}                     ║  {BYE}☁  ☁  ☁  {DM+WH} ║{R}   {BCY}≋≋ atmospheric capture ≋≋{R}
{DM+WH}                     ║  {BCY}≋≋≋≋≋≋≋≋{DM+WH}  ║{R}
{DM+WH}                     ╠══════════════╣{R}
{DM+WH}                    /║{BYE}  LEXARA v2  {DM+WH}║\\{R}
{DM+WH}                   / ║{DM+WH}  [H₂O TANK] {DM+WH}║ \\{R}
{BYE}                  ☀  {DM+WH}╠══════════════╣  {BYE}☀{R}
{DM+WH}                   \\ ║{MA}    ╔══╗     {DM+WH}║ /{R}
{DM+WH}                    \\║{MA}    ║  ║     {DM+WH}║/{R}   {MA}← THE MONOCLE{R}
{DM+WH}                     ║{MA}    ╚══╝     {DM+WH}║{R}      {DM+WH}(sees nothing){R}
{DM+WH}                     ║{DM+WH}  PLATFORM  {DM+WH}║{R}      {DM+WH}(knows everything){R}
{DM+WH}                     ╠══╦═══════╦══╣{R}
{DM+WH}                     ║  ║{BGR} BAT  {DM+WH}║  ║{R}   {DM+WH}← 40 bats · 40,000 mosquitoes/hr{R}
{DM+WH}                     ║  ║{BGR} HAUS {DM+WH}║  ║{R}
{DM+WH}                     ║  ╚═══════╝  ║{R}
{DM+WH}                     ║  {BRE}📡TORNADO {DM+WH}║{R}   {BRE}← infrasound + baro + cam{R}
{DM+WH}                     ╠══════════════╣{R}
{DM+WH}                     ║   {BCY}UV-C ≋≋≋  {DM+WH}║{R}   {BCY}← potable output{R}
{DM+WH}                     ║   {GR}CARBON▓▓▓  {DM+WH}║{R}
{DM+WH}                     ╠══════════════╣{R}
{DM+WH}                    /║\\{DM+WH}            /║\\{R}
{DM+WH}                   / ║ \\{DM+WH}          / ║ \\{R}
{DM+WH}                  /  ║  \\{DM+WH}        /  ║  \\{R}
{DM+WH}═════════════════╧══╧══╧═════════════╧══╧══╧══════════{R}
"""

PORCH_WELL = f"""
{DM+WH}          ┌─────────────────────────────┐
{DM+WH}          │  {BYE}PORCH·WELL{DM+WH}               │
{DM+WH}          │  {BCY}≋ DESICCANT LOOP ≋{DM+WH}       │
{DM+WH}          │                             │
{DM+WH}          │  {YE}[ABSORB]{DM+WH}→{BCY}[REGEN]{DM+WH}→{BL}[DRIP]{DM+WH}  │
{DM+WH}          │   {BYE}zeolite  solar  condense{DM+WH}  │
{DM+WH}          │                             │
{DM+WH}          │  {BGR}COOL BREEZE  ──→  EXIT{DM+WH}   │
{DM+WH}          │  {BCY}POTABLE WATER ──→  TANK{DM+WH}  │
{DM+WH}          │                             │
{DM+WH}          │  {DM+WH}BOM: ~$200-350  {BGR}✓ VIABLE{DM+WH} │
{DM+WH}          └─────────────────────────────┘{R}
"""

FORGE_ART = f"""
{DM+WH}    ╔═══════════════════════════════════════════╗
{DM+WH}    ║         {BYE}⚒  THE·FORGE  ⚒{DM+WH}              ║
{DM+WH}    ║                                           ║
{DM+WH}    ║  {BGR}KNOWLEDGE{DM+WH}→{BYE}COMPETENCE{DM+WH}→{BMA}MASTERY{DM+WH}→{BCY}MENTOR{DM+WH} ║
{DM+WH}    ║                                           ║
{DM+WH}    ║  {BRE}❌ SEAT·TIME{DM+WH}   {BGR}✓ BUILD·TIME{DM+WH}        ║
{DM+WH}    ║  {BRE}❌ GRADES{DM+WH}      {BGR}✓ ARTIFACTS{DM+WH}         ║
{DM+WH}    ║  {BRE}❌ CONSUME{DM+WH}     {BGR}✓ CREATE{DM+WH}            ║
{DM+WH}    ║  {BRE}❌ PASSIVE{DM+WH}     {BGR}✓ VERIFIED{DM+WH}          ║
{DM+WH}    ║                                           ║
{DM+WH}    ║  {BCY}NODES:{DM+WH} Code·Music·Ecology·Electronics  ║
{DM+WH}    ║         Robotics·Math·Medicine·Build     ║
{DM+WH}    ║                                           ║
{DM+WH}    ║  {BYE}PHASE 0{DM+WH}: SaveSystem + ScriptableObjects ║
{DM+WH}    ║  {BYE}PHASE 1{DM+WH}: Hub Scene + Unlock Anchors     ║
{DM+WH}    ║  {BYE}PHASE 2{DM+WH}: ONE Vertical Slice Quest       ║
{DM+WH}    ║  {BYE}PHASE 3{DM+WH}: 2nd Node + Skill Tree UI       ║
{DM+WH}    ║  {BYE}PHASE 4{DM+WH}: Two-Player Co-op (Photon)      ║
{DM+WH}    ║  {BYE}PHASE 5{DM+WH}: Reputation + Guild Layer       ║
{DM+WH}    ║                                           ║
{DM+WH}    ║  {DM+WH}ENGINE: Unity · PLATFORM: Desktop/Mobile  ║
{DM+WH}    ╚═══════════════════════════════════════════╝{R}
"""

GERALD_ART = f"""
{DM+WH}   ┌──────────────────────────────────────────┐
{DM+WH}   │   {BGR}G·E·R·A·L·D{DM+WH}                        │
{DM+WH}   │   {DM+WH}Geological Environmental Reclamation{DM+WH}   │
{DM+WH}   │   {DM+WH}Autonomous Landfill Disassembler{DM+WH}       │
{DM+WH}   │                                          │
{DM+WH}   │  {BYE}🦝{DM+WH} Gerald always had a phone.{DM+WH}       │
{DM+WH}   │  {BYE}🐕{DM+WH} Biscuit runs field ops.{DM+WH}          │
{DM+WH}   │  {BYE}🦆{DM+WH} Quacktharion: Unquenchable.{DM+WH}      │
{DM+WH}   │  {BMA}👁 {DM+WH}Nerak: amber eyes, ozone warmth.{DM+WH}  │
{DM+WH}   │  {DM+WH}🏠 Dave: reluctant. Three houses down.{DM+WH}   │
{DM+WH}   │                                          │
{DM+WH}   │  {BCY}METHANE→POWER · METAL→FINANCE{DM+WH}        │
{DM+WH}   │  {BGR}BIOMASS→DESERT·RECLAMATION{DM+WH}           │
{DM+WH}   │  {BYE}SWARM·8·UNIT·TYPES · SELF·FUNDING{DM+WH}    │
{DM+WH}   └──────────────────────────────────────────┘{R}
"""

SPECS_BANNER = [
    bo(BYE,  "  ╔══════════════════════════════════════════════════════╗"),
    bo(BYE,  "  ║           BEKW·CODE  OPEN·HARDWARE·SPECS            ║"),
    bo(BYE,  "  ╠══════════════════════════════════════════════════════╣"),
    f"  {BO+BYE}║{R}  {BGR}01{R} · {BWH}CHRONOVOLT·CASE{R}  {DM+WH}flick-spin flywheel piezo phone charger{R}  {BO+BYE}║{R}",
    f"  {BO+BYE}║{R}  {BGR}02{R} · {BWH}ADAPTAFIT{R}        {DM+WH}air-bladder shoe · gait-compensation · piezo{R}  {BO+BYE}║{R}",
    f"  {BO+BYE}║{R}  {BGR}03{R} · {BWH}WINDWARD·STAKE{R}   {DM+WH}VAWT · solar skin · nightlight · bug zapper{R}  {BO+BYE}║{R}",
    f"  {BO+BYE}║{R}  {BGR}04{R} · {BWH}PORCH·WELL{R}       {DM+WH}desiccant AWG · cool breeze · potable water{R}   {BO+BYE}║{R}",
    f"  {BO+BYE}║{R}  {BGR}05{R} · {BWH}LEXARA·TOWER·v2{R}  {DM+WH}self-fill · rain · bats · tornado · monocle{R}   {BO+BYE}║{R}",
    bo(BYE,  "  ╠══════════════════════════════════════════════════════╣"),
    f"  {BO+BYE}║{R}  {DM+WH}ALL SPECS: proven tech · wrong combinations · now fixed{R}  {BO+BYE}║{R}",
    f"  {BO+BYE}║{R}  {DM+WH}LICENSE: open · free · before breakfast · no permission{R}  {BO+BYE}║{R}",
    bo(BYE,  "  ╚══════════════════════════════════════════════════════╝"),
]

PHILOSOPHY = [
    (BMA, "  ·  INVERSION·ENGINE  ·"),
    (BCY, "  See the meta. Imagine the exact inverse. Build that."),
    (BYE, "  The gap between what components DO and what they COULD DO"),
    (BGR, "  is where every BEKW spec lives."),
    (BWH, ""),
    (BRE, "  You cannot meter a tower that fills itself."),
    (BRE, "  You cannot bill monthly for zeolite and Alabama sky."),
    (BRE, "  You cannot subscription-model a bat colony."),
    (BWH, ""),
    (BGR, "  That is exactly why it was never built."),
    (BGR, "  That is exactly why we're building it."),
    (BWH, ""),
    (BYE, "  DAMASCUS·TO·DIGITAL·DIAMONDS"),
    (BYE, "  Given away free. Before breakfast. No permission required."),
    (BWH, ""),
    (BCY, "  We are enough."),
    (BCY, "  We just have to be smart about it."),
]

MANTRA = [
    "  BUILD·REALITY·BY·LEARNING",
    "  LEARN·BY·BUILDING",
    "  LEAVE·EVERY·PLACE·BETTER·THAN·YOU·FOUND·IT",
]

KETH_PROFILE = f"""
{DM+WH}  ┌─────────────────────────────────────────────────────┐
{DM+WH}  │  {BMA}KETH'AR{DM+WH} :: MULTI·TRADE · PATTERN·RECOGNITION{DM+WH}  │
{DM+WH}  │                                                     │
{DM+WH}  │  {BYE}~40 yrs{DM+WH}: military · radar · excavation         │
{DM+WH}  │          plumbing · blacksmithing · leather · cook  │
{DM+WH}  │                                                     │
{DM+WH}  │  {BGR}METHOD{DM+WH}: convergent pattern recognition          │
{DM+WH}  │          not specialist. cross-domain seeing.       │
{DM+WH}  │                                                     │
{DM+WH}  │  {BCY}TOOLS{DM+WH}: Claude · Grok · Copilot · Gemini · GPT  │
{DM+WH}  │  {BCY}ARCHIVE{DM+WH}: GitHub · BEKW-CODE                     │
{DM+WH}  │  {BCY}PLATFORM{DM+WH}: porch · phone · tablet · Guinness     │
{DM+WH}  │                                                     │
{DM+WH}  │  {BMA}SIMULTANEOUSLY SILLY AND SERIOUS ABOUT IT.{DM+WH}      │
{DM+WH}  │  {BMA}THAT IS NOT A CONTRADICTION.{DM+WH}                    │
{DM+WH}  │  {BMA}THAT IS THE WHOLE THING.{DM+WH}                        │
{DM+WH}  └─────────────────────────────────────────────────────┘{R}
"""

MONOCLE_VERSE = [
    bo(MA, "  ┌─────────────────────────────────────────┐"),
    bo(MA, "  │         THE·MONOCLE  ::  IMMOVABLE      │"),
    bo(MA, "  │                                         │"),
    f"  {BO+MA}│{R}  {DM+WH}It serves no optical function.{R}          {BO+MA}│{R}",
    f"  {BO+MA}│{R}  {DM+WH}It admits no light.{R}                     {BO+MA}│{R}",
    f"  {BO+MA}│{R}  {DM+WH}It corrects no vision.{R}                  {BO+MA}│{R}",
    f"  {BO+MA}│{R}  {DM+WH}It magnifies nothing.{R}                   {BO+MA}│{R}",
    f"  {BO+MA}│{R}                                         {BO+MA}│{R}",
    f"  {BO+MA}│{R}  {BMA}It is simply there.{R}                    {BO+MA}│{R}",
    f"  {BO+MA}│{R}  {BMA}Permanently. As is correct.{R}             {BO+MA}│{R}",
    f"  {BO+MA}│{R}                                         {BO+MA}│{R}",
    f"  {BO+MA}│{R}  {DM+WH}The bats see everything.{R}               {BO+MA}│{R}",
    f"  {BO+MA}│{R}  {DM+WH}Lexara does not need to.{R}               {BO+MA}│{R}",
    bo(MA, "  └─────────────────────────────────────────┘"),
]

SONG_FRAGMENT = f"""
{DM+WH}  ── SEAT·TIME (excerpt) ───────────────────────────────────
{BRE}  Bell rings, sit down, don't ask why
{BRE}  Thirty kids, one pace, watch the clock go by
{BRE}  They measure minds in hours not in skill
{BRE}  Pass the test, forget it, that's the drill
{BWH}
{BYE}  SEAT TIME — they're grading how long you stayed
{BYE}  Not what you made, not what you made
{BYE}  Burn the clock, keep the craft
{BYE}  Mastery's the only path
{BWH}
{BGR}  Forge don't ask "how long did you sit"
{BGR}  Forge asks "show me — did you build it?"{R}
  {DM+WH}── end fragment ──────────────────────────────────────────{R}
"""

CLOSING = [
    bo(BCY,  ""),
    bo(BCY,  "  ┌──────────────────────────────────────────────────┐"),
    bo(BCY,  "  │          BEKW·CANON  ::  TRANSMISSION·END        │"),
    bo(BCY,  "  ╠══════════════════════════════════════════════════╣"),
    f"  {BO+BCY}│{R}  {DM+WH}Not inventions. Combinations.{R}                  {BO+BCY}│{R}",
    f"  {BO+BCY}│{R}  {DM+WH}Proven tech. Wrong arrangement. Now fixed.{R}      {BO+BCY}│{R}",
    f"  {BO+BCY}│{R}                                                  {BO+BCY}│{R}",
    f"  {BO+BCY}│{R}  {BGR}The world is metered.{R}                          {BO+BCY}│{R}",
    f"  {BO+BCY}│{R}  {BGR}The specs are free.{R}                            {BO+BCY}│{R}",
    f"  {BO+BCY}│{R}  {BGR}The bats work the night shift.{R}                  {BO+BCY}│{R}",
    f"  {BO+BCY}│{R}  {BGR}The monocle watches nothing.{R}                    {BO+BCY}│{R}",
    f"  {BO+BCY}│{R}  {BGR}The Forge is being built.{R}                       {BO+BCY}│{R}",
    f"  {BO+BCY}│{R}                                                  {BO+BCY}│{R}",
    f"  {BO+BCY}│{R}  {BYE}BEKW·CODE :: GITHUB · OPEN · PERMANENT{R}         {BO+BCY}│{R}",
    f"  {BO+BCY}│{R}  {BMA}Kelvrix.{R}                                        {BO+BCY}│{R}",
    bo(BCY,  "  └──────────────────────────────────────────────────┘"),
    "",
]

# ── MAIN ─────────────────────────────────────────────────────────────────────
def main():
    cls()
    w = min(width(), 120)

    # ── HEADER ────────────────────────────────────────────────────────────────
    particle_burst(2, w)
    print()
    pulse("B · E · K · W", cycles=5, colors=[BYE, BMA, BCY, BGR, BWH])
    pulse("FORGE  ·  CANON  ·  TRANSMISSION", cycles=3, colors=[BWH, BYE, BCY])
    print()

    wave_line("  ≋ ≋ ≋  SIMULTANEOUSLY·SILLY·AND·PERMANENTLY·SERIOUS  ≋ ≋ ≋",
              [BYE, BMA, BCY, BGR, BWH, BCY, BMA])
    print()
    particle_burst(1, w)
    print()
    delay(0.3)

    # ── TRIPLE WAVE ──────────────────────────────────────────────────────────
    rule("═", BYE, w)
    print(c(DM+WH, "  SYSTEM·WAVEFORMS  ::  HEAT · WATER · FORGE"))
    rule("─", DM+WH, w)
    triple_wave(cycles=3)
    rule("═", BYE, w)
    print()
    delay(0.2)

    # ── KETH PROFILE ─────────────────────────────────────────────────────────
    scroll(KETH_PROFILE.split("\n"), 0.015)
    print()
    delay(0.2)

    # ── BEKW SPECS ────────────────────────────────────────────────────────────
    scroll(SPECS_BANNER, 0.025)
    print()
    delay(0.3)

    # ── LEXARA TOWER ─────────────────────────────────────────────────────────
    rule("─", DM+WH, w)
    print(bo(BYE, "  SPEC·05  ::  LEXARA·TOWER·v2.0"))
    rule("─", DM+WH, w)
    scroll(TOWER.split("\n"), 0.018)
    delay(0.2)

    # ── PORCH WELL ───────────────────────────────────────────────────────────
    rule("─", DM+WH, w)
    print(bo(BCY, "  SPEC·04  ::  PORCH·WELL"))
    rule("─", DM+WH, w)
    scroll(PORCH_WELL.split("\n"), 0.018)
    print()
    delay(0.2)

    # ── THE FORGE ────────────────────────────────────────────────────────────
    rule("─", DM+WH, w)
    print(bo(BYE, "  PROJECT  ::  THE·FORGE  ::  UNITY·VOCATIONAL·EDU"))
    rule("─", DM+WH, w)
    scroll(FORGE_ART.split("\n"), 0.018)
    print()
    delay(0.2)

    # ── GERALD ───────────────────────────────────────────────────────────────
    rule("─", DM+WH, w)
    print(bo(BGR, "  PROJECT  ::  G·E·R·A·L·D"))
    rule("─", DM+WH, w)
    scroll(GERALD_ART.split("\n"), 0.018)
    print()
    delay(0.2)

    # ── MONOCLE ──────────────────────────────────────────────────────────────
    particle_burst(1, w)
    scroll(MONOCLE_VERSE, 0.04)
    particle_burst(1, w)
    print()
    delay(0.3)

    # ── PHILOSOPHY ───────────────────────────────────────────────────────────
    rule("═", BMA, w)
    print(bo(BMA, "  INVERSION·ENGINE  ::  BEKW·DOCTRINE"))
    rule("─", DM+WH, w)
    for col, line in PHILOSOPHY:
        print(c(col, line))
        delay(0.04)
    print()
    delay(0.2)

    # ── SONG FRAGMENT ────────────────────────────────────────────────────────
    rule("─", DM+WH, w)
    scroll(SONG_FRAGMENT.split("\n"), 0.022)
    print()
    delay(0.2)

    # ── MANTRA ───────────────────────────────────────────────────────────────
    rule("═", BGR, w)
    for line in MANTRA:
        pulse(line, cycles=2, colors=[BGR, BWH, BYE, BGR])
    rule("═", BGR, w)
    print()
    delay(0.3)

    # ── PARTICLE FINALE ───────────────────────────────────────────────────────
    for i in range(4):
        spark_line(w)
        delay(0.06)

    # ── CLOSING ──────────────────────────────────────────────────────────────
    scroll(CLOSING, 0.03)

    # ── FINAL PULSE ──────────────────────────────────────────────────────────
    pulse("≋  KELVRIX  ≋", cycles=6, colors=[BMA, BWH, BCY, BYE, BMA, BCY])
    print()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{c(DM+WH, '  transmission interrupted. the monocle remains.')}\n")
