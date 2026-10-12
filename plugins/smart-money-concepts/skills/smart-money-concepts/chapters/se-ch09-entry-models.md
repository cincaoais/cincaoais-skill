# Section 9: Entry Models (Explanation of "Input Types")
> **Source**: *E-book Smart Money SMC* (anonymous, 33 pp., translated), PDF pp. 25–29

*Terminology note: "input"/"login"/"entrance" = entry; "input module" = entry model; "withdrawal of liquidity" = liquidity sweep; "absorption" = engulfing; "D2S/S2D" = demand-to-supply / supply-to-demand flip.*

## Core Idea
Every strategy is "right"; the edge is **how you work the POI on the lower timeframe**, using LTF entry models whose purpose is to reduce risk and maximise profit. Six LTF entry models are covered here. The book's own list (pp. 3, 25) names five types — CHoCH / BOS / FLiP / general liquidity-sweep entry / previous-candle (one-candle) entry; below, CHoCH is split into with-IDM and without-IDM modules as the book numbers them, and the BOS type, which the book only shows on the p. 27 chart, is written up as model 6. The universal rule: **before buying or selling you need inducement or liquidity taken — no entry without IDM, even in Flip and CHoCH cases** (model 3 is the sole exception, because the HTF POI itself supplied the liquidity).

## Frameworks Introduced
- **1. CHoCH with IDM**:
  - When: price taps an HTF POI (e.g. extreme OB).
  - How: (1) on the LTF, the **nearest** high/low break after the tap is the CHoCH — no need to wait for the LTF main high/low; (2) at entry time on the LTF even a **wick** counts as a valid CHoCH (close not required); (3) wait for the IDM (first pullback after CHoCH) to be swept; (4) enter at the OB (e.g. single-candle OB); (5) no IDM/no liquidity → no trade. IDM is always on the left of the structure and must break a high/low.
- **2. FLiP with IDM**:
  - When: price reaches HTF supply (OB/OF) but does **not** directly break the recent LTF low.
  - How: (1) price reacts from the LTF demand OB, fails to hold, and breaks it; (2) the failed demand becomes supply (**D2S**) — or failed supply becomes demand (**S2D**); (3) wait for IDM below; (4) sell at the first nearest OB after the IDM sweep, preferring a supply that itself took liquidity over an adjacent block without liquidity ("more likely than block A, since it has liquidity", p. 26); (5) if an unmitigated OB sits above yours, wait for a one-candle OB (absorption) or a one-candle liquidity sweep instead of a direct entry.
- **3. CHoCH without IDM**:
  - When: the reversal starts straight from a swept HTF POI.
  - How: (1) price sweeps the previous POI low/high; (2) directly breaks the previous LTF high (wick acceptable); (3) buy at the last OB without waiting for IDM — the OB already has liquidity (the POI) on its left.
- **4. Previous-candle liquidity withdrawal (scaling entry)**:
  - When: once price touches an LTF POI; valid until the next major LTF low (for sells) breaks.
  - How: (1) sell as soon as the LTF OB is mitigated; (2) each time a candle takes the **previous candle's high** and closes bearish, add a sell at the next candle's open; (3) stop adding when the main low breaks — wait for new structure and its IDM. "If you don't know how to scale gains and cut losses, SMC is not for you."
- **5. Single-candle entry and liquidity-sweep entry**:
  - Definitions: sweeping structure highs/lows or IDM/POI liquidity = **liquidity sweep entry**; taking the previous candle's high/low = **one-candle formation entry**.
  - How (buy): at an extreme POI, a candle takes the previous candle's low and closes bullish → buy at the next candle's open; repeat on each qualifying candle.
  - The liquidity-sweep entry executes the same way: after a candle sweeps a larger low (structure/IDM/POI), buy at the next candle's open ("pre-take large minimum and purchase at the opening of the next candle, and the same in all entries on one candle", p. 29).
- **6. BOS entry (continuation)**:
  - When: the LTF reversal is already in place (CHoCH printed) and price keeps printing BOS in the new direction. This is the "BOS" entry type from the book's list (pp. 3, 25), shown on the p. 27 chart under the module 3 heading.
  - How (buy): (1) after an LTF BOS in the new direction, mark its IDM (the first pullback); (2) wait for the IDM to be swept; (3) enter at the OB beyond it (below the IDM for buys) — "once the BOS market has been released by IDM, click on the order block and buy here"; (4) alternatively, once the IDM is withdrawn after the next BOS, buy at a one-candle absorption (engulfing) OB — "withdrawing IDM and buying on a block of orders for one candle after absorption"; (5) each new BOS + IDM sweep offers another entry (p. 27 shows two in a row).

