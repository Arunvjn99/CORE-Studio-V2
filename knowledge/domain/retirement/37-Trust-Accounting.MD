# Skill: Trust Accounting
**Skill-ID:** 37-Trust-Accounting
**World:** Retirement World v1.0
**Category:** Compliance Operations
**Last-Reviewed:** 2026-03-06

---

## Purpose

This skill defines trust accounting — the asset-holding and accounting layer of a retirement plan that sits alongside the recordkeeping system. It covers the trustee's role, trust fund structure, the NAV/pricing data flow, trade execution and confirmation, daily asset reconciliation, and the critical distinction between the recordkeeping system of record and the trust's asset-level records. Trust accounting integrity is the financial foundation of the plan.

---

## 1. What Trust Accounting Is

Trust accounting is the **asset-level** recordkeeping performed by the custodian/trustee. While the recordkeeper (CORE) maintains the participant-level books of record, the trustee maintains the asset-level records — what securities are held, in what quantities, and at what value.

**The fundamental reconciliation principle:**
- **Recordkeeper:** Sum of all participant account balances = Total plan assets
- **Trustee:** Total plan assets held in trust = Total securities positions × NAV

These two numbers must agree at all times. The daily reconciliation between the recordkeeping system and the trust system is the mechanism that ensures they do.

---

## 2. Trustee Types and Their Platform Interaction

### Directed Trustee (Most Common in DC Plans)

The directed trustee **acts only on instructions from the plan's named fiduciary** (the plan sponsor, investment manager, or recordkeeper acting at the plan sponsor's direction). The directed trustee does not exercise discretion over investment decisions.

**Platform interaction:**
- The recordkeeper sends **trade instructions** to the directed trustee: which funds to buy or sell, in what dollar amounts, on behalf of the plan
- The directed trustee executes the trades at end-of-day NAV as instructed
- The directed trustee returns **trade confirmations** (unit quantities purchased/sold at the executed NAV) to the recordkeeper the following business day
- The directed trustee sends daily **asset position reports** and periodic **trust accounting statements** to the recordkeeper for reconciliation

### Discretionary Trustee (Rare in DC Plans)

The discretionary trustee has independent authority to make investment decisions. The platform may receive investment direction from the trustee rather than providing direction to the trustee.

**Agent rule:** Confirm trustee type before designing any trade instruction workflow. Directed trustee = recordkeeper sends instructions to trustee. Discretionary trustee = trustee provides direction to recordkeeper.

---

## 3. Trust Fund Structure

In a DC plan, the trust typically holds assets in:
- **Separate investment sub-accounts per fund:** Each investment fund on the plan's menu has a sub-account in the trust holding the units of that fund owned by the plan
- **Cash account:** Contributions received but not yet invested; proceeds from trades pending settlement
- **Loan sub-account (if applicable):** Outstanding loan principal (participant loans are plan assets — the trust holds the promissory note as an asset)

**Platform requirements:**
- Maintain fund-level unit balances in the recordkeeping system that correspond to the trust's fund-level positions
- Maintain a cash account balance that reconciles to uninvested contribution receipts
- Reconcile loan principal on the books to the trust's loan asset balance

---

## 4. NAV Pricing and Daily Valuation Interface

**Pricing flow:**
1. Fund companies (or a pricing aggregator) publish NAV prices after market close each business day
2. Prices are transmitted to the recordkeeper via a pricing data feed
3. The recordkeeper applies the NAV prices to participant account unit balances: unit balance × NAV = dollar value
4. The trust system independently receives and applies NAV prices to its asset positions
5. The recordkeeper's total dollar values and the trust's total dollar values are compared in the daily reconciliation

**Platform requirements:**
- Receive and apply NAV prices by the defined valuation window cut-off
- Validate received prices: positive value; reasonable deviation from prior day
- Apply a stale price protocol if a fund's NAV is not received by the cut-off (use prior day's price or hold valuation — per platform policy)
- Maintain a price history per fund per date for historical valuation and audit

---

## 5. Trade Instruction and Confirmation Flow

**Trade instruction flow (recordkeeper → trustee):**
1. Participant transactions (investment elections, fund transfers, contribution allocations, distributions, loan originations) are aggregated at the recordkeeping level
2. Net fund-level trade instructions are calculated (net buys and sells across all participants per fund)
3. Net trade instructions are transmitted to the trustee/custodian before the trading cut-off (typically 4:00 PM ET)
4. The trustee executes the trades at end-of-day NAV

**Trade confirmation flow (trustee → recordkeeper):**
1. Next business day, the trustee returns confirmation data: fund, units purchased/sold, NAV at which trades executed, settlement amount
2. The recordkeeper posts the trade confirmations to participant accounts:
   - Units purchased are credited to participant sub-accounts in proportion to each participant's contribution to the net buy
   - Units sold are debited from participant sub-accounts in proportion to each participant's contribution to the net sell
