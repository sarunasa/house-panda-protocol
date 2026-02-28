# 🐼 House Panda Protocol

**AI-Managed Token Lending via Bonding Curve** | NVIDIA Inception — East Asia Cohort

---

## Overview

House Panda Protocol is an AI-managed token lending mechanism where market makers borrow tokens directly from a bonding curve rather than purchasing them. The curve simultaneously determines price, lending rate, and AI development allocation.

**Core Thesis:** The bonding curve is the mechanism. LLMs are the management. NVIDIA is the infrastructure. The bet is that all three improve over time.

## Architecture

```
Bonding Curve (immutable smart contract)
    ├── Price: P = k × S^n
    ├── Lending Rate: f(curve position, market cap)
    ├── AI Allocation: 50% at launch → 15% floor
    └── Default Response: permanent upward curve shift

Inference Bank (countercyclical reserve)
    ├── Surplus accumulates when income > AI spend
    ├── AI draws from reserve when income drops
    └── Development never stops

AI Layer (NVIDIA stack)
    ├── AgentIQ — multi-agent orchestration
    ├── NIM — inference microservices
    ├── NeMo — model lifecycle management
    └── Output = GitHub commits (public, 3-month delay)
```

## Interactive Explorer

Run locally:
```bash
pip install -r app/requirements.txt
streamlit run app/bonding_curve_app.py
```

## Documentation

| Document | Description |
|----------|-------------|
| [V6 Action Items](docs/v6-action-items.md) | All pending additions for next documentation iteration |
| [Asian ETF Strategy](docs/asian-etf-strategy.md) | Asia-first benchmark infrastructure positioning |
| [MM Protection Framework](docs/mm-protection-framework.md) | 5-layer defense against lending extraction |
| [World Models Roadmap](docs/world-models-roadmap.md) | Expansion from LLMs to financial world models |
| [Securities &amp; ETF Readiness](docs/securities-etf-checklist.md) | Howey test avoidance and ETF prerequisites |
| [Competitive Landscape](docs/asian-competitive-landscape.md) | Asian token projects and HPT positioning |

## Venue Strategy (Asia-First)

| Tier | Region | Venues | Status |
|------|--------|--------|--------|
| 1 | Hong Kong | HashKey Exchange, OSL | Immediate |
| 2 | South Korea | Upbit, Bithumb | When ETF framework launches |
| 3 | Japan | bitFlyer, Coincheck, bitbank | ~2028 ETF framework |
| 4 | United States | Coinbase, Kraken | Parallel |

## Status

- **NVIDIA Inception:** Member since 2016 (East Asia cohort, 8x more selective)
- **JETRO:** Japanese government trade investment support
- **AI Credits:** Low 7-figure inference credits secured (AWS + GCP)
- **Community:** 250K+ Telegram airdrop bot users, 2,800 organic Twitter followers
- **Trading System:** PVD v3 backtesting live on Railway

---

*House Panda — NVIDIA Inception East Asia Cohort — 2026*
