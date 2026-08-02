# REFERENCES.md — what was measured, and what it changed

Measurements taken **programmatically** from the images in `references/` (PIL edge
detection and pixel sampling), not estimated by eye. Where a measurement could not
be taken, that is stated rather than guessed.

---

## Important limitation, stated up front

**None of the nine references contains a hero action card.** They are map
dashboards: Google Flood Hub (×4), Flood4Cast, one dark medical-monitoring
dashboard, and three 3D city renders. Not one has an emergency-instruction
element.

So "hero card height / padding / type size from Reference 1" **cannot be read off
these images.** Any number presented as such would be invented and falsely
attributed. What follows is what the references actually contain.

---

## UI references

### R1 — Dark medical monitoring dashboard (Dribbble), 3024×1964

The closest analogue to JalNetra: dark theme, map substrate, floating data cards.

| Measured | Value |
|---|---|
| Icon rail width | 68 px (displayed) |
| Left card column | ~355 px, 26% of content width |
| Map area | ~857 px |
| Page background | `rgb(76,75,82)` |
| Card background | `rgb(27,26,29)` — cards are **darker** than the page |
| Card border | `rgb(30,30,32)`, barely-there 1 px |
| **Map pixels with saturation > 40** | **2.0%** |

**The finding that matters:** 98% of the map is neutral grey. Only the two or
three objects actually alerting carry colour — one orange cluster, one green.
Everything else is unlit dark blocks.

### R2 — Google Flood Hub (Bangladesh, Niger, Brazil), ~1160–1180 px wide

| Measured | Bangladesh | Niger | Brazil |
|---|---|---|---|
| Left data panel | 319 px | 292 px | — |
| Right options panel | 204 px | 166 px | 245 px |

Consistent pattern: a **~300 px** data panel and a **~200 px** options panel.
Severity always ordered Extreme → Danger → Warning → No data → Normal, rendered
as a coloured dot plus a label. Threshold lines are drawn as horizontal rules
across the forecast chart, and a dashed vertical "Now" line splits observed
(solid) from forecast (dotted).

### R3 — Flood4Cast Vlaams-Brabant, 1170×608

No detectable panel edges at all — the interface is a small radio group, a
bottom-edge timeline, and a compact legend. Chrome occupies roughly 5% of the
screen. The most restrained reference in the set.

---

## 3D city references

Sampled in HSL so hue families and lightness could be compared numerically.

### R-A — New York 3D, 3024×1964

| Surface | RGB | HSL |
|---|---|---|
| Water | `168,200,251` | 217°, 91%, **82%** |
| Ground / street | `229,225,223` | 20°, 10%, **89%** |
| Building, lit face | `105,107,125` | 234°, 9%, **45%** |
| Building, shadow face | `24,29,34` | 210°, 17%, **11%** |

- **Hue span: 214°** across four families.
- **Lightness spread: 11% → 89% = 78 points.**
- **Lit vs shadow on the same building: 34 points.**

### R-B — TMC Helix Park isometric

Near-monochrome, so it carries *no* hue information — its legibility is entirely
value-driven, which corroborates R-A. Silhouette variety is extreme: towers,
low slabs, curved blocks and stepped forms in one frame.

---

## What actually changed, and what did not

### Already matching — no change made

**Map colour restraint.** JalNetra measured at **2.0% saturated map pixels**,
identical to R1's 2.0%. The zone circles are semi-transparent, so they tint
without saturating. This principle was already satisfied and was left alone
rather than "fixed".

**Hue separation in the diorama.** JalNetra's hue span measured **232°** against
R-A's 214° — already wider. Sky 273°, buildings 210°, water 220°, lamps 41°,
figure 300°. Four-plus families confirmed present.

**Panel widths.** JalNetra's rails are 244 px and 356 px against Flood Hub's
~300 px and ~200 px. Same order; the right rail is wider because it carries two
scrolling lists rather than toggles. Left unchanged.

### Changed, because the measurement showed a real gap

**Diorama lightness separation.** This was the one genuine failure.

| | R-A reference | JalNetra before |
|---|---|---|
| Overall lightness spread | 78 pts | **32 pts** |
| Lit vs shadow, same building | 34 pts | **6 pts** |

Six points of facet contrast is why the buildings read as flat slabs. The cause
was the hemisphere light flooding every face at 1.25 intensity, drowning the
directional key.

- Hemisphere 1.25 → 0.70
- Ambient 0.50 → 0.28
- Key directional 1.05 → 1.45
- Building base lightened `#3E5364` → `#4A6274`, top `#6B86A2` → `#8AA6C2`
- Ground darkened `#4A4640` → `#3B3833`, road `#33302E` → `#252220`

**Silhouette variety**, from R-A and R-B showing 4-storey blocks beside towers:
heights `7–30 m` → `7–38 m`, low-rise `3.5–7.5` → `3–7.5`, widths `3.5–10` → `3–11`.

**Figure legibility.** Emissive intensity 0.9 → 0.35 (the glow was flattening it
into a lit blob), arms moved out `±0.185` → `±0.225` with more splay, own point
light 0.85 → 0.5. It now reads as head / shoulders / arms / torso standing in
water rather than a container.

---

## Honest assessment against the references

JalNetra is a **dark night scene** by `DIRECTION.md` commitment. R-A is a
**daylight render** with an 89%-lightness ground. Matching its absolute values
would mean abandoning the committed visual world, so the ratios were carried
across into the dark band rather than the raw numbers. Post-change spread is
~35–40 points, not 78, and it will not reach 78 while the scene stays at night.
That is a deliberate limit, not an oversight.
