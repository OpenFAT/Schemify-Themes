#!/usr/bin/env python3
"""Port spicetify-themes' colour schemes to Schemify presets. Stdlib only.

Usage: spicetify.py <spicetify-themes checkout>

Every theme's `color.ini` scheme becomes one row of `themes/palettes.tsv`: the colours that fill the
`@token` slots of `themes/template.records` (the Modern preset with its colours named). Each role
starts from the scheme's own colour; a role that misses a gate contrast threshold is pushed toward
white (dark themes) or black (light themes) until it passes, so the hue stays the scheme's.
"""
import configparser
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import check_theme as ct  # noqa: E402

ROOT = os.path.dirname(HERE)
TEMPLATE = os.path.join(ROOT, "themes", "template.records")
PALETTES = os.path.join(ROOT, "themes", "palettes.tsv")

# Modern's highlight sets (gate-searched); kept per canvas luminance.
HL = {
    "dark": ["9406f9", "06f906", "b8148f", "7f75f0", "06f9a8", "c78605", "14b89c", "e6196e"],
    "light": ["0606f9", "149cb8", "b81474", "f906f9", "1c0495", "4e0a5c", "5c180a", "959504"],
}
HL_TOKENS = [f"hl{n}" for n in ct.HILITE]


def rgb(h):
    return [int(h[i:i + 2], 16) for i in (0, 2, 4)]


def hexs(c):
    return "".join(f"{max(0, min(255, round(v))):02x}" for v in c)


def mix(a, b, t):
    return hexs([x + (y - x) * t for x, y in zip(rgb(a), rgb(b))])


def push(c, bg, need, limit=1.0):
    """`c` moved toward white or black (away from `bg`) until contrast(c, bg) >= need."""
    end = "ffffff" if ct.luminance(bg) < 0.18 else "000000"
    t = 0.0
    while ct.contrast(c, bg) < need and t < limit:
        t += 0.02
        c = mix(c, end, 0.02 / (1.0 - t + 0.02))
    return c


def sep(a, b):
    """Gate separation score: >= 1 passes ΔE76 20 normal, 10 deutan, 10 protan."""
    return min(ct.delta_e(a, b) / 20, ct.delta_e(a, b, "deutan") / 10, ct.delta_e(a, b, "protan") / 10)


def candidates(bg):
    import colorsys
    out = []
    for h in range(0, 360, 10):
        for s_ in (0.7, 1.0):
            for l in (0.3, 0.4, 0.5, 0.6, 0.7, 0.8):
                c = hexs(v * 255 for v in colorsys.hls_to_rgb(h / 360, l, s_))
                if ct.contrast(c, bg) >= 3.2:
                    out.append(c)
    return out


def rotate(h, deg):
    import colorsys
    r, g, b = (v / 255 for v in rgb(h))
    hh, l, s = colorsys.rgb_to_hls(r, g, b)
    return hexs(v * 255 for v in colorsys.hls_to_rgb((hh + deg / 360) % 1, l, max(s, 0.55)))


def scheme_roles(c):
    """spicetify colour keys -> the scheme's base roles."""
    g = lambda *ks: next((c[k] for k in ks if k in c), None)
    bg = g("main", "background", "sidebar")
    text = g("text")
    accent = g("button", "accent", "button-active", "nav-active", "text")
    return {
        "bg": bg,
        "panel": g("sidebar", "main-secondary") or bg,
        "raised": g("card", "main-elevated", "player", "sidebar") or bg,
        "text": text,
        "muted": g("subtext", "extratext", "text"),
        "accent": accent,
        "second": g("button-secondary", "playback-bar", "accent-active", "button-active", "nav-active", "misc"),
        "error": g("notification-error"),
    }


def readable(surface, text, fallback):
    return surface if ct.contrast(text, surface) >= 4.5 else fallback