## Key Concepts
- **HTF POI tapped**: precondition for all LTF entries.
- **LTF CHoCH**: nearest high/low break after the tap; wick allowed at entry time.
- **IDM requirement**: liquidity must be taken before entry (except model 3).
- **FLiP (D2S/S2D)**: failed demand turns into supply, or vice versa.
- **Absorption**: engulfing one-candle OB.
- **One-candle formation**: candle takes the prior candle's high (low) and closes bearish (bullish); enter next open. (p. 22 case 4 uses a different confirmation: the **next** candle closes back above.)
- **BOS entry**: continuation entry — LTF BOS, its IDM swept, enter at the OB beyond it or at a one-candle absorption OB.
- **Scaling/adding**: repeated one-candle entries inside the POI leg.

## Mental Models
- "**No liquidity, no entry**" — IDM is the ticket.
- Think of FLiP as a **failed defence**: demand that couldn't hold becomes the new supply.
- Scale like a ladder: each previous-candle sweep is a rung until the main low breaks.

## Anti-patterns
- **Selling right after CHoCH with no IDM and no liquidity.**
- **Entering a Flip OB with an unmitigated OB above it.**
- **Continuing to add after the main low has broken** — structure reset; wait for new IDM.
- **Waiting for an LTF main-low break at an HTF POI** — the nearest break is enough.
- **Buying straight after a continuation BOS** before its IDM is swept.

## Reference Tables
| Model | Trigger on LTF | IDM needed? | Entry |
|---|---|---|---|
| 1 CHoCH + IDM | Nearest high/low break after HTF POI tap | Yes | OB after IDM sweep |
| 2 FLiP + IDM | Demand OB reacts then breaks (D2S) | Yes | First OB after IDM |
| 3 CHoCH, no IDM | Direct break after POI sweep | No | Last OB (liquidity on left) |
| 4 Previous-candle sweep | Candle takes prior high, closes bearish | Inside POI leg | Next open; add repeatedly |
| 5 Single-candle / sweep | Candle takes prior low (or a larger low), closes bullish | — | Next open |
| 6 BOS (continuation) | LTF BOS in the new direction | Yes | OB beyond the IDM, or one-candle absorption OB |

## Worked Example
Model 4, p. 28 (LTF, bearish): price rallies into an **extreme POI for sell**, candle K tops it; a CHoCH and IDM follow. When the LTF OB is mitigated, the trader sells immediately. Candle **H** takes the previous candle's high, touches the POI and closes bearish → sell at the next open. Candle **A** takes the previous high → sell at the open after A closes. Another **A** closes bearish → entry at candle B's open. Candle **C** sweeps the previous high and closes lower → sell next open. Candle **D**'s high and C's low are mitigated, but **no entry** — the main low (BOS) has broken, so the trader waits for new structure and the IDM that forms after it. The real-chart version shows a stack of shaded one-candle OB entries stair-stepping down into a large drop.

## Key Takeaways
1. Work every POI on the LTF with a defined entry model.
2. Take liquidity first — IDM before entry (except CHoCH without IDM).
3. At an HTF POI, the nearest LTF break (even a wick) is the CHoCH.
4. FLiP: failed demand → supply (D2S), failed supply → demand (S2D).
5. Scale in with previous-candle sweeps until the main low breaks.
6. In continuation, every new LTF BOS whose IDM gets swept is another entry (BOS model).

## Connects To
- **[se-ch02](se-ch02-bos-choch-structure.md)**: CHoCH-at-POI rule.
- **[se-ch07](se-ch07-poi-identification.md)**, **[se-ch08](se-ch08-multi-timeframe.md)**: POI and timeframe context.
- **[fm-ch06](fm-ch06-poi-advanced-choch.md)**, **[fm-ch07](fm-ch07-complete-toolkit.md)**: Miller's Advanced CHoCH → OB limit entry.
- **[fm-ch08](fm-ch08-candle-breakout-strategy.md)**: Miller's engulfing reaction-candle entry.
- ⚖️ Other book: Miller never accepts a wick as CHoCH (pitfall #4) and has no Flip model; his candle breakout requires a full engulf at a POI, whereas this e-book's one-candle entry only needs the previous candle's high/low swept and a close in the trade direction (bearish for sells, bullish for buys).
