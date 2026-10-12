# Section 4: Order Flow and Order Block
> **Source**: *E-book Smart Money SMC* (anonymous, 33 pp., translated), PDF pp. 12–14

*Terminology note: "softened"/"relaxed"/"eased" = mitigated; "block order"/"block of orders"/"OV" = order block (OB); "Decesional" = decisional; "IBM" = imbalance.*

## Core Idea
**Order flow (OF)** is the whole last counter-move before an impulse; the **order block (OB)** is its refined candle. A valid OB must **sweep liquidity** (previous candle or structure) **and create an imbalance**. Price reacts to only two OBs — the **decisional OB** (first block before/after IDM) and the **extreme OB** (at the impulse origin); every other block is a trap.

## Frameworks Introduced
- **Order Flow (OF)**: bearish OF = the last buying leg before a drop; bullish OF = the last selling leg before a rally.
  - When to use: to frame the zone in which an OB lives; trade OF or OB by preference.
  - How: (1) box the last opposite leg before the impulse; (2) check whether price has returned to it; (3) mitigated OF = single-use, forget it (and the OB inside is unlikely to work); (4) unmitigated OF = price may bounce from it before continuing; (5) if all OF on the chart is mitigated, look for an untouched OB in the **last impulse**.
- **Valid Order Block test**:
  - When to use: every time you mark an OB for entry.
  - How: (1) the candle takes the previous candle's high (bearish OB) or low (bullish OB), or a structure point; (2) it is followed by an imbalance; (3) if a candle has liquidity but no imbalance, the OB "moves" to the next candle that does; (4) if a candle has an imbalance but no sweep, it is a **smart trap**, not an OB.
- **Decisional vs. Extreme OB**: The decisional OB is the first block before or after the IDM; the extreme OB is the most extreme block at the start of the impulse. If price breaks through the decisional OB from the IDM side, expect it to travel to the extreme OB.

## Key Concepts
- **Order flow (OF)**: the full last counter-leg before an impulse; single-use once touched.
- **Order block (OB)**: refined OF candle with liquidity sweep + imbalance.
- **Decisional OB**: first valid OB adjacent to the IDM.
- **Extreme OB**: the OB at the impulse origin; the deepest valid zone.
- **Smart trap**: a candle with imbalance but no liquidity sweep, looking like an OB.
- **Mitigated ("softened")**: price has already returned to the zone; its orders are spent.
- **Moved OB**: when the obvious candle lacks an imbalance, the OB shifts to the next candle after which an imbalance appears; that candle need not sweep again (the previous candle already took the liquidity).

## Mental Models
- Think of OF as the **neighbourhood** and OB as the **house**: price sometimes reacts at the neighbourhood edge and never knocks on the door.
- Use "two doors only": decisional or extreme; everything between is bait.
- Mitigation is consumption: a zone that has been touched has already filled its orders.

## Anti-patterns
- **Last-opposite-candle OB**: marking the last bearish candle before a rally without checking sweep + imbalance.
- **Trading a mitigated OF/OB**: single use only.
- **Trading middle blocks**: blocks other than decisional/extreme are traps.
- **Ignoring the sweep**: "correct imbalance, but no liquidity — it's a smart trap."

## Reference Tables
| Candle (pp. 13–14) | Sweeps prior candle? | Imbalance after? | Verdict |
|---|---|---|---|
| Takes previous candle's high, gap follows | ✅ | ✅ | Valid bearish OB |
| Previous candle "peaked" but no gap | ✅ | ❌ | Cancelled — look at candles below |
| Clean gap but prior high untouched | ❌ | ✅ | Smart trap |
| Takes liquidity, no gap | ✅ | ❌ | Not an OB ("moved" to next candle) |
| Takes previous low, gap above | ✅ | ✅ | Valid bullish OB |

| OF status | Implication |
|---|---|
| Unmitigated | Price may react before reaching the OB |
| Mitigated | Forget it; OB inside unlikely to hold |
| All OF mitigated | Seek an untouched OB in the last impulse |

## Worked Example
p. 14 "Bearish block order" real chart: after a CHoCH and a marked **basic IDM**, the author scans the supply above. Two candles that **took the previous candle's high and left a proper imbalance** get green ticks as valid OBs. Two other boxes are crossed out — "no liquidity, so this is an invalid block of orders" — even though they look like supply. Price returns to a valid OB and drops to the target. "Bullish block order" chart: the valid OB is the candle that removed the previous candle's low with an imbalance above; a later candle that took liquidity but left **no imbalance** is rejected ("no order block").

## Key Takeaways
1. OB = liquidity sweep + imbalance — both required.
2. OF is the context; OB is the refined entry.
3. Mitigated zones are single-use; skip them.
4. Only decisional and extreme OBs matter; others are traps.
5. If the decisional OB fails, target the extreme OB.

## Connects To
- **[se-ch03](se-ch03-imbalance-fvg.md)**: imbalance definition.
- **[se-ch06](se-ch06-liquidity-types.md)**: SMT — the first pullback/OB after BOS is a trap.
- **[se-ch09](se-ch09-entry-models.md)**: single-candle OB entries on the LTF.
- **[fm-ch04](fm-ch04-order-blocks.md)**: Miller's three-criteria OB (sweep + imbalance + MSS), OB selection rules and ATR sizing.
- ⚖️ Other book: Miller adds a third criterion (BOS/CHoCH after the OB), picks the lower OB in uptrends/higher in downtrends and uses premium/discount; he does not label middle blocks as traps or use decisional/extreme terminology.
