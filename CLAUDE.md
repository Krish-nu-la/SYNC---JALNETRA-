# CLAUDE.md — SYNC 2026 Flood Nowcasting (Frontend)

## What this is
A real-time **urban flood nowcasting** web app for **Kochi, Kerala** — the most
flood- and waterlogging-affected city in the state. It forecasts *street-level*
flood risk over the next ~2 hours from rainfall + terrain + drainage, renders it
on a live map, and lets a human act on it.

Built for **SYNC 2026 — Human × AI Hackathon** (national level). The required
deliverable is a working interactive website. This repo is the frontend.

**Thesis:** the decision comes from physics + ML; the *forecast* is AI, the
*action* is human. AI flags risk, a citizen reports ground truth, a dispatcher
acts. Keep the human-in-the-loop framing visible in the UI.

## My role
I own the **frontend / UI** only. A teammate owns the backend (hydrology model +
ML depth model + rainfall ingestion). **Do not build backend logic here.** The UI
must run fully standalone against mock data and integrate later via ONE function.

## Tech decisions
- **Framework:** single-file `index.html` + vanilla JS/CSS. Reliable on stage,
  trivial handover, no build step. (Precedent: my GuardRail hackathon build.)
  *If asked to switch to React/Vite later, keep the data contract identical.*
- **Map:** Leaflet + CartoDB **dark_matter** tiles. Real, credible, dark
  aesthetic. Risk zones as colored polygon/circle overlays on top.
  *Fallback if network is a stage risk: pre-baked static tile / stylized map.*
- No secrets, no API keys committed. Tiles are keyless.

## THE DATA CONTRACT (build the whole UI against this)
The UI never calls the backend directly. It calls one async function whose shape
is frozen now. Backend swap = replace the body, nothing else changes.

```js
// Returns flood risk for every zone at a given rainfall + time offset.
// rainfallMmHr: number (0–120)   timeOffsetMin: 0 | 30 | 60 | 90 | 120
async function getFloodRisk(rainfallMmHr, timeOffsetMin) {
  // MOCK now → real fetch() later. Contract below must not change.
  return {
    generatedAt: "2026-08-01T10:00:00Z",
    rainfallMmHr: 62,
    timeOffsetMin: 60,
    zones: [
      {
        id: "kaloor",
        name: "Kaloor",
        lat: 9.997, lng: 76.299,
        risk: 0.82,               // 0–1
        level: "severe",          // safe | watch | high | severe
        depthCm: 41,              // predicted standing-water depth
        population: 18400,        // people in zone (for "at risk" stat)
        trend: "rising"           // rising | steady | falling
      }
      // ...one object per zone
    ]
  };
}
```

Mock rule of thumb (physically plausible): risk rises non-linearly with rainfall,
low-lying zones (higher `baseSusceptibility`) flood first, and higher
`timeOffsetMin` accumulates more depth. Seed each zone with a
`baseSusceptibility` 0–1 and derive `risk`/`depthCm` from rainfall × offset ×
susceptibility. Keep it deterministic so the demo is repeatable.

## Kochi zones (seed data — approx coords, refine later)
Real waterlogging hotspots from news reports. Kalamassery, Kaloor, Edappally are
explicitly the worst-hit.

| id            | name             | lat     | lng     | susceptibility |
|---------------|------------------|---------|---------|----------------|
| kalamassery   | Kalamassery      | 10.054  | 76.320  | high           |
| edappally     | Edappally        | 10.025  | 76.308  | high           |
| kaloor        | Kaloor           | 9.997   | 76.299  | high           |
| palarivattom  | Palarivattom     | 10.007  | 76.305  | high           |
| vyttila       | Vyttila          | 9.967   | 76.318  | high           |
| elamkulam     | Elamkulam        | 9.973   | 76.301  | med            |
| cbd_mgroad    | CBD / MG Road    | 9.978   | 76.283  | high           |
| marinedrive   | Marine Drive     | 9.982   | 76.276  | med            |
| kacheripady   | Kacheripady      | 9.985   | 76.283  | med            |
| panampilly    | Panampilly Nagar | 9.965   | 76.295  | med            |
| thevara       | Thevara          | 9.942   | 76.292  | med            |
| vennala       | Vennala          | 9.998   | 76.323  | low            |

## UI components to build
1. **Map (hero)** — Kochi, dark tiles, zones as risk-colored overlays. Popups on
   click: name, depth, population, trend.
2. **Rainfall control** — scenario slider (drizzle → cloudburst, 0–120 mm/hr).
   Named presets are friendlier than raw numbers.
