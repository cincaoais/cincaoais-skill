# Chapter 9: Pitfalls of Profit
> **Source**: *Smart Money Concepts: Unlocking the Path to High Probability Trading* — Frank Miller (2024), Ch 9, PDF pp. 105–111

## Core Idea
SMC is "a double-edged sword": following the steps mechanically without mastering structure, timeframes, OB selection and asset choice produces losses. Miller lists **eight common mistakes** and closes with a mandatory path of **backtest → demo → live**.

## Frameworks Introduced
- **The 8 Pitfalls** (use as a pre-trade and post-trade checklist):
  1. **Incorrect Market Structure Identification** — relying on OBs alone; structure is the core element.
  2. **Ignoring Past Price Movements** — each day, define your timeframes (Miller: H1 and M5) and scroll back to find key highs/lows; a short-term uptrend may sit inside a larger downtrend.
  3. **Not Taking the Impact of News into Consideration** — e.g. economic data or rate changes can move gold sharply; track fundamentals.
  4. **Misinterpreting BOS and CHoCH** — marking them before the candle closes, or on wicks.
  5. **Overlooking Higher Time Frames** — HTF (H1/H4) defines structure, POIs and inducement; LTF (M5/M1) only finds reversal points at HTF levels. Miller notes that special LTF-only methods exist, but they need a different set of conditions and are not in this book — you can't just mark BOS and OBs on M5 and expect them to hold.
  6. **Using Too Many Time Frames** — pick exactly **two** (e.g. H1 + M5) and ignore the rest.
  7. **Choosing the Wrong Order Block** — the "last opposite candle" definition is incomplete; use structure, liquidity and inducement. A wrong OB means a wrong entry *and* a wrong stop, so you get stopped out more; Miller ranks OB selection among the most important SMC skills.
  8. **Choosing Low Liquidity Cryptocurrencies/ Currency Pairs/ Assets to Trade** — low-liquidity coins are manipulated by whales (long wicks, poor waves); news-driven pairs sweep stops erratically.
- **Validation path**:
  - When to use: before risking real money on any SMC variant.
  - How: 1) backtest chosen timeframes/assets — did setups hit SL or TP as planned? 2) demo trade in real time; 3) only then go live, small size.

## Key Concepts
- **Market structure primacy**: structure > isolated OBs.
- **Historical context**: scrolling left to see the bigger trend and key levels.
- **Two-timeframe rule**: one HTF for structure/POI/IDM, one LTF for entries.
- **Candle-close confirmation**: wicks never confirm BOS/CHoCH.
- **Asset liquidity**: prefer "top coins" and major pairs (EUR/USD "EU", GBP/USD "GU"); avoid JPY pairs (news-driven). Note that Miller himself trades a GBP/JPY H1 long in Ch 8, so treat the JPY warning as a preference, not an absolute rule.
- **Backtesting / demo trading**: required before live.
- **Diligence**: studying and practicing, not staring at charts all day.

## Mental Models
- Think "structure first, zones second, entries third".
- Use the HTF as the map and the LTF as the magnifying glass — never navigate by the magnifier alone.
- Think of extra timeframes as noise that costs winning trades more than it saves losing ones.
- Treat asset choice as part of the edge: clean liquidity produces clean structure.

## Anti-patterns
- **OB-only trading**: expecting any touched OB to bounce.
- **Zoomed-in bias**: reading a local uptrend without seeing the larger downtrend into a POI.
- **Trading through news** without awareness.
- **Pre-close structure marking**: fake-outs stop you out.
- **LTF-only SMC**: identifying BOS/POIs on M5 without HTF context violates core principles.
- **Timeframe hopping**: conflicting signals, missed winners.
- **Illiquid/whale-driven or news-heavy instruments**: erratic wicks break analysis.
- **Going live before backtest and demo.**

## Reference Tables

| # | Pitfall | Fix |
|---|---|---|
| 1 | Wrong structure | Label BOS/CHoCH first; OBs only in context |
| 2 | No historical context | Scroll back daily; mark key highs/lows on chosen TFs |
| 3 | Ignoring news | Check calendar and fundamentals for your asset |
| 4 | Early BOS/CHoCH | Wait for candle body close beyond the level |
| 5 | No HTF | HTF (H1/H4) for structure, POI, IDM; LTF (M5/M1) for entries |
| 6 | Too many TFs | Max two (e.g. H1 + M5) |
| 7 | Wrong OB | Apply sweep + imbalance + structure + inducement |
| 8 | Illiquid / news-heavy assets | Top coins; EU, GU; avoid JPY pairs |

| Stage | Question to answer |
|---|---|
| Backtest | Did setups hit SL/TP as calculated on chosen TFs/assets? |
| Demo | Does the plan work in real time? |
| Live | Small positions, same rules |

## Worked Example
Miller's zoom-out scenario (pitfall #2): looking only at a short-term uptrend, a trader reads the market as bullish and goes long. Pulling the chart further back reveals a longer-term downtrend; when price meets resistance or a POI it drops sharply and the long is stopped out. *Skill illustration, not in the book:* the HTF-consistent alternative would be to wait at that POI for a bearish LTF Advanced CHoCH (Ch 6–7) and look for a short instead.

Wick example (pitfall #4): while watching a POI or OB, you see price wick to a previous high or low and think a BOS has formed. Until a candle closes beyond that level, the BOS is not confirmed; entering before the close exposes you to fakeouts where price reverses and triggers your stop. The fix is patience: wait for the close.

## Key Takeaways
1. Market structure is the core; OBs are secondary.
2. Scroll back and use an HTF to set bias before any LTF work.
3. Confirm BOS/CHoCH only on candle closes.
4. Use exactly two timeframes (e.g. H1 + M5).
5. Select OBs with sweep, imbalance, structure and inducement — not "last opposite candle".
6. Trade liquid instruments (top coins, EU/GU), avoid JPY and low-liquidity coins, watch news.
7. Backtest, then demo, then go live small.
8. No strategy wins 100% — the market runs on probabilities; sticking to your principles, managing capital and staying patient is what produces results over time.
9. Patience and discipline are the long-term success factors; diligence means studying and practising your method, not staring at charts all day.

## Connects To
- **[fm-ch00](fm-ch00-introduction-and-conclusion.md)**: the mindset, patience and practice path the book closes on.
- **[fm-ch02](fm-ch02-bos-choch.md)**: close-confirmation rule behind pitfall #4.
- **[fm-ch04](fm-ch04-order-blocks.md)**: correct OB identification behind pitfall #7.
- **[fm-ch06](fm-ch06-poi-advanced-choch.md)**, **[fm-ch07](fm-ch07-complete-toolkit.md)**: HTF POI + LTF Advanced CHoCH workflow behind pitfalls #5–6.
- **[se-ch08](se-ch08-multi-timeframe.md)**: e-book also says a day trader uses exactly 2 timeframes (M15/M1 for forex/indices, H1/M5 for crypto).
- **[se-ch10](se-ch10-trade-examples-risk-management.md)**: e-book risk rules (1–2% own account, 0.25–1% funded) and trade-without-emotion guidance.
- ⚖️ Other book: agrees on two timeframes and patience; the e-book adds explicit risk-per-trade percentages, which Miller does not specify.
