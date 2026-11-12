"""Write Tableau colour palettes as .tps files.

One Preferences.tps holds every palette (drop it into My Tableau Repository).
One .tps per family lets someone take just the palette they want.
Run: python3 make_palettes.py OUT_DIR
"""
import sys
from pathlib import Path

# name, Tableau palette type, colours. Types: regular (categorical),
# ordered-sequential, ordered-diverging.
PALETTES = {
    "house": [
        ("House Categorical", "regular",
         ["#1F4E79", "#B35C00", "#0F6E6E", "#6A3D9A", "#8C564B", "#5A5A5A"]),
        ("House Sequential Blue", "ordered-sequential",
         ["#D9E2EC", "#A9BED3", "#7A9ABA", "#4C76A0", "#1F4E79"]),
        ("House Diverging Copper Blue", "ordered-diverging",
         ["#B35C00", "#D9A066", "#F2F2F2", "#7A9ABA", "#1F4E79"]),
        ("House Text Greys", "regular", ["#333333", "#5A5A5A", "#767676"]),
    ],
    "accessible": [
        # Okabe and Ito colour blind safe set.
        ("Okabe Ito Colour Blind Safe", "regular",
         ["#000000", "#E69F00", "#56B4E9", "#009E73", "#F0E442", "#0072B2", "#D55E00", "#CC79A7"]),
        ("Status Red Amber Green", "regular", ["#C62828", "#B35C00", "#2E7D32"]),
        ("Neutral Greys Sequential", "ordered-sequential",
         ["#F2F2F2", "#CCCCCC", "#999999", "#767676", "#4D4D4D", "#262626"]),
    ],
    "field-notes": [
        ("Field Notes Navy Blue", "regular",
         ["#032D60", "#0176D3", "#4E79A7", "#59A14F", "#F28E2B", "#E15759"]),
        ("Field Notes Navy Sequential", "ordered-sequential",
         ["#E5F1FB", "#9CC7EF", "#0176D3", "#014486", "#032D60"]),
    ],
    "beverage": [
        # Approximate beer colour by SRM, straw to black.
        ("Beer SRM Colour", "ordered-sequential",
         ["#FFE699", "#FFCA5A", "#FBB123", "#F39C00", "#D77200", "#BB5100", "#8E2900", "#5A1400", "#260000"]),
        ("Wine Rose to Red", "ordered-sequential",
         ["#F6D5D9", "#E79AA6", "#C44E63", "#8E1F36", "#4E0B1E"]),
        ("Whisky Cask Amber", "ordered-sequential",
         ["#F5E3B5", "#E6BE6A", "#C98E2B", "#9A5B14", "#5C3209"]),
        ("Brewhouse Stages", "regular",
         ["#C9A227", "#8C564B", "#0F6E6E", "#1F4E79", "#6A3D9A", "#5A5A5A"]),
    ],
}


def tps(palettes):
    rows = ["<?xml version='1.0'?>", "", "<workbook>", "  <preferences>"]
    for name, kind, colours in palettes:
        rows.append(f"    <color-palette name=\"{name}\" type=\"{kind}\">")
        rows += [f"      <color>{c}</color>" for c in colours]
        rows.append("    </color-palette>")
    rows += ["  </preferences>", "</workbook>", ""]
    return "\n".join(rows)


def main(out):
    out = Path(out)
    out.mkdir(parents=True, exist_ok=True)
    every = [p for family in PALETTES.values() for p in family]
    (out / "Preferences.tps").write_text(tps(every))
    for family, pals in PALETTES.items():
        (out / f"{family}.tps").write_text(tps(pals))
    return every


def demo():
    every = main(sys.argv[1] if len(sys.argv) > 1 else "palettes")
    names = [p[0] for p in every]
    assert len(names) == len(set(names)), "palette names must be unique"
    for name, kind, colours in every:
        assert kind in {"regular", "ordered-sequential", "ordered-diverging"}, name
        assert all(len(c) == 7 and c.startswith("#") for c in colours), name
    print(f"{len(every)} palettes written")


if __name__ == "__main__":
    demo()