3. **Time scrubber** — Now / +30 / +60 / +90 / +120 min. Dragging re-runs
   `getFloodRisk` and animates the map. This is the "make the room go quiet" moment.
4. **Risk dashboard** — ranked list of affected zones, total population at risk,
   worst zone, city-wide risk index.
5. **Alert feed** — live-style entries as zones cross into high/severe.
6. **Human-in-loop** — (a) citizen "Report waterlogging here" (drops a pin,
   nudges nearby risk), (b) dispatcher "Acknowledge / dispatch" on an alert.
7. **Legend** — the 4 risk levels + what depth each maps to.

## Design direction
Dark, operational, credible — a control room, not a landing page. This is a
public-safety tool; restraint reads as trustworthy. Spend boldness on ONE thing:
the time-scrubber animation of risk spreading across the map. Everything else quiet.
- Give it its own identity — NOT a reuse of GuardRail's palette. Pick a water/
  hydrology-grounded scheme (deep ink base; a cool "safe" hue; risk ramp that
  reads instantly: calm → amber → red for severe).
- Pair a characterful display face with a clean data/UI face. Numbers are the
  content here — set them well (tabular figures for the dashboard).
- Working name options: **JalNetra** ("water-eye") or **FloodLens Kochi**.

## Design skills — three layers, different mechanics
Three design tools installed. They work DIFFERENTLY — don't treat them the same,
don't run all three on one element at once. Same ecosystem (Emil sponsors taste),
so their rules align. Sequence, don't stack.

### 1. taste-skill (`design-taste-frontend`) — auto-loading baseline
Loads automatically and shapes generation as you build; you don't invoke it.
Install: `npx skills add https://github.com/Leonxlnx/taste-skill --skill "design-taste-frontend"`
Tune the 3 dials at the top of its SKILL.md for a control-room dashboard (NOT a
landing page):
- `DESIGN_VARIANCE 5` — structured, not wild-asymmetric
- `MOTION_INTENSITY 6` — scrubber earns motion; rest restrained
- `VISUAL_DENSITY 7` — data-dense dashboard

### 2. impeccable — command system + passive anti-slop detector
NOT a one-shot review. It's `/impeccable <command>` (23 commands) plus a hook
that auto-flags slop on every UI edit (no Inter, no gray-on-color, tint blacks,
no nested cards, no bounce easing).
Install: `npx impeccable install` → then `/impeccable init` → choose **PRODUCT**.
`init` writes PRODUCT.md + DESIGN.md = single source of truth for audience, voice,
colors, type. **Let impeccable's DESIGN.md own the visual tokens; this CLAUDE.md
owns the app spec + data contract.** (Avoids two conflicting palettes.)
Command order for this build:
- `/impeccable shape` — plan UI before code
- build against the data contract
- `/impeccable critique` — UX review (hierarchy, clarity)
- `/impeccable typeset` · `/impeccable layout` · `/impeccable colorize` — targeted
- `/impeccable audit` — a11y + responsive + perf
- `/impeccable polish` — shipping pass

### 3. emil-design-eng — deep animation craft, narrowest scope
Reserve for the **signature time-scrubber** + micro-interactions. `/impeccable
animate` covers general motion; use Emil for the one moment that must be perfect.
Invoke by name AND with a target: *"Use emil-design-eng to review the scrubber
animation in index.html."* (Bare invocation just returns an intro.)
Emil enforces (pre-empt so it has less to fix):
- Custom easing, never `ease-in` on UI, never `transition: all`.
  `--ease-out: cubic-bezier(0.23,1,0.32,1)`; `--ease-drawer: cubic-bezier(0.32,0.72,0,1)`.
- UI animations < 300ms. Enter `ease-out`. Exit faster than enter.
- Rapid actions → transitions not keyframes (retarget vs restart).
- Popovers scale from trigger origin, start `scale(0.95)`+`opacity:0`, never `scale(0)`.
- Stagger list entries 30–80ms; `prefers-reduced-motion` drops movement, keeps opacity.

**Division of labor:** taste = baseline while generating · impeccable =
structured critique→polish + auto-detector · emil = the hero animation.

## Quality floor (non-negotiable)
Responsive to mobile · visible keyboard focus · `prefers-reduced-motion`
respected · deterministic mock so demos never surprise you · every number on
screen traceable to the contract.

## Out of scope for this repo
Hydrology / DEM / flow-accumulation · ML depth model · real rainfall API ·
persistence. Those are the backend teammate's. The seam between us is
`getFloodRisk()` — keep it clean.
