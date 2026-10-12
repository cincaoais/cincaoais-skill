---
name: smart-money-concepts
description: "Knowledge base from two Smart Money Concepts (SMC) trading ebooks: \"Smart Money Concepts: Unlocking the Path to High Probability Trading\" by Frank Miller (2024) and the anonymous \"E-book Smart Money SMC\". Use when analysing charts or trade ideas with SMC, marking market structure (BOS, CHoCH, inducement/IDM), liquidity sweeps, order blocks, FVG/imbalance, POI, premium/discount, session liquidity, entry models, risk management, or when writing indicators, screeners, backtests or trading journals that implement SMC rules, or when answering questions about either book."
---

<!-- argument-hint: [topic, rule name, chapter id like fm-ch04 / se-ch09, or a task] -->

# Smart Money Concepts — two-book knowledge base
**Book FM**: *Smart Money Concepts: Unlocking the Path to High Probability Trading* — Frank Miller, 2024 · 114 pp · 9 chapters · cumulative (each chapter builds on the previous) · stated outcomes: Market Structure Mastery · Liquidity Zones & POI · Order Blocks & Premium/Discount · Trading Strategies · for forex, crypto, stocks, commodities
**Book SE**: *E-book Smart Money SMC* — anonymous, machine-translated from Russian (Russian captions survive on p. 8), 33 pp · 10 sections, chart-heavy
**Generated**: 2026-09-29 with the book-to-skill method (virgiliojr94/book-to-skill spec, applied by hand)

## How to Use This Skill

- **No argument** → use the Core Frameworks below; they answer most questions.
- **Topic** (`order block`, `inducement`, `session liquidity`) → look it up in the Topic Index, read that chapter file, then answer.
- **Chapter id** (`fm-ch04`, `se-ch09`) → read `chapters/<id>-*.md`.
- **A task** (analyse a chart, grade a setup, code a BOS detector, write a trading plan) → read [playbook.md](playbook.md) first; it maps task types to the files and procedure to follow.
- **Rule precision / code** → [algorithmic-definitions.md](algorithmic-definitions.md) turns the books' rules into testable definitions.
- **Books disagree?** → [book-comparison.md](book-comparison.md). Always say which book a rule comes from when they differ.

Read the relevant chapter file before answering anything not covered below. Never invent rules the books don't state; label your own extrapolations as such.

---

## Core Frameworks & Mental Models

**The thesis (both books).** Price is driven by institutions ("smart money") that need liquidity — the stop-losses and pending orders of retail traders — to fill large positions. So price sweeps obvious highs/lows (equal highs/lows, trendlines, range edges, session highs/lows, previous-candle/day highs/lows) *before* making its real move. SMC = **structure + liquidity**: read the trend from confirmed structure, wait for liquidity to be taken, and enter from the zone where institutions left unfilled orders.

**1. Valid pullback / corrective wave (FM ch1, SE s1).** A pullback only exists when a candle breaks the previous candle's extreme: in an uptrend, the low of the highest candle must be taken (by body or wick); in a downtrend, the high of the lowest candle. Inside bars (candles within the range of the extreme candle) are **not** a pullback — the whole move counts as one impulse. Colour of the candle doesn't matter (SE s1).

**2. BOS vs CHoCH (FM ch2, SE s2).** BOS = trend *continuation*: body **close** beyond the last major high (uptrend) / low (downtrend). A wick through a major high/low without a close beyond it is a **liquidity sweep**, not a BOS (FM also counts a close through a *pullback* high/low as a sweep — the wick-vs-close test only decides BOS/CHoCH); after such a sweep, the confirming close must also clear the sweeping candle's own high/low (SE s2). CHoCH = first structural break *against* the trend: close beyond the low (uptrend) / high (downtrend) that produced the most recent BOS. FM: a valid BOS also needs a liquidity sweep of the prior pullback first. Treat CHoCH as a warning; a CHoCH followed by a BOS in the new direction confirms reversal. SE context rule: breaking the nearest low is only IDM unless price has tapped an HTF POI/OB — after the tap, that same break is the LTF CHoCH; without a POI, CHoCH needs the main low to break.

