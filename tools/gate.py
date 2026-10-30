#!/usr/bin/env python3
"""Run the theme gate on every scheme in themes/palettes.tsv over Schemify's base ui.records.

Usage: gate.py <ui.records>

Exit 1 when any scheme fails a contrast or separation check. The accent budget is reported but
not enforced: a ported theme keeps its original colours, and many of them are colourful by design.
"""
import os
import re
import subprocess
import sys
import tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEMPLATE = open(os.path.join(ROOT, "themes", "template.records")).read()


def schemes():
    lines = open(os.path.join(ROOT, "themes", "palettes.tsv")).read().splitlines()
    head = lines[0].split("\t")
    for line in lines[1:]:
        yield dict(zip(head, line.split("\t")))


def main(base):
    hard = loud = 0
    for s in schemes():
        text = re.sub(r"@(\w+)", lambda m: s[m.group(1)], TEMPLATE)
        with tempfile.NamedTemporaryFile("w", suffix=".records") as f:
            f.write(text)
            f.flush()
            out = subprocess.run([sys.executable, os.path.join(ROOT, "tools", "check_theme.py"), base, f.name],
                                 capture_output=True, text=True).stdout
        fails = [l for l in out.splitlines() if l.startswith("FAIL")]
        budget = [l for l in fails if "decorative saturated" in l]
        loud += bool(budget)
        if len(fails) > len(budget):
            hard += 1
            print(f"FAIL {s['theme']}/{s['scheme']}: " + " | ".join(l for l in fails if l not in budget))
    print(f"{hard} scheme(s) failing, {loud} over the accent budget (allowed for ports)")
    sys.exit(1 if hard else 0)


if __name__ == "__main__":
    main(sys.argv[1])
