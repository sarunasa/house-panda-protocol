# 🐼 House Panda Protocol

**AI-Managed Token Lending via Bonding Curve** | NVIDIA Inception — East Asia Cohort

---

## Overview

House Panda Protocol is an AI-managed token lending mechanism where market makers borrow tokens directly from a convex bonding curve rather than purchasing them. The curve simultaneously serves as price discovery, treasury, and liquidity backstop.

**Core Thesis:** The bonding curve is the mechanism. LLMs are the management. NVIDIA is the infrastructure. The bet is that all three improve over time.

**Key Innovation:** MMs borrow, not buy. They're exposed to spread risk, not directional risk. This means MMs will provide liquidity for any token on the platform — because they don't need to believe in it.

## Architecture

```
Convex Elliptical Bonding Curve
    ├── Price: p(s) = P_max × (1 - √(1 - (s/S_max)²))
    ├── MM Borrowing: collateral → borrow → provide liquidity → pay interest
    ├── Fee System: curve-linked dynamic fees + flat operational fees
    └── Reserves: mathematically impossible to drain (dp/ds → ∞ as s → S_max)

5-Step Platform Evolution
    ├── Step 1: Launch own token on own curve (proof of concept)
    ├── Step 2: Open curve to other tokens (launchpad)
    ├── Step 3: Add new curve types (multi-curve platform)
    ├── Step 4: Open all curves to others (curve-as-a-service)
    └── Step 5: Unify liquidity pool (protocol)

AI Infrastructure (Hybrid)
    ├── MiniMax M2.5 agents — routine coding, CI/CD, tests (~$1K/month)
    ├── Claude API — architecture, strategic reasoning (~$600/month)
    ├── DGX Spark — always-on protocol inference (~$333/month amortized)
    └── Output = GitHub commits (verifiable AI artifacts)
```

## Interactive Explorer

Run locally:
```bash
pip install -r app/requirements.txt
streamlit run app/bonding_curve_app.py
```

## Documentation

### Core Design
| Document | Description |
|----------|-------------|
| [**Protocol Design**](docs/protocol-design.md) | Full mechanism design — elliptical curve math, MM borrowing, obligation framework, fee architecture, revenue model, anti-manipulation analysis, Uniswap differentiation, 5-step platform evolution |
| [MM Protection Framework](docs/mm-protection-framework.md) | 5-layer defense against MM lending extraction |
| [Securities & ETF Readiness](docs/securities-etf-checklist.md) | Howey test avoidance and ETF prerequisites |

### Strategy
| Document | Description |
|----------|-------------|
| [Asian ETF Strategy](docs/asian-etf-strategy.md) | Asia-first benchmark infrastructure positioning |
| [Competitive Landscape](docs/asian-competitive-landscape.md) | Asian token projects and HPT positioning |
| [World Models Roadmap](docs/world-models-roadmap.md) | Expansion from LLMs to financial world models |

### AI Infrastructure
| Document | Description |
|----------|-------------|
| [**AI Infrastructure Costs**](docs/ai-infrastructure-costs.md) | MiniMax M2.5 pricing, $200/month per-agent economics, hybrid architecture (M2.5 + Claude + DGX Spark) |
| [DGX Spark Analysis](docs/dgx-spark-analysis.md) | Hardware specs, coding benchmarks, API vs local comparison, competitive landscape |

### Planning
| Document | Description |
|----------|-------------|
| [V6 Action Items](docs/v6-action-items.md) | All pending additions for next documentation iteration |

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