def tokens(r):
    dark = ct.luminance(r["bg"]) < 0.18
    r = dict(r, text=push(r["text"], r["bg"], 4.6))
    r["panel"] = readable(r["panel"], r["text"], r["bg"])
    r["raised"] = readable(r["raised"], r["text"], mix(r["bg"], r["text"], 0.05))
    strong = "ffffff" if dark else "000000"
    t = {
        "bg": r["bg"], "panel": r["panel"], "raised": r["raised"],
        "hover": mix(r["raised"], r["text"], 0.06), "active": mix(r["raised"], r["text"], 0.11),
        "border": mix(r["bg"], r["muted"], 0.30), "preview": mix(r["bg"], r["panel"], 0.5),
        "text": r["text"], "text2": mix(r["text"], r["bg"], 0.08), "muted": r["muted"],
        "dim1": mix(r["muted"], r["bg"], 0.25), "dim2": mix(r["muted"], r["bg"], 0.35), "dim3": mix(r["muted"], r["bg"], 0.5),
        "strong": strong, "accent": r["accent"],
        "accent_bg": mix(r["bg"], r["accent"], 0.40), "accent_bg2": mix(r["bg"], r["accent"], 0.25),
    }
    # Status colours keep their meaning; darker on light panels.
    status = {"ok": "6fcf7f", "bad": "ff6b6b", "warn": "e0a040", "staged": "7fd18f", "staged_line": "3f8f55"}
    for k, v in status.items():
        t[k] = v if dark else mix(v, "000000", 0.45)
    t["staged_bg"] = mix(r["bg"], "3f8f55", 0.25)
    t["bad_bg"] = mix(r["bg"], "ff6b6b", 0.15)
    t["warn_bg"] = mix(r["bg"], "e0a040", 0.15)
    # Canvas: the scheme's background, its accent for wires, its text; a second hue for symbols, red for pins.
    second = r["second"] if r["second"] and ct.delta_e(r["second"], r["accent"]) >= 25 else rotate(r["accent"], 120)
    pin = r["error"] if r["error"] and ct.chroma(r["error"]) > 40 else ("e2574c" if dark else "b3261e")
    t.update({"c_bg": r["bg"], "c_wire": r["accent"], "c_text": r["text"], "c_symbol": second, "c_pin": pin,
              "c_sel": strong, "c_grid": mix(r["bg"], r["text"], 0.10)})
    t.update(dict(zip(HL_TOKENS, HL["dark" if dark else "light"])))
    return t


def fix(t):
    """Push failing foreground tokens until the template's contrast checks pass."""
    for k, need in (("c_wire", 3), ("c_symbol", 3), ("c_pin", 3), ("c_sel", 3), ("c_text", 4.5)):
        t[k] = push(t[k], t["c_bg"], need)
    for k in HL_TOKENS:
        t[k] = push(t[k], t["c_bg"], 3)
    floor = min(ct.contrast(t[k], t["c_bg"]) for k in ("c_wire", "c_symbol", "c_pin"))
    for s in range(1, 60):  # grid: visible, dimmer than the circuit
        g = mix(t["c_bg"], t["c_text"], s / 100)
        if ct.contrast(g, t["c_bg"]) >= 1.33:
            t["c_grid"] = g if ct.contrast(g, t["c_bg"]) < floor else t["c_grid"]
            break
    bg = t["c_bg"]
    if sep(t["c_wire"], t["c_sel"]) < 1:  # a white/black wire: the selection takes a hue instead
        t["c_sel"] = max(candidates(bg), key=lambda c: (min(sep(c, t["c_wire"]), 2), ct.contrast(c, bg)))
    fixed = [t["c_wire"], t["c_sel"]]
    hl = [t[h] for h in HL_TOKENS]
    if min(sep(a, b) for i, a in enumerate(hl + fixed) for b in (hl + fixed)[i + 1:]) < 1:
        hl = []  # Modern's set does not fit this background: greedy search, as the theme skill describes
        pool = candidates(bg)
        while len(hl) < len(HL_TOKENS):
            hl.append(max(pool, key=lambda c: min(sep(c, o) for o in hl + fixed)))
            pool.remove(hl[-1])
    t.update(zip(HL_TOKENS, hl))
    # Chrome text pairs: a foreground unreadable on the base background is pushed; otherwise the
    # surface under it moves back toward the base background, so the scheme's text keeps its colour.
    tpl = open(TEMPLATE).read()
    for _ in range(120):
        styles, _ = parse_text(expand(tpl, t))
        base = styles.get("*", {})
        bad = []
        for sel, p in styles.items():
            if sel.startswith("canvas.") or sel in ct.NO_TEXT or "bg" not in p:
                continue
            fg = p.get("fg", base.get("fg"))
            if fg and ct.contrast(fg, p["bg"]) < 4.5:
                bad.append(sel)
        if not bad:
            break
        for sel in bad:
            fg = TOKEN_OF.get((sel, "fg"), TOKEN_OF[("*", "fg")])
            bg = TOKEN_OF[(sel, "bg")]
            if ct.contrast(t[fg], t["bg"]) < 4.7:
                t[fg] = push(t[fg], t["bg"], 4.8)
            elif bg != "bg":
                t[bg] = mix(t[bg], t["bg"], 0.2)
    return t


