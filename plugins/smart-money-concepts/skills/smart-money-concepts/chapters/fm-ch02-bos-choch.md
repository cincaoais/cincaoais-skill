# Chapter 2: BOS and CHoCH
> **Source**: *Smart Money Concepts: Unlocking the Path to High Probability Trading* — Frank Miller (2024), Ch 2, PDF pp. 17–23

## Core Idea
A **Break of Structure (BOS)** confirms trend continuation and a **Change of Character (CHoCH)** signals a potential reversal — but in Miller's method both are only valid when (1) a liquidity sweep of the prior pullback has occurred and (2) a candle **body closes** beyond the structural level. Wicks never confirm structure.

## Frameworks Introduced
- **Valid BOS — two key elements**:
  - When to use: to decide whether the trend is still intact and whether a new leg can produce a tradeable POI/OB.
  - How (uptrend; mirror for downtrend):
    1. **Liquidity sweep**: the current pullback must break below the lowest point of the previous pullback (by close *or* wick). Miller marks this "C – Correction".
    2. **Cross the previous high**: price then rallies and a candle **closes above** the prior swing high.
    3. If only a wick exceeds the high, it is not a BOS — wait for a body close.
    4. If price makes a new high without first sweeping the latest pullback low, do not mark a new BOS (it is still the same leg).
- **Valid CHoCH**:
  - When to use: to detect the first structural sign that the trend is reversing.
  - How (uptrend → downtrend):
    1. Identify the low that produced the most recent BOS (the origin of the last up-leg).
    2. A candle must **close below** that low → CHoCH. A wick below does not qualify.
    3. Typically the CHoCH move begins with a liquidity sweep of the prior highs.
    4. Treat CHoCH as an *initial signal only* — do not enter immediately.
    5. Reversal confidence rises when a **CHoCH is followed by a BOS** in the new direction.

## Key Concepts
- **Break of Structure (BOS)**: close beyond the previous swing high/low in the trend direction, after a liquidity sweep.
- **Change of Character (CHoCH)**: close beyond the low (uptrend) or high (downtrend) that created the latest BOS.
- **Liquidity sweep**: price trading through a prior high/low (e.g. a pullback taking out the prior pullback's extreme), triggering stops/pending orders. A body close *or* a wick through the level both count as a sweep; the wick-vs-close distinction only applies when confirming a BOS/CHoCH.
- **Candle-close confirmation**: body close, not wick, is the test for BOS/CHoCH.
- **Structural level**: the swing high/low that must be closed through.
- **CHoCH + BOS sequence**: the combination that confirms a reversal.

## Mental Models
- Use "sweep first, then close through" as the two-step key that unlocks any BOS or CHoCH.
- At a structural level (the prior swing high for a BOS, the BOS origin for a CHoCH), think of a wick beyond it as only a liquidity grab and a body close beyond it as the structural break — same price, different meaning. At a pullback extreme, either a wick or a close is simply a sweep.
- Think of CHoCH as a yellow light, and CHoCH + BOS as the green light.
- Treat structure analysis as the foundation only; trade setups need more confluence (POI, OB, inducement).

## Anti-patterns
- **Marking BOS on a wick**: a wick above the high without a close is a sweep, not a break — the classic fake-out.
- **Marking BOS without a sweep**: a new high with no prior pullback liquidity taken does not create a new BOS (e.g. the move to 9 in the example).
- **Entering on CHoCH alone**: CHoCH is only the first sign; enter after further confirmation.
- **Marking structure before the candle closes**: repeated in Ch 9 as a top mistake.

## Reference Tables

| Event | Sweep of prior pullback? | Body close beyond level? | Verdict |
|---|---|---|---|
| Wave 4 sweeps wave 2's low, wave 7 closes above wave 3's high | ✅ | ✅ | Valid BOS |
| Pullback 6→ rally to 9 without breaking 6's low | ❌ | — | No new BOS |
| Rally at 15 after sweep, closes above prior high | ✅ | ✅ | Valid BOS |
| Wick exceeds prior high, body closes below | ✅/❌ | ❌ | Not BOS (sweep only) |
| Close below low of latest BOS (point 12) after sweeping highs 11 and 13 | ✅ | ✅ | Valid CHoCH |
| Downtrend diagram (Fig 2.2): sweep at point 15, then close above the high that produced the last bearish BOS | ✅ | ✅ | Valid bullish CHoCH |
| Wick below latest BOS low, close back above | — | ❌ | Not CHoCH |

| Signal | Meaning | Action |
|---|---|---|
| BOS | Trend continues | Look for POI/OB in the new leg |
| CHoCH | Possible reversal | Watch; no entry yet |
| CHoCH → BOS (new direction) | Reversal confirmed | Plan trades in new direction |

## Worked Example
Theoretical chart (uptrend, waves 1–15): up-moves 1, 3, 5, 7 and pullbacks 2, 4, 6. Pullback 4 dips below pullback 2's low (by wick or close — either is a sweep). Then wave 7 closes above wave 3's high → **BOS**. The next rally to 9 is *not* marked, because pullback 6's low was never swept. At 15, a sweep occurs and price closes above the prior high → another **BOS**. Later, after sweeping two consecutive highs (11 and 13), price closes below point 12 — the low that created the latest BOS → **CHoCH**, uptrend → downtrend.

Live chart: two valid corrections ("C") sweep nearby lows. After the first pullback, the first attempt at the prior high only wicks above it → not BOS; the second attempt closes above → valid BOS. The second pullback is followed by one strong candle closing above the high → a very clear second BOS. Later, alternating moves end with a close below the low that formed the latest BOS → CHoCH.

Bullish mirror (separate downtrend diagram, Fig 2.2): price sweeps liquidity and makes a BOS, sweeps again and makes a second bearish BOS. The reversal leg then begins with a liquidity sweep at point 15, and a candle closes above the most recent prior high — the high that produced the last bearish BOS → **bullish CHoCH**. As in the bearish case, the CHoCH starts with a sweep; look for a following bullish BOS before trusting the new trend.

## Key Takeaways
1. BOS = liquidity sweep of the prior pullback + body close beyond the prior swing.
2. CHoCH = body close beyond the low/high that created the most recent BOS.
3. A wick beyond a structural level is a liquidity sweep, never a confirmation. For the sweep itself, a wick or a close through the prior extreme both count.
4. No sweep → no new BOS, even if price prints a new extreme.
5. Treat CHoCH as a warning; a following BOS confirms the reversal.
6. Structure identification comes first, but it alone is not a trade setup.

## Connects To
- **[fm-ch01](fm-ch01-impulsive-corrective-waves.md)**: valid corrections define which lows/highs can be swept.
- **[fm-ch03](fm-ch03-liquidity-premium-discount.md)**: liquidity sweeps explained in full.
- **[fm-ch05](fm-ch05-inducement.md)**: inducement adds the requirement that a major high/low be confirmed before a BOS is valid.
- **[fm-ch06](fm-ch06-poi-advanced-choch.md)**: "Advanced CHoCH" is the same idea on the lower timeframe after a POI.
- **[fm-ch09](fm-ch09-pitfalls.md)**: Pitfall #4 — misinterpreting BOS and CHoCH.
- **[se-ch02](se-ch02-bos-choch-structure.md)**: the e-book's BOS/CHoCH structure display with IDM-based major high/low confirmation.
- ⚖️ Other book: agrees that HTF structure needs a full candle close, but the e-book allows a **wick** to count as CHoCH on the **LTF at entry time** and defines CHoCH as the break of the first recent high/low after price touches a POI.
