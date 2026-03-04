# House Panda Protocol — Technical Stack Briefing

*Use this document as context for a new conversation about implementation architecture.*

---

## What This Project Is

House Panda Protocol is an AI-managed token lending system on a convex bonding curve. Market makers borrow tokens by posting collateral, provide liquidity on exchanges, and pay interest back to the curve treasury. The long-term vision is a curve-as-a-service platform where anyone can launch a token, pick a curve shape, and plug into shared liquidity.

All AI operations produce GitHub commits as verifiable output. The protocol is designed to run semi-autonomously.

**Full documentation:** [github.com/sarunasa/house-panda-protocol](https://github.com/sarunasa/house-panda-protocol)

---

## Current Stack

### Protocol Layer
- **Bonding curve math:** Convex elliptical — `p(s) = P_max × (1 - √(1 - (s/S_max)²))`
- **Implementation status:** Contractual first (not on-chain initially). Curve math is reference, not deployed smart contract.
- **Streamlit/Plotly explorer app:** Live in repo (`app/bonding_curve_app.py`), deployable via Render
- **Margin call oracle:** Contractual TWAP across 3+ independent price sources, 24-hour rolling window

### Trading System (PVD)
- **PVD (Price-Volume-Direction/Dynamics):** Systematic trading system analyzing price and volume signals across crypto and equities
- **Core metric:** True 24-hour rolling volume % change from 1-minute candlestick data
- **Signal structure:** 8 binary ranking strategies combining price/volume direction across custom 1.5-hour "Alora" datetime intervals. One strategy consistently dominates.
- **Data:** Twelve Data Pro API (equities), CoinGecko API (crypto), covering CEX spot, perpetuals (Hyperliquid, Aster, Lighter, EdgeX, Paradex)
- **Storage:** Raw Python + Parquet files (moved away from no-code tools)
- **Infrastructure:** Railway/Render deployment, GitHub as source of truth, Linear as visual planning mirror (one-way sync)
- **Backtesting:** PVD v3 backtests running on Railway, accessible via MCP tool

### AI Development
- **Claude API (Sonnet/Opus):** Primary for architecture, complex reasoning, strategic decisions
- **MiniMax M2.5 API:** Planned for volume coding agents (~$200/month per full-time agent, 80.2% SWE-Bench)
- **Cowork (Claude-based):** Autonomous coding agents handling most code commits
- **Contract developer (Jia):** Implementation work alongside AI agents

### NVIDIA Relationship
- **NVIDIA Inception:** Member since 2016, East Asia cohort (8x more selective than standard)
- **JETRO:** Japanese government trade investment support
- **AI credits:** Low 7-figure inference credits (AWS + GCP)
- **Hardware consideration:** DGX Spark ($3,999) evaluated for always-on protocol inference. 128GB unified memory, 273 GB/s bandwidth. Good for capacity (120B+ models), not for throughput (API is 4–6x faster for coding).

### NVIDIA Software Stack (As Referenced in Protocol Design)
```
AI Layer (NVIDIA stack — from protocol documentation)
    ├── AgentIQ — multi-agent orchestration
    ├── NIM — inference microservices  
    ├── NeMo — model lifecycle management
    └── Output = GitHub commits (public, 3-month delay)
```

---

## The Technical Questions

### Question 1: What drives the AI layer?

The protocol documentation references NVIDIA's AgentIQ, NIM, and NeMo as the AI stack. But in practice, the actual AI work is done by Claude API, MiniMax M2.5 API, and Cowork agents. The NVIDIA stack is more narrative/positioning than current implementation.

**What needs to be figured out:**

- Is there a role for NVIDIA's stack in the actual architecture, or is it purely an investor narrative tied to the Inception membership?
- If NVIDIA's tools DO have a role, where do they sit relative to the LLM APIs already in use?
- Can NIM actually serve LLMs via API in a way that's competitive with calling Claude/MiniMax directly? Or is NIM primarily for serving models on your own hardware (DGX Spark)?
- Is NeMo relevant if we're not training custom models?
- Is AgentIQ useful for orchestrating coding agents, or is it designed for a different kind of multi-agent workflow?

### Question 2: Natural language interface for protocol operations

The protocol needs a natural language layer where the operator can:

- Issue commands: "Increase MM borrowing rate by 2% for addresses exceeding 20% of borrowed supply"
- Query state: "What's the current utilization ratio and which MMs are closest to margin call?"
- Ideate: "If we launched a sigmoid curve for stablecoin projects, what parameters would match Curve Finance's fee structure?"
- Monitor: "Alert me if any MM's collateral ratio drops below 65%"

**What needs to be figured out:**

- Should PVD's signal processing feed into this natural language layer? (e.g., "PVD detected volume anomaly on HPT — cross-reference with MM borrowing activity")
- What's the right orchestration framework? Options include:
  - **NVIDIA AgentIQ** (if it actually does what the docs suggest)
  - **Claude's native tool use / computer use** (already working for us)
  - **LangChain / LangGraph** (popular but heavy)
  - **Raw Python with function calling** (simplest, matches our Parquet/Python philosophy)
  - **Something else entirely**
- Where does the LLM inference actually run? API calls to Claude/MiniMax? Self-hosted on DGX Spark? NIM microservices?
- How do we keep this "Glass Box" — every AI decision auditable, every command logged, every output a verifiable artifact?

### Question 3: Does NVIDIA's stack support LLM APIs?

Specific sub-questions:

- **NIM (NVIDIA Inference Microservices):** Can NIM serve open-source LLMs (Llama, Qwen, Mistral) as API endpoints comparable to calling OpenAI/Anthropic/MiniMax APIs? Or is it optimized for NVIDIA's own models? What's the latency/throughput vs direct API calls?
- **NeMo:** Is this only for training/fine-tuning, or does it have an inference serving component? Is it relevant if we're using off-the-shelf models?
- **AgentIQ:** Is this a real multi-agent orchestration framework, or is it more of a demo/reference architecture? Can it orchestrate heterogeneous agents (some on Claude API, some on local NIM, some on MiniMax)?
- **Build.nvidia.com:** NVIDIA offers hosted API endpoints for various models. Are these competitive on price/speed with MiniMax ($0.15/$1.20 per M tokens) or Claude? Or is this a "try before you self-host" tier?

### Question 4: Proposed architecture to evaluate

```
┌─────────────────────────────────────────────────────┐
│                  OPERATOR INTERFACE                  │
│         Natural language commands & queries          │
└──────────────────────┬──────────────────────────────┘
                       │
┌──────────────────────▼──────────────────────────────┐
│              ORCHESTRATION LAYER                     │
│    AgentIQ? Claude tool use? Raw Python? LangGraph?  │
│                                                      │
│  ┌─────────┐ ┌──────────┐ ┌───────────┐ ┌────────┐ │
│  │  PVD    │ │ Protocol │ │    MM     │ │ Market │ │
│  │ Signals │ │  State   │ │ Monitor  │ │  Data  │ │
│  └────┬────┘ └────┬─────┘ └─────┬─────┘ └───┬────┘ │
└───────┼──────────┼────────────┼──────────┼────────┘
        │          │            │          │
┌───────▼──────────▼────────────▼──────────▼────────┐
│                 INFERENCE LAYER                     │
│                                                     │
│  Claude API          MiniMax M2.5       DGX Spark  │
│  (strategic          (volume            (always-on  │
│   reasoning)          coding)            protocol   │
│                                          inference) │
│                                                     │
│  ┌─ NIM serving local models on DGX? ─┐            │
│  │  Or just direct API calls?          │            │
│  └─────────────────────────────────────┘            │
└─────────────────────────────────────────────────────┘
        │          │            │          │
┌───────▼──────────▼────────────▼──────────▼────────┐
│                   DATA LAYER                       │
│                                                     │
│  Parquet files    Twelve Data    CoinGecko    DEX  │
│  (PVD signals)    Pro API        API          APIs │
│                                                     │
│  GitHub (source of truth)    Linear (visual mirror)│
└─────────────────────────────────────────────────────┘
        │
┌───────▼────────────────────────────────────────────┐
│                   OUTPUT LAYER                      │
│                                                     │
│  GitHub commits (verifiable artifacts)              │
│  Margin call triggers                               │
│  MM performance reports                             │
│  PVD trading signals                                │
│  Protocol state dashboards (Streamlit)              │
└─────────────────────────────────────────────────────┘
```

**The core decision:** Is the orchestration layer NVIDIA-native (AgentIQ + NIM + NeMo), API-first (Claude tool use + MiniMax for volume), or hybrid? And does the answer change if we're running on DGX Spark hardware vs cloud?

---

## Constraints & Preferences

- **Glass Box philosophy:** Every AI decision must be auditable. No black box operations.
- **Raw Python preference:** We moved away from no-code tools (Baserow, Supabase, Dify) toward raw Python + Parquet. Same philosophy should apply here — simplicity over frameworks.
- **GitHub as source of truth:** All code, all documentation, all AI output commits to GitHub.
- **Contractual first, on-chain later:** The bonding curve and MM lending are contractual initially. Smart contract implementation comes after the mechanism is proven.
- **Budget:** ~$2,000/month total for AI infrastructure (M2.5 agents $1K, Claude API $600, DGX Spark amortized $333).
- **Solo founder + contract developer + AI agents:** No large team. Architecture must be operable by one person with AI assistance.

---

## What I Need From This Conversation

1. **Reality check on NVIDIA stack:** What parts of AgentIQ/NIM/NeMo are actually useful vs marketing? Specifically for serving LLMs and orchestrating agents.
2. **Orchestration recommendation:** What should the natural language command layer actually be built on?
3. **PVD integration:** How should PVD signals feed into protocol operations (margin call monitoring, MM performance tracking, anomaly detection)?
4. **Implementation plan:** Concrete steps to build the first version of this stack, starting from what already works (Claude API, PVD backtests on Railway, Streamlit app).
