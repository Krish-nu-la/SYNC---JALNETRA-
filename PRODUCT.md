# Product

<!-- impeccable:product-schema 1 -->

## Platform

web

## Stack

Vanilla JS and CSS, no build step. Map is Leaflet with CartoDB `dark_matter`
tiles (keyless). Chosen by the user, not delegated — the reasons are stage
reliability, trivial handover, and no build tooling to fail during a live demo.
No secrets or API keys in the repo.

**Everything is vendored** in `vendor/`: Leaflet 1.9.4 + CSS + control images,
Three.js r128, and 16 self-hosted woff2 font subsets. There is **no network
dependency at runtime**. This follows directly from the stage-reliability reason
above — an earlier build loaded Leaflet from a CDN, which meant a slow or absent
network produced a blank page rather than a degraded one. The map bootstrap is
now wrapped so the console renders its forecast even with no basemap at all.

## Surfaces

Three pages, deliberately separated:

- **`login.html`** — a demo gate. No authentication exists and the page states
  that plainly; it frames the console as an operational tool rather than a toy.
- **`index.html`** — the dispatcher console. Live operations only.
- **`admin.html`** — zone configuration and model status. Separate on purpose:
  configuration and live operation are different jobs, and a dispatcher during
  an event should not be able to edit a susceptibility value by accident.

## Users

**Primary: a municipal dispatcher / operations officer**, monitoring Kochi city-wide
during a rain event, deciding where to send crews. The product opens directly into their
console view.

**Embedded second role: a citizen on the ground**, reporting observed waterlogging. This
is *not* a separate mode or a second screen — the citizen action lives inside the same
console as an inbound signal. The two roles coexisting on one surface is deliberate: it
is what makes the Human × AI relationship visible rather than asserted.

**Evaluating audience: SYNC 2026 judges** (Ahalia School of Engineering and Technology,
national-level Human × AI Hackathon). They are a real constraint on the design, not the
product's users — see Operating Context.

## Product Purpose

JalNetra forecasts **street-level flood risk for Kochi, Kerala over the next ~2 hours**
from rainfall, terrain, and drainage, and puts it on a live map someone can act on.

Kochi is Kerala's most flood- and waterlogging-affected city. Existing official warnings
are issued at **district** resolution, which is too coarse to tell anyone which junction
will be impassable. Success is a dispatcher looking at the screen and knowing *which
specific zone* to move on, and in how many minutes.

The thesis: the forecast is AI, the action is human. AI flags risk, a citizen confirms
ground truth, a dispatcher acts.

## Positioning

India's Meteorological Department already issues four-level colour-coded warnings —
Green (No warning) / Yellow (Watch) / Orange (Alert) / Red (Warning) — and its own term
for a sub-24-hour forecast is a **nowcast**.

JalNetra implements that exact official warning vocabulary at **street resolution
instead of district resolution.** It does not invent a risk language; it refines the
national one. A neighbouring project can build a flood model, but claiming continuity
with IMD's issued warning ladder requires actually matching it.

Second, non-copyable element: the forecast is grounded in Kochi's *named, documented*
drainage failure — the Thevara–Perandoor Canal and the reverse-sloped Mullassery Canal —
not in generic terrain.

## Operating Context

**The build context is a hackathon, and it shapes real requirements.** The product will
be evaluated twice over, in two different ways, and must hold up in both:

1. **Narrated on a projector**, with the user driving and judges watching from a
   distance. Needs a single obvious focal point per moment and to read from across a
   room.
2. **Then handed over**, with judges exploring unguided on a laptop in whatever order
   they choose. Needs self-evident affordances, an obvious first action, and no state it
   can be poked into that leaves it looking broken.

Assume no hand-holding after the first two minutes. This is the higher bar of the two
and it governs.

The scenario the product depicts: a rain event in progress, a dispatcher watching risk
develop over a 0–120 minute horizon, adjusting a rainfall scenario to ask "what if it
gets worse."

## Capabilities and Constraints

- **This repo is the frontend only.** A teammate owns the hydrology model, the ML depth
  model, and rainfall ingestion.
- **The seam between the two is one function:** `getFloodRisk(rainfallMmHr,
  timeOffsetMin)`. Its shape is frozen and specified in `CLAUDE.md`. The UI never calls a
  backend directly. Swapping mock for real means replacing that function's body and
  nothing else.
- **The mock must be deterministic**, so a demo never surprises us.
- **Every number displayed must be traceable to the contract.** No decorative figures.
- No persistence, no accounts, no backend calls, no API keys.
- Terminology is IMD's: *nowcast*, and the Watch / Alert / Warning ladder.
- **Undecided:** whether tide state enters the model. Kochi's canals back up at high
  tide and it is a real driver of waterlogging, but adding it changes the shared data
  contract. The question is with the backend teammate; until it returns, `getFloodRisk()`
  is unchanged and no tide UI or stub exists. Tracked in `DIRECTION.md` §4.

## Brand Commitments

- **Name: JalNetra** ("water-eye"). Chosen over the alternative FloodLens Kochi.
- **`DIRECTION.md` is binding** and is the authority for palette, typography, layout
  concept, and the signature interaction. It was researched and accepted before this
  file was written; treat its decisions as constraints, not suggestions. It is not
  restated here.
- Voice: operational and plain. Public-safety register — warnings are written as a
  *what* plus a *what-to-do*, in the manner of GOV.UK's flood service, never as a bare
  score.
- The product is a control room, not a landing page. Restraint is what reads as
  trustworthy in this category.

## Evidence on Hand

Provenance is **mixed**, and the distinction has to survive into the UI because judges
will explore it unguided and may ask where a number came from.

**Real and citable:**
- The hotspot list and approximate coordinates for the twelve Kochi zones, drawn from
  news reporting on actual waterlogging. Kalamassery, Kaloor, and Edappally are
  documented as worst-hit.
- The Thevara–Perandoor Canal's route (Panampilly Nagar → Kadavanthra → KSRTC → Kaloor →
  Perandoor Kayal), its siltation and encroachment, and the Mullassery Canal's reverse
  slope — all from Kerala Irrigation Department material and press coverage. Operation
  Breakthrough is the state's real anti-flooding project.
- IMD's four-level warning ladder and its definition of "nowcast".
- Sources are listed in `DIRECTION.md`.

**Estimated, not sourced:**
- Per-zone population figures. These are approximations, not census or ward data.
- Per-zone `baseSusceptibility` values. These are authored to be physically plausible,
  not derived from a DEM.

**Does not exist and must never be implied:**
- Any live rainfall feed. There is none.
- Any real model output. Every figure the UI shows today comes from a deterministic
  mock.
- Any deployment, agency partnership, endorsement, or user base. Nothing of the kind
  exists and no copy may suggest it.

The honest framing is available and is stronger than a fake one: the *geography* is
real, the *warning vocabulary* is real, the *drainage failure* is real, and the forecast
is a working simulation pending the model. Future work states this rather than blurring
it.

## Product Principles

1. **Every number is traceable.** If it's on screen, it came from the contract or it
   doesn't ship. This is a public-safety tool; an unsourced figure is a defect.
2. **Real geography beats plausible geography.** Kochi's actual canals, actual hotspots,
   actual failure modes. Specificity is the whole advantage and it is not reusable by
   anyone who didn't do the reading.
3. **Say what's simulated.** Honest labelling of mock data is a credibility asset in
   front of judges, not a weakness to hide.
4. **The human layer is the product, not a feature.** A forecast alone is table stakes.
   What's defensible is that a citizen's observation and a dispatcher's decision are
   first-class on the same screen as the model's output.
5. **Restraint is the register.** Saturated colour, motion, and emphasis are scarce
   resources spent on what is genuinely urgent. A control room that shouts everywhere
   communicates nothing.

## Accessibility & Inclusion

- Responsive down to mobile.
- Visible keyboard focus throughout; the time scrubber is keyboard-operable.
- `prefers-reduced-motion` respected — the signature animation degrades to opacity and
  snapped values with no movement.
- Risk level must never be conveyed by colour alone; the IMD ladder carries a text label
  wherever it appears.
- Kochi is a Malayalam-speaking city. Bilingual zone labelling (English / Malayalam) is
  intended; `DIRECTION.md` records the type decision that supports it.
