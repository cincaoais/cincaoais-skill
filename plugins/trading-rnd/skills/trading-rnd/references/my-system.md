# My Auto Trading System — Context

This file is the standing context for every /R&D fit assessment. Keep it updated as the
system evolves — a 5-minute edit here sharpens every future report. Replace the
placeholders below with real values; anything left as a placeholder will be treated as
unknown and flagged as an assumption in reports.

Note: code-level details (languages, libraries, architecture) are deliberately NOT
tracked here — Claude Code discovers those from the real codebase when planning and
implementing. This file only holds the domain facts research needs.

## Broker & execution
- Broker + API: `<e.g., Interactive Brokers via ib_insync / Alpaca REST>`
- Order types used: `<e.g., market, limit, bracket orders>`
- Trading frequency: `<e.g., end-of-day / intraday on 5-min bars / minutes-level, not HFT>`
- Account constraints worth remembering: `<e.g., PDT rule applies, cash account, margin>`

## Data
- Market data sources: `<e.g., Alpaca minute bars, yfinance daily EOD>`
- Granularity available: `<e.g., 1-min bars intraday, daily history back to 2005>`
- Universe: `<e.g., S&P 500 constituents / all US equities / specific watchlist>`
- Data I do NOT currently have: `<e.g., options chains, fundamentals, level-2, news feeds>`

## Validation process
- How I validate a strategy before going live: `<e.g., 5y backtest, then 1 month paper trading>`
- Paper trading available: `<yes/no, via which broker>`

## Current features & strategies
- What the system already does: `<e.g., momentum screener, daily rebalance, Telegram alerts>`
- Strategies currently live: `<list>`
- Strategy rule summaries (optional, but makes /R&D improve runs much sharper):
  `<for each live strategy, 2–3 lines: entry/exit logic, universe, holding period, sizing>`

## Preferences & constraints
- Risk appetite / position sizing rules: `<e.g., max 5% per position, no leverage>`
- Monthly budget for data/tools: `<e.g., prefer free tiers, up to $50/mo acceptable>`
- Things I've already ruled out: `<e.g., HFT, crypto, options selling>`
