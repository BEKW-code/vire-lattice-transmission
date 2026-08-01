#!/usr/bin/env python3
"""
ANALOG CASCADE :: DEEP RENDER
Real gear geometry, real meshing trains, real pendulum physics, real dial hands.
Built to last, forever-ish.
"""
import time
import sys
import math

RESET = '\033[0m'; BOLD = '\033[1m'; DIM = '\033[2m'
BRASS = '\033[38;5;178m'; STEEL = '\033[38;5;250m'; COPPER = '\033[38;5;166m'
GOLD = '\033[38;5;220m'; GREY = '\033[38;5;240m'; WHITE = '\033[38;5;255m'
BLUE = '\033[38;5;39m'; RUST = '\033[38;5;130m'

def out(s=""):
    sys.stdout.write(s)
    sys.stdout.flush()

def type_line(text, color, delay=0.01):
    out(color)
    for ch in text:
        out(ch)
        time.sleep(delay)
    out(RESET + "\n")

def rule(char="="):
    out(f"{GREY}{char * 74}{RESET}\n")

def tag(text):
    out(f"\n{BOLD}{WHITE}  {text}{RESET}\n")
    time.sleep(0.08)

def move_up(n):
    out(f"\033[{n}A")

def clear_lines(n):
    for _ in range(n):
        out("\033[2K")
        out("\033[1B")
    move_up(n)

def render_gear(teeth, rotation, radius=7, w=19, h=19, char='#', hub='+'):
    grid = [[' ' for _ in range(w)] for _ in range(h)]
    cx, cy = w // 2, h // 2
    for i in range(teeth):
        angle = (2 * math.pi * i / teeth) + rotation
        for r in (radius, radius + 1):
            x = int(round(cx + r * math.cos(angle)))
            y = int(round(cy + r * math.sin(angle) * 0.5))
            if 0 <= x < w and 0 <= y < h:
                grid[y][x] = char
    for i in range(teeth * 3):
        angle = (2 * math.pi * i / (teeth * 3)) + rotation
        r = radius - 2
        x = int(round(cx + r * math.cos(angle)))
        y = int(round(cy + r * math.sin(angle) * 0.5))
        if 0 <= x < w and 0 <= y < h:
            if grid[y][x] == ' ':
                grid[y][x] = '.'
    grid[cy][cx] = hub
    return [''.join(row) for row in grid]

def render_two_gear_train(rot1, rot2, color1, color2):
    g1 = render_gear(10, rot1, radius=7, char='#', hub='@')
    g2 = render_gear(14, rot2, radius=9, char='#', hub='@')
    h = max(len(g1), len(g2))
    lines = []
    for i in range(h):
        l1 = g1[i] if i < len(g1) else ' ' * 19
        l2 = g2[i] if i < len(g2) else ' ' * 23
        lines.append(f"  {color1}{l1}{RESET}  {color2}{l2}{RESET}")
    return lines

def animate_gear_train(frames=18, delay=0.06):
    printed = 0
    for f in range(frames):
        rot1 = f * (2 * math.pi / 10) / 3
        rot2 = -f * (2 * math.pi / 14) / 3 * (10 / 14)
        lines = render_two_gear_train(rot1, rot2, BRASS, COPPER)
        if printed:
            clear_lines(printed)
        for ln in lines:
            out(ln + "\n")
        printed = len(lines)
        time.sleep(delay)
    out(f"  {DIM}{STEEL}great wheel (10T) driving pinion (14T) -- torque up, speed down{RESET}\n")

