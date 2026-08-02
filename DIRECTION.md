# DIRECTION.md — JalNetra visual & product direction

**Status:** accepted 2026-08-01. Items 1–9 in §3 are locked. Item in §4 is an open
question, not a decision.

**Scope:** this file owns *direction* — the reasoning behind the look, the layout, and
the signature interaction. `CLAUDE.md` owns the app spec and the data contract.
impeccable's `DESIGN.md` owns the final token values; what follows is the brief that
feeds it, not a competing palette.

**For the backend teammate:** §4 is the only thing here that touches your side. Nothing
in §1–3 changes `getFloodRisk()`.

---

## 0. Positioning, in one sentence

India's Meteorological Department already issues four-level colour-coded warnings —
Green / Yellow / Orange / Red — and calls a sub-24-hour forecast a **nowcast**.
JalNetra implements that exact official warning language at **street resolution**
instead of district resolution.

We are not inventing a risk vocabulary. We are implementing the national one, finer.

---

## 1. Research findings this direction rests on

Each of these earned a specific decision downstream; they are not decoration.

| Source | What we took |
|---|---|
| **IMD colour-coded warnings** — Green=No warning, Yellow=Watch, Orange=Alert, Red=Warning; "nowcast" = sub-24h forecast | The four-level ladder and its wording. Our contract's `safe\|watch\|high\|severe` *is* this ladder. |
| **Thevara–Perandoor (TP) Canal** — Kochi Corporation's main drainage artery: Panampilly Nagar → Kadavanthra → KSRTC → Kaloor → Perandoor Kayal. Silted, encroached, overflows at high tide. **Mullassery Canal has a reverse slope**, pushing water back into the TP Canal. | The canal layer. Our hotspots are strung along a real, named, failing drainage line — that's *why* they flood. |
| **Operation Breakthrough** — Kerala Irrigation Dept's anti-flooding project, phase four | Local vocabulary for dispatcher context. |
| **FAA / ATC display research** — red reserved for collision alert; **the alert blinks until the controller acknowledges it**; colour used strategically, never decoratively | The acknowledge mechanic. Unacknowledged severe pulses; acknowledgement stops it. An operational state made visible, not an animation added for delight. |
| **GOV.UK "Check for flooding"** — four severities written as *what + what-to-do* pairs; timestamped status; imperative language | Two-line legend and popup copy. Never a bare risk number. And a home for `generatedAt`. |
| **Google Flood Hub** — renders inundation extent *and depth* over real tiles, down to village scale | Depth in cm is the headline number; the 0–1 risk score is secondary. |
| **NOAA National Water Model / NWS FIM viewer** — layers named "Latest Analysis" vs "5-Day Max Forecast"; observed and predicted never blurred | Visual separation of observed "Now" from forecast +30…+120. |
| **Map UI Patterns — timeline slider** — tick marks, snapping, and *don't hide* filtered features; drop them to low opacity so context survives | Scrubber behaviour. |
| **Hackathon judging writeups** — "AI is table stakes, not a differentiator"; judges have seen a hundred GPT wrappers | Human-in-the-loop promoted from item 6 of 7 to near-top billing. |

---

## 2. The design

### 2.1 Palette — "wet asphalt at night"

Base is tinted ink, never pure black. The risk ramp is IMD's, adjusted for legibility
on dark.

**Amended 2026-08-01 by an accepted intensity pass.** The original values read
as muted to the point that Watch / Alert / Warning barely separated. Same hues,
pushed chroma — no new colours were introduced.

| Role | Value | Was | Note |
|---|---|---|---|
| Base | `#080D14` | `#0A0F16` | blue-tinted ink, not `#000` |
| Surface | `#101A24` | `#121B24` | panels floating on the map |
| Hairline | `#22323F` | `#1E2A36` | borders; `#2E4252` for the stronger tier |
| **Safe** | `#17E0CC` | `#3FB6AD` | cyan-teal — water-calm |
| **Watch** | `#FFC93C` | `#E5B23C` | IMD yellow, warmed |
| **Alert** | `#FF7A1A` | `#EF7A29` | IMD orange |
| **Warning** | `#FF2E4D` | `#E03A38` | IMD red — **the only fully saturated colour in the app** |
| Text | `#EAF2F8` | `#E4EDF4` | muted: `#93A5B3` (raised for contrast) |
| **Human** | `#B26BFF` | `#A78BFA` | violet — see below |

