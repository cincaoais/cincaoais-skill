# Chapter 6: The Last Weapons for SMC Trading
> **Source**: *Smart Money Concepts: Unlocking the Path to High Probability Trading* — Frank Miller (2024), Ch 6, PDF pp. 70–78

## Core Idea
A **Point of Interest (POI)** is a higher-timeframe zone that only needs a **liquidity sweep** to qualify; when price reaches (or sweeps into) a POI, you drop to a lower timeframe and wait for an **Advanced CHoCH** — a structure shift on the LTF — before looking for the Order Block to enter from.

## Frameworks Introduced
- **POI vs OB distinction**:
  - **OB** requires liquidity sweep + Imbalance + market structure shift.
  - **POI** requires **liquidity sweep only**.
  - POIs are marked on the **higher timeframe** (e.g. H4); OBs are usually found on the **lower timeframe** (e.g. M15) after an advanced CHoCH, to pinpoint entry.
  - A POI followed by an imbalance is also an OB → a very strong POI.
- **POI Variations (types 1–4)**:
  1. **Basic POI** — a pullback sweeps the previous minor high (downtrend) before price continues and makes a new BOS. Wait for price to retrace to it, then go to LTF. The most basic and one of the most reliable.
  2. **Modified POI** — the first pullback did *not* sweep (point B fails to exceed point A) → discard it; use the lower zone where a sweep of the previous high happened just before the drop.
  3. **Advanced POI (type 3)** — of pullbacks AB, CD, EF, only EF breaks above the nearest previous high. Do *not* wait for a return: go straight to LTF when the sweep happens. Two forms: (a) wick above the nearest high then sharp drop — **the best liquidity-sweep pattern**; (b) a bullish candle closes above the nearest high (point D) followed by a bearish candle → go to LTF and look for CHoCH.
  4. **Advanced POI (type 4)** — same as type 3, but price sweeps liquidity from an earlier, **higher high** rather than the nearest one.
- **Advanced CHoCH**:
  - When to use: after a POI is touched (types 1–2) or immediately after a sweep creates a POI (types 3–4).
  - How:
    1. Mark the POI on HTF.
    2. When price reaches/sweeps it, switch to the LTF (H1→M5, H4→M15).
    3. Wait for a CHoCH on the LTF — break of the minor high/low that formed the nearest swing.
    4. Only then find the OB for entry. If no CHoCH yet, stay patient.

## Key Concepts
- **Point of Interest (POI)**: HTF zone with a liquidity sweep; like S/R but more selective.
- **Basic POI / Modified POI / Advanced POI (3, 4)**: the four variations above.
- **Advanced CHoCH**: CHoCH on the LTF triggered after a POI interaction; entry-refinement tool.
- **Liquidity sweep**: required ingredient for every POI.
- **One key OB**: many POIs may exist in a wave (2–3), but typically only one OB is traded.
- **HTF/LTF pairing**: e.g. H4/M15, H1/M5.

## Mental Models
- Think "POI = where to look, Advanced CHoCH = when to act, OB = where to enter".
- Use sweep presence as the POI filter: no sweep, no POI.
- Treat support/resistance traders' "touch and trade" as the mistake — POI touches trigger analysis, not orders.
- Think of types 3–4 as "the sweep is the signal" — no need to wait for a retrace.

## Anti-patterns
- **Entering the moment price touches a POI** on the HTF: always switch to LTF for confirmation.
- **Using a pullback that never swept liquidity** as a POI (modified-POI case).
- **Trading every POI** in a wave — verify the structure shift first; one key OB.
- **Assuming a POI must be an OB**: it needn't have an imbalance; if it does, it is stronger.

## Reference Tables

| Type | Liquidity pattern | Wait for retrace? | Next step |
|---|---|---|---|
| 1 Basic | Pullback sweeps previous minor high/low, then BOS | Yes | LTF CHoCH at POI |
| 2 Modified | First pullback no sweep → use lower zone that swept | Yes | LTF CHoCH at POI |
| 3 Advanced | Only the latest pullback breaks the nearest high (wick = best; close + opposite candle = OK) | No | LTF CHoCH immediately |
| 4 Advanced | Sweep of an earlier higher high | No | LTF CHoCH immediately |

| Attribute | POI | OB |
|---|---|---|
| Liquidity sweep | Required | Required |
| Imbalance | Optional (adds strength) | Required |
| Structure shift | Not required | Required |
| Timeframe | HTF | LTF (after Advanced CHoCH) |
| Count per wave | Several | Usually one key OB |

## Worked Example
**Type 3, Gold H1 → M5**: Gold is in an H1 uptrend with no liquidity sweep until point A; the sweep defines the POI, and price bounces immediately, showing buyer dominance. No H1 entry — switch to M5. On M5 an Advanced CHoCH forms (structure shift up); price then retraces back into the identified POI and surges higher.

**Type 1, H1 basic POI**: a pullback swept liquidity (LS1) and price made a new BOS. Pullback LS2 also held liquidity; price then swept it with a series of wicky candles. The marked POI is excellent because (1) liquidity was swept on the way to it, (2) the sweep cleared the X low from the bullish BOS wave, and (3) an imbalance followed, so it is also a valid OB. When price enters it, go to LTF and wait for CHoCH.

## Key Takeaways
1. POI needs only a liquidity sweep; OB needs sweep + imbalance + structure shift.
2. Mark POIs on HTF; find OBs on LTF after an Advanced CHoCH.
3. Types 1–2: wait for price to return; types 3–4: act on the sweep via LTF.
4. A wick sweep followed by a sharp move is the best sweep pattern.
5. POI + imbalance = very strong zone.
6. Several POIs per wave, usually one key OB to trade.

## Connects To
- **[fm-ch02](fm-ch02-bos-choch.md)**: CHoCH definition that Advanced CHoCH applies on the LTF.
- **[fm-ch04](fm-ch04-order-blocks.md)**: OB criteria used after the Advanced CHoCH.
- **[fm-ch07](fm-ch07-complete-toolkit.md)**: full 5-step setup built on POI + Advanced CHoCH + OB.
- **[fm-ch08](fm-ch08-candle-breakout-strategy.md)**: CBS as an alternative when price does not retrace to the LTF OB.
- **[se-ch07](se-ch07-poi-identification.md)**: e-book lists many POI kinds (session sweeps, engulfing, candle sweeps).
- **[se-ch08](se-ch08-multi-timeframe.md)**: HTF/LTF pairs (M15→M1, H1→M5).
- **[se-ch09](se-ch09-entry-models.md)**: LTF entry models after POI touch.
- ⚖️ Other book: the e-book says once price touches the HTF POI, the **nearest LTF high/low break (even by wick) is the CHoCH** — no need to wait for the main LTF high/low; Miller's Advanced CHoCH is described without that wick allowance.
