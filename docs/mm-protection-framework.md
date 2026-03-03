# Market Maker Protection Framework

*5-Layer Defense Against Lending Extraction*

---

## The Attack Vector

MM posts collateral worth X. Borrows tokens from the bonding curve. Token price appreciates. Tokens now worth 3X. MM walks away — forfeits collateral worth X, keeps tokens worth 3X, nets 2X profit. The "lending" was actually a discounted purchase.

---

## Why Obvious Solutions Fail

| Solution | Problem |
|----------|---------|  
| Over-collateralization (150%+) | Defeats the purpose — MMs borrow because they don't want to buy outright |
| Fixed collateral ratio at borrow time | THIS is the vulnerability — collateral set when borrowed, token value moves |
| Token-denominated collateral | Circular — if MM had HPT to post, they wouldn't need to borrow |

---

## Layer 1: Dynamic Collateral with Margin Calls

Collateral marked to market continuously. If HPT appreciates 20%, requirement increases proportionally. Top up within 48 hours or face liquidation.

Collateral maintained at **60-70% of current token value** (not borrowing-time value). Default profitable only above ~2.5-3x appreciation, with margin calls forcing continuous top-ups.

### Margin Call Oracle — Price Source Resolution

**The problem:** The margin call mechanism requires a reliable price to determine when to demand additional collateral. Both available price sources are manipulable by the MM:

| Price Source | Manipulation Vector |
|-------------|-------------------|
| **Curve price** | MM temporarily deposits tokens back into the curve to suppress the price reading, avoids margin call trigger, then withdraws. Cheap to execute in the flat zone. Deterministic but gameable. |
| **Exchange market price** | MM wash trades or spoofs on the exchange to temporarily crash the visible price. Illegal in most jurisdictions but enforcement is patchy in crypto. The MM literally controls the order book as primary liquidity provider. |

**The deeper problem:** The MM is the entity most capable of manipulating *either* price. They sit on both sides — controlling curve activity (as borrower) and exchange activity (as market maker). Any single price source gives them a lever.

**Resolution: Contractual TWAP with dispute terms.**

Since borrowing will be contractual at first (referring mathematically to the bonding curve but not implemented on-chain initially), the margin call trigger is defined as:

- **Weighted average price** across multiple independent price sources (e.g., 3+ exchanges or aggregators where HPT trades)
- **24-hour rolling window** — momentary manipulation gets averaged out
- **Dispute resolution terms** built into the lending contract — if MM contests a margin call, defined arbitration process applies

This means manipulation has to be **sustained across multiple venues for 24+ hours** to succeed, which is dramatically more expensive and visible than gaming a single source in a single block.

**Future migration path:** As the protocol matures and moves on-chain, the contractual TWAP transitions to a Chainlink-style oracle aggregation or a custom TWAP oracle reading from multiple DEX pools. The contractual version serves as the specification for what the on-chain version must replicate.

**Open item for legal review:** The lending contract should specify exact price sources, weighting methodology, margin call notification procedure, cure period, and dispute resolution venue. Securities lawyer should review.

## Layer 2: Restricted Token Custody

Borrowed tokens sit in smart contract permitting only transfers to approved exchange deposit addresses. Cannot be moved to personal wallets, DEXes, or bridges. Forces any extraction to happen on-venue where it's visible and attributable.

## Layer 3: Tranche-Based Lending

| Tranche | Amount | Release Condition |
|---------|--------|-------------------|
| 1 | 40% | Immediate |
| 2 | 30% | After 30 days of demonstrated MM activity |
| 3 | 30% | After 60 days of demonstrated MM activity |

Limits maximum exposure. If extracting from Tranche 1, never gets Tranche 2.

## Layer 4: Economic Penalty Stack

- **Future access revocation:** Permanent protocol ban
- **Public attribution:** Default published on-chain and in GitHub commit history
- **Cross-MM socialization:** Default shifts curve up, costing OTHER MMs money (social enforcement)
- **Legal recourse:** MM is KYC'd entity, lending agreement is legal contract

## Layer 5: Dynamic Risk Pricing

Lending rate = base rate + risk premium. Risk premium increases as mark-to-market gap widens. Makes holding position increasingly expensive as default temptation grows. Rational choice becomes return-and-reborrow rather than hold-and-default.

---

## Combined Defense

A rogue MM would need to: defeat transfer restrictions (L2) within margin call window (L1) with only partial allocation (L3) accepting permanent exclusion + legal exposure (L4) while paying escalating rates (L5).

**Goal: make default irrational at every decision point.**

---

*Last updated: 2026-03-03*