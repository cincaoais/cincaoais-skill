# Section 5: IFC — Institutional Funding Candle
> **Source**: *E-book Smart Money SMC* (anonymous, 33 pp., translated), PDF p. 15

*Terminology note: "removed"/"stripping" liquidity = liquidity sweep; "ENG LQD" = engineered liquidity (a chart label the book never defines).*

## Core Idea
An **IFC** is a candle that breaks a major level — swing high/low, session high/low, or the IDM — **but fails to close beyond it**. It marks the moment all the major stop-losses were taken; once that liquidity is squeezed out, trade the reversal on **LTF confirmation**. Candle colour does not matter.

## Frameworks Introduced
- **IFC identification**:
  - When to use: to define a POI at a liquidity event, especially around sessions and IDM.
  - How: (1) mark the major levels: swing highs/lows, session highs/lows (Asia/London/NY), IDM, engineered liquidity (ENG LQD; the p. 15 example is a swept prior high → sell), and internal HTF structure (p. 15 lower chart: "stripping the inside structures in HTF"); (2) find a candle that trades through one of them; (3) confirm it **closes back inside** (wick through, body not beyond); (4) label it IFC — that candle's range becomes the POI.
- **IFC trade**:
  - How: (1) wait for the IFC candle to close; (2) drop to the LTF; (3) enter only after LTF confirmation (CHoCH, one-candle entry — see Section 9); (4) stop beyond the IFC extreme (interpretation — not stated in SE).

## Key Concepts
- **IFC**: sweep candle through a major level that closes back inside.
- **Major level**: swing high/low, session high/low, IDM, engineered liquidity, internal HTF structure.
- **Stop-hunt completion**: IFC = all major stops triggered; fuel collected for reversal.
- **LTF confirmation**: required before entering at an IFC.
- **Colour-agnostic**: bullish or bearish body is irrelevant.

## Mental Models
- Think of the IFC as the **receipt of a stop hunt** — the market has "funded" itself with trapped orders.
- Use IFC as a POI generator: every sweep-and-fail candle at a key level is a candidate zone.

## Anti-patterns
- **Entering on the IFC candle itself** without LTF confirmation.
- **Calling a body close beyond the level an IFC** — that's a break, not a sweep.

## Reference Tables
| IFC trigger (p. 15 charts) | Direction | Action |
|---|---|---|
| Candle A sweeps the **session high** | Sell | LTF confirmation |
| Candle K sweeps a preliminary large **low** | Buy | LTF confirmation |
| Candle H removes the **IDM** (below) | Buy | After H closes + LTF confirms |
| Candle N removes the **IDM** (above) | Sell | After N closes + LTF confirms |
| Sweep of **session low** | Buy | LTF confirmation |
| Sweep of **engineered liquidity** (ENG LQD) | Sell | After candle close |
| Sweep of previous **major structure** / major low | Reverse | LTF confirmation |
| Candle strips (sweeps) **internal structure on the HTF** | Reverse | LTF confirmation (p. 15 lower chart) |

## Worked Example
p. 15 top chart: an up-move approaches the session high. Candle **A** wicks above the "session high sweep" line and closes back below → IFC; sell on LTF confirmation. Later, candle **N** takes out the IDM above and closes back → "removed IDM, sell after confirmation of N closing on LTF". On the way down, candle **K** had swept a large prior low ("preliminary large low sweep") — an IFC for a buy — and candle **H** removed the IDM below before the rally: "buy after H closes and LTF is confirmed." The lower real chart shows the same: session-low sweep IFC → buy; engineered-liquidity sweep (a prior high) → sell after the candle closes; a shaded zone where price strips internal HTF structure is marked as another IFC/POI location; previous-major-structure and major-low sweeps → IFC.

## Key Takeaways
1. IFC = wick through a major level, close back inside.
2. It signals that major stops are cleared.
3. Always wait for the candle close, then LTF confirmation.
4. Session highs/lows and IDM are the prime IFC locations.

## Connects To
- **[se-ch06](se-ch06-liquidity-types.md)**: session and daily liquidity levels where IFCs form.
- **[se-ch07](se-ch07-poi-identification.md)**: IFC candles become POIs (e.g. candle T sweeping the session low).
- **[fm-ch06](fm-ch06-poi-advanced-choch.md)**: Miller's POI types 3/4 — trade immediately after a wick sweep via LTF Advanced CHoCH.
- **[fm-ch08](fm-ch08-candle-breakout-strategy.md)**: Miller's reaction candle at a POI is a comparable single-candle trigger.
- ⚖️ Other book: Miller has no "IFC" term; the closest idea is his wick-sweep POI (types 3–4) followed by an LTF Advanced CHoCH.
