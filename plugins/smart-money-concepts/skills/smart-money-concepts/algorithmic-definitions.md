# Algorithmic Definitions

The books' rules restated as testable definitions for indicators, screeners and backtests. Book rule sources in brackets; lines marked **[interp]** are implementation choices the books leave open — expose them as parameters.

Notation: candle `c[i]` has `o, h, l, cl` (open, high, low, close); `i` increases with time; evaluate only closed candles.

## 1. Valid pullback (corrective wave) [FM ch1, SE s1]
Uptrend, running extreme candle `E` = candle with the highest high since the last structural low.
- Pullback starts when a later candle `j` has `l[j] < l[E]` (body or wick; colour irrelevant per SE s1).
- Also valid (advanced case, FM): candle `j` breaks above `h[E]` making a new extreme `E' = j`, then `j+1` has `l[j+1] < l[j]`.
- Candles with `l >= l[E]` and `h <= h[E]` are inside bars → no pullback; the leg continues.
Downtrend mirrors with highs.

## 2. Swing points and internal vs major [FM ch5, SE s2]
- **Internal pullback low (uptrend)**: lowest low of a valid pullback inside the current leg.
- **IDM (uptrend)**: the most recent internal pullback low before the leg's current high `H`.
- **Major high confirmed** when a later candle trades below IDM (`l < IDM`, close or wick) [FM ch5: body close *or* wick sweep counts].
- On confirmation, the lowest low between the previous major high and `H` becomes the **major low** (protected low) **[interp]**. SE p. 9 times it differently: the lowest point of the retracement that swept the IDM is confirmed as the main low when the next BOS prints.
- FM: the IDM is the last internal pullback formed *before* the BOS candle, and an inducement only counts as confirmed once price then closes beyond the major high/low (valid BOS). SE: the first pullback/OB after the BOS is the trap (SMT).
- If price makes a higher high before IDM is taken, the IDM moves up to the newest internal pullback (SE: "IDM is carried over").
Downtrend mirrors.

## 3. BOS [FM ch2, SE s2]
Uptrend: `cl[j] > major_high` where `major_high` is confirmed (section 2).
- FM mode adds: the pullback preceding `j` swept the prior pullback low (`l < prior_pullback_low`) before `j`.
- A candle with `h[j] > major_high` and `cl[j] <= major_high` = **sweep**, not BOS. A later candle closing above = BOS (second attempt); SE requires that close to exceed the sweeping candle's high too (`cl > max(major_high, h[sweep])`).
- SE: a break with no IDM formed before it is not a valid BOS (treat as one impulse).
Downtrend mirrors with `cl[j] < major_low`.

## 4. CHoCH [FM ch2, SE s2, s9]
Uptrend → bearish CHoCH at the first `cl[j] < L_bos`, where `L_bos` = the low from which the last bullish BOS leg started.
- SE context rule: a break of the nearest internal low is IDM unless price has tapped an HTF POI/OB; after the tap it is the LTF CHoCH.
- Parameter `choch_requires_close` default `True` (FM). SE LTF entry mode: `False` on the LTF after an HTF POI tap (wick counts).
- Reversal confirmed when a BOS in the new direction follows the CHoCH [FM ch2].

## 5. Liquidity sweep [FM ch2–3, SE s2]
Level `X` (swing high, EQH, session high, PDH, TL value), buy-side; mirror for sell-side.
- FM mode: sweep when `h[j] > X` (wick **or** close through a pullback/liquidity level both count).
- SE mode / structural levels: `h[j] > X and cl[j] <= X` = sweep; `cl[j] > X` at a major level = BOS/CHoCH candidate (sections 3–4), not a sweep.
- **EQH/EQL**: ≥2 swing highs/lows within tolerance `eq_tol` **[interp; e.g. 0.1 × ATR]**; double (2), triple (3).
- **Trendline liquidity**: line through ≥2 minor lows (uptrend) / highs; liquidity lies just beyond it [FM ch3].
- **Session levels** [SE s6]: high/low of Asia, London, New York **[interp: session hours are broker/market specific; parameterise]**.
- **Previous-candle liquidity**: `h[j] > h[j-1]` (or `l[j] < l[j-1]`).

## 6. Imbalance / FVG [FM ch4, SE s3]
- Bullish at `i` (middle candle): `h[i-1] < l[i+1]`; zone = `[h[i-1], l[i+1]]`.
- Bearish at `i`: `l[i-1] > h[i+1]`; zone = `[h[i+1], l[i-1]]`.
- Filled when later price trades through the whole zone (SE: "eliminated") **[interp: full vs partial fill as parameter]**.