**3. Inducement (IDM) confirms highs and lows (FM ch5, SE s2/s6).** A new high is only a confirmed *major* high after price takes out the most recent internal pullback low beneath it (the IDM). Without IDM there is no valid major high/low, therefore no valid BOS and no valid order block. Which zone is the IDM: **FM** = the last internal pullback (X) formed *before* the BOS candle, and it only counts as confirmed once price then closes beyond the major high/low (valid BOS); **SE** = the first pullback / first OB *after* the BOS — a trap ("SMT", smart money trap). Either way: expect price to sweep it, then trade the next zone beyond it. If a new high prints before the IDM is taken, the IDM moves up to the newest pullback; a BOS with no IDM before it is invalid. ("SMT" in SE = smart money trap, not SMT divergence.)

**4. Liquidity pools to target (FM ch3, SE s6).** Structural highs/lows · equal highs/lows (double/triple tops-bottoms) · trendline liquidity · range (sideways) edges · session highs/lows (Asia/London/NY) · previous candle/day highs/lows (PDH/PDL). A zone is only tradeable if liquidity has been swept on the way to it; an untested zone with no sweep in front of it is itself liquidity.

**5. Imbalance / FVG (FM ch4, SE s3).** Three-candle gap: candle 1's high does not overlap candle 3's low (bullish), or candle 1's low vs candle 3's high (bearish). Overlapping wicks = no imbalance. Price tends to return to fill it. Imbalance marks where institutions pushed price and qualifies order blocks.

**6. Order block — valid only with (FM ch4):** (1) the last candle that **sweeps the previous candle's liquidity** before the strong move, (2) followed by an **imbalance**, (3) followed by a **structure shift (BOS/CHoCH)**. SE agrees on (1)+(2). "Last opposite candle before the move" alone is insufficient — often a trap.
- Several OBs in one leg: uptrend → use the **lower** one, downtrend → the **higher** one (the nearer one is liquidity). Exception (downtrend example in FM): if the lower OB's candle already tapped the upper OB, the upper is triggered → use the lower. Never use a triggered/mitigated OB (FM Rules 1–3); don't apply the rules mechanically.
- Prefer OBs in **discount** for longs, **premium** for shorts.
- SE: price reacts to the **decisional OB** (first block before/after IDM) or the **extreme OB** (origin of the impulse); all other blocks are traps. If the decisional fails, price goes to the extreme.
- Small OB (< 60% of ATR(14)) → widen it symmetrically until the **whole zone = 1 ATR** (FM: ATR 30 pips, OB < 18 pips → 30-pip zone), or use a larger stop. Oversized OB → refine on LTF.

**7. Premium / Discount (FM ch3).** Fib the last impulse A→B; 50% = equilibrium. Buy only in discount (below 50%) in uptrends, sell only in premium in downtrends: safer entry, better R:R (first target = B), safer stop (beyond A).

