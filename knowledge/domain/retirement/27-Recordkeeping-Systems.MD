# Skill: Recordkeeping Systems
**Skill-ID:** 27-Recordkeeping-Systems
**World:** Retirement World v1.0
**Category:** Technology & System Landscape
**Last-Reviewed:** 2026-03-06

---

## Purpose

This skill defines what a recordkeeping system is, its core functional modules, and the architecture decisions that shape platform design. Understanding recordkeeping system architecture is prerequisite to writing requirements for any CORE feature.

---

## 1. What a Recordkeeping System Does

A recordkeeping system maintains the **individual account records** of every plan participant. It is the system of record for participant-level plan data.

Core functions:
- Track contributions, investment activity, distributions, loans, fees, and resulting account balances by contribution source and investment fund
- Maintain participant records (demographics, eligibility, enrollment, elections)
- Process payroll data into participant account postings
- Communicate with the custodian/trustee for investment execution and reconciliation
- Generate participant statements, plan sponsor reports, and regulatory data

**The recordkeeper is NOT the asset holder** — assets are held by the custodian/trustee. The recordkeeper holds the books of record; the custodian holds the assets. These must reconcile daily.

---

## 2. Daily Valuation vs. Balance-Forward Plans

### Daily Valuation

Account balances are updated daily based on current investment fund NAV prices received from the fund company or pricing aggregator. Most modern DC plans are daily-valued.

**Characteristics:**
- Participants can view current account values on any business day
- Participants can transact (investment changes, loan requests, distribution requests) any business day
- NAV pricing feeds must be received and applied before the day's valuation closes
- Trade execution windows apply (cut-off times for same-day NAV processing)

### Balance-Forward Plans

Account balances are updated only at defined valuation dates (e.g., quarterly, semi-annually). Less common in current market; legacy plans may operate this way.

**Characteristics:**
- Simpler platform architecture
- Limited participant self-service capability
- Transaction processing batched at valuation dates
- Lower data feed requirements

**Platform implication:** Requirements must specify whether a plan is daily-valued or balance-forward. Platform features designed for daily-valued plans may not function correctly for balance-forward plans.

---

## 3. Key Functional Modules

| Module | Purpose |
|---|---|
| **Participant Record Management** | Master record for each participant; eligibility, enrollment, elections, demographics |
| **Contribution Processing** | Payroll file intake, validation, allocation, posting |
| **Investment Election and Trade Execution** | Capture fund elections; generate trade instructions; process investment changes |
| **Loan Origination and Administration** | Loan request, max calculation, repayment tracking, default handling |
| **Distribution Processing** | Initiation, tax withholding, settlement, 1099-R |
| **Vesting Calculation** | Service tracking, vesting schedule application, forfeiture processing |
| **Compliance Testing Data Collection** | HCE classification, contribution aggregation, test data preparation |
| **Notice Generation and Delivery** | Automated generation, e-delivery, tracking |
| **Participant and Plan Sponsor Portal** | Self-service and administrative interfaces |
| **Reporting and Statement Generation** | Participant statements, plan sponsor reports, regulatory data |
| **Trust/Custodian Interface** | Trade instruction output, NAV pricing input, asset reconciliation |
| **Payroll Integration** | File/API intake, mapping, validation, bidirectional data exchange |
| **Document Management** | Plan document storage, version control, notice storage |
| **Audit Trail** | Immutable log of all system events, changes, and user actions |

---

## 4. System of Record Principles

The recordkeeping system is the **single source of truth** for participant-level plan data. This creates several design principles:

- **Immutability of original records:** Corrections must be posted as new transactions; original records are never overwritten or deleted.
- **Audit trail completeness:** Every state change — contribution posting, investment election, distribution, correction — must be logged with timestamp, actor, and change detail.
- **Referential integrity:** Transactions must link to originating events (payroll file, participant request, plan event).
- **Reconcilability:** The sum of all participant account balances must equal the total plan assets held by the custodian at any point in time.

---

## 5. Data Flows — Key Integration Points

| Integration | Direction | Data | Frequency |
|---|---|---|---|
| Payroll → Recordkeeper | Inbound | Contribution data, census updates | Per payroll cycle |
| Recordkeeper → Payroll | Outbound | Loan repayment schedules, distribution events | As needed / cycle |
| Recordkeeper → Custodian | Outbound | Net trade instructions | Daily |
| Custodian → Recordkeeper | Inbound | Trade confirmations, NAV pricing, asset positions | Daily |
| Fund Managers → Recordkeeper | Inbound | NAV prices, fund data | Daily |
| Recordkeeper → TPA | Outbound | Compliance testing data, 5500 data | Annual / as needed |
| Recordkeeper → Plan Sponsor | Outbound | Reports, statements, exception alerts | Per schedule |
| Participant Portal → Recordkeeper | Bidirectional | Elections, requests, account view | Real-time / daily |

---

## 6. Multi-Plan Architecture

Many recordkeepers (including CORE) support multiple plans on a single platform. Key architectural requirements for multi-plan support:
- Complete data isolation between plans (participant data, contribution data, investment data)
- Plan-level configuration (each plan has its own adoption agreement parameters)
- Cross-plan reporting for plan sponsors with multiple plans
- Controlled group data management — employees may participate in multiple plans; census and service must be tracked across plans

---

## 7. Performance and Scalability Considerations

The retirement recordkeeping domain has specific scalability characteristics:
- **Payroll processing surge:** All plans with the same payroll frequency (e.g., bi-weekly) submit files in the same week — the platform must handle high-volume concurrent payroll processing
- **Year-end processing surge:** Compliance testing, statement generation, 1099-R production all converge at plan year-end
- **Daily valuation window:** NAV pricing must be applied and account balances updated within a defined daily window
- **Audit trail volume:** Every transaction generates audit trail records — at scale, audit trail storage and retrieval must be purpose-designed

---

## Agent Rules

- Requirements must specify whether they apply to daily-valued or balance-forward plans — these have fundamentally different processing architectures.
- The recordkeeper holds the books of record; the custodian holds the assets. Reconciliation between these two systems is non-negotiable and must occur daily for daily-valued plans.
- Audit trail requirements are absolute — no system event, transaction, or configuration change may occur without an audit trail entry.
- Original records are never overwritten — corrections are new transactions. This is foundational to the integrity of the system of record.

---

## Sources

- IRS Retirement Plans — Plan Administration | https://www.irs.gov/retirement-plans | Retrieved 2026-03-06
- DOL ERISA Regulations | https://www.dol.gov/agencies/ebsa | Retrieved 2026-03-06
- SPARK Institute Technology Standards | https://www.sparkinstitute.org | Retrieved 2026-03-06
- ASPPA Plan Administration Resources | https://www.asppa.org | Retrieved 2026-03-06