TOKEN_OF = {}

# spicetify fills keys a scheme leaves out with Spotify's own colours.
SPOTIFY = {"text": "ffffff", "subtext": "b3b3b3", "main": "121212", "sidebar": "000000", "card": "282828",
           "button": "1db954", "button-active": "1ed760", "notification-error": "e22134"}


def parse_text(text):
    import tempfile
    with tempfile.NamedTemporaryFile("w", suffix=".records") as f:
        f.write(text)
        f.flush()
        return ct.parse([f.name])


def load_template():
    sel = None
    for line in open(TEMPLATE):
        if line.strip() and not line[0].isspace():
            w = line.split()
            sel = w[1] if w[0] == "style" and len(w) > 1 else None
        m = re.match(r"\s+(\S+)\s+@(\w+)", line)
        if m and sel:
            TOKEN_OF[(sel, m.group(1))] = m.group(2)


def expand(tpl, t):
    return re.sub(r"@(\w+)", lambda m: t[m.group(1)], tpl)


def read_schemes(src):
    for theme in sorted(os.listdir(src)):
        ini = os.path.join(src, theme, "color.ini")
        if not os.path.isfile(ini):
            continue
        cp = configparser.ConfigParser(inline_comment_prefixes=(";", "#"), comment_prefixes=(";", "#"), strict=False)
        cp.read_string(open(ini, encoding="utf-8").read())
        for scheme in cp.sections():
            cols = {k: v.strip().lstrip("#")[:6].lower() for k, v in cp[scheme].items()}
            cols = {k: v for k, v in cols.items() if re.fullmatch(r"[0-9a-f]{6}", v)}
            yield theme, scheme, {**SPOTIFY, **cols}


def authors(src):
    m = json.load(open(os.path.join(src, "manifest.json")))
    out = {}
    for e in m:
        theme = e["schemes"].split("/")[0]
        out[theme] = ", ".join(a["name"] for a in e.get("authors", []))
    return out


def main(src):
    load_template()
    tpl = open(TEMPLATE).read()
    names = sorted(set(re.findall(r"@(\w+)", tpl)))
    by = authors(src)
    rows, failed = [], []
    for theme, scheme, cols in read_schemes(src):
        t = fix(tokens(scheme_roles(cols)))
        styles, other = parse_text(expand(tpl, t))
        ct.fails = 0
        import io, contextlib
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            for th in ("dark", "light"):
                ct.check_canvas(styles, th)
            ct.check_chrome(styles, other)
        hard = [l for l in buf.getvalue().splitlines() if l.startswith("FAIL") and "decorative saturated" not in l]
        if hard:
            failed.append((theme, scheme, hard))
        rows.append([theme, scheme, by.get(theme, "")] + [t[n] for n in names])
    with open(PALETTES, "w") as f:
        f.write("\t".join(["theme", "scheme", "authors"] + names) + "\n")
        for r in rows:
            f.write("\t".join(r) + "\n")
    print(f"{len(rows)} schemes, {len(failed)} with gate failures")
    for th, sc, hard in failed:
        print(f"  {th}/{sc}: " + " | ".join(hard))


if __name__ == "__main__":
    main(sys.argv[1])
