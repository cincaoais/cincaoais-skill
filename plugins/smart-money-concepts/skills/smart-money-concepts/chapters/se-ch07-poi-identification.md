# Section 7: POI Identification
> **Source**: *E-book Smart Money SMC* (anonymous, 33 pp., translated), PDF p. 22

*Terminology note: "softens" = mitigates; "fulcrum" = the bullish candle used as a POI; "click on the POI" = price taps the POI.*

## Core Idea
A **POI** is any zone that has itself **taken liquidity** — a session-sweep candle, an order block, a one-candle engulf OB, a candle that took the previous candle's high/low. You don't have to trade every POI, but you must know all of them; the highest-probability POI is the one reached **after the IDM has been removed**, ideally the **extreme block**.

## Frameworks Introduced
- **POI catalogue** (from the numbered AUDUSD M15 chart):
  - When to use: mapping every candidate zone on the HTF before switching to the LTF.
  - How — a candle/zone is a POI if it: (1) sweeps a **session** high/low (it can be any session) and closes back; (2) is a valid **order block**; (3) is a **one-candle OB** — a candle that closes beyond the prior candle (engulfing works as OB); (4) knocks out the **previous candle's** low/high and the next candle closes back beyond it; (5) sweeps a session high after touching another POI.
- **POI validity filter**:
  - How: (1) is the recent structure intact? If the main CHoCH just broke structure, the old POI is invalid — wait for new structure and a new IDM sweep; (2) was the IDM removed? After IDM removal the POI is high probability, but **without LTF confirmation the odds are only 50%** — don't enter blind; (3) is it SMT (no IDM, no liquidity check)? → skip.
- **Execution by timeframe**: If you are on the HTF when price reaches the POI, switch to the LTF and wait for a CHoCH; if you are already on the LTF, you may enter directly at the POI (or at the next candle open after a candle sweep).
- **Counter-trend exception**: A buy against the trend is allowed in two cases — the IDM has **not** been withdrawn, or the IDM is broken.

## Key Concepts
- **POI**: zone that took liquidity (candle, OB, engulf, session sweep).
- **One-candle OB**: a candle that closes beyond the previous candle; engulfing qualifies.
- **Extreme block**: deepest valid OB; best POI after IDM removal.
- **Wick POI vs. whole-candle POI**: two ways to draw the zone — the author works the **shadow** (wick) when a pullback has already mitigated part of it.
- **Minor IDM**: small inducement inside the LTF structure that must be taken if minor structure breaks.
- **50% rule**: IDM removed but no LTF confirmation = coin flip.

## Mental Models
- Map **all** POIs, trade the **one after IDM**.
- Think of structure breaks as a **reset button**: after a CHoCH, previous POIs are void until a new IDM forms.
- HTF finds the place; LTF gives permission.

## Anti-patterns
- **Selling a POI on the K pullback right after a CHoCH** — wait for the IDM to be removed first.
- **Marking every high as a POI** (candle B had a high but structure had broken → not valid).
- **Trading after IDM removal with no LTF confirmation** — 50% odds.
- **Trading SMT zones** (no IDM, no liquidity).

## Reference Tables
| # (AUDUSD M15) | POI | Action |
|---|---|---|
| 1 | Candle T sweeps the session low (it can be any session); candle also forms an OB | Buy after LTF confirmation |
| 2 | Price reaches an OB acting as POI | Buy on LTF confirmation, or directly if on LTF |
| 3 | Candle A closes above candle R → one-candle OB; D mitigates it | Buy on LTF confirmation / directly |
| 4 | Candle I takes previous low, next candle closes above → I is POI; N mitigates | Buy |
| 5 | After touching a POI, candle G sweeps the session high | Sell on LTF confirmation |
| 6 | Candle B high after main CHoCH | ❌ not a POI — wait for IDM |
| 7 | Small POI with swept liquidity but no IDM | Optional sell |
| 8 | Candle U takes the prior candles' high | Sell next open (LTF) / mark as POI |
| 9 | Candle H taps U's POI after IDM taken; A and N took previous highs | Sell on LTF confirmation |

## Worked Example
Lower p. 22 chart (HTF POI above, Asian low below): price sweeps the **Asian low** and the bullish sweep candle is used as a POI ("fulcrum"). A zone marked "part of SMT — no IDM, no liquidity check" is skipped. When the previous low is passed and the next candle closes back above it, the author buys the next pullback on LTF confirmation. Higher up, price reaches the **HTF POI** after the IDM was removed and the extreme block touched → "high-probability POI; sell on LTF confirmation with large profit." Two drawing options appear — the whole candle or the wick; the author uses the wick. A later sweep is rejected because minor structure broke — sell only after a new minor IDM is removed.

## Key Takeaways
1. A POI must have taken liquidity.
2. Know every POI type; trade the one after IDM removal.
3. After a CHoCH, wait for new structure and IDM before using POIs.
4. IDM removed + no LTF confirmation = 50% → skip.
5. On HTF, confirm with LTF CHoCH; on LTF, enter at the POI directly.

## Connects To
- **[se-ch04](se-ch04-order-flow-order-block.md)**: OB/extreme OB definitions.
- **[se-ch05](se-ch05-ifc-candle.md)**: IFC candles as POIs.
- **[se-ch08](se-ch08-multi-timeframe.md)** and **[se-ch09](se-ch09-entry-models.md)**: LTF confirmation methods.
- **[fm-ch06](fm-ch06-poi-advanced-choch.md)**: Miller's POI (sweep only) vs OB (sweep + imbalance + MSS) and POI types 1–4.
- ⚖️ Other book: Miller formalises four POI types and requires an Advanced CHoCH on the LTF plus an OB limit order; this e-book lets you enter directly at the POI when already on the LTF.