def animate_pendulum(cycles=2, width=41, delay=0.03):
    steps = 40
    printed = 0
    for c in range(cycles):
        for s in range(steps):
            t = s / steps
            angle = math.sin(2 * math.pi * t) * 0.55
            length = 8
            bob_x = int(round(width // 2 + length * math.sin(angle)))
            bob_y = int(round(length * math.cos(angle)))
            lines = []
            for y in range(length + 2):
                row = [' '] * width
                if y == 0:
                    row[width // 2] = '+'
                elif y < bob_y:
                    frac = y / max(bob_y, 1)
                    x = int(round(width // 2 + frac * length * math.sin(angle)))
                    if 0 <= x < width:
                        row[x] = '|'
                elif y == bob_y:
                    if 0 <= bob_x < width:
                        row[bob_x] = 'O'
                lines.append(''.join(row))
            if printed:
                clear_lines(printed)
            for ln in lines:
                out(f"  {STEEL}{ln}{RESET}\n")
            printed = len(lines)
            time.sleep(delay)
    out(f"  {DIM}isochronism: period independent of amplitude{RESET}\n")

def animate_escapement(teeth=8, delay=0.12):
    for i in range(teeth):
        pallet = "\\" if i % 2 == 0 else "/"
        bar = "=" * i + pallet + "=" * (teeth - i - 1)
        out(f"\r  {GOLD}escape wheel [{bar}] tooth {i+1}/{teeth} released{RESET}")
        sys.stdout.flush()
        time.sleep(delay)
    out("\n")

def render_ferraris(rotation, radius=8, w=19, h=19):
    grid = [[' ' for _ in range(w)] for _ in range(h)]
    cx, cy = w // 2, h // 2
    for y in range(h):
        for x in range(w):
            dx, dy = x - cx, (y - cy) * 2
            dist = math.sqrt(dx * dx + dy * dy)
            if dist <= radius:
                ang = math.atan2(dy, dx) - rotation
                sector = int((ang % (2 * math.pi)) / (math.pi / 2))
                grid[y][x] = ['#', '.', '#', '.'][sector % 4]
    grid[cy][cx] = '@'
    return [''.join(row) for row in grid]

def animate_ferraris(frames=30, delay=0.05):
    printed = 0
    for f in range(frames):
        rotation = f * 0.35
        lines = render_ferraris(rotation)
        if printed:
            clear_lines(printed)
        for ln in lines:
            out(f"  {COPPER}{ln}{RESET}\n")
        printed = len(lines)
        time.sleep(delay)
    out(f"  {DIM}eddy currents -- torque proportional to real power (V x I x cos phi){RESET}\n")

def render_clock(hour_angle, min_angle, radius=8, w=19, h=19):
    grid = [[' ' for _ in range(w)] for _ in range(h)]
    cx, cy = w // 2, h // 2
    for i in range(12):
        ang = (2 * math.pi * i / 12) - math.pi / 2
        x = int(round(cx + radius * math.cos(ang)))
        y = int(round(cy + radius * math.sin(ang) * 0.5))
        if 0 <= x < w and 0 <= y < h:
            grid[y][x] = 'o'
    for r, ang, ch in ((radius - 3, hour_angle, 'H'), (radius - 1, min_angle, 'M')):
        steps = max(int(r), 1)
        for s in range(1, steps + 1):
            rr = r * s / steps
            x = int(round(cx + rr * math.cos(ang - math.pi / 2)))
            y = int(round(cy + rr * math.sin(ang - math.pi / 2) * 0.5))
            if 0 <= x < w and 0 <= y < h:
                grid[y][x] = ch
    grid[cy][cx] = '+'
    return [''.join(row) for row in grid]

def animate_clock(frames=24, delay=0.05):
    printed = 0
    for f in range(frames):
        min_angle = f * (2 * math.pi / frames)
        hour_angle = f * (2 * math.pi / frames) / 12
        lines = render_clock(hour_angle, min_angle)
        if printed:
            clear_lines(printed)
        for ln in lines:
            out(f"  {WHITE}{ln}{RESET}\n")
        printed = len(lines)
        time.sleep(delay)
    out(f"  {DIM}motion work: gear reduction driving hour hand from minute hand{RESET}\n")

def main():
    rule()
    type_line("  ANALOG CASCADE // DEEP RENDER", BOLD + BRASS, 0.018)
    type_line("  real geometry. real meshing. built to last, forever-ish.", DIM + WHITE, 0.01)
    rule()
    print()

    tag("ROOT LAYER: THE SIX SIMPLE MACHINES")
    for m in ["lever", "wheel and axle", "pulley", "inclined plane", "wedge", "screw"]:
        out(f"    {STEEL}- {m}{RESET}\n")
        time.sleep(0.08)
    print()

    tag("GEAR TRAIN -- GREAT WHEEL MESHING WITH PINION (rendered, not simulated)")
    animate_gear_train(frames=24, delay=0.05)
    t1, t2 = 10, 14
    ratio = t2 / t1
    out(f"  {STEEL}RECORD: teeth(great wheel)={t1}  teeth(pinion)={t2}{RESET}\n")
    out(f"  {STEEL}RECORD: gear ratio = {t2}/{t1} = {ratio:.4f}{RESET}\n")
    out(f"  {STEEL}RECORD: pinion completes {ratio:.4f} rotations per 1 great-wheel rotation{RESET}\n")
    out(f"  {STEEL}RECORD: torque multiplies by {ratio:.4f}x, speed drops by the same factor{RESET}\n")
    out(f"  {DIM}This is the whole mechanism. A person with these four lines and{RESET}\n")
    out(f"  {DIM}two gear blanks can cut this train from scratch, no source needed.{RESET}\n")
    print()

    tag("PENDULUM OSCILLATOR -- REAL SWING PHYSICS")
    animate_pendulum(cycles=2, delay=0.025)
    length_m = 0.9939  # meters, seconds pendulum reference length
    g = 9.80665
    period = 2 * math.pi * math.sqrt(length_m / g)
    out(f"  {STEEL}RECORD: period T = 2*pi*sqrt(L/g){RESET}\n")
    out(f"  {STEEL}RECORD: for a seconds pendulum, L = {length_m:.4f} m gives T = {period:.4f} s{RESET}\n")
    out(f"  {STEEL}RECORD: this equation predates every clock built from it and will outlast all of them{RESET}\n")
    print()

    tag("ESCAPEMENT -- DEAD-BEAT RELEASE, ONE TOOTH AT A TIME")
    animate_escapement(teeth=10, delay=0.1)
    print()

    tag("FERRARIS INDUCTION DISK -- QUADRANT-SHADED ROTATION")
    animate_ferraris(frames=34, delay=0.045)
    out(f"  {COPPER}RECORD: real power P = V * I * cos(phi){RESET}\n")
    out(f"  {COPPER}RECORD: disk torque proportional to P; eddy-current brake makes speed proportional to torque{RESET}\n")
    out(f"  {COPPER}RECORD: disk rotations, via gear reduction, = energy consumed (kWh) on the register{RESET}\n")
    out(f"  {DIM}No semiconductor in this measuring path. A flood, an EMP, a century -- none of it matters.{RESET}\n")
    print()

    tag("CLOCK FACE -- MOTION WORK DRIVING BOTH HANDS")
    animate_clock(frames=28, delay=0.045)
    print()

    tag("WEAR PHILOSOPHY")
    for line in [
        "soft metal wears before hard metal",
        "lubrication is sacrificial and visible",
        "no sealed black boxes",
        "every surface can be cleaned, polished, re-bushed",
    ]:
        out(f"    {RUST}- {line}{RESET}\n")
        time.sleep(0.1)
    print()

    tag("THE COVENANT")
    type_line("  understood by eye and hand.", BOLD + GOLD, 0.02)
    type_line("  restorable a century later with hand tools.", BOLD + GOLD, 0.02)
    type_line("  no software update required.", BOLD + GOLD, 0.02)
    print()

    rule()
    type_line("  copy. fork. teach. restore. no license required.", BOLD + BRASS, 0.015)
    rule()
    print()

if __name__ == "__main__":
    main()
              
