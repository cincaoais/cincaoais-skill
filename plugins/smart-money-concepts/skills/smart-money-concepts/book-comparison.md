# Book Comparison — Frank Miller (FM) vs E-book Smart Money SMC (SE)

## At a glance
| | FM | SE |
|---|---|---|
| Length / style | 114 pp, prose-heavy, 9 chapters, each with worked examples | 33 pp, chart-first, captions on candles lettered A, B, H, K, N, U… |
| Language quality | native English | machine translation; needs the [glossary translation key](glossary.md#se-translation-key-original-wording--standard-term) |
| Emphasis | rule-based OB selection, POI types, advanced CHoCH, CBS, mistakes | IDM everywhere, entry modules, session/daily liquidity, IFC, FLiP, risk sizing |
| Unique content | premium/discount via Fib 50%, ATR 60% OB rule, OB Rules 1–3, POI types 1–4, CBS, 8 pitfalls, asset selection, backtest→demo | order flow, decisional vs extreme OB, IFC candle, SMT, session manipulation rule, daily candle liquidity, 6 entry modules, risk % by account type, scaling with previous-candle entries |

## Where they agree
- SMC = structure + liquidity; retail patterns (TL, SnR, EQH/EQL, ranges) are liquidity.
- Valid pullback requires breaking the extreme candle's opposite end; inside bars aren't pullbacks.
- BOS needs a **body close**; a wick is a sweep.
- IDM (inducement) must be swept to confirm a major high/low; it is a trap zone, not an entry.
- OB needs a liquidity sweep of the previous candle **and** an imbalance.
- HTF POI → LTF confirmation (CHoCH) → LTF OB entry; exactly two timeframes.
- Mitigated zones are single-use.

## Where they differ (say which book you're applying)
| Topic | FM | SE |
|---|---|---|
| OB criteria | 3: sweep + imbalance + BOS/CHoCH after | 2: sweep + imbalance (structure implied by context) |
| IDM placement | last internal pullback (X) formed before the BOS; confirmed when price closes beyond the major high/low | first pullback / first OB after the BOS (SMT) |
| Liquidity sweep | wick or close through a pullback/liquidity level | shadow through the level (a close = structure break) |
| BOS extra condition | pullback must sweep liquidity (prior pullback low) before the close beyond the high | high must be IDM-confirmed (first pullback taken) before the break counts |
| CHoCH confirmation | structure CHoCH (ch2): body close, same TF, a warning until a BOS confirms; entry CHoCH ("Advanced CHoCH", ch6–7): on the LTF after a POI sweep/tap, acted on via IDM + OB without waiting for a new BOS | on LTF at entry time, a wick through the nearest high/low counts as CHoCH; also defines CHoCH as the break after price touches/sweeps a POI (without POI, that first break is IDM) |
| Which OB to pick | lower in uptrend / higher in downtrend, except (downtrend) when the lower OB already tapped the upper; never a triggered OB; filter by discount/premium | decisional OB (first before/after IDM) or extreme OB (impulse origin); all others are traps |
| POI definition | HTF zone with a liquidity sweep only; types 1–4 | any zone that swept liquidity: OB, IFC candle, session low, previous-candle sweep candle, engulfing candle |
| Entry trigger | Advanced CHoCH + OB limit; or CBS engulfing | 6 modules: CHoCH±IDM, FLiP, previous-candle, single-candle/sweep, BOS (continuation) |
| Timeframe examples | H1+M5 main; M15→M3; H4→M15; M30→M5 | Forex/indices M15→M1; crypto/Forex H1→M5 |
| Risk | SL beyond OB/POI; TP 2R–5R or next major swing; trail SL; SL to entry after a new LTF BOS | 1–2% own / 0.25–1% funded; BE after recent structure breaks only if no IDM/unmitigated block remains; R:R 1:5–1:10; partials when BE is far |
| Time-of-day | not covered (news awareness only) | session highs/lows, Asia/London/NY manipulation rule, PDH/PDL |
| Assets | forex, crypto, stocks, commodities (Intro); examples use Gold, EURUSD, GBPJPY; ch9 advises liquid majors (EU, GU) and top coins, avoiding JPY pairs and low-liquidity coins (yet ch8 trades GBPJPY) | "any market": Forex, crypto (BTCUSDT), stocks, indices, synthetics |

## How to reconcile when doing a task
- **Strict/conservative mode** (default for grading setups or coding a detector): require FM's 3 OB criteria + SE's IDM confirmation + body-close BOS/CHoCH on the HTF.
- **Execution on the LTF**: SE's wick-CHoCH is allowed only on the LTF after an HTF POI tap.
- **Risk**: use SE's percentages with FM's SL/TP placement.
- Report conflicts explicitly: "FM says X; SE says Y; I applied X because…".
