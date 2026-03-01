# AI Infrastructure Cost Analysis — Coding Agent Economics

*Analysis date: March 2026*

## MiniMax M2.5 Pricing

Released February 12, 2026. 230B-parameter MoE model, activates 10B parameters per forward pass.

| Variant | Input (/M tokens) | Output (/M tokens) | Speed | Cost/hour continuous |
|---------|-------------------|--------------------:|-------|---------------------|
| **Standard** | $0.15 | $1.20 | 50 tok/s | $0.30 |
| **Lightning** | $0.30 | $2.40 | 100 tok/s | $1.00 |

### Performance

- SWE-Bench Verified: 80.2% (vs Opus 4.6 ~80.8%)
- Multi-SWE-Bench: 51.3% (vs Opus 50.3% — M2.5 leads)
- AIME 2025: 45% (trails Opus significantly on general reasoning)
- Terminal-Bench 2: 52% (vs 65.4% for Opus)

**Assessment:** Specialist that matches the generalist on coding. Not an across-the-board replacement. Weaker on complex reasoning and terminal operations.

MiniMax uses M2.5 for 80% of its own newly committed code and 30% of all company tasks.

## $100/Day Budget Analysis

### M2.5 Standard

| Allocation | Tokens |
|-----------|--------|
| All input | 667M tokens |
| All output | 83M tokens |
| Blended (30/70 coding split) | ~113M tokens |

### What $100/Day Buys in Practice

**By task complexity:**
- Complex SWE-Bench-level tasks (~3.52M tokens each): ~32 tasks/day
- Smaller tasks (50K–200K tokens): 500–2,000 tasks/day

**By continuous operation:**
- Standard at $0.30/hour: 333 hours (way more than 24h)
- Could run ~14 parallel coding agents simultaneously, 24/7

**Throughput constraint:** Single stream at 50 tok/s only generates ~4.3M output tokens/day. To spend $100/day requires ~18 parallel streams. This is the right architecture for agentic coding — multiple agents on different tasks.

## Full-Time Agent Cost

One always-on coding agent ≈ **~$200/month**

| Variant | 24/7 continuous | Realistic utilization (25–30%) |
|---------|----------------|-------------------------------|
| Standard (50 tok/s) | $216/month | ~$55–65/month |
| Lightning (100 tok/s) | $720/month | ~$180–216/month |

Five agents running around the clock: ~$1,000/month.

## Comparison: $100/Day Across Providers

| Provider | $100 buys (blended) | Quality tier |
|----------|--------------------:|-------------|
| MiniMax M2.5 Standard | ~113M tokens | Frontier-coding specialist |
| MiniMax M2.5 Lightning | ~56M tokens | Same quality, 2x speed |
| Claude Sonnet 4.5 | ~8.8M tokens | Frontier general |
| Claude Opus 4.6 | ~5.3M tokens | Best general reasoning |
| GPT-5 Mini | ~15M tokens | General mid-tier |

M2.5 delivers 13–21x more tokens per dollar than Claude.

## Recommended Hybrid Architecture for House Panda

### M2.5 Standard (~$80/day)
14 parallel agents handling:
- Routine coding, code review, test generation
- Documentation, CI/CD maintenance
- Data pipeline work, PVD signal processing code
- ~25 SWE-Bench-level tasks or ~1,500 smaller tasks

### Claude Opus/Sonnet (~$20/day)
1–4M tokens for:
- Architecture decisions
- Complex debugging
- Strategic reasoning, security audits
- The thinking that requires frontier general intelligence

### DGX Spark (if applicable)
Always-on inference for:
- Protocol operations (bonding curve AI, MM monitoring)
- PVD signal processing (24/7 without API costs)
- The "AI that never sleeps" narrative
- GitHub commits as verifiable AI output artifacts

### Total Monthly Budget

| Component | Monthly Cost | What You Get |
|-----------|-------------|-------------|
| M2.5 agents (5 full-time) | $1,000 | Volume coding, routine tasks |
| Claude API | $600 | Strategic intelligence |
| DGX Spark (amortized) | $333 | Always-on protocol infra |
| **Total** | **~$2,000** | **Small engineering team equivalent** |

This gets the volume of a small engineering team on routine work, frontier intelligence for hard problems, and always-on protocol infrastructure — all transparent via GitHub commits.