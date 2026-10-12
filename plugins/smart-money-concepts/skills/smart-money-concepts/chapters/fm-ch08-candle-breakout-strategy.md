# Chapter 8: Breakout Strategy with SMC
> **Source**: *Smart Money Concepts: Unlocking the Path to High Probability Trading* — Frank Miller (2024), Ch 8, PDF pp. 88–104

## Core Idea
The **Candle Breakout Strategy (CBS)** solves the "price accelerated without retracing to my LTF order block" problem: at a POI/Order Block, a **reaction candle** followed by an engulfing **confirmation candle** gives a safe, clear entry — either directly on the analysis timeframe or refined on a lower one.

## Frameworks Introduced
- **Candle Breakout Pattern**:
  - Bullish: bearish **reaction candle** that touches a POI/OB, then a bullish **confirmation candle** that fully engulfs the reaction candle's body.
  - Bearish: bullish reaction candle at the POI, then a bearish candle fully engulfing its body.
  - The reaction candle is valid only if it touches an important POI or OB.
- **Trading The Candle Breakout (steps)**:
  1. Identify market structure; decide long or short.
  2. Identify the BOS.
  3. Identify the POI where the pattern must form. The POI must already be validated by inducement/liquidity — an IDM swept, or EQH/trendline liquidity taken on the way in — in every CBS variant, single-TF included (drawn from Miller's worked examples; his formal steps 1–4 don't state it).
  4. Wait for the breakout pattern confirmation.
  5. Execute via one of two methods:
- **Method 1 — Trading on Two Timeframes** (HTF = M30, H1, H4, D1, W; e.g. M15 → M5/M1):
  - **Scenario 1**: the confirmation candle **sweeps the reaction candle's liquidity** → on LTF, find the OB inside the reaction candle's range and wait for a retrace; **no inducement needed** (liquidity already swept on HTF).
  - **Scenario 2**: the confirmation candle does **not** sweep the reaction candle → on LTF, find the OB inside the reaction candle's range **and** an inducement; wait for the IDM sweep, then the OB retrace.
  - Optional: scale in with multiple limits at several OBs inside the reaction candle; SL below the reaction candle.
- **Method 2 — Trading on One Timeframe** (H1 and below):
  - Long: limit at the **high of the reaction candle** (or its close); SL below the reaction candle or, safer, below the POI; TP at the nearest major high or 3R/5R.
  - Short: limit at the **low of the reaction candle**; SL above the reaction candle or above the POI; TP at nearest major low or 3R/5R.
- **Trade management**: after an LTF BOS in your favour, move SL to entry; close at TP immediately; avoid overly ambitious TPs.

## Key Concepts
- **Candle Breakout Strategy (CBS)**: SMC execution variant using a two-candle engulfing pattern at a POI.
- **Reaction candle**: first candle touching/mitigating the POI/OB.
- **Confirmation (rejection) candle**: engulfs the reaction candle's body in the trade direction.
- **Engulfing**: second candle's body covers the first's body.
- **Mitigation phase → rejection phase**: price pushes into the POI with weakening momentum, then rejects.
- **Marubozu**: strong full-body candle often seen after entry.
- **Dynamic liquidity**: stops below a trendline feeding the move into the OB.

## Mental Models
- Think of CBS as the engulfing candle doing the LTF CHoCH's job on the HTF.
- Use "did the confirmation candle sweep the reaction candle?" to decide whether an LTF inducement is required.
- Think "safety over R:R": CBS may not offer the biggest reward but has the clearest entries.
- Match timeframe to temperament (SMC is not one-size-fits-all): larger TF = wider stops, fewer trades, lower R:R but a larger gain per trade; smaller TF = tighter stops, higher R:R, more activity — suits a higher risk appetite.

## Anti-patterns
- **Engulfing patterns away from a POI/OB**: invalid reaction candle.
- **Skipping the LTF inducement in Scenario 2**: entry before liquidity is swept.
- **Greedy targets**: holding too long increases exposure near liquidity zones.
- **Not moving SL to entry** after an LTF BOS confirms the move.

## Reference Tables

