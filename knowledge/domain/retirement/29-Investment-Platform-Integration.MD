# Skill: Investment Platform Integration
**Skill-ID:** 29-Investment-Platform-Integration
**World:** Retirement World v1.0
**Category:** Technology & System Landscape
**Last-Reviewed:** 2026-03-06

---

## Purpose

This skill defines the investment platform integration between the recordkeeping system, the custodian/trust accounting system, and investment managers. It covers NAV pricing feeds, trade execution flows, asset reconciliation, revenue sharing, and Rule 22c-2 shareholder data reporting. Investment platform integration is the financial backbone of the recordkeeping platform.

---

## 1. Overview of Investment Data Flows

| Flow | Direction | Content | Frequency |
|---|---|---|---|
| NAV Pricing Feed | Fund Manager / Pricing Aggregator → Recordkeeper | Daily NAV prices for all funds on the investment menu | Daily (after market close) |
| Trade Instructions | Recordkeeper → Custodian | Net buy/sell instructions by fund | Daily (before custodian cut-off) |
| Trade Confirmations | Custodian → Recordkeeper | Confirmed trade executions, unit quantities | Daily (following business day) |
| Asset Positions | Custodian → Recordkeeper | Asset-level holdings by fund and sub-account | Daily |
| Revenue Sharing Data | Fund Manager → Recordkeeper | Revenue sharing rates, accrual amounts | Monthly or as agreed |
| Shareholder Data | Recordkeeper → Fund Manager | Participant-level transaction data (Rule 22c-2) | Upon request |

---

## 2. NAV Pricing Feeds

**What NAV is:** Net Asset Value — the per-unit price of a mutual fund or collective investment trust (CIT) calculated after market close each business day.

**NAV feed sources:**
- Directly from individual fund companies
- From a pricing aggregator (e.g., Bloomberg, DTCC, SS&C) that consolidates NAV data for multiple funds

**Platform requirements:**
- Receive and apply NAV prices for all funds on the investment menu by the end of the daily valuation window
- Alert operations if any fund's NAV price is not received by the cut-off time
- Validate NAV data: prices must be positive; significant deviations from the prior day's price should be flagged for review
- Apply NAV prices to update unit-based participant account values
- Maintain NAV price history for audit and retroactive valuation purposes

**Special considerations:**
- Stable value funds do not have a daily market-price NAV — their unit price is typically maintained at a fixed value or calculated using a book value method
- Target-date funds price at the series-level NAV for the specific vintage (year-based) fund
- CITs (collective investment trusts) price differently from mutual funds and may have T+1 or T+2 pricing delays

---

## 3. Daily Valuation Process

After NAV prices are applied, the platform performs daily valuation:
1. Apply received NAV prices to all unit balances (unit balance × NAV = dollar value per sub-account)
2. Aggregate sub-account values to total participant account value
3. Aggregate participant account values to total plan value
4. Reconcile total plan value against the custodian's reported asset positions
5. Flag any discrepancy for investigation

**Platform requirements:**
- Complete daily valuation within the defined valuation window
- Generate the daily valuation report (total plan assets, by fund, by participant)
- Reconcile to custodian positions before the next business day's trading begins

---

## 4. Trade Execution Flow

### Aggregating Net Trades

The platform aggregates individual participant transaction instructions (investment elections, fund transfers, contribution allocations, distributions) into net fund-level trade instructions:
- Sum all buys for each fund across all participants
- Sum all sells for each fund across all participants
- Net buys and sells: if $1M is being bought and $600K sold in Fund A, the net instruction is a $400K buy
- Netting reduces transaction costs and custodian processing

### Trade Instruction Submission

Net trade instructions are submitted to the custodian before the custodian's trading cut-off time (typically 4:00 PM ET for end-of-day NAV execution). Instructions submitted before cut-off are executed at that day's closing NAV.

**Platform requirements:**
- Aggregate participant transactions into net trade instructions by fund
- Submit net trade instructions to the custodian before the cut-off time
- Log trade instruction submission timestamp and instruction details
- Handle trade instruction failures or rejections from the custodian

### Trade Confirmation and Posting

After the custodian executes trades, confirmation data is returned (typically next business day):
- Confirmed unit quantities purchased/sold at the executed NAV
- Settlement amounts

The platform posts the trade confirmations to participant accounts in units.