**The rule that carries the thesis:** everything the AI produces uses the risk ramp.
Everything a human does — the citizen's dropped pin, the dispatcher's acknowledgement —
uses violet, deliberately *outside* the ramp. Two visual systems coexisting on one
screen. The Human × AI argument becomes legible before anyone reads a word of it.

**Declared deviation:** safe is cyan, not IMD's literal green. Green on a dark map reads
"go" and fights the basemap. Label it "Safe / No warning" so the mapping to IMD stays
explicit and honest.

**Saturation discipline:** red appears rarely. Most zones sit quiet most of the time.
When red arrives it has to mean something.

### 2.2 Type

- **Archivo** — wordmark and section headers. Institutional, signage-like; reads as
  infrastructure, not as a startup.
- **IBM Plex Sans** — all UI. Designed for technical and operational contexts.
- **IBM Plex Mono** — every number. Tabular by default, so digits don't jitter as the
  scrubber animates values. Non-negotiable given how much our numbers move.
- **Noto Sans Malayalam** — for bilingual zone names (`Kaloor / കലൂർ`).
  **Corrected 2026-08-01:** this originally specified *IBM Plex Sans Malayalam*,
  which **does not exist** — Google Fonts returns HTTP 400 for it. Malayalam text
  was silently falling back to an arbitrary system font. Noto Sans Malayalam is
  the systematic, neutral substitute and is the right register for Operate.

### 2.3 Layout — console, not page

Full-bleed map as substrate. Panels float *on* it with real edges. **No nested cards.**

```
┌──────────────────────────────────────────────────────────┐
│ JALNETRA   Nowcast issued 10:04 IST · valid to 12:04     │  status strip
├────────────┬───────────────────────────────┬─────────────┤
│ RAINFALL   │                               │ ZONES ↓risk │
│ scenario   │        KOCHI  (map)           │ ─────────── │
│ ──────○──  │     canal layer beneath       │ alert feed  │
│            │                               │             │
├────────────┴───────────────────────────────┴─────────────┤
│  NOW ──── +30 ──── +60 ──── +90 ──── +120     [▶ RUN]    │  the hero
└──────────────────────────────────────────────────────────┘
```

The scrubber gets full width along the bottom — the most horizontal real estate on
screen, because it's what we want people looking at.

**Mobile:** map on top, controls collapse to a bottom sheet, scrubber pinned above it.

### 2.4 The ONE signature moment — "the two-hour sweep"

A single **RUN** control sweeps 0 → 120 min over ~6 seconds. During the sweep:

1. A thin light-line travels the scrubber track; the head moves on custom easing.
2. Zones don't just recolour — **they fill.** Fill height and opacity interpolate
   continuously. Water rising, not a palette swap. Colour crosses IMD thresholds as it
   goes.
3. As each zone crosses into Alert or Warning, an entry **drops into the feed**,
   staggered 30–80 ms, and the zone emits **one** pulse ring — then stops. Pulsing
   continues only on *unacknowledged severe*.
4. Counters count up in tabular mono — population at risk, worst zone, depth. Zero
   layout shift.
5. It settles: *"+120 min · 4 zones in Warning · 61,200 people at risk."*

Six seconds, one gesture, static map → story, every number traceable to the contract.

**Craft constraints (pre-empting emil-design-eng):**
- **Transitions, not keyframes** — dragging retargets rather than restarts.
- The sweep stays **interruptible**; grabbing the scrubber mid-run takes over immediately.
- UI chrome < 300 ms. The sweep itself is longer because it's *content*, not chrome.
- `prefers-reduced-motion` → values snap, opacity only, no movement, no pulse.

**Second-read moment:** the canal line. First glance, a subtle stroke beneath the zones.
Second glance — every flooding zone is strung along it.

### 2.5 SECOND signature moment — the zone diorama

