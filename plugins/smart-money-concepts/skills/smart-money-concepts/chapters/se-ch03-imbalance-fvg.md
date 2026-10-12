# Section 3: Imbalance / Fair Value Gap (FVG)
> **Source**: *E-book Smart Money SMC* (anonymous, 33 pp., translated), PDF pp. 10–11

*Terminology note: "unbalance"/"mispricing" = imbalance; "eliminated"/"closed"/"softened" = filled/mitigated; "IBM"/"IMB" = imbalance.*

## Core Idea
A sharp move leaves an **unfilled gap between the wicks of candle 1 and candle 3** — the imbalance (FVG). It is primarily a tool for locating POIs and order blocks, and becomes an entry zone itself when every block beneath it has already been mitigated.

## Frameworks Introduced
- **Three-candle imbalance test**:
  - When to use: while marking POIs and order blocks after an impulse.
  - How: (1) take three consecutive candles in a fast move; (2) bullish: compare candle 1's **high** with candle 3's **low**; bearish: candle 1's **low** with candle 3's **high**; (3) if the wicks do not overlap, the space between is an imbalance; (4) if later price trades back through the gap ("eliminated"), it is no longer an imbalance.
- **Imbalance as OB qualifier**: The e-book's order-block definition (Section 4) requires the OB candle to be followed by an imbalance — no imbalance, no OB.
- **Extreme imbalance entry**: If all order blocks below (for buys) the imbalance are mitigated, the market has no reason to go lower — main liquidity is already taken — so use the last imbalance as the entry area.
  - How: (1) after a BOS, list the OBs beneath the imbalance; (2) confirm each is mitigated; (3) treat the imbalance fill as the POI; (4) enter on LTF confirmation (interpretation — not stated in SE; p. 11 only says "you can use the imbalance as a place to enter").

## Key Concepts
- **Imbalance / FVG**: wick-to-wick gap between candles 1 and 3 of a sharp move.
- **Mispricing**: the sharp, one-sided move that creates the gap.
- **Eliminated (filled) imbalance**: price has traded back through it; no longer valid.
- **Bullish imbalance**: gap below price after a rally (support on return).
- **Bearish imbalance**: gap above price after a drop (resistance on return).
- **Extreme imbalance**: the last unfilled gap at the origin of an impulse, used when no fresh OB remains.

## Mental Models
- Think of the FVG as a **magnet with a lid**: price tends to return to fill it, and the lid (unmitigated OB or gap edge) is where it reacts.
- Use the imbalance **to qualify zones, not as a standalone signal** — it upgrades a candle into an OB.
- "Nothing left below" logic: when every block below is mitigated, the imbalance is the only remaining institutional footprint.

## Anti-patterns
- **Counting overlapped wicks as a gap**: if candle 1's and candle 3's wicks touch, there is no imbalance even if the bodies look gapped.
- **Trading an already-filled gap**: once eliminated, forget it.
- **Entering at the imbalance while fresh OBs sit below it**: price will likely drive through to the OB.

## Reference Tables
| Setup (p. 10) | Gap between | Filled? | Imbalance? |
|---|---|---|---|
| Bearish drop, candles K → H | K low vs H high | No | ✅ |
| Bearish drop, candles K → H | K low vs H high | Yes | ❌ |
| Bearish drop, candles A → N | A low vs N high | No | ✅ |
| Bearish drop, candles A → N | A low vs N high | Already filled | ❌ |
| Bullish rally, K → H | K high vs H low | No | ✅ |
| Bullish rally, K → H | K high vs H low | Closed | ❌ |
| Bullish rally, A → N | A high vs N low | No | ✅ |
| Bullish rally, N → A | N high vs A low | Closed | ❌ |

## Worked Example
p. 11, upper chart: price breaks structure upward (BOS), rallies, then pulls back deeply. Every order block beneath the last imbalance has already been mitigated ("all blocks are softened below the imbalance"), so the author reasons the market has no reason to fall further — its main liquidity is gone. Price drops exactly into the last imbalance, fills it, and continues upward in a strong impulse. Lower chart repeats the idea for a bearish move: after a bearish BOS, price retraces into the upper imbalance and then collapses. Lesson: when OBs are exhausted, the imbalance itself is the POI.

## Key Takeaways
1. Imbalance = unfilled wick gap between candles 1 and 3.
2. Filled gaps are dead; only unfilled ones count.
3. Its main job is to qualify order blocks and POIs.
4. Use the imbalance as the entry zone only when all blocks beyond it are mitigated.
5. Confirm on the LTF before entering from an imbalance (interpretation — not stated in SE).

## Connects To
- **[se-ch04](se-ch04-order-flow-order-block.md)**: OB validity requires liquidity sweep + imbalance.
- **[se-ch07](se-ch07-poi-identification.md)**: imbalances help rank POIs.
- **[fm-ch04](fm-ch04-order-blocks.md)**: Miller's identical 3-candle imbalance definition and its role as OB criterion #2.
- **[fm-ch03](fm-ch03-liquidity-premium-discount.md)**: Miller's "gap acts as a magnet" under a demand zone.
- ⚖️ Other book: Miller treats imbalance, inefficiency and FVG as one concept and never proposes trading the imbalance alone; this e-book allows it when all OBs below are mitigated.
