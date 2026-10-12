# Chapter 4: Powerful Order Blocks in SMC Trading
> **Source**: *Smart Money Concepts: Unlocking the Path to High Probability Trading* — Frank Miller (2024), Ch 4, PDF pp. 42–60

## Core Idea
An Order Block is not simply "the last opposite candle before a move": Miller's rule-based OB is **the last candle that sweeps liquidity** in the move, **followed by an Imbalance**, and **followed by a market structure shift (BOS or CHoCH)**. When several OBs qualify, choose by position, mitigation status, and premium/discount.

## Frameworks Introduced
- **Imbalance (3-candle gap)**:
  - How: take candles 1, 2, 3. Draw a line at candle 1's high and candle 3's low (bullish case). If they do not overlap, the gap is an **Imbalance**. If the wicks overlap, there is no imbalance, even if it looks like one.
  - Imbalance = inefficiency = fair value gap in Miller's usage; it shows smart money entered and price tends to return to fill remaining orders.
  - Always mark imbalances while mapping structure — Miller calls this the first rule of identifying a valid OB, because the supply/demand area that created the imbalance becomes the strong level.
- **Proper Order Block — 3 criteria**:
  1. The **last candlestick that performs a liquidity sweep** during a strong up/down move (its wick exceeds the prior candle's wick).
  2. It must be **followed by an Imbalance**.
  3. There must be a **market structure shift** (BOS or CHoCH) after it.
  - When the sweep candle is not immediately followed by the gap but the next candle is, the OB spans **both candles** (OB cluster; can be 3 candles).
- **Choosing among multiple OBs**:
  - **Rule No.1: Use the lower Order Block in an uptrend.**
  - **Rule No.2: Use the higher Order Block in a downtrend.** (the nearer OB acts as the liquidity pool for the farther one)
  - **Rule No.3: Do not use an Order Block that has already been triggered.** If the lower OB's wick already tapped the upper OB, the upper one's orders are used up → trade the other one.
  - **Premium/discount filter**: draw 0/50/100% on the wave A→B (or estimate the 50% visually); discard OBs in the wrong half and mitigated OBs; the remainder is the trade.
- **OB sizing rules**:
  - Too large (long body + long wicks): refine on a lower timeframe for a tighter entry.
  - Too small: if OB range < **60% of ATR(14)**, widen the zone symmetrically (both sides) until its **total height = 1 × ATR** (e.g. ATR 30 pips → OB under 18 pips → the zone becomes 30 pips; a 15-pip OB gets +7.5 pips above and below), or keep the OB and use a larger stop below it.
- **Types of OB**: **Continuation** (with trend, higher success rate) vs **Reversal** (forms after CHoCH, against the old trend, larger R:R potential).

## Key Concepts
- **Order Block (OB)**: supply/demand area meeting the 3 criteria; every OB is supply/demand, not every supply/demand is an OB.
- **Imbalance (IBL)**: non-overlapping gap between candle 1 and candle 3.
- **Liquidity sweep candle**: candle whose wick exceeds the previous candle's wick.
- **Mitigated / triggered OB**: already touched; pending orders consumed.
- **OB cluster**: 2–3 candles forming one OB when the imbalance appears after a delay.
- **Origin of the move**: the OB that launched a BOS leg — the best opportunity; others are likely liquidity grabs.
- **ATR (Average True Range)**: 14-period volatility measure used for the 60% sizing rule.
- **Internal/external structure**: promised in Miller's Ch 4 opening but not covered here; internal structure is defined in Ch 5, and "external structure" is never defined in the book.
- **Imbalance as support/resistance**: a retrace into an imbalance zone is likely to rebound (the aggressive buying that created it is still there); where there is no imbalance, support is weak and price may continue straight through.

## Mental Models
- Think "sweep + gap + break" — all three or no OB.
- Think of every nearer, unswept OB as liquidity for the farther OB.
- Use the origin of the BOS leg as the default candidate; use lower risk on intermediate OBs.
- Think of an OB as a pool of pending limit orders: once touched, it is spent.

## Anti-patterns
- **"Last bullish candle before the drop" OB**: often the wrong candle; the correct OB is typically the next candle that swept it.
- **OB without a sweep**: imbalance alone makes it a trap ("false signal").
- **Trading an imbalance on its own**: Miller says to use it together with other tools — it is one of three OB criteria, not a setup.
- **Trading a triggered OB**: its orders are gone.
- **Buying an OB in premium** during an uptrend.
- **Tight stop on a tiny OB**: gets run; apply the ATR extension.

## Reference Tables

| Candidate | Sweep | Imbalance | Structure shift | Verdict |
|---|---|---|---|---|
| Last white candle in a down move | ❌ | — | — | Not OB (lucky at best) |
| Black candle right after it, wick above white's wick | ✅ | ✅ | ✅ | Valid, reliable OB |
| Bullish candle touching prior body but not beyond prior wick | ❌ | ✅ | — | Trap |
| First candle sweeps, gap appears on the next candle | ✅ | ✅ (delayed) | ✅ | OB = both candles |

| Situation | Choose |
|---|---|
| 2 valid OBs, uptrend | Lower OB |
| 2 valid OBs, downtrend | Higher OB |
| Lower OB's wick tapped the upper OB (downtrend) | Lower OB (upper is triggered) |
| 3 OBs, uptrend | Drop premium OBs, drop mitigated ones → remaining discount OB |

## Worked Example
Premium/discount selection: uptrend wave A→B with OB1, OB2, OB3. Fibonacci 0/50/100 shows OB1 above 50% → premium → ignore. OB2 and OB3 are in discount, but OB2 was already mitigated → ignore. Trade OB3; OB2 now serves as liquidity above it.

Chart example 1 (bearish BOS): a pullback swept liquidity, then price broke lower → valid BOS. Two OBs: a middle one (swept previous high + imbalance) and a higher one that swept *multiple* highs (stronger). Short trade → choose the higher OB. Price first reacted at the lower OB, then ran up into the higher OB and dropped sharply.

Chart example 2 (OB cluster): at the end of a downtrend the longest-wick candle swept prior lows; the imbalance only appeared two candles later → the 3-candle cluster is the OB. It is wide, so drop to a lower timeframe to find a narrower OB and better R:R.

## Key Takeaways
1. OB = last liquidity-sweep candle + following imbalance + subsequent BOS/CHoCH.
2. Imbalance exists only if candle 1's and candle 3's wicks do not overlap.
3. Uptrend → lower OB; downtrend → higher OB; never a triggered OB.
4. Filter OBs with premium/discount (buy discount, sell premium).
5. OB < 60% ATR(14) → widen symmetrically to a total height of 1 ATR; oversized OB → refine on LTF.
6. Continuation OBs win more often; reversal OBs pay more.

## Connects To
- **[fm-ch03](fm-ch03-liquidity-premium-discount.md)**: sweeps and premium/discount that qualify and select OBs.
- **[fm-ch05](fm-ch05-inducement.md)**: the nearer OB before a BOS is inducement, not a trade zone.
- **[fm-ch06](fm-ch06-poi-advanced-choch.md)**: POI = sweep only; OB = sweep + imbalance + shift.
- **[fm-ch09](fm-ch09-pitfalls.md)**: Pitfall #7 — choosing the wrong OB.
- **[se-ch04](se-ch04-order-flow-order-block.md)**: e-book OB (liquidity + imbalance), decisional vs extreme OB, order flow.
- **[se-ch03](se-ch03-imbalance-fvg.md)**: imbalance/FVG examples.
- ⚖️ Other book: the e-book requires only **liquidity + imbalance** for an OB (no explicit structure-shift criterion) and says price reacts to the **decisional** OB (first block before/after IDM) or the **extreme** OB (at the impulse origin); "all other blocks are traps".