**Accepted 2026-08-01.** Opening a zone's popup offers a **street-level view**: a
full-screen Three.js scene of that zone with water risen to its predicted
`depthCm` at the current rainfall and horizon.

**This is stylized and illustrative. It is NOT literal 3D terrain, and that
distinction must not be lost later.** The street, the building silhouettes, and
the figure are abstractions with exactly one job: giving the depth number a
human scale. Nothing in the scene is surveyed, and no elevation data exists
behind it. The on-screen label says so, and so does the code comment above the
module.

- The figure is **1.72 m tall** and is the scale reference the whole scene
  exists for. 41 cm of water reading as mid-shin on a person is the point.
- Water colour is the zone's IMD level colour, so the diorama and the map agree.
- Rain density is driven by the rainfall control, tying the scene to the console.
- Depth is labelled in cm on screen and is the contract's `depthCm` — the
  provenance principle applies here exactly as it does on the map.
- Layout per zone is **deterministic** (seeded from the zone id), so a zone looks
  the same every time. Demos stay repeatable.
- **Three.js r128, vendored at `vendor/three.r128.min.js`** — no network at
  runtime. r128 has no `CapsuleGeometry`; the figure is cylinders and a sphere.

**It reads `depthCm` and adds no fields to the data contract.**

---

## 3. Accepted changes to the spec (1–9, locked)

1. **Adopt IMD wording in the UI.** Contract ids stay frozen (`safe|watch|high|severe`);
   display "No warning / Watch / Alert / Warning." Add GOV.UK-style consequence lines
   under each.
2. **Safe becomes cool cyan, not green.** Only severe gets full saturation.
3. **Reserve violet for human actions** — outside the risk ramp entirely.
4. **Add the canal layer** — TP Canal + Mullassery Canal. Consider adding
   **Kadavanthra** to the zone list; it sits directly on the TP Canal and is currently
   missing from `CLAUDE.md`.
5. **Depth becomes the hero number**; the 0–1 risk index is secondary.
6. **Distinguish observed from forecast.** "Now" is observed; +30…+120 are predicted.
   Different border treatment.
7. **Surface `generatedAt`** as "Nowcast issued HH:MM IST · valid to HH:MM."
8. **Scrubber gains** a play control, keyboard ← →, tick marks, snapping, and
   low-opacity (not hidden) inactive states.
9. **Promote human-in-the-loop.** Currently item 6 of 7 in the `CLAUDE.md` component
   list; it should sit near the top. If AI is table stakes, the human layer is the
   differentiator and deserves proportional screen weight.

None of these change `getFloodRisk()`.

### Accepted 2026-08-01 — intensity pass and diorama (10–13)

10. **Full-bleed map with a floating HUD**, replacing the even three-column grid.
    Rails are deliberately unequal (244 px left, 356 px right) and the scrubber
    floats between them. This is not new invention — §2.3 above already specified
    "full-bleed map as substrate, panels float on it with real edges"; the first
    build quietly opted out of it.
11. **Saturation raised across the risk ramp and the human violet** (§2.1 table).
    Statement type for the hero numbers — city risk index at 52 px, popup depth
    at 44 px, diorama depth at 92 px, Archivo 800/900.
12. **Legend moved out of the map overlay** into a collapsible left-rail
    disclosure, collapsed by default. Data provenance sits beside it in the same
    pattern.
13. **The zone diorama** (§2.5) as the second signature moment.

**Rejected during the same pass:** a perspective-raked grid overlay on the map.
The mechanical detector flagged it, and the reasoning holds — a tinted grid over
real geography on a public-safety console reads as if it *means* something, and
it measures nothing. A false measurement affordance is worse than a flat map.
The depth cue is now atmospheric falloff only (`.map-grade`), which does the same
job of pushing the edges back without inventing a coordinate system.

---

### Accepted 2026-08-01 — calibration, transition, and two new surfaces (14–19)

