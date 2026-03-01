# AI Infrastructure Strategy — Cost Analysis & Architecture

_March 2026_

## MiniMax M2.5 Overview

Released February 12, 2026. 230B-parameter MoE model activating only 10B parameters per forward pass. Open-source on Hugging Face.

**Key benchmarks:**
- SWE-Bench Verified: 80.2% (vs Opus 4.6 ~80.8%)
- Multi-SWE-Bench: 51.3% (vs Opus 4.6 ~50.3%)
- AIME 2025: 45% (significantly trails frontier on general reasoning)
- Terminal-Bench 2: 52% (vs Opus 65.4%)

**Verdict:** Specialist that matches the generalist on coding, not an across-the-board replacement. MiniMax itself uses M2.5 for 80% of newly committed code internally.

## Pricing

| Variant | Input/M tokens | Output/M tokens | Speed | Cost/hour continuous |
|---------|---------------|-----------------|-------|---------------------|
| M2.5 Standard | $0.15 | $1.20 | 50 tok/s | $0.30 |
| M2.5 Lightning | $0.30 | $2.40 | 100 tok/s | $1.00 |

### What $100/Day Buys (M2.5 Standard, 30/70 input/output split)

- ~113M total tokens
- ~32 SWE-Bench-level coding tasks (real GitHub issue resolution)
- ~500-2,000 smaller tasks (module creation, bug fixes, code review)
- 14 parallel coding agents running 24/7

### Comparison: $100 Token Purchasing Power

| Model | $100 buys (blended) | Multiplier vs Opus |
|-------|--------------------|-----------|
| M2.5 Standard | ~113M tokens | 21× |
| M2.5 Lightning | ~56M tokens | 11× |
| Claude Sonnet 4.5 | ~8.8M tokens | 1.7× |
| Claude Opus 4.6 | ~5.3M tokens | 1× |

## Full-Time Agent Economics

**~$200/month per always-on coding agent.**

- M2.5 Standard at 50 tok/s: $0.30/hour × 720 hours = $216/month (24/7)
- M2.5 Lightning at 100 tok/s: $1/hour nominal, but real utilization ~25-30% → $180-216/month
- 5 parallel agents: ~$1,000/month
- 14 parallel agents: ~$3,000/month

## Recommended Hybrid Architecture

### Tier 1: Volume Work — MiniMax M2.5 (~80% of budget)

Parallel agents handling:
- Routine code generation and refactoring
- Code review and test generation
- Documentation generation
- CI/CD maintenance
- Data pipeline work
- PVD signal processing code

### Tier 2: Frontier Intelligence — Claude Opus/Sonnet (~20% of budget)

- Architecture decisions
- Complex debugging
- Strategic reasoning
- Security audits
- Tasks requiring maximum general intelligence

### Budget Example: $100/Day

| Tier | Allocation | Capability |
|------|-----------|------------|
| M2.5 Standard | $80/day | ~25 SWE-Bench tasks or ~1,500 smaller tasks via 10+ parallel agents |
| Claude Opus/Sonnet | $20/day | ~1-4M tokens for high-complexity work |

## DGX Spark vs API vs MiniMax

| Factor | 2× DGX Spark ($8K one-time) | MiniMax M2.5 API ($200/mo/agent) | Claude API ($20/day) |
|--------|---------------------------|--------------------------------|---------------------|
| Model quality | Open models (good, not frontier) | 80.2% SWE-Bench (frontier coding) | Frontier general + coding |
| Token speed | 15-40 tok/s | 50-100 tok/s | 80-120 tok/s |
| Context window | 16-32K practical | 200K | 200K |
| Privacy | Complete on-prem | Data to MiniMax (China) | Data to Anthropic |
| Cost structure | Fixed hardware + power | Variable per token | Variable per token |
| Concurrent tasks | 1-2 models max | Unlimited parallel | Unlimited parallel |
| Best for | On-prem compliance, 120B+ models | High-volume routine coding | Complex reasoning |

## Strategic Implications for House Panda

The protocol's "AI that never sleeps" narrative becomes economically viable:

1. **$1,000/month** runs 5 parallel coding agents producing verifiable GitHub commits 24/7
2. **GitHub as transparency mechanism** — all AI output is auditable artifacts
3. **Hybrid routing** matches the community consensus: cheap models for routine work, frontier models for hard problems
4. **Self-hosting option** via Hugging Face open weights if data sovereignty becomes a requirement

The question is no longer whether AI agents are affordable for continuous protocol operation — they are. The question is orchestration: how to route tasks between tiers efficiently.
