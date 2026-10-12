# Chapter 7: SMC Complete Toolkit
> **Source**: *Smart Money Concepts: Unlocking the Path to High Probability Trading* — Frank Miller (2024), Ch 7, PDF pp. 79–87

## Core Idea
Miller's complete, highest-win-rate SMC setup chains everything together: **HTF structure (BOS/CHoCH) → POI → wait for price at POI → LTF Advanced CHoCH → LTF Order Block → limit order**, with a hidden step of confirming that liquidity/inducement was swept, longs in discount and shorts in premium.

## Frameworks Introduced
- **Detailed Steps for Entering a Trade (5 main steps)**:
  1. **Identify the Market Structure** — uptrend or downtrend via BOS or CHoCH.
  2. **Identify the POI** — the zone price is likely to retrace to (longs: in discount; shorts: in premium).
  3. **Wait for Price to Retrace to the POI** — patience; then switch to a lower timeframe.
  4. **Identify the Advanced CHoCH and Order Block on a lower timeframe** — choose the best OB in the zone.
  5. **Place the Limit Order** — at the OB's edge (long: upper edge; short: lower edge); stop just beyond the OB; TP at 2R, 3R, 5R or the next major high/low (liquidity).
  - **Hidden step**: identify liquidity/inducement and confirm it has been swept before execution.
  - Premium/discount also picks between multiple OBs.
- **Immediate-sweep variant (POI types 3–4)**:
  - When to use: price has just swept a pullback with a strong wick candle.
  - How: the wick candle becomes the POI; do not wait for a retrace — go to LTF (e.g. M5), find the Advanced CHoCH, wait for an extra inducement to form and be taken, then place a limit at the OB (last candle that swept previous liquidity).
- **Stop trailing**: as price moves, trail the stop to successive structure levels (X1, X2, X3) above entry → risk reduced to zero.

## Key Concepts
- **Setup chain**: structure → POI → retrace → Advanced CHoCH → OB → limit order.
- **Advanced CHoCH (LTF)**: break of the minor high from which the nearest low (X) was formed.
- **LTF OB**: last candle of the counter wave that swept the previous candle, with imbalance after it.
- **Inducement (post-CHoCH)**: the pullback candle that sweeps the lowest liquidity after the CHoCH.
- **Limit entry at OB edge**: upper edge for longs, lower edge for shorts.
- **Liquidity target**: previous highs/lows where price tends to return.
- **R multiples**: 2R/3R/5R fixed targets or structure targets.
- **Trailing stop X1–X3**: stop moved to new structure levels.

## Mental Models
- Think of the chain as gates — each must pass before the next is checked.
- Use HTF for *where* and LTF for *when/exactly where*.
- Think "targets are liquidity": set TP at the previous high/low that will be swept.
- Prefer rare, clean setups; Miller says these models have the highest win rate but appear infrequently — start with them if new.

## Anti-patterns
- **Skipping the retrace wait**: entering before price reaches the POI.
- **Entering on the HTF touch** without an LTF Advanced CHoCH.
- **Forgetting the hidden inducement step**: entering before liquidity is swept.
- **Longs in premium / shorts in discount**.
- **Leaving the stop at the original level** when structure allows trailing.

## Reference Tables

| Step | Timeframe | Output | Pass condition |
|---|---|---|---|
| 1 Structure | HTF (e.g. M15, H1) | Trend direction | Valid BOS/CHoCH |
| 2 POI | HTF | Zone | Liquidity swept; discount (long) / premium (short) |
| 3 Retrace | HTF | Price at POI | Touch |
| 4 Advanced CHoCH + OB | LTF (e.g. M3, M5) | Entry zone | CHoCH + OB (sweep + imbalance) + IDM taken |
| 5 Order | LTF | Limit, SL, TP | SL beyond OB; TP at liquidity or R multiple |

| Trade parameter | Long | Short |
|---|---|---|
| Entry | Upper edge of OB | Lower edge of OB |
| Stop loss | Just below OB | Just above OB |
| Take profit | Previous highs / next major high / 2–5R | Previous lows / next major low / 2–5R |

## Worked Example
**Example 1 — 11R long (M15 → M3)**:
1. M15 uptrend: price swept the pullback's liquidity, then broke the high that started the pullback → new BOS.
2. POI in the discount zone, with an inducement above it (a sweep of the previous candle). The POI is marked *before* the A–B pullback occurs.
3. Price touches the POI → switch to M3.
4. M3: the Advanced CHoCH forms when price breaks the minor high from which the nearest low X was formed. OB = last candle of the bearish wave (small body, wicks) — it swept the previous candle and has a large imbalance above it. After the CHoCH, a pullback sweeps the previous candle's low → inducement.
5. Limit at the OB's upper edge, SL just below the OB, TP at previous highs (liquidity) → **11R**. Price chopped briefly and then hit TP quickly.

**Example 2 — 4.5R long, immediate sweep (M5)**:
CHoCH from downtrend to uptrend; a pullback is swept by a very strong wick candle → that wick candle is the POI; no waiting. On M5 the Advanced CHoCH takes two steps: (a) a pullback that breaks and sweeps above the previous candle's high qualifies as a *valid pullback*; (b) when price then breaks above that pullback's high, the Advanced CHoCH is confirmed. Then wait for inducement: pullback A→B is valid only if price breaks above A; it does, forming minor high C → inducement present. OB = last candle that swept previous liquidity. Limit long at the OB's upper border, SL below the OB, TP at the previous high where liquidity was swept → **4.5R**. Stop trailed to X1, X2, X3 above entry as price rose, making the trade risk-free.

## Key Takeaways
1. Five steps: structure → POI → retrace → LTF Advanced CHoCH + OB → limit order.
2. Always confirm liquidity/inducement has been swept first (the hidden step).
3. Longs in discount, shorts in premium; use it to choose between OBs.
4. Entry at the OB edge, stop beyond the OB, target the next liquidity pool or 2–5R.
5. A strong wick sweep can itself be the POI — enter via LTF without waiting.
6. Trail the stop along new structure to take risk to zero.

## Connects To
- **[fm-ch02](fm-ch02-bos-choch.md)**, **[fm-ch03](fm-ch03-liquidity-premium-discount.md)**, **[fm-ch04](fm-ch04-order-blocks.md)**, **[fm-ch05](fm-ch05-inducement.md)**, **[fm-ch06](fm-ch06-poi-advanced-choch.md)**: every building block used here.
- **[fm-ch08](fm-ch08-candle-breakout-strategy.md)**: alternative execution when price never retraces to the LTF OB.
- **[se-ch09](se-ch09-entry-models.md)**: e-book entry modules (CHoCH with/without IDM, Flip, one-candle entries).
- **[se-ch10](se-ch10-trade-examples-risk-management.md)**: e-book trade examples and risk rules (1–2% risk, move SL to BE after recent high/low breaks).
- ⚖️ Other book: the e-book targets 1:5–1:10 R:R and warns against chasing 1:30–50; it also adds scaling in with previous-candle-sweep entries, which Miller's toolkit does not use.
