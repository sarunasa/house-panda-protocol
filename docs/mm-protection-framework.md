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

**Oracle question:** Curve price (deterministic but manipulable) vs exchange market price (real but needs oracle) vs hybrid TWAP.

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

*Last updated: 2026-02-28*