14. **Depth bands widened to 10 / 25 / 50 cm** (from 5 / 15 / 30), anchored to
    what water does to a street. At the default Heavy scenario the worst zone
    now peaks at 41 cm / risk 0.55 with **zero** Warning zones; Cloudburst
    brings **three** zones over. Red kept scarce, and 92/120 mm/hr now have
    somewhere worse to go.
    *Consequence to tell the backend: `CLAUDE.md`'s worked example still
    produces `depthCm: 41` exactly, but that depth now classifies as Alert
    rather than severe.*
15. **`risk` rescaled to `depth / 75`** so band edges land on 0.13 / 0.33 /
    0.66. "risk ≥ 0.66 means Warning" is now true by construction instead of
    being a second scale that disagreed with the depth bands.
16. **Susceptibilities respread** (0.95 → 0.22, same ranking, same high/med/low
    grouping from `CLAUDE.md`). The originals clustered five zones at
    0.85–0.92, which no exponent could separate — the city either went entirely
    red or entirely dry.
17. **"Now" carries antecedent water.** The accumulation curve started at 7% of
    saturation, i.e. it assumed rain began the instant you pressed play. A
    nowcast issued during a cloudburst must show water already on the street.
18. **Diorama palette rebuilt on five distinct hue families** — indigo sky,
    cool slate buildings, *warm* asphalt road, warm concrete pavement, vivid
    level-coloured water, violet figure. The earlier version was five shades of
    one blue and read as black. Buildings gained varied footprints, setbacks,
    low-rise rhythm and plinths; the figure was rebuilt at ~7.5-head
    proportions with shoulders, arms and neck; lampposts were moved onto the
    kerb line.
19. **Map → street-level transition.** Map scales toward the zone while a
    blackout veil fades up (400 ms), the swap happens at full black, then the
    diorama fades in as the camera eases forward (320 + 620 ms). Water is
    already at depth on arrival — the answer, not a filling tank. Exit reverses
    in ~500 ms, faster than entry. Total under the 1200 ms ceiling.

### Surfaces beyond the console

- **`login.html`** — demo gate. Performs **no authentication**; any input opens
  the console, and the page says so on screen. Split layout: the product's
  argument on the left, the gate on the right.
- **`admin.html`** — zone configuration and model status. Deliberately separate
  from the console: a dispatcher mid-event must not be able to change a
  susceptibility by accident. Writes to `localStorage`; the console reads the
  same key.
- **`vendor/tokens.css`** — the palette and type tokens now live in one file
  linked by all three pages, so they cannot drift.

### Final layout — accepted 2026-08-01

Implements the Figma frame **"JalNetra Console Clean"** (file
`6cnkPwwW9utcjgPTwmuJkP`, node `1:4`, 1440×900). Measurements were read from
the file, not estimated:

| Region | Figma node | Size | Position |
|---|---|---|---|
| Hero · Action | `1:5` | 812 × **135** | 16, 16 |
| Citizen · Reports | `1:9` | 472 × **95** | 16, 165 |
| Map · Kochi | `1:13` | **1000** × 280 | 16, 255 |
| Scrubber · Timeline | `1:15` | 1000 × **60** | 16, 840 |
| Right Rail | `1:17` | **320** × 900 | 1100, 0 |

Built as a CSS grid — `1fr + 320px`, 16px gaps, status strip spanning both
columns — rather than absolute positioning, so it survives other viewports.

**Top to bottom:**

1. **Status strip**, 56px. JALNETRA wordmark, nowcast issued/valid, Simulated
   chip, offline indicator, three stats (deepest depth, population in Warning
   zones, risk index), and Admin / Sign out navigation.
2. **Hero action card**, 135px. `#101A24` ground, 1px border in the *current
   level colour* (yellow at Watch), 24px sides / 16px top-bottom. The state
   word is **52px Archivo Black** — Figma's text node measured 57px tall.
   Below it, the action line at 14px with a bold `Bring:` prefix.
3. **Citizen reports**, 472px wide, 95px tall. `#101A24` with a 2px violet
   border. Title 12px Archivo uppercase in violet, counts by zone, and the
   report control.
4. **Rainfall scenario**, ~512px, in the slot beside the citizen card. Slider
   plus six presets: Dry / Drizzle / Moderate / Heavy / Very heavy / Cloudburst.