## 7. Order block [FM ch4, SE s4]
Bullish OB candidate candle `k` (end of a down move, before the up move):
1. `l[k] < l[k-1]` (sweeps previous candle's low).
2. A bullish imbalance exists at `k+1` — or at `k+2`/`k+3`, in which case the OB zone spans candles `k..(imbalance start)` [FM ch4 "cluster"].
3. FM mode: a bullish BOS or CHoCH occurs after `k` in the same move.
- SE: if the sweep candle has no imbalance after it, the OB moves to the adjacent next candle(s) after which an imbalance appears; that candle need not sweep again (the previous candle already took the liquidity).
- Zone: `[l[k], h[k]]` **[interp: SE charts use the full candle incl. wicks; FM enters at the upper edge]**. SE p. 22: when a pullback already mitigated part of the candle, the author draws the POI on the remaining wick — expose `poi_draw = 'candle' | 'wick'`.
- Small OB: if `h[k]-l[k] < 0.6 × ATR(14)`, set `mid=(h[k]+l[k])/2; zone=[mid-ATR/2, mid+ATR/2]` (total height 1 ATR) [FM ch4; **interp**: FM says only "extend… from both sides", the equal split is ours].
- **Mitigated** when price later returns into the zone; mitigated OBs are ignored [FM Rule 3, SE].
- Multiple OBs in one leg: bullish → choose lowest unmitigated; bearish → highest, except when the lower OB's candle already tapped the upper OB (upper is triggered → use the lower); never use a triggered OB [FM Rules 1–3].
- Premium/discount filter: bullish OB must be below 50% of impulse A→B [FM ch3–4].
- SE classes: **decisional** = first OB before/after IDM; **extreme** = OB at impulse origin.
Bearish mirrors.

## 8. Order flow [SE s4]
Bearish OF = the last up-move (leg) before the down impulse; bullish OF = last down-move before the up impulse. Single-use once touched.

## 9. POI [FM ch6, SE s7]
HTF zone whose formation swept liquidity (`l[k] < prior low` for demand). POI with imbalance + structure shift = OB (strongest).
- Type 1 basic: pullback sweeps previous minor high/low, then BOS; wait for retrace.
- Type 2 modified: skip non-sweeping pullbacks; use the zone that swept.
- Types 3–4: sweep of nearest high/low during a pullback (wick sweep, or close-above + bearish candle pair) → go to LTF immediately.

## 10. Premium / discount [FM ch3]
Impulse `A` (start) → `B` (end). `eq = (A+B)/2`. Uptrend: discount = price < eq. Downtrend: premium = price > eq.

## 11. Candle Breakout Pattern [FM ch8]
At a POI/OB, bullish: reaction candle `r` (bearish) touches the zone; confirmation `r+1` bullish with `cl[r+1] > o[r]` and `o[r+1] <= cl[r]` (engulfs body).
- Liquidity-swept variant: `l[r+1] < l[r]` → no LTF IDM required.
- 1-TF long: limit at `h[r]` (or `cl[r]` per FM's later examples), SL < `l[r]` or < POI low. The POI must already be inducement/liquidity-validated.
- In FM's EURUSD H1 example the reaction candle is the first *same-direction* candle touching the POI; expose `reaction_color_strict` (default `True`).

## 12. IFC [SE s5]
Candle sweeps a major swing / session high-low / IDM (`h > X`, `cl <= X`) → becomes POI; enter only on LTF confirmation.

## 13. Previous-candle entry [SE s9]
Inside an active LTF POI, short: `h[j] > h[j-1]` and `cl[j]` bearish/back below → enter at `o[j+1]`. Repeat to add until the LTF major low breaks. Long mirrors.

## 14. Session bias [SE s6] **[interp: direction = close vs open of session]**
- `dir(Asia) == dir(London)` → expect NY reversal.
- London swept Asia high or low → expect NY continuation of London.

## 15. Risk [SE s10, FM ch7–8]
`position_size = equity × risk_pct / |entry − stop|`; `risk_pct` ∈ [0.01, 0.02] own, [0.0025, 0.01] funded. Break-even: FM → move stop to entry after a new LTF BOS in favour; SE → move to BE after the recent structure breaks only when no IDM/unmitigated block remains between price and the recent high/low (`be_requires_clear_idm=True`). TP = nearest opposing major swing / liquidity, or fixed `R` (2, 3, 5).