| Execution | Entry | Stop | LTF inducement needed? |
|---|---|---|---|
| One TF, long | Reaction candle high/close | Below reaction candle or below POI | No (but the POI must already be IDM/liquidity-validated) |
| One TF, short | Reaction candle low/close | Above reaction candle or above POI | No (but the POI must already be IDM/liquidity-validated) |
| Two TF, Scenario 1 (confirmation swept reaction candle) | LTF OB inside reaction range | Beyond LTF OB or HTF pattern | No |
| Two TF, Scenario 2 (no sweep) | LTF OB inside reaction range | Below reaction candle | Yes |

In every row the HTF POI itself must already be validated by inducement or swept liquidity before the reaction candle counts.

| Take-profit options | When |
|---|---|
| Nearest major high/low | Default, structure-based |
| 3R / 5R | Fixed-ratio plan |
| Most recent opposite imbalance | Quick nearby target |

## Worked Example
**M30 long**: new BOS, POI marked, inducement appears. First retrace misses the POI; the second touches it, turning the prior bearish attempt into inducement. Then the breakout pattern forms → the prior candle is the reaction candle. Option A: limit long at the reaction candle, SL below the OB/POI (or just below the reaction candle for better R:R), TP at the nearest major high → ~**5R**, with a strong marubozu soon after entry. Option B: on M5, find an OB with imbalance inside the reaction candle's range; because the HTF reaction candle was *not* swept, wait for price to sweep inducement before it touches the OB.

**M15 → M3 short**: downtrend, OB + inducement form a valid POI. The confirmation candle engulfs and sweeps the reaction candle → no further inducement needed. On M3, limit short at the OB's lower edge, SL above the M3 OB (or above the HTF pattern), TP at the nearest major low → **4.5R**; SL moved to entry after an M3 BOS. Single-TF alternative: short at the reaction candle's low, SL above the POI, TP below the major low → **3.5R**.

**EUR/USD H1 short**: downtrend with two BOS; price sweeps equal-highs liquidity into an unmitigated OB (the extreme POI). Two bearish candles follow bullish ones; Miller calls the first *bearish* candle at the POI the reaction candle; an engulfing candle then breaks below, engulfing it and several earlier candles. Note the inconsistency: by the pattern definition a bearish CBS needs a *bullish* reaction candle, so here the reaction candle has the trade's colour — treat reaction-candle colour as flexible when matching Miller's own charts. Limit at the reaction candle's close; SL above the POI or engulfing candle; TP at the recent bullish imbalance or the major low.

**GBP/JPY H1 long**: uptrend, unmitigated OB with trendline (dynamic) liquidity below. Price sweeps the trendline liquidity into the OB; reaction candle then bullish engulfing. Buy at the reaction candle's close, SL below its low or the POI, TP at the next major high → **4R**.

## Key Takeaways
1. CBS = reaction candle at POI/OB + engulfing confirmation candle.
2. The reaction candle must touch a meaningful POI or OB.
3. One-TF: enter at the reaction candle's extreme/close; stop beyond it or beyond the POI.
4. Two-TF: find the LTF OB inside the reaction range; require LTF inducement only if the confirmation candle did not sweep the reaction candle.
5. Move SL to entry after an LTF BOS; take profit at reasonable, liquidity-based targets.
6. Entries must align with structure and a validated POI; CBS is ultimately disciplined risk management plus the patience to wait until the market gives the signal.

## Connects To
- **[fm-ch06](fm-ch06-poi-advanced-choch.md)**: POIs where the pattern must form.
- **[fm-ch07](fm-ch07-complete-toolkit.md)**: the main method CBS substitutes for when price will not retrace.
- **[fm-ch05](fm-ch05-inducement.md)**: inducement requirement in Scenario 2.
- **[fm-ch03](fm-ch03-liquidity-premium-discount.md)**: equal-highs and trendline liquidity feeding the examples.
- **[se-ch09](se-ch09-entry-models.md)**: e-book "one-candle formation" entry (previous-candle sweep, enter next open) and engulfing-as-OB.
- **[se-ch05](se-ch05-ifc-candle.md)**: IFC candle — sweep-and-fail candle at key liquidity, similar spirit.
- ⚖️ Other book: the e-book's one-candle entry requires the entry candle to **sweep the previous candle's high/low and close back**, entering at the next candle's open; Miller's CBS requires **body engulfing**, with the sweep optional (it only removes the LTF inducement requirement).