**Platform requirements:**
- Receive trade confirmations from the custodian
- Apply unit quantities to participant account sub-accounts
- Reconcile confirmed trade units against the instructions sent
- Alert operations for any unconfirmed trades or unit discrepancies

---

## 5. Asset Reconciliation

Asset reconciliation is the process of verifying that the total participant account balances in the recordkeeping system equal the total plan assets held by the custodian.

**Reconciliation levels:**
- **Plan-level:** Total recordkeeping balance = Total custodian asset balance
- **Fund-level:** Recordkeeping units × NAV = Custodian position value per fund
- **Participant-level (sample or full):** Individual participant balances reconcile to custodian sub-account records

**Reconciliation frequency:** Daily for daily-valued plans; at each valuation date for balance-forward plans.

**Common reconciliation breaks:**
- Timing differences (trade confirmations not yet received)
- Pricing differences (stale NAV used in one system)
- Missing or duplicated transaction records
- Currency rounding differences

**Platform requirements:**
- Generate daily reconciliation report (recordkeeping vs. custodian, by fund)
- Automatically flag breaks above a defined dollar or percentage threshold
- Require resolution of breaks before the next business day's valuation
- Maintain reconciliation records for audit

---

## 6. Revenue Sharing and Fee Processing

Investment managers may pay revenue sharing to the recordkeeper or the plan based on plan assets invested in their funds. Common forms:
- **12b-1 fees:** A portion of the fund's annual operating expenses paid to distributors (including recordkeepers)
- **Sub-transfer agency (sub-TA) fees:** Fees paid for participant-level recordkeeping services

**ERISA fee disclosure requirements:**
- Revenue sharing rates must be disclosed to plan fiduciaries under ERISA Section 408(b)(2)
- Revenue sharing amounts must be disclosed to participants under ERISA Section 404(a)(5) fee disclosures

**Revenue sharing application (plan-configurable):**
- Applied to offset plan administrative expenses
- Credited directly to participant accounts (pro-rata based on assets)
- Retained by the recordkeeper as compensation (disclosed under 408(b)(2))

**Platform requirements:**
- Maintain revenue sharing rates per fund in the investment data module
- Calculate revenue sharing accruals based on average plan assets per fund
- Apply revenue sharing credits per the plan's revenue sharing policy
- Generate revenue sharing data for inclusion in 404(a)(5) fee disclosures and 408(b)(2) disclosures

---

## 7. Rule 22c-2 Shareholder Data Reporting

SEC Rule 22c-2 requires recordkeepers to report participant-level transaction data to fund companies (or their designated agents) upon request to assist in detecting market timing and excessive trading.

**Data required:**
- Participant-level purchase, redemption, and exchange transactions for the fund
- Participant identifying information (taxpayer identification number or plan-assigned identifier)
- Transaction amounts and dates

**Platform requirements:**
- Generate Rule 22c-2 shareholder data reports upon request from fund companies
- Deliver data within the timeframe specified in the intermediary agreement (typically within a specified number of business days of the request) [DATE-VERIFY — confirm current Rule 22c-2 response timing requirements]
- Maintain participant-level transaction history at sufficient granularity to satisfy Rule 22c-2 data requests

---

## Agent Rules

- NAV pricing is the foundation of daily valuation — delayed or missing NAV data must generate an alert before the valuation window closes. Do not allow stale prices to be used without explicit approval.
- Asset reconciliation breaks must be resolved daily. A carry-forward unresolved break indicates a fundamental data integrity issue.
- Revenue sharing rates are fund-specific and subject to change — maintain them as configurable data, not hardcoded values.
- Trade instruction cut-off times are a hard deadline — trades submitted after the cut-off are processed at the next business day's NAV.
- Rule 22c-2 compliance requires maintaining participant-level transaction history — do not aggregate or summarize transaction data in a way that would prevent Rule 22c-2 responses.

---

## Sources

- SEC Rule 22c-2 (Market Timing) | https://www.sec.gov | Retrieved 2026-03-06
- ERISA Section 404(a)(5), 408(b)(2) (Fee Disclosure) | U.S. Department of Labor | https://www.dol.gov/agencies/ebsa | Retrieved 2026-03-06
- DTCC Mutual Fund Services | https://www.dtcc.com | Retrieved 2026-03-06
- ASPPA Investment Administration Resources | https://www.asppa.org | Retrieved 2026-03-06
