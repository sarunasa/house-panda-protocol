# House Panda Protocol — Core Mechanism Design

## Overview

House Panda Protocol is a token lending system built on a convex bonding curve. Instead of the traditional launch model (presale to insiders → dump on retail), the protocol presells only 1–3% of supply and offers the remaining 97–99% to market makers as borrowable inventory against the curve.

Market makers borrow tokens by posting collateral, provide liquidity on external venues (DEX/CEX), pay interest back to the curve treasury, and return tokens or get liquidated. The bonding curve acts simultaneously as price discovery mechanism, treasury, and liquidity backstop.

## Curve Shape: Convex Elliptical (Quarter-Circle)

The protocol uses a convex curve — specifically the lower-right quarter of an ellipse:

```
p(s) = P_max * (1 - sqrt(1 - (s / S_max)^2))
```

Where `s` is supply borrowed (0 to S_max), `p` is price, `P_max` is the asymptotic price ceiling, and `S_max` is the maximum borrowable supply.

**Why this shape:**

- **Cheap bootstrapping zone.** The flat early portion means MMs can borrow large amounts cheaply when the token needs liquidity most. Subsidizes early market-making through curve geometry rather than token grants.

- **Accelerating scarcity premium.** Each additional token costs dramatically more as supply is consumed. MMs self-regulate because borrowing becomes prohibitive.

- **Built-in defense against over-extraction.** Borrowing the last 20–30% is astronomically expensive. Mathematically impossible to drain the curve — it acts as its own circuit breaker.

- **Organic transition point.** There's a natural inflection where buying on the open market becomes cheaper than borrowing from the curve. The token "graduates" to organic liquidity automatically.

**Marginal cost (derivative):**
```
dp/ds = (P_max * s) / (S_max^2 * sqrt(1 - (s/S_max)^2))
```
Goes to infinity as s → S_max, meaning full extraction is impossible.

**Why convex beats alternatives:**

| Curve | Bootstrapping | Scarcity | Anti-manipulation | Notes |
|-------|--------------|----------|-------------------|-------|
| **Convex elliptical** ✓ | Cheap early zone | Accelerating | Strong — expensive to pump, brutal to dump | Best overall for this use case |
| Linear | No discount | Proportional | Mediocre — symmetric entry/exit | Too predictable |
| Sigmoid | Some early discount | Capped | Good at extremes, weak in middle | Flattening at top is wrong — we want acceleration |
| Concave | Expensive early | Diminishing | **Terrible** — facilitates pump and dump | Small buys create big price jumps |
| Logarithmic | Steep early | Diminishing | Strong against pumps, weak against dumps | Sophisticated actors can exploit flat upper zone |
| Pure exponential | Too steep at origin | Strong | Good | Quarter-circle gives flatter bootstrapping zone |

## Market Maker Borrowing Module

MMs deposit collateral (ETH/USDC) → borrow tokens at curve price → provide liquidity on DEXs/CEXs → pay interest to curve treasury → return tokens or get liquidated.

**The critical design challenge:** Without constraints, MM borrowing is a guaranteed profit machine. A MM who borrows cheaply from the flat zone controls circulating supply and extracts rent from every participant. That's not market making — it's a subsidized monopoly.

### Obligation Framework

Borrowing from the curve is a **license, not a right.** It comes with enforceable conditions:

1. **Concentration penalties.** Fee discount scales inversely with share of borrowed supply. First MM to borrow 30% pays more per unit than someone borrowing 5%. Concentration becomes expensive.

2. **Performance-based interest.** Tied to realized spread, not flat. Fat spreads = higher interest. Tight spreads = low interest. Taxes monopoly rents directly.

3. **Two-sided quoting obligation.** Minimum depth, maximum spread, minimum uptime — enforced on-chain via observable order book / AMM positions. Failure to meet obligations triggers liquidation or loss of borrowing privileges.

4. **Time-decay on borrowing advantage.** Grace period with cheap rates, but interest ratchets up over time unless MM demonstrably adds value (tight spreads, high fill rates, consistent uptime). Prevents "borrow and sit" strategies.

## Fee Architecture

Three revenue streams from one mechanism:

### 1. Borrow Interest
Paid by MMs on borrowed tokens. Variable rate tied to MM performance metrics and curve utilization.

### 2. Curve-Linked Transaction Fees
Every transfer generates a fee proportional to curve position — essentially **congestion pricing for the token economy:**

- Early stage (flat curve, low utilization): fees near zero → encourages adoption
- Mid stage: fees ramp gradually → meaningful revenue as ecosystem matures
- Late stage (steep curve): fees high, but organic activity absorbs the cost

**Cap the fee** asymptotically at 1–2% to avoid killing liquidity at the top of the curve.

### 3. Flat Operational Fee
Small fixed percentage goes to treasury for operations/marketing.

### Fee Split
- One portion (curve-linked) → curve reserves (deepens liquidity)
- One portion (flat) → treasury (funds operations)
- MM borrowers get fee discount proportional to collateral ratio

**Critical constraint:** Total cost of transacting (borrow interest + transaction fee + gas) must stay below ~3–4% at any realistic utilization level. Beyond that, MMs leave for competing venues.

## Revenue Model

At moderate adoption levels:

| Stream | Assumptions | Annual Revenue |
|--------|-------------|---------------|
| Borrow interest | $10M notional borrowed, 5–10% rate | $500K–$1M |
| Transaction fees | $5M daily volume, 0.3% avg fee | ~$5.5M |
| Curve reserve appreciation | Demand-driven | Treasury value growth |

**Conservative case:** $300K daily volume → ~$328K/year. Still viable.
**Moderate case:** $5M daily volume with 3–5 active MMs → well above $1M/year.

**Key insight:** Marketing spend has a **direct, measurable ROI loop.** Marketing → new buyers → curve activity → fees → treasury → more marketing. With a convex curve, each unit of demand generates more fee income than the last. Marketing ROI improves over time.

This is unusual: the team benefits from **volume and activity**, not from holding and dumping. Incentivized to drive sustained usage, not pump-and-dump hype cycles.

## Anti-Manipulation Properties

The convex curve is among the best shapes for resisting pump and dump:

- **Expensive to pump.** Must buy huge supply to move price meaningfully from the flat zone.
- **Brutal to dump.** Selling back down the steep portion gives terrible execution. The bigger the dump, the worse the exit price.
- **Visible.** Every buy/sell moves the curve visibly. No hiding accumulation.
- **MM support layer.** Active MMs provide sell-side depth during pumps and buy-side support during dumps — not from altruism, but from their position economics.

No mechanism fully eliminates manipulation. A sufficiently capitalized, patient actor can game any curve. But the curve makes manipulation **visible, expensive, and less profitable** — eliminated by economics rather than rules.

## Uniswap Differentiation

**Uniswap says:** bring your own liquidity, we'll facilitate trades.
**House Panda says:** we provide the liquidity, you choose the economics.

| Dimension | Uniswap | House Panda |
|-----------|---------|-------------|
| LP/MM relationship | LPs **buy** assets, take directional risk | MMs **borrow** assets, take spread risk only |
| Curve selection | One curve (x*y=k) for everything | Token launcher chooses curve shape |
| Liquidity | Fragmented per pair | Shared pool across tokens |
| LP obligations | Passive — deposit and walk away | Active — quoting obligations enforced |
| New token liquidity | Zero on day one, must attract own LPs | Instant access to shared pool |

The fundamental distinction: Uniswap LPs own the token and eat impermanent loss. House Panda MMs never own the token. They're exposed to spread income and interest costs, not price trajectory. MMs will provide liquidity for tokens they don't believe in — because they don't have to.

## Platform Evolution (5-Step Roadmap)

Each step is a viable business on its own. No pressure to promise the full vision on day one.

### Step 1: Launch own token on own convex curve
Proof of concept. First customer of own infrastructure. If it breaks, it only breaks for us.

### Step 2: Open that curve to others
"Launch your token on the same curve type that's already working with active MMs and real liquidity." Credible pitch because it's a live system, not a whitepaper.

### Step 3: Add new curve types
Build what the market tells us to build. Stablecoin projects need concave? Gaming tokens want sigmoid? Demand-driven.

### Step 4: Open new curves to others
Same playbook as step 2, repeated per curve type. Each proven internally before offered externally.

### Step 5: Unify the liquidity pool
One giant pool. Many pricing functions. Any token. MMs borrow once and operate everywhere.

The pool is the light. The curves are the prism. The tokens are the colors.

**Isolation mechanism:** Collateral is logically partitioned but physically unified. Each token has a claim on a portion of the pool; liquidations can only touch that token's allocated portion. Idle collateral available across the system for capital efficiency. This is essentially how modern clearinghouses work.

**Network effects at scale:**
- Token launchers: "Launch on our curve and get instant liquidity from a $50M shared pool"
- MMs: Borrow once, make markets across everything. Risk diversified, capital efficiency maximized.
- Traders: Every token has real liquidity from day one.
- Flywheel: More tokens → bigger pool → better liquidity → more tokens → bigger pool

## Design Philosophy

**Go plain.** The bonding curve mechanism IS the product. No need to promise prediction markets, governance modules, or metaverse integrations.

Why:
- Promising products means being judged on delivery — every week without updates becomes FUD
- The more products promised, the more it looks like a security
- Plain tokens with strong mechanisms outperform promise tokens long-term
- Aligns with operational reality: a bonding curve can run autonomously

"Plain" doesn't mean "nothing." Open-source the contracts, let community build on top, position the curve as infrastructure that *could* underpin anything — without committing to building it.

## Engineering Scope

The bonding curve is not a weekend smart contract. Full scope includes:

- Core curve contract (elliptical math, collateral management, precision handling, overflow/rounding protection)
- Borrowing module (collateral deposits, health factors, liquidation engine, interest accrual, MM registration, obligation enforcement)
- Fee system (curve-linked dynamic fees, split logic, MM discounts, fee-on-transfer compatibility)
- Oracle and price feeds (curve price readable by external protocols, manipulation-resistant)
- Liquidation mechanism (cascade handling along convex curve — each liquidation changes price for subsequent ones)
- Security (multiple audits, formal verification — the system holds real collateral)
- Frontend (dashboard showing curve state, borrow positions, fee income, MM performance)
- Multi-chain deployment, governance, upgradability, documentation

This scope justifies the token's existence and "go plain" strategy. The mechanism deserves full engineering attention.