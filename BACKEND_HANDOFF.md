# BACKEND_HANDOFF.md — JalNetra

For whoever owns the hydrology model, the ML depth model, and rainfall ingestion.

**The short version:** the frontend already works end to end against a
deterministic mock. There is exactly one function between your side and mine.
Replace its body, change nothing else, and the console runs on real forecasts.

Visual version of everything below:
**[JalNetra — System Architecture (FigJam)](https://www.figma.com/board/bL7v8WCLtloNh9DtzncFHT)**

---

## 1. The contract

```js
async function getFloodRisk(rainfallMmHr, timeOffsetMin) { … }
```

Defined in `index.html`. It is the **only** point of contact between the UI and
your model. The UI never calls a backend directly.

### Inputs

| Argument | Type | Range | Meaning |
|---|---|---|---|
| `rainfallMmHr` | number | `0`–`120` | Rainfall intensity in mm/hr. Comes from the scenario slider, so it is a *hypothetical*, not necessarily observed. |
| `timeOffsetMin` | number | **exactly** `0 \| 30 \| 60 \| 90 \| 120` | Minutes ahead of "now". `0` is observed/current state; the rest are forecast. |

`timeOffsetMin` is never called with any other value. The UI animates
*between* these five samples by interpolating client-side for rendering only —
it does not ask you for `+47`.

### Output

```js
{
  generatedAt: "2026-08-01T10:00:00Z",   // ISO 8601, when this forecast was produced
  rainfallMmHr: 62,                      // echo the input back
  timeOffsetMin: 60,                     // echo the input back
  zones: [ /* one object per zone */ ]
}
```

Each entry in `zones`:

| Field | Type | Meaning |
|---|---|---|
| `id` | string | Stable zone key, e.g. `"kaloor"`. Must match across calls. |
| `name` | string | Display name, e.g. `"Kaloor"`. |
| `lat` / `lng` | number | Zone centre. |
| `depthCm` | number | **Predicted standing-water depth in centimetres. This is the headline number** — the UI shows it larger than anything else, so it is the field that most needs to be right. |
| `risk` | number `0`–`1` | Normalised risk index. Secondary. |
| `level` | `"safe"` \| `"watch"` \| `"high"` \| `"severe"` | Warning level. See §2. |
| `population` | number | People in the zone. Currently an estimate — see §5. |
| `trend` | `"rising"` \| `"steady"` \| `"falling"` | Direction of change vs the previous 30-minute step. |

**All four `level` strings are frozen.** Don't rename them; the UI maps them to
IMD's published wording.

---

## 2. Warning levels and depth bands

The UI displays India Meteorological Department's four-level warning scale. The
`level` ids are internal; these are the labels the user sees:

| `level` | Shown as | Depth band | Copy on screen |
|---|---|---|---|
| `safe` | **No warning** | under 10 cm | No significant water expected. |
| `watch` | **Watch** | 10–24 cm | Surface water on roads. Drive slowly. |
| `high` | **Alert** | 25–49 cm | Waterlogging. Roads risky. Avoid low-lying routes. |
| `severe` | **Warning** | 50 cm+ | Deep water. Roads impassable. Danger to life. |

Bands are anchored to what water does to a street: ~15 cm and vehicles lose
traction, ~30 cm and most cars stall, ~50 cm and it is genuinely impassable.

**If your model derives `level` from something other than depth, tell me** —
right now the frontend assumes `level` and `depthCm` agree, and the legend
states the bands explicitly. If they disagree the UI will contradict itself.

`risk` is currently `min(1, depthCm / 75)`, chosen so band edges land on 0.13 /
0.33 / 0.66. If you produce a real probabilistic risk, say so and I'll stop
deriving it from depth.

---

## 3. What is mocked, and where the swap happens

**Everything is mocked.** There is no live rainfall feed, no trained model, and
no deployment. The current implementation is a deterministic function of
rainfall × susceptibility × time, tuned to be physically plausible and to make
demos repeatable.

The swap is one function body:

```js
async function getFloodRisk(rainfallMmHr, timeOffsetMin) {
  const res = await fetch(`${API}/nowcast?rain=${rainfallMmHr}&offset=${timeOffsetMin}`);
  if (!res.ok) throw new Error(`nowcast ${res.status}`);
  return res.json();          // must match the shape in §1
}
```

Nothing else in the file changes. Not the map, not the scrubber, not the
dashboard, not the diorama.

### Things that will break the frontend

- Returning a **subset** of zones. Return every zone every time; use
  `depthCm: 0` for dry ones.
- Changing **zone order** between calls. Order is not relied on for identity,
  but `id` must be stable.
- Returning `depthCm` as a string.
- Taking longer than ~200 ms per call. The UI calls you **five times** on
  startup and again whenever rainfall changes, to build its interpolation
  frames. If a call is slow, that's 5× the latency before anything renders.
  If you can only serve one offset per request, tell me and I'll batch.

### Nice to have, not required

A single endpoint returning **all five offsets at once** would remove the 5×
round trip entirely. If that's easy on your side, it's the highest-value change
you could make to this interface.

---

## 4. OPEN QUESTION — tide. Your call, not mine.

**This is not decided. Please decide it.**

Kochi's canals back up at high tide. The Thevara–Perandoor Canal — the city's
main drainage artery, running Panampilly Nagar → Kadavanthra → KSRTC → Kaloor →
Perandoor Kayal — is silted and encroached, and the Mullassery Canal has a
reverse slope that pushes water *into* the TP Canal rather than away. Tide state
is a real, documented driver of whether that system drains at all.

Modelling it would make the forecast substantially more honest, and no competing
team is likely to have it.

**Why it's parked:** it changes the shared contract, and the contract is the
seam between us. Options as I see them:

1. **Tide is internal to your model.** You ingest a tide feed yourself; the
   contract does not change. *Frontend cost: zero.* My preference unless you
   need the UI to expose it.
2. **Tide becomes an input.** `getFloodRisk(rainfallMmHr, timeOffsetMin, tideState)`.
   Needs a UI control, and the scenario space doubles.
3. **Tide becomes an output field.** e.g. `tideState: "high" | "falling" | "low"`
   at the payload level, displayed as context. Small UI cost, no new control.
4. **Skip it for the hackathon.** Defensible; say so and I'll note it as future
   work rather than an omission.

Until you answer, `getFloodRisk()` is unchanged and there is no tide field, no
tide UI, and no speculative stub. Tracked in `DIRECTION.md` §4.

---

## 5. Data provenance — please keep this honest

The UI states, on screen, exactly what is real and what isn't. If your model
changes any of these, tell me so the labels stay true.

| | Status |
|---|---|
| Zone list, coordinates | **Real** — from reporting on actual Kochi waterlogging |
| TP / Mullassery canal routes and failure modes | **Real** — Kerala Irrigation Dept material |
| IMD warning scale, the term "nowcast" | **Real** — IMD's published system |
| `population` per zone | **Estimated.** Not census or ward data. Labelled `est.` everywhere it appears |
| `baseSusceptibility` | **Authored** to be plausible. Not from a DEM. Replace this with real terrain data and it becomes a genuine strength |
| Rainfall feed | **Does not exist** |
| Model output | **Does not exist** — deterministic simulation |

If you produce real susceptibility from a DEM or flow-accumulation, that is the
single biggest credibility upgrade available, and I'll relabel the UI to say so.

---

## 6. What "done" looks like from your side

You are done when:

1. A single HTTP endpoint accepts a rainfall value (0–120) and an offset
   (0/30/60/90/120) and returns the §1 JSON shape, with every zone present.
2. `id` values match the frontend's zone ids, or you send me your list and I
   adopt yours. **Either is fine — just tell me which.**
3. `depthCm` is a number in centimetres and is the field you're most confident in.
4. `level` agrees with the §2 bands, or you tell me it doesn't and why.
5. Responses are under ~200 ms, or you offer a batched all-offsets endpoint.
6. CORS allows the frontend origin.
7. You've answered §4 (tide) with one of the four options.

Then I change one function body and we're integrated.

---

## 7. Testing against the frontend before you're ready

You don't need the real model to test the seam. In `index.html`, replace the
mock body with a hardcoded response matching §1 and confirm the console still
renders. If it does, your shape is correct.

The current mock's calibration, for reference — at 62 mm/hr, +60 min, Kaloor
produces `depthCm: 41`, which is the worked example in `CLAUDE.md`.

**Contact me before changing the contract shape.** Everything on screen is
traceable to these fields, and the UI states publicly that it is.
