# Chapter 5: Inducement – The Untold Secrets
> **Source**: *Smart Money Concepts: Unlocking the Path to High Probability Trading* — Frank Miller (2024), Ch 5, PDF pp. 61–69

## Core Idea
**Inducement (IDM)** is the most recent valid internal pullback inside an impulse — the last one formed *before* price breaks structure; price must take it out before a high/low is confirmed as *major*, before a BOS is valid, and before the deeper OB becomes tradeable. The zone nearest to price is usually the inducement trap, not the trade.

## Frameworks Introduced
- **Three sub-movements of a trend**: **Impulse → Correction → Continuation**, each built from internal candle structure.
  - Internal moves from A to B that never sweep a prior internal low form **one unified impulse leg**; minor corrections/continuations inside it are internal.
  - A **corrective movement** (bullish case) exists only when price breaks below, or sweeps with a shadow, the low of an internal pullback/internal low (B→C).
  - A **continuation** is the next push that breaks the latest swing high.
- **Candlestick-based inducement**:
  - When to use: to confirm major highs/lows and to decide whether a BOS and its OB are valid.
  - How (bullish; mirror for bearish):
    1. Find the **most recent valid pullback** — the latest bearish candle (cluster) inside the impulse.
    2. Its low is the **inducement** level.
    3. Price must take out that low — by body close, or by a wick that sweeps below and retraces.
    4. Once taken, the high above is confirmed as the **major high**.
    5. A later body close above that major high = valid BOS. Taking the IDM makes the high major, but the inducement itself is only *confirmed* once price closes beyond that major high and forms a valid BOS. The new inducement is the last internal pullback (X) formed *before* that BOS candle.
    6. If the inducement low is not taken, the move is still a single impulse — no major high, no valid BOS.
- **Inducement-based zone selection**:
  - The upper (nearer) order block formed by the most recent pullback before BOS **is the inducement zone** → do not trade it; expect it to be taken.
  - Only after price takes out that upper OB (inducement formed) do you treat the **lower (extreme) OB** as the POI for a long.
  - **No inducement → no valid BOS → no valid OB for trading.**

## Key Concepts
- **Inducement (IDM)**: liquidity at the latest internal pullback that lures early entries; taken before the real move.
- **Major high / major low**: swing confirmed only after its inducement is taken.
- **Internal structure**: minor impulses/pullbacks within a swing leg.
- **Internal pullback (X)**: last minor pullback before a BOS; the next inducement.
- **Unified impulse leg**: sequence of internal moves with no internal low swept.
- **Extreme demand/supply zone**: OB at the origin of the leg; the zone to trade after IDM.
- **Single impulse movement**: a "BOS" that happened without prior IDM — not valid.

## Mental Models
- Think of the nearest zone as bait: it exists to be taken.
- Use "IDM swept?" as the gate before calling any high/low major.
- Think of IDM as rolling forward: each new BOS moves the IDM to the last internal pullback (X) printed before that break.
- Treat a close through an unconfirmed low/high as continuation of one impulse, not a new structural break.

## Anti-patterns
- **Buying the nearest OB after a BOS**: it sits at the last pullback formed before the break — the inducement — and usually gets run.
- **Marking BOS through an unconfirmed low/high**: without IDM, the break is invalid.
- **Treating visual pullbacks as IDM**: the pullback must itself be valid (previous-candle break, Ch 1).
- **Ignoring wick sweeps**: a wick through the IDM low that retraces does count as taking IDM.

## Reference Tables

| Condition (bullish) | Result |
|---|---|
| Price takes low of most recent valid pullback (close or wick sweep) | Inducement valid → high above = major high |
| Pullback low not taken | Single impulse; no major high |
| Close above confirmed major high | Valid BOS (inducement now confirmed); new IDM = last internal pullback X before the break |
| Close above an unconfirmed high | Not a valid BOS |
| Upper OB = latest pullback before BOS | Inducement zone — do not trade |
| Upper OB taken, lower OB intact | Lower OB = POI for long |

## Worked Example
EURUSD M15, bearish momentum:
1. Price prints internal bearish impulses and pullbacks, pauses, then pushes up and takes out the most recent pullback's high → valid inducement → the low is now a confirmed **major low**. Price then closes below it → valid **BOS**, which also confirms the latest lower high as the **major high**.
2. Next IDM = the latest internal pullback of the impulse that caused the BOS (here the new major high candle). Price tries to rise but fails to surpass that internal high → no inducement → the new lower low is **not** confirmed. Price then closes below that structure — Miller rejects this as a BOS because no IDM formed first; it is one impulse.
3. Now X is the latest internal pullback, and an upper internal pullback holds a high-probability OB. Plan: wait for price to rise above X (sweep IDM), which validates the lower low as major and the BOS as valid, then look for the supply zone at the extreme. Price did exactly this: swept above X, mitigated the extreme OB, reversed with stronger bearish momentum and made a new BOS.

Diagram version (bullish): after BOS, the upper demand zone (last pullback before the break, X candle) and a lower extreme demand zone both look valid. The upper one is the inducement; wait for it to be taken, then buy the lower one.

## Key Takeaways
1. IDM = low (bull) / high (bear) of the most recent valid internal pullback, formed before the BOS.
2. A major high/low is confirmed only after its IDM is taken (close or wick sweep).
3. No IDM → no valid BOS → no valid OB.
4. The nearest OB before a BOS is the inducement; trade the extreme OB after it is taken.
5. Treat internal moves without internal sweeps as one impulse leg.
6. An IDM is confirmed only when price then closes beyond the major high/low (valid BOS); the next IDM is the last internal pullback before that break.

## Connects To
- **[fm-ch01](fm-ch01-impulsive-corrective-waves.md)**: valid pullback rule used to locate IDM.
- **[fm-ch02](fm-ch02-bos-choch.md)**: BOS definition refined here with IDM.
- **[fm-ch04](fm-ch04-order-blocks.md)**: OB-selection rules; IDM adds a new lens.
- **[fm-ch07](fm-ch07-complete-toolkit.md)**: "hidden step" — confirm liquidity/inducement before entry.
- **[se-ch02](se-ch02-bos-choch-structure.md)**: e-book: price must break the first rollback/IDM to confirm the major high; IDM carried over when a new high forms.
- **[se-ch06](se-ch06-liquidity-types.md)**: Smart Money Trap (SMT) — first pullback after BOS is a trap acting as IDM.
- ⚖️ Other book: agrees strongly, though the timing differs — Miller's IDM is the last internal pullback *before* the BOS, while the e-book's SMT is the first pullback *after* it; the e-book adds that IDM "always sits on the left side of the structure" and allows a **CHoCH without IDM** entry when the OB itself swept POI liquidity.
