# Chapter 1: Impulsive and Corrective Waves
> **Source**: *Smart Money Concepts: Unlocking the Path to High Probability Trading* — Frank Miller (2024), Ch 1, PDF pp. 9–16

## Core Idea
Market structure is built from strong **impulsive waves** (with the trend) and lighter **corrective waves** (against it), but in SMC a pullback only counts as a *valid* corrective wave when a candle actually breaks the extreme of the previous candle — visual dips that stay inside a candle's range do not count.

## Frameworks Introduced
- **Valid Corrective Wave rule**: in an uptrend, price must break below the **low of the previous candle**; in a downtrend, it must break above the **high of the previous candle**.
  - When to use: every time you label a pullback/swing before marking BOS, CHoCH, inducement or POIs.
  - How:
    1. Find the extreme candle of the current leg (highest candle in an uptrend, lowest in a downtrend).
    2. Check whether a later candle trades beyond the *opposite* extreme of that candle (below its low in an uptrend; above its high in a downtrend).
    3. A body close *or* a wick through counts — Miller treats the break itself as a **liquidity sweep**.
    4. If candle 2 fails but candle 3 breaks the level, the wave is still valid.
    5. If no candle breaks it, the leg is still one impulsive move.
- **Inside-bar exclusion**: candles that stay entirely within a large candle's high–low range form an "inside bar" pattern, not a correction.
  - When to use: after a big-range candle, before calling the next few candles a pullback.
  - How: the pullback only starts at the first candle that breaks the big candle's high or low.
- **Impulsive Wave checklist** (3 conditions):
  1. **Strong Movement in Price** — large bodies, little/no wick, big distance in short time.
  2. **Break of the Previous High/Low** — breaks the extreme formed during the prior corrective wave.
  3. **Consistent (Sustained) Momentum** — consecutive same-direction candles with strong closes and little retracement.

## Key Concepts
- **Impulsive wave**: dominant-direction leg; shows where smart money is accumulating/distributing.
- **Corrective wave** (pullback / retracement wave): counter-trend leg, valid only after the previous-candle break.
- **Liquidity sweep**: price breaking through a high or low to capture resting orders; used here to validate corrections.
- **Inside bar**: candle(s) contained within a prior candle's range; not a correction.
- **Previous candle break**: the atomic test for structure — it underlies every later concept in the book.
- **Advanced correction**: two candles that together break both sides (e.g. candle 7 breaks above candle 6, candle 8 breaks below candle 7) — still a valid corrective wave.

## Mental Models
- Think of each candle's high/low as a tiny liquidity pool; a correction exists only once one of those pools is taken.
- Use "does a later candle take the extreme candle's opposite side?" as a binary switch, not a visual judgment.
- Think of a fast single candle that sweeps both the prior low and then the high (candle 5 example) as a full correction compressed into one bar — a lower timeframe would show rise-fall-rise.
- Treat impulsive waves as the source of direction and corrective waves as the source of entries.
- Spend your scrutiny on corrections: impulses are comparatively easy to spot, while corrections hide the subtle candle-by-candle nuances that decide whether a pullback is real.

## Anti-patterns
- **Calling a visual dip a pullback**: if the candles never break the high candle's low, it is one impulsive move; labeling it a swing creates fake structure.
- **Counting inside bars as corrections**: candles within a large candle's range carry no structural information.
- **Skipping this chapter's rule**: every later label (BOS, IDM, POI, OB) inherits errors from wrongly identified waves.

## Reference Tables

| Scenario (uptrend) | Valid correction? | Why |
|---|---|---|
| Candle 2 breaks below candle 1's low | ✅ | Previous-candle low swept |
| Candle 2 fails, candle 3 breaks candle 1's low | ✅ | Break still happens within the sequence |
| Candle 5 breaks below candle 4's low and sweeps above its high | ✅ | Fast correction in one candle |
| Candle 7 breaks above 6, candle 8 breaks below 7 | ✅ | Advanced two-candle correction |
| Candles 10–11 never break candle 9's low | ❌ | Still inside the impulsive move |
| Candles 12–13 never break candle 5's high or low | ❌ | Inside bar |

| Scenario (downtrend) | Valid correction? | Why |
|---|---|---|
| Candles 2–3 break above candle 1 (the low candle) | ✅ | Previous-candle high broken |
| Candle 2 breaks candle 1's low and keeps falling | ❌ until a later candle breaks above candle 1's high | Continuation, not a pullback |
| Candles 5–6 stay inside large candle 4 | ❌ | Inside bar; needs candle 5 beyond 4, or candle 6 above 4's high |
| Candle 7 sweeps both high and low of prior candle; 8–9 stay inside 7 | ✅ only candle 7 | 8–9 are inside bars |
| Candle 11 sweeps candle 10's low, candle 12 breaks above 11's high | ✅ | Advanced pattern |

| Visual tells (body/colour row from the Ch 3 recap; wick and structure rows from Ch 1) | Impulsive | Corrective |
|---|---|---|
| Candle bodies | Large, same colour | Small, mixed colour |
| Wicks | Few, short | Sideways wicks |
| Structure effect | Breaks previous swing high/low | Sweeps previous candle only |

## Worked Example
Miller's uptrend illustration: a strong rally, then three candles. Candle 1 drops sharply; candle 2 continues down and trades below candle 1's low → the corrective wave is confirmed; candle 3 falls further, reinforcing it. Further up the same chart, candle 9 is the high, but candles 10 and 11 hold above candle 9's low. They look like a dip, yet Miller rejects them: no previous-candle low was taken, so the rise remains one impulsive leg. Practical result: you do not mark a new swing low under candles 10–11, and you do not look for inducement or order blocks there.

Downtrend mirror: after low candle 1, candle 2 breaks candle 1's low and continues — not a correction. Only when a candle breaks above candle 1's high (candle 3 in the figure) does a corrective wave exist.

Impulse illustration: after a downtrend prints its low, a large green candle breaks above the previous high, and the next few candles keep closing higher with little retracement. The whole leg from that bottom to the new high is the impulsive wave — all three conditions (strong movement, break of the prior high, sustained momentum) are visible. Mirror after a top: large bearish candles break the most recent low and later candles keep closing lower with minimal retracement.

## Key Takeaways
1. A correction requires a break of the previous candle's opposite extreme — wick or body both count.
2. If the break takes two or three candles, it is still valid; if it never comes, the leg is one impulse.
3. Inside bars never form corrections, no matter how they look.
4. Impulses need strong movement, a break of the prior swing, and sustained one-directional momentum.
5. Get this right first: every other SMC label depends on correctly segmented waves.

## Connects To
- **[fm-ch02](fm-ch02-bos-choch.md)**: valid corrections are the liquidity sweeps that BOS requires.
- **[fm-ch05](fm-ch05-inducement.md)**: the "most recent valid pullback" candle becomes the inducement level.
- **[fm-ch03](fm-ch03-liquidity-premium-discount.md)**: impulse A→B defines the premium/discount range.
- **[se-ch01](se-ch01-pulse-and-correction.md)**: the e-book's "Pulse and Correction / Correction Rule" teaches the same previous-candle-break test with lettered candles (H, K, M, U, A, N, B).
- ⚖️ Other book: agrees — the e-book also accepts either a body close or a shadow beyond the previous candle as a "sure pullback".
