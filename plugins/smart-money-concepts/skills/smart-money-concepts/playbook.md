# Playbook — using this knowledge to do tasks

Pick the recipe that matches the request. Each lists what to read and the procedure. Always name the book (FM/SE) behind each rule you apply, and state that the output is educational, not financial advice.

## 1. Answer a question about the books
1. Topic Index in SKILL.md → read the 1–3 chapter files named there.
2. If FM and SE differ, read [book-comparison.md](book-comparison.md) and give both.
3. Cite as `(FM ch4)` / `(SE s9)`. For page-level precision, the chapter file header gives PDF pages; the originals are in `ebooks/`.

## 2. Analyse a chart (screenshot or OHLC data)
Read: cheatsheet.md, fm-ch02, fm-ch05, fm-ch06, se-ch09.
1. Identify the two timeframes (ask if unknown; default H1+M5 or M15+M1).
2. HTF: mark valid pullbacks → IDM-confirmed major highs/lows → BOS/CHoCH (body closes only) → current trend.
3. Mark liquidity: EQH/EQL, trendlines, range edges, session highs/lows, PDH/PDL; note which are already swept.
4. Draw the current impulse A→B, 50% equilibrium; list POIs/OBs, flag mitigated ones, pick per OB Rules 1–3 / decisional-extreme.
5. State the scenario: "wait for price to sweep X, tap POI Y, then LTF CHoCH + OB" — not "buy now".
6. Output: bias, key levels table (level, type, swept?/mitigated?), primary + alternative scenario, invalidation level.

## 3. Grade or review a trade idea / journal entry
Read: cheatsheet.md (trade-grade checklist), fm-ch09, se-ch10.
1. Run the 8-point trade-grade checklist; mark each pass/fail with the rule source.
2. Check risk: % risk by account type, SL placement beyond OB/POI, TP at liquidity, R:R.
3. Match mistakes to FM ch9's list (1–8).
4. Output: grade (A = all pass, B = one non-critical miss, C/no-trade = any critical miss), fixes.

## 4. Write code (indicator, screener, backtester, Pine Script, Python)
Read: algorithmic-definitions.md first, then the chapters behind each rule you implement.
1. Implement definitions in dependency order: swing points → valid pullback → IDM → major swings → BOS/CHoCH → sweeps → FVG → OB → premium/discount → POI → LTF trigger.
2. Make every discretionary choice a named parameter with the book's default (e.g. `atr_len=14`, `small_ob_ratio=0.6`, `choch_requires_close=True`, `mode="FM"|"SE"`).
3. Evaluate only on closed candles (no repainting); BOS/CHoCH on close.
4. Test with small hand-built candle sequences mirroring the books' valid/invalid examples (fm-ch01, fm-ch02, se-ch02 reference tables) — each example is one test case.
5. Backtests: report per-setup win rate, average R, max drawdown; include costs. The books give no statistics — never claim an edge without results.

## 5. Build a trading plan / checklist / study notes
Read: SKILL.md core, patterns.md, cheatsheet.md, se-ch10.
- Plan skeleton: markets & TFs → daily bias routine (scroll back HTF, sessions, PDH/PDL, news) → allowed setups (from patterns.md) → entry checklist → risk rules → journaling fields (setup, TF, POI type, IDM swept?, CHoCH type, R result, mistake # from FM ch9).
- Study plan: FM ch0→1→2→3→4→5→6→7→8→9 in order (the book is cumulative), with SE s1–s2 beside FM ch1–2, s3–s5 beside ch4, s6 beside ch3/ch5, s7–s9 beside ch6–8, s10 beside ch9.

## 6. Explain / teach a concept
Read the concept's chapter files. Structure: definition (exact book wording) → valid vs invalid example (from the chapter's Reference Tables / Worked Example) → why it works (liquidity logic) → common mistake → which book says what.

## Guardrails
- Don't mark a BOS/CHoCH on a wick or unclosed candle.
- Don't call a zone an OB without the sweep + imbalance check.
- Don't give "enter now" calls; give conditional scenarios with invalidation.
- Keep the skill and anything reproducing the books private.
