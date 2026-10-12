# Section 1: Pulse and Correction (Impulse vs. Pullback Rules)
> **Source**: *E-book Smart Money SMC* (anonymous, 33 pp., translated), PDF pp. 4–5

*Terminology note: the translation says "pulse" (= impulse), "rollback"/"kickback" (= pullback/correction). Standard SMC terms are used below.*

## Core Idea
Price only moves in two modes — **impulse** (institutional flow, one-directional) and **correction** (retail range-trading) — and a correction only "counts" when a candle actually breaks the high or low of the extreme candle of the prior move; otherwise the whole sequence is still one move.

## Frameworks Introduced
- **Impulse / Correction model**: Strong directional legs are driven by banks and institutions; the counter-moves are where retail traders buy/sell inside a range.
  - When to use: before labelling any swing, high, low, BOS or IDM — every later concept depends on which candles form a valid pullback.
  - How: (1) find the extreme candle of the current leg (highest candle in an up-leg, lowest in a down-leg); (2) watch the next candles; (3) the leg is "corrected" only when a later candle trades beyond the opposite end of that extreme candle.
- **Correction Rule (valid pullback test)**: A pullback is valid when price breaks the previous candle's high/low — candle colour irrelevant (bullish or bearish).
  - When to use: every time you decide whether a new swing point exists.
  - How: (1) body close beyond the prior candle's high/low → "sure pullback"; (2) a wick (shadow) beyond the high/low that closes back inside → also a "sure pullback"; (3) candles trapped inside the extreme candle's range (inside bars) → **not** a pullback, the move is still one leg.
- **Extreme-candle hand-off**: If, before the pullback triggers, a new candle makes a fresh extreme (e.g. candle U prints above candle H in an up-leg), the reference candle moves to U. The pullback is then valid only when U's low is taken.

## Key Concepts
- **Impulse (pulse)**: a strong one-way leg; treated as a single move until a valid correction appears.
- **Correction / pullback**: counter-trend move that has broken the extreme candle's opposite side.
- **Extreme candle**: the highest candle of an up-leg (or lowest of a down-leg) — the pullback reference.
- **Inside-bar sequence**: candles that stay within the extreme candle's high–low; they do not create a pullback.
- **Sure pullback**: body close or wick through the previous candle's high/low.
- **One move**: a sequence with no valid pullback; its internal wiggles are not structure.

## Mental Models
- Think of the extreme candle as a **gate**: until price exits through its far side, nothing structural has happened.
- Use "who is in control" framing: impulse = institutions positioning; correction = retail trading a range that institutions will later harvest.
- Treat wicks and bodies equally **for pullbacks** (contrast: BOS needs a body close — see Section 2).

## Anti-patterns
- **Counting visual dips as pullbacks**: small red candles inside a big green candle's range are not corrections — you will mark false highs/IDMs.
- **Keeping a stale reference candle**: once a new extreme candle prints, the old one no longer defines the pullback.
- **Judging by candle colour**: a bullish candle can be the pullback candle if it takes the prior low.

## Reference Tables
| Situation (up-leg) | Valid pullback? | Why |
|---|---|---|
| K breaks the low of M (M = highest candle of the move) | ✅ | Extreme candle's low taken |
| A and N stay inside candle H's high–low | ❌ | Inside bars; still one impulsive move |
| U breaks above H, then B takes U's low | ✅ | Reference moved to U; U's low taken |
| H's high and low never broken both ways | ❌ | Counts as one move |
| Last candle made a new low vs. previous candle (any colour) | ✅ | Previous candle's low taken |
| Price ranges while last bullish candle's high and low stay intact | ❌ | Range inside the candle, no correction |

The same table mirrors for a down-leg (take the extreme candle's **high**).

## Worked Example
From the p. 5 "Correction rules" diagrams (up-leg): price rallies; candle **M** is the highest candle. Candle **K** trades below M's low → valid pullback, M marks the swing high. Later, a large candle **H** prints; candles **A** and **N** stay entirely inside H → no pullback, H-A-N is one impulsive move. In the right-hand diagram, candle **U** breaks above H before any correction, so U becomes the extreme candle; candle **B** then takes U's low → valid retracement, and the swing high is U, not H. On the "Reliable rollback identification" real chart, every tick-mark pullback is a candle that took the previous candle's high/low; three spots carry a red X. The two captioned ones are ranges where the last bullish candle's high and low were never broken ("not a valid pullback"); the third X, near the top right, has no caption.

## Key Takeaways
1. A pullback exists only when the extreme candle's opposite side is taken — by wick or body.
2. Candle colour never matters for the pullback test.
3. Inside-bar clusters are part of the prior move, not structure.
4. When a new extreme candle prints, re-anchor the test to it.
5. Get this right first: highs, lows, IDM and BOS all inherit from it.

## Connects To
- **[se-ch02](se-ch02-bos-choch-structure.md)**: valid pullbacks define the IDM and main highs/lows used for BOS/CHoCH.
- **[se-ch09](se-ch09-entry-models.md)**: the "previous candle liquidity" entry is the same candle-sweep logic applied on the LTF.
- **[fm-ch01](fm-ch01-impulsive-corrective-waves.md)**: Miller's corrective-wave rules (candle 2 or 3 must break candle 1's low; inside bars don't count).
- ⚖️ Other book: Miller agrees on the core rule but adds that a correction may be confirmed by the 2nd *or* 3rd candle and lists body/wick-size criteria for impulsive waves; this e-book gives no impulse-quality criteria.