**8. POI and the top-down entry (FM ch6–7, SE s7–s9).** POI = HTF zone that required only a **liquidity sweep** (an OB also needs imbalance + structure shift). Price reaching a POI is *not* an entry: drop to the LTF, wait for a **CHoCH** ("Advanced CHoCH" in FM), then enter at the LTF OB created by that move, after its own IDM is swept.
- FM 5-step setup: structure (BOS/CHoCH) → POI → wait for price to reach POI → LTF advanced CHoCH + OB → limit order at OB edge, SL beyond OB, TP 2R/3R/5R or next major high/low. Hidden step: liquidity/inducement must be swept first.
- SE entry modules: (1) CHoCH with IDM, (2) FLiP with IDM (failed demand becomes supply D2S / failed supply becomes demand S2D), (3) CHoCH without IDM (when the HTF POI itself swept liquidity), (4) previous-candle liquidity entry (candle takes prior candle's high and closes bearish / takes its low and closes bullish → enter next open; add positions until the LTF major low/high breaks), (5) single-candle / liquidity-sweep entry (same next-open execution), (6) BOS (continuation) entry — after an LTF BOS, wait for its IDM sweep, enter at the OB or a one-candle absorption OB. "No IDM, no entry" except module 3.
- FM mindset: trade fewer setups — wait for price to come to your zone and act only when the odds favour you.

**9. Candle Breakout Strategy (FM ch8).** At a POI/OB: *reaction candle* touches the zone, *confirmation candle* engulfs its body. Single-TF: limit at reaction candle's high (long) / low (short), SL beyond reaction candle or POI. Two-TF: find an LTF OB inside the reaction candle; if the confirmation candle swept the reaction candle's liquidity no further IDM is needed, otherwise wait for LTF IDM.

**10. Timeframes (both).** Exactly two: HTF for structure/POI/IDM, LTF for the entry trigger. FM uses H1+M5 (also M15→M3, H1→M5, H4→M15, M30→M5). SE: Forex/indices M15→M1; crypto/Forex H1→M5. Never trade LTF structure without HTF context; never use more than two TFs.

**11. Time & session liquidity (SE s6).** Every session high/low is liquidity; at least one session per day manipulates. If Asia and London trend the same way, New York tends to reverse (manipulates London); if London swept Asia's high/low, NY tends to continue London's direction. Daily: in a bullish day, buy after the previous candle's low is swept (switch to M15 for structure break); mirror for bearish.

**12. Risk (SE s10, FM ch7–9).** Own account 1–2% per trade; funded/prop 0.25–1%. Break-even: FM moves SL to entry after a new LTF BOS in favour; SE moves it only after the recent structure breaks **and** no IDM/unmitigated block remains near the recent high/low (otherwise price will come back for it). SE: take partial profit when the BE point is far from entry and at the recent major low/high, leaving the rest at BE. Realistic R:R 1:5–1:10 (SE); FM's examples 3.5R–11R, TP at nearest major high/low or liquidity; FM trails SL under successive higher lows. Backtest → demo → small live (FM).

**13. Pitfalls (FM ch9).** Trading OBs without structure · ignoring history/HTF · ignoring news · marking BOS/CHoCH on wicks or before the close · LTF-only analysis · too many timeframes · wrong OB · illiquid assets (avoid low-cap coins, JPY pairs; prefer majors like EURUSD/GBPUSD, top coins). FM's key takeaway: success needs a disciplined mindset, not just patterns — "patience, practice, and persistence are the foundation of consistent profitability"; no strategy wins 100%.

---

## Chapter Index

| # | Title | Key Frameworks |
|---|-------|----------------|
| [fm-ch00](chapters/fm-ch00-introduction-and-conclusion.md) | Introduction & Conclusion | four outcomes, mindset, personal method, backtest→demo→live |
| [fm-ch01](chapters/fm-ch01-impulsive-corrective-waves.md) | Impulsive and Corrective Waves | valid pullback rule, inside bar, impulse criteria |
| [fm-ch02](chapters/fm-ch02-bos-choch.md) | BOS and CHoCH | sweep + close = BOS, CHoCH, CHoCH→BOS confirmation |
| [fm-ch03](chapters/fm-ch03-liquidity-premium-discount.md) | Liquidity and Premium/Discount Zones | 4 liquidity models, equal highs/lows, 50% equilibrium |
| [fm-ch04](chapters/fm-ch04-order-blocks.md) | Powerful Order Blocks | imbalance, 3 OB criteria, OB Rules 1–3, ATR 60% rule, continuation vs reversal OB |
| [fm-ch05](chapters/fm-ch05-inducement.md) | Inducement – The Untold Secrets | impulse/correction/continuation, candlestick IDM, IDM validates BOS & OB |
| [fm-ch06](chapters/fm-ch06-poi-advanced-choch.md) | The Last Weapons: POI & Advanced CHoCH | POI vs OB, POI types 1–4, LTF advanced CHoCH |
| [fm-ch07](chapters/fm-ch07-complete-toolkit.md) | SMC Complete Toolkit | 5-step setup, 11R and 4.5R examples |
| [fm-ch08](chapters/fm-ch08-candle-breakout-strategy.md) | Breakout Strategy with SMC | Candle Breakout Strategy (reaction/confirmation candle), 1-TF vs 2-TF |
| [fm-ch09](chapters/fm-ch09-pitfalls.md) | Pitfalls of Profit | 8 common mistakes, backtest→demo |
| [se-ch01](chapters/se-ch01-pulse-and-correction.md) | Pulse and Correction | impulse vs correction, correction rule |
| [se-ch02](chapters/se-ch02-bos-choch-structure.md) | BOS/CHoCH Structure Display | IDM-confirmed highs/lows, body-close BOS, internal structure |
| [se-ch03](chapters/se-ch03-imbalance-fvg.md) | Imbalance / FVG | filled vs unfilled gap, imbalance as entry when blocks mitigated |
| [se-ch04](chapters/se-ch04-order-flow-order-block.md) | Order Flow & Order Block | order flow, decisional vs extreme OB, liquidity+imbalance |
| [se-ch05](chapters/se-ch05-ifc-candle.md) | IFC Candle | institutional funding candle, sweep + LTF confirmation |
| [se-ch06](chapters/se-ch06-liquidity-types.md) | Liquidity Types | retail/trendline/SnR, SMT/IDM, session & daily liquidity |
| [se-ch07](chapters/se-ch07-poi-identification.md) | POI Identification | 9 POI cases on AUDUSD M15 |
| [se-ch08](chapters/se-ch08-multi-timeframe.md) | Multiple Time Interval | M15→M1, H1→M5 pairings |
| [se-ch09](chapters/se-ch09-entry-models.md) | Entry Types | 6 entry modules (incl. BOS entry), FLiP D2S/S2D, previous-candle entries |
| [se-ch10](chapters/se-ch10-trade-examples-risk-management.md) | Trade Examples & Risk Management | worked trades, 1–2% / 0.25–1% risk, BE rules |

## Topic Index

- **ATR 60% rule** → fm-ch04
- **Advanced CHoCH** → fm-ch06, fm-ch07
- **BOS (break of structure)** → fm-ch02, se-ch02, fm-ch05
- **Candle Breakout Strategy (CBS), reaction / confirmation candle** → fm-ch08
- **CHoCH (change of character)** → fm-ch02, se-ch02, se-ch09
- **BOS (continuation) entry** → se-ch09
- **CHoCH with / without IDM** → se-ch09
- **Continuation vs reversal OB** → fm-ch04
- **Corrective wave / pullback validity** → fm-ch01, se-ch01
- **Daily candle liquidity, PDH/PDL** → se-ch06
- **Decisional vs extreme order block** → se-ch04, se-ch06
- **Equal highs / equal lows (EQH/EQL)** → fm-ch03, se-ch06
- **FLiP, D2S / S2D** → se-ch09
- **FVG / imbalance** → fm-ch04, se-ch03
- **IFC (institutional funding candle)** → se-ch05
- **Impulsive wave** → fm-ch01, se-ch01, fm-ch05
- **Inducement (IDM)** → fm-ch05, se-ch02, se-ch06, se-ch09
- **Internal vs major structure** → fm-ch05, se-ch02
- **Liquidity sweep** → fm-ch02, fm-ch03, se-ch06
- **Mindset, discipline, learning outcomes** → fm-ch00, fm-ch09
- **Mistakes / pitfalls** → fm-ch09
- **Multi-timeframe pairing** → se-ch08, fm-ch09, fm-ch06
- **News & asset selection** → fm-ch09
- **Order block (OB)** → fm-ch04, se-ch04
- **Order flow (OF)** → se-ch04
- **POI (point of interest), POI types** → fm-ch06, se-ch07
- **Premium / discount, equilibrium** → fm-ch03, fm-ch04
- **Previous-candle liquidity / single-candle entry** → se-ch09
- **Retail patterns as liquidity (trendline, SnR, ranges)** → fm-ch03, se-ch06
- **Risk management, SL/BE/TP** → se-ch10, fm-ch07, fm-ch08
- **Session liquidity (Asia/London/NY)** → se-ch06
- **SMT (smart money trap)** → se-ch06
- **Trade walk-throughs** → fm-ch07, fm-ch08, se-ch08, se-ch10

## Supporting Files

- [playbook.md](playbook.md) — how to carry out tasks with this knowledge (chart analysis, setup grading, coding, journaling)
- [algorithmic-definitions.md](algorithmic-definitions.md) — rules as precise, codeable definitions
- [cheatsheet.md](cheatsheet.md) — decision rules, checklists, thresholds
- [patterns.md](patterns.md) — every setup and technique: when / how / trade-offs
- [glossary.md](glossary.md) — every term and abbreviation, plus SE translation key
- [book-comparison.md](book-comparison.md) — where the two books agree and differ

---

## Scope & Limits

Covers the two books only. Miller stresses his SMC variant is personal, differs from other SMC teachings and should be adapted to your own personality and style; they are discretionary price-action methods with no statistical evidence of edge offered — treat all rules as hypotheses to backtest, never as financial advice. SE's text layer is badly translated and most of its meaning lives in chart annotations; its chapter files were written from the rendered pages. SE pp. 32–33 contain captions only (no chart images) and p. 30's caption boxes are empty, so its trade-example and risk sections rest on captions alone. FM's ~78 figures and SE's ~31 chart images were reviewed selectively, not exhaustively. Derived from copyrighted books for personal study: keep this skill private.
