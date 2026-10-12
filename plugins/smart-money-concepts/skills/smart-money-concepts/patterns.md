# Patterns & Techniques

Every setup and technique in the two books. Source in brackets.

## Top-down POI → LTF CHoCH → OB entry (the core model) [FM ch7, SE s8–s9]
**When to use**: default setup in any trending market.
**How**: HTF: confirm trend via BOS (with sweep + IDM) → mark POI (swept liquidity, ideally OB + imbalance, in discount for longs / premium for shorts) → wait for price to tap it → LTF: wait for CHoCH → mark the LTF OB that caused the CHoCH → wait for LTF IDM sweep → limit at OB edge (upper edge for longs, lower for shorts), SL beyond OB, TP at next liquidity (major high/low) or 2R/3R/5R.
**Trade-offs**: highest quality, infrequent; price may run without retracing to the LTF OB (→ CBS or module 4).

## Candle Breakout Strategy (CBS) [FM ch8]
**When to use**: price reacts at a POI but won't retrace deep enough to fill the LTF extreme OB; or you want a single-TF execution.
**How**: reaction candle touches POI/OB; confirmation candle engulfs its body. 1-TF: limit at reaction candle high (long) / low (short) — or at its close in FM's later examples — SL beyond reaction candle or POI, TP nearest major high/low or 3R/5R. 2-TF: find LTF OB inside the reaction candle; if the confirmation candle swept the reaction candle's liquidity, no IDM needed; else wait for LTF IDM. Scale in at several LTF OBs inside the reaction candle.
**Trade-offs**: safer, clearer entries; lower R:R than LTF OB entries.

## CHoCH with IDM [SE s9 module 1]
**When to use**: LTF reversal at an HTF POI.
**How**: HTF POI tapped → first LTF break of the nearest high/low = CHoCH (on LTF at entry time even a wick counts) → wait for the pullback that forms IDM → enter at the OB beyond the IDM (or single-candle OB).
**Trade-offs**: skipping the IDM wait = entering the trap block.

## FLiP with IDM (D2S / S2D) [SE s9 module 2]
**When to use**: at an HTF supply POI, price does not break structure directly but reacts off a small LTF demand, then breaks it.
**How**: failed demand becomes supply; after IDM, sell the first nearest OB/supply above; if another unmitigated block sits above, wait for single-candle or liquidity-sweep confirmation instead of selling directly.
**Trade-offs**: needs clear failure of the flipped zone.

## CHoCH without IDM [SE s9 module 3]
**When to use**: the HTF POI touch itself swept liquidity (liquidity POI on the left).
**How**: after LTF CHoCH (wick acceptable), buy/sell the last OB immediately without waiting for IDM.
**Trade-offs**: faster, fills more often; lower confirmation.

## Previous-candle liquidity entry / single-candle entry [SE s9 modules 4–5]
**When to use**: price is inside a defined LTF POI and trending away from it.
**How**: a candle takes the previous candle's high and closes bearish (shorts), or takes its low and closes bullish (longs) → enter at the next candle's open. The liquidity-sweep entry (a larger structure/IDM/POI low or high taken) executes the same way. Repeat to add positions until the LTF major low/high breaks; then wait for a new structure and its IDM.
**Trade-offs**: excellent for scaling winners; useless outside a POI.

## BOS (continuation) entry [SE s9 module 6]
**When to use**: after a new LTF BOS in the direction of the move (SE p. 27 shows it following a CHoCH at an HTF POI).
**How**: once the BOS has been "released by IDM" (its IDM swept), enter at the OB beyond it or at a one-candle absorption (engulfing) OB.
**Trade-offs**: the chart shows it repeating on consecutive BOS; waiting for the IDM costs fills when price runs.

## Liquidity-sweep-then-zone [FM ch3, SE s6]
**When to use**: equal highs/lows, trendline, range edge or session high/low sits in front of an OB/demand/supply.
**How**: do not trade the pattern; wait for price to sweep it and tap the zone beyond it; then take LTF confirmation.
**Trade-offs**: misses trades when price reverses before the sweep.

## Selecting among multiple OBs [FM ch4, SE s4]
**When to use**: two or more valid OBs in the same leg.
**How**: uptrend → lower OB, downtrend → higher OB (nearer one = liquidity); skip mitigated OBs; downtrend exception: if the lower OB's candle already tapped the upper one, use the lower; filter with premium/discount (discount only for buys). SE: decisional OB first, extreme OB if the decisional breaks.
**Trade-offs**: the extreme OB may never be reached.

## OB sizing [FM ch4]
**When to use**: marking the OB zone.
**How**: OB range < 0.6 × ATR(14) → widen it symmetrically until the total zone = 1 ATR (or use a larger SL); OB too wide → refine to an LTF OB.

## IFC reversal [SE s5]
**When to use**: a candle sweeps a major swing/session high-low/IDM but closes back inside.
**How**: mark the IFC candle as POI; enter on LTF confirmation (CHoCH or one-candle entry) after its close.

## Session manipulation [SE s6]
**When to use**: intraday Forex/indices.
**How**: Asia + London same direction → expect NY to reverse (sell/buy NY after it sweeps London); London swept Asia → NY continues London. Enter after a session high/low sweep with one-candle entry or LTF CHoCH. A candle that closes with a body beyond the session high/low is not a sweep setup — trade it only after an LTF CHoCH. The session can be any session.

## Daily-candle liquidity [SE s6]
**When to use**: planning the day's bias.
**How**: momentum bullish → buy after the previous daily candle's low is swept; bearish → sell after its high is swept; drop to M15 and wait for the nearest structure break. Trades against momentum are short-term counter-trades only.

## Trendline trap [SE s6, FM ch3]
**When to use**: a clean retail trendline forms.
**How**: breakout traders get trapped; after the TL breaks, find the IDM and the first OB beyond it, enter on LTF confirmation in the opposite direction of the retail breakout (or with trend after the TL liquidity sweep into the extreme demand/supply).

## Imbalance entry [SE s3]
**When to use**: all OBs below (for longs) are already mitigated.
**How**: use the last unfilled imbalance as the entry zone — main liquidity is already gone.

## Stop management [SE s10, FM ch7–8]
**How**: SL beyond OB/POI; FM: move to entry after a new LTF BOS; SE: move to BE after the recent structure breaks only when no IDM/unmitigated block remains near the recent high/low; SE: take partials when the BE point is far from entry and at the recent major low/high; trail to successive higher lows (X1, X2, X3) in trending trades; close at TP rather than stretching targets.