3. The recordkeeper reconciles the confirmed unit quantities to the instructions sent

**Platform requirements:**
- Aggregate net trade instructions before the custodian cut-off time
- Transmit trade instructions via the configured integration method (SFTP file or API)
- Receive and post trade confirmations within the next-business-day timeline
- Reconcile confirmed units to instructions sent; flag any discrepancy
- Support trade instruction failure handling (custodian rejection of a trade instruction requires escalation and resolution)

---

## 6. Daily Asset Reconciliation

Daily reconciliation compares the recordkeeper's participant-level account totals to the trustee's asset-level positions.

**Reconciliation levels:**

### Level 1 — Plan Total
Sum of all participant account dollar values (recordkeeper) must equal total plan assets (trustee).

### Level 2 — Fund Level
Recordkeeper's unit balance per fund × that day's NAV must equal the trustee's fund position value per fund.

### Level 3 — Cash
Recordkeeper's uninvested cash (pending contributions, pending distributions) must equal the trust's cash account balance.

**Reconciliation break investigation:**
- **Timing differences:** Most common. A trade confirmed by the trustee yesterday has not yet been applied to the recordkeeper's unit balances. These resolve with the next confirmation cycle.
- **Price differences:** The recordkeeper and trustee used different NAV prices for the same fund. Usually resolves when the definitive NAV is published.
- **Missing transactions:** A contribution was posted in the recordkeeper but the trust did not receive the funding wire. Requires investigation.
- **Rounding differences:** Small differences accumulating over time from rounding at the sub-account level.
- **System errors:** A trade instruction was sent but not executed, or was executed for the wrong amount.

**Platform requirements:**
- Generate daily reconciliation report comparing recordkeeper and trustee totals at plan, fund, and cash level
- Classify breaks by type (timing difference, price difference, unresolved)
- Escalate unresolved breaks above defined dollar or percentage thresholds
- Require resolution of all non-timing breaks before processing the next business day's trades
- Maintain reconciliation history for audit

---

## 7. Trust Accounting Statement and 5500 Reporting

The trustee generates periodic trust accounting statements (monthly, quarterly, annual) that form the basis for:
- Form 5500 Schedule H (Large Plan Financial Statements) — requires independently audited financial statements for large plans
- Annual asset reconciliation sign-off

**Platform requirements:**
- Receive and store trust accounting statements
- Reconcile the annual trust statement to the platform's year-end balance
- Provide trust accounting data to the TPA or auditor as part of the 5500 preparation process

---

## 8. Loan Asset Accounting

Participant loans are plan assets — the participant's promissory note is held by the trust.

**Trust loan accounting:**
- The trust records outstanding loan principal as a plan asset
- As loan repayments are received, the trust records the principal reduction and interest income
- At loan payoff or deemed distribution, the trust removes the loan asset from its records

**Recordkeeper-trust loan reconciliation:**
- Outstanding loan balance in the recordkeeping system (per participant) must equal the total loan asset in the trust
- Discrepancies indicate processing errors in loan origination, repayment, or payoff

---

## 9. Revenue Sharing Accounting

Revenue sharing payments from investment managers to the plan (sub-TA fees, 12b-1 fees) flow through the trust:
- The trust receives revenue sharing payments from fund companies
- Revenue sharing is allocated per the plan's revenue sharing policy (offset expenses, credit to participants, or retain as recordkeeper compensation)
- The platform must track revenue sharing receivables and receipts

---

## Agent Rules

- The directed trustee acts only on explicit trade instructions — the platform must generate clear, complete trade instructions per fund before the custodian cut-off. Vague or incomplete instructions are rejected.
- Daily reconciliation is non-negotiable. An unreconciled trust position is a financial integrity failure.
- Never assume a trade was executed because an instruction was sent — always require and post the trade confirmation before updating participant account unit balances.
- Trust accounting statements (not just recordkeeper reports) are required for Form 5500 Schedule H and audit purposes. Ensure trust statement receipt and reconciliation is built into the year-end workflow.
- Loan balances must be reconciled between the recordkeeper and the trust — loans are plan assets and must appear in both systems.

---

## Sources

- ERISA Section 403 (Trustee Requirements) | U.S. Department of Labor | https://www.dol.gov/agencies/ebsa | Retrieved 2026-03-06
- IRS Form 5500 Schedule H Instructions | https://www.dol.gov/agencies/ebsa | Retrieved 2026-03-06
- SPARK Institute API Integration Guidelines, June 2025 | https://www.sparkinstitute.org | Retrieved 2026-03-06
- DTCC Mutual Fund Services (Trade Settlement) | https://www.dtcc.com | Retrieved 2026-03-06
- DOL Field Assistance Bulletin 2004-3 (Directed Trustees) | https://www.dol.gov/agencies/ebsa | Retrieved 2026-03-06
