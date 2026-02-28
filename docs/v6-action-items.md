# V6 Action Items — All Postponed Additions

*Compiled from design sessions on 2026-02-28*

---

## Priority 1: New Mechanisms

### AI Output = GitHub Commits
- **What:** Every AI decision produces a verifiable GitHub commit
- **Public with 3-month delay:** Protects live strategies while ensuring auditability
- **Design decision needed:** Commits to House Panda repo or dedicated protocol repo? Dedicated protocol repo is stronger for decentralization optics — AI commits to the protocol's public repo, House Panda the company is just one contributor alongside the AI
- **Implications:**
  - Commit history becomes de facto prospectus for institutional evaluators
  - Securities law defense: public code closer to open-source infrastructure than managed investment vehicle
  - NVIDIA angle: inference stack running AI that produces auditable commits resonates with technical institutional audiences

### 5-Layer MM Protection Framework
- **What:** Defense-in-depth against MMs using lending to effectively buy tokens cheaply
- **Layers:** Dynamic collateral with margin calls, restricted token custody, tranche-based lending, economic penalty stack, dynamic pricing mechanism
- **Full framework:** See [mm-protection-framework.md](mm-protection-framework.md)
- **Design decision needed:** Oracle for margin calls — bonding curve price vs exchange market price? If market price, need reliable oracle. If curve price, MM could manipulate by temporarily depositing tokens

### Inference Bank (Already in v5, needs expansion)
- Expand explanation of countercyclical buffer mechanics
- Add drawdown policies and trigger conditions
- Model surplus accumulation scenarios across different utilization rates

---

## Priority 2: Asia-First Strategy

### Restructure MM Obligations for Asian Venue Priority
- **Tier 1 (Hong Kong — Immediate):** Two-sided quotes on HashKey Exchange and OSL, enhanced depth during HKEX reference rate window (15:00-16:00 HKT)
- **Tier 2 (Korea — When market opens):** Listing on Upbit or Bithumb within 90 days of regulatory approval
- **Tier 3 (Japan — Long-dated):** Listing on JFSA-registered exchange within 180 days of ETF framework
- **Tier 4 (US — Parallel):** Two CME CF Constituent Exchanges (Coinbase, Kraken)
- **Full strategy:** See [asian-etf-strategy.md](asian-etf-strategy.md)

### Add Competitive Positioning
- HPT as category-of-one in Asian institutional crypto
- No existing Asian-origin token designed for institutional infrastructure
- **Full analysis:** See [asian-competitive-landscape.md](asian-competitive-landscape.md)

### Add HKEX/CCData vs CF Benchmarks Context
- HKEX launched Virtual Asset Index Series (November 2024), administered by CCData
- No ETF has switched from CF Benchmarks yet, but HKEX signaling intent to own pricing infrastructure
- Hong Kong approved Asia's first spot Solana ETF (October 2025)

---

## Priority 3: Design Variables Under Evaluation

### Market Cap-Adjusted Lending Price
- **Open question:** Inverse vs direct relationship between market cap and lending rate
- **Inverse:** Cheaper to borrow when cap is high — rewards MM success, incentivizes activity when things work
- **Direct:** More expensive when cap is high — protects reserves when tokens are valuable
- **Both have logic.** Needs dedicated modeling session before committing publicly
- Currently flagged as "design variable under evaluation" in v5 materials

### World Models Expansion
- **What:** Research roadmap beyond LLMs to financial world models
- **Staging:** LLMs now → simulation layer Year 1-2 → real-time world model inference Year 2-3
- **Key framing:** Bonding curve as "financial physics" environment for world model research
- **Full roadmap:** See [world-models-roadmap.md](world-models-roadmap.md)
- **Decision needed:** Include in materials as research roadmap section, or keep as conversation point for sophisticated investors?

---

## Priority 4: Legal & Compliance

### Formal Securities Law Opinion
- Get Howey analysis from securities lawyer experienced with tokens that got ETFs
- **Critical items:** Bonding curve immutability as "no efforts of others" defense, AI spending as protocol infrastructure (not profit distribution), utility at launch
- **Full checklist:** See [securities-etf-checklist.md](securities-etf-checklist.md)

### MM Contractual Language
- Finalize legal templates for tiered venue obligations
- Cross-reference with standard prime brokerage margin call provisions
- Include public attribution clause for defaults (ties to GitHub transparency)

---

## Files Created This Session

| File | Type | Location |
|------|------|----------|
| Bonding Curve Explorer | Streamlit app | `app/bonding_curve_app.py` |
| MM Overview v5 | PDF | `assets/house_panda_mm_overview_v5.pdf` |
| This document | Markdown | `docs/v6-action-items.md` |

---

*Last updated: 2026-02-28*
