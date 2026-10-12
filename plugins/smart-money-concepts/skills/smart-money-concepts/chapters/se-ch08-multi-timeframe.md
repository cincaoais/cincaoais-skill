# Section 8: Multiple Time Interval (Multi-Timeframe Analysis)
> **Source**: *E-book Smart Money SMC* (anonymous, 33 pp., translated), PDF pp. 23–24

*Terminology note: "time interval" = timeframe; "click on the POI" = price taps the POI; "OV" = OB; "busted IDM" = IDM swept.*

## Core Idea
Use **exactly two timeframes** as a day trader: the **HTF** for structure, trend and POIs, the **LTF** for confirmation and entry. Pair choice depends on market and style — **M15 → M1** for Forex/indices, **H1 → M5** for crypto (and also usable for Forex).

## Frameworks Introduced
- **Two-timeframe pairing**:
  - When to use: every trading day, before looking for setups.
  - How: (1) pick the pair for your market: Forex/indices M15/M1; crypto (BTCUSDT) H1/M5; Forex may also use H1/M5; (2) on the HTF mark structure (BOS/IDM), session liquidity and POIs; (3) wait for price to reach a POI; (4) switch to the LTF and wait for a CHoCH (or other entry model); (5) enter after IDM/SMT on the LTF is removed.
- **HTF-to-LTF hand-off**:
  - How: (1) HTF POI tapped; (2) LTF: first structure broken after the tap = CHoCH; (3) LTF: locate the OB (often a one-candle OB after a liquidity exit); (4) enter after the LTF IDM is swept; (5) stop below the LTF major low "because everything below it is mitigated".

## Key Concepts
- **HTF**: timeframe for trend, structure, POI (M15 or H1 in the examples).
- **LTF**: timeframe for confirmation/entry (M1 or M5).
- **Timeframe ratio**: roughly 15:1 (M15/M1) or 12:1 (H1/M5) (interpretation — not stated in SE; derived from the pairs).
- **Extreme OB/POI on HTF**: the target zone where the LTF is consulted.
- **Flip entry**: an alternative LTF entry at the same POIs (see Section 9).
- **LTF major low**: the stop anchor after entry.

## Mental Models
- HTF = **map**, LTF = **trigger**.
- Two timeframes, no more: extra charts add noise, not edge.
- A setup is only as good as its HTF location; LTF only times it.

## Anti-patterns
- **Using LTF structure alone** to pick trades.
- **Entering at the HTF POI without an LTF CHoCH/IDM sweep.**
- **Mixing pairs** (e.g. crypto on M15/M1 when your plan is H1/M5) mid-trade (interpretation — not stated in SE).

## Reference Tables
| Market / style | HTF | LTF |
|---|---|---|
| Forex / Indices (day trading) | M15 | M1 |
| Crypto (BTCUSDT, day trading) | H1 | M5 |
| Forex (alternative) | H1 | M5 |
| Stocks, synthetics, others | Choose by style | Keep 2 TFs |

## Worked Example
**Forex, M15 → M1 (p. 23)**: On M15, price makes a low (BOS), rallies, and the recent high is lifted, then a lower low confirms the bearish leg. Two supply POIs above are marked "where we can sell after confirmation on LTF M1"; a Flip entry is noted as also applicable. On M1, price climbs into the **extreme OB after the IDM is extracted**; the first entry is a one-candle entry (candle takes the previous candle's high). When price later taps the next POI, the trader waits for an M1 CHoCH and sells after IDM/SMT removal.
**Crypto, BTCUSDT H1 → M5 (p. 24)**: On H1, price sweeps below the lows into the **extreme POI** ("already withdrawn from liquidity"). On M5, the first broken structure after the tap is the CHoCH; the trader buys at a one-candle OB after the liquidity exit, adds after the IDM is busted, and places the stop below the M5 major low. Price then rallies strongly.

## Key Takeaways
1. Use two timeframes only.
2. M15/M1 for Forex/indices, H1/M5 for crypto (or Forex).
3. HTF: structure + POI; LTF: CHoCH + IDM + entry.
4. Stop goes below the LTF major low once everything below is mitigated.

## Connects To
- **[se-ch07](se-ch07-poi-identification.md)**: what to mark on the HTF.
- **[se-ch09](se-ch09-entry-models.md)**: LTF entry models.
- **[fm-ch06](fm-ch06-poi-advanced-choch.md)**, **[fm-ch07](fm-ch07-complete-toolkit.md)**: Miller's HTF POI → LTF Advanced CHoCH workflow (M15→M3, H1→M5).
- **[fm-ch09](fm-ch09-pitfalls.md)**: Miller's pitfalls #5–6 (overlooking HTF; too many TFs).
- ⚖️ Other book: Miller also caps at two TFs but uses pairs like H1/M5, H4/M15, M15/M3, M30/M5; this e-book's default Forex pair is M15/M1.
