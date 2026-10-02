# Web-search playbook

Your training data stops at your knowledge cutoff, so everything about *today's* market comes from
here. Fill each template's `{placeholders}` from `system-map.md`, and put `{year}`/`{month}` from
today's date into every query.

## Tools

- **Search:** use the session's web-search tool (WebSearch, or firecrawl search if that's what is
  available).
- **Fetch with CloakBrowser** (stealth Chromium) in two cases:
  - the site is known to block bots: Reddit, ForexFactory, Medium, SSRN, Investing.com, prop-firm
    sites;
  - a normal fetch returns 403, a captcha, a bot check, or an empty page.

  Run it from Bash:
  ```bash
  python -c "from cloakbrowser import launch; b=launch(headless=True); p=b.new_page(); p.goto('URL', timeout=60000); print(p.inner_text('body')[:20000]); b.close()"
  ```
  If the import fails, tell the user to `pip install cloakbrowser`; it downloads its own binary.
  Don't install packages yourself.
- **Never** use the Claude-in-Chrome extension for this research.

## Recency rules

| Kind of claim | Counts as current if published within | Older |
|---|---|---|
| Market regime, prices, volatility, flows | 6 months | background only |
| Prop-firm rules, venue or contract specs, margins | the official page as retrieved today | third-party sources older than 6 months are stale |
| Strategy-class health, practitioner reports | 12 months | background only |
| Techniques (academic) | 3–5 years, if replicated | flag single unreplicated papers |
| Red-flag reports (outages, payout denials, bugs) | 3 months | ignore |

## Source tiers

- **primary:** an exchange or regulator notice, an official prop-firm or broker page, a central
  bank, the World Gold Council or LBMA, an exchange data page, or the paper itself. Primary
  overrides everything else.
- **secondary:** Reuters, Bloomberg, a reputable financial press article, or a paper summary.
- **anecdotal:** Reddit, forums, Trustpilot, Discord, YouTube, vendor blogs. Use only for sentiment,
  and never let it settle a verdict alone.

## Output discipline

Every claim in `market-research.md` and `techniques-research.md` follows this shape:

```
- CLAIM: ... | DATE: published YYYY-MM-DD, retrieved YYYY-MM-DD | SOURCE: title + URL | TIER: primary/secondary/anecdotal | VERIFIED (opened the page) / UNVERIFIED (snippet only, or why)
```

Two more rules:

- When only snippets exist, say so.
- Never call a system "outdated" from web results alone. Pair the claim with `recency` and
  `breakdown.by_regime` from `metrics.json`.

## A — Market regime now (W3)

- `{instrument} volatility regime {month} {year}`
- `{instrument} realized volatility ATR {year} record`
- `{instrument} all-time high drawdown correction {month} {year}`
- `{instrument} drivers {month} {year}`. For gold: real yields, DXY, central-bank buying
  (World Gold Council). For crypto: spot ETF flows, funding, open interest.
- `{instrument} session liquidity spreads {year}`

Answer this: is the current regime (volatility level, trend vs range, drivers) the same as the
backtest period's profitable regimes?

## B — Strategy-class health (W3)

- `{strategy_class} strategy edge decay {year}`
- `{strategy_class} {instrument} stopped working {year} reddit algotrading`
- `{strategy_class} {instrument} backtest vs live degradation`
- `{strategy_class} crowding alpha decay site:ssrn.com OR site:arxiv.org`
- For breakout or trend: `trend following CTA performance {year}`. For mean reversion:
  `mean reversion {instrument} regime failure {year}`.

## C — Venue and rule changes (W3)

- `{prop_firm} rules change {year}`, then confirm on `site:{prop_firm_domain}` (FAQ / terms)
- `{prop_firm} expert advisor EA policy news trading rule {year}`
- `{exchange} {contract} margin change {month} {year}` and `CME advisory {product} specifications {year}`
- `{broker} {instrument} spread swap leverage change {year}`
- `MT5 OR {platform} build update {year} breaking change`

## D — New techniques (W4)

Always pair a technique query with a critique query.

- `{technique} trading out-of-sample evidence {year}`. Techniques to try: volatility-targeted
  sizing, regime filter, meta-labeling, news/event filter, walk-forward re-optimisation, portfolio of
  uncorrelated strategies.
- `site:arxiv.org {technique} {asset_class} backtest {year}`
- `{technique} {instrument} critique OR replication failure OR "not a silver bullet"`
- If the system has an AI/LLM component: `LLM trading filter look-ahead bias {year}` and
  `LLM trade veto forward test results`.

## E — Red flags (W3)

- `{platform} outage OR bug {month} {year}` (MT5, Tradovate, Rithmic, the broker's API)
- `{prop_firm} payout denied OR account breach complaints {month} {year}`
- `{instrument} flash crash OR gap {month} {year}`. This checks the stop and slippage assumptions.
