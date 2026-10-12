# SMC Cheatsheet — decide like the authors

## Decision rules
- **Candle wicked through a high/low but closed back** → liquidity sweep, not BOS/CHoCH. Wait for a body close (FM ch2, ch9; SE s2).
- **New high made, internal pullback low not yet taken** → high unconfirmed; no BOS, no OB to trade yet. Wait for IDM sweep (FM ch5, SE s2).
- **Price retraces into the IDM zone** (FM: last internal pullback before the BOS; SE: first pullback/OB after the BOS = SMT) → trap. Don't enter; expect it to break and target the zone beyond (FM ch5, SE s6).
- **Zone reached with no liquidity swept on the way** → low quality; treat the zone as liquidity for a deeper one (FM ch3–4).
- **Price at an HTF POI** → not an entry. Drop to LTF, wait for CHoCH, then the LTF OB (FM ch6–7).
- **LTF CHoCH printed but no IDM yet** → wait for IDM, unless the HTF POI itself swept liquidity (SE module 3).
- **Two OBs in one leg** → uptrend lower, downtrend higher; skip mitigated; downtrend exception: lower OB already tapped the upper → lower (FM ch4).
- **OB in premium for a long / discount for a short** → skip (FM ch3–4).
- **Price broke the decisional OB** → expect the extreme OB (SE s4).
- **Trend-line / double-top / range pattern forming** → mark it as liquidity, not a signal (FM ch3, SE s6).
- **Asia + London trended together** → expect NY reversal. London swept Asia → NY continues London (SE s6).
- **Trade moving in favour** → FM: SL to entry after a new LTF BOS. SE: SL to BE after the recent structure breaks **only if** no IDM/unmitigated block remains near the recent high/low; if one does, wait (SE s10).
- **Price in POI and trending** → add on each previous-candle sweep until the LTF major low/high breaks (SE s9).
- **Counter-trend trade** → only if the IDM hasn't been taken yet, or the IDM is broken (SE s7).
- **High-impact news for your asset** → be aware and factor it in; FM gives no stand-aside rule (FM ch9). **Illiquid asset / JPY pair** → avoid (FM ch9).
- **Candle closes with a body beyond a session high/low** → not a sweep trade; only trade it after an LTF CHoCH (SE s6).

## Structure decision tree
- Is there a valid pullback (extreme candle's opposite end taken)?
  - No → still one impulse leg.
  - Yes → has price closed beyond the last *IDM-confirmed* major swing?
    - Same direction as trend → **BOS** (trend continues; mark new IDM).
    - Opposite direction, beyond the swing that made the last BOS → **CHoCH** (alert; wait for BOS in new direction to confirm).
    - Only a wick → **sweep** (liquidity taken; often reversal fuel).

## OB validity checklist (all three = FM valid OB)
| Check | Pass |
|---|---|
| Candle sweeps previous candle's high (bearish OB) / low (bullish OB) | ☐ |
| Imbalance follows (candle 1 and 3 wicks don't overlap) — may appear 1–2 candles later → OB spans the cluster | ☐ |
| BOS or CHoCH follows | ☐ |
| Unmitigated | ☐ |
| In discount (long) / premium (short) | ☐ |
| Liquidity/IDM swept before price reaches it | ☐ |

## Trade-grade checklist
1. HTF trend from confirmed structure (scroll back) 2. POI with prior sweep 3. Correct premium/discount 4. IDM swept 5. LTF CHoCH 6. LTF OB (+ imbalance) 7. SL beyond OB/POI, TP at liquidity, R ≥ 1:3 preferred 8. News checked and factored in (FM ch9); liquid asset, not a JPY pair or low-liquidity coin (FM ch9). **Missing 1, 2, 4 or 5 → no trade.**

## Thresholds & defaults
| Item | Value | Source |
|---|---|---|
| Timeframes | exactly 2 (HTF + LTF) | FM ch9, SE s8 |
| Pairings | H1→M5 · M15→M1 · M15→M3 · H4→M15 · M30→M5 | FM, SE |
| Equilibrium | 50% of impulse A→B | FM ch3 |
| Small OB | < 60% ATR(14) → widen symmetrically to a total zone of 1 ATR | FM ch4 |
| Risk, own account | 1–2% per trade | SE s10 |
| Risk, funded account | 0.25–1% per trade | SE s10 |
| Realistic R:R | 1:5–1:10 (don't chase 1:30–50) | SE s10 |
| Minimum R:R | > 1:1; FM targets 2R/3R/5R | FM ch3, ch7 |
| Probability after IDM sweep at POI without LTF confirmation | ~50% → don't enter | SE s7 |
| Sessions | Asia · London · New York; ≥1 manipulates daily | SE s6 |

## Tells & smells
- Long wicks, erratic structure → illiquid asset; skip (FM ch9).
- BOS marked on an unclosed candle → premature; recheck at close (FM ch9).
- Setup only visible on M5 → missing HTF context (FM ch9).
- "OB" with imbalance but no sweep → smart trap (SE s4, FM ch4).
- "OB" with sweep but no imbalance → not an OB; look at candles below/above (SE s4).
- Inside bars after a big candle → not a pullback (FM ch1).