5. **Map**, 1000px wide, filling the remaining height. **No depth badges on the
   map** — permanent badges collided wherever zones sit close together, so depth
   lives in the rail list. The citizen report control floats bottom-left over it.
6. **Scrubber**, 60px, full width of the content column. Horizon readout,
   observed/forecast marker, track with five stops, RUN control, and Legend /
   Sources disclosures.
7. **Right rail**, 320px. Zones by depth and Alert feed *only*, as two
   independently scrolling panes so a 13-row zone list can never push the feed
   off the bottom.

**Three deviations from the Figma frame, all so the console stays operable:**

- **The frame contains no rainfall control.** Without one the scenario can never
  change and the hero can never escalate — the core interaction. It takes the
  ~512px slot the frame leaves empty beside the 472px citizen card, which is
  what explains that card being narrower than the 812px hero.
- **The frame leaves 305px empty** between the map bottom (y=535) and the
  scrubber (y=840). The map fills it.
- **The frame has no status strip.** The wordmark, offline badge, stats and
  navigation were all accepted earlier and are kept.

One further departure: the hero runs the full 1000px rather than the frame's
812px. At 812 it leaves a 188px void beside it, which reads as unfinished.

## 4. OPEN QUESTION — not decided, do not implement

**Tide state.** Kochi's canals back up **at high tide** — a real, cited driver of
waterlogging, and the TP Canal's documented overflow behaviour depends on it. Modelling
it would be physically honest and is something no competing team is likely to have.

**Why it's parked:** it would change the shared data contract, and the contract is the
seam between frontend and backend. Sent to the backend teammate for a decision first.

Until that comes back: **`getFloodRisk()` is unchanged.** No tide field, no tide UI, no
speculative stubs.

---

## 5. Quality floor (inherited from CLAUDE.md, restated because it's non-negotiable)

Responsive to mobile · visible keyboard focus · `prefers-reduced-motion` respected ·
deterministic mock so demos never surprise us · every number on screen traceable to the
contract.

---

## Sources

- [IMD Colour-Coded Warnings — Drishti IAS](https://www.drishtiias.com/daily-updates/daily-news-analysis/imd-colour-coded-warnings)
- [IMD District-Wise Nowcast Warnings](https://mausam.imd.gov.in/responsive/districtWiseNowcastGIS.php)
- [Flood Mitigation Kochi — Kerala Irrigation Dept (PDF)](https://irrigation.kerala.gov.in/sites/default/files/2021-08/kochiflood.pdf)
- [Despite frequent flooding risk, Kochi still lacks drainage master plan — The News Minute](https://www.thenewsminute.com/kerala/despite-frequent-flooding-risk-kochi-still-lacks-drainage-master-plan-166481)
- [Colour Usability on Air Traffic Control Displays](https://www.researchgate.net/publication/253111803_Color_Usability_on_Air_Traffic_Control_Displays)
- [A Standardized Color Palette for Terminal Situation Displays (DOT)](https://rosap.ntl.bts.gov/view/dot/71713/dot_71713_DS1.pdf)
- [Check for flooding — GOV.UK](https://check-for-flooding.service.gov.uk/)
- [Flood alerts and warnings — GOV.UK](https://check-for-flooding.service.gov.uk/alerts-and-warnings)
- [Expanding our ML-based flood forecasting — Google](https://blog.google/innovation-and-ai/products/expanding-our-ml-based-flood-forecasting/)
- [About the National Water Model — NOAA](https://water.noaa.gov/about/nwm)
- [NWS FIM Viewer Instructions (PDF)](https://www.weather.gov/media/owp/operations/nws_fim_viewer_instructions.pdf)
- [Timeline slider — Map UI Patterns](https://mapuipatterns.com/timeline-slider/)
- [Color map design for visualization in flood risk assessment — IJGIS](https://www.tandfonline.com/doi/full/10.1080/13658816.2017.1349318)
- [Hackathon judging: 6 criteria to pick winning projects — TAIKAI](https://taikai.network/en/blog/hackathon-judging)
- [Public Alert System — KSDMA](https://sdma.kerala.gov.in/public-alert-system/)
