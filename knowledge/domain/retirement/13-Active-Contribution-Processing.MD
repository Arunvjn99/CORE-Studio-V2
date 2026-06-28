# Skill: Active Contribution Processing
**Skill-ID:** 13-Active-Contribution-Processing
**World:** Retirement World v1.0
**Category:** Participant Lifecycle
**Last-Reviewed:** 2026-03-06

---

## Purpose

This skill defines the contribution processing workflow during a participant's active period — from payroll cycle data receipt through allocation to participant accounts. It covers limit monitoring, match calculation, auto-escalation, and the validation rules that must pass before contributions are posted.

---

## 1. Payroll Cycle Processing Overview

Each payroll cycle, the payroll provider transmits contribution data to the recordkeeper via file or API. The platform processes this data in a defined sequence:

1. **File/API receipt** — contribution data received from payroll provider
2. **Format validation** — verify file structure, field completeness, and data types
3. **Participant matching** — match each contribution record to a participant record
4. **Eligibility check** — verify participant is eligible for the contribution source
5. **Limit monitoring** — check contributions against applicable limits (deferral, 415)
6. **Employer match calculation** — calculate employer match per plan formula
7. **Exception handling** — route failures to exception queue
8. **Contribution posting** — post validated contributions to participant accounts by source
9. **Investment allocation** — invest posted contributions per participant investment elections
10. **Trade instruction** — send net trade instructions to custodian for execution
11. **Funding reconciliation** — reconcile posted amounts to trust receipt

---

## 2. Contribution Source Tracking

Every contribution must be attributed to its correct source / money type before posting. Source determines:
- Vesting schedule applied
- Distribution eligibility rules
- 415 annual additions limit inclusion
- Tax withholding on eventual distribution
- Nondiscrimination testing classification (ADP applies to elective deferrals; ACP applies to match and after-tax)

**Platform requirements:**
- Map payroll source codes to plan money types at the plan level
- Validate source code for each contribution record
- Reject contributions with unrecognized or invalid source codes to the exception queue
- Never post a contribution without a valid source tag

---

## 3. Contribution Limit Monitoring

[COMPLIANCE-SENSITIVE]

The platform must monitor contributions throughout the year against applicable limits. All limits are plan-configurable parameters sourced from current IRS limit tables — never hardcode.

### Annual Elective Deferral Limit (IRC 402(g))

- Applies to the combined total of pre-tax and Roth elective deferrals per participant across all plans of the same employer
- Monitor year-to-date deferrals against the plan-year limit
- Stop contributions when the limit is reached; alert participant and plan sponsor
- Catch-up contributions (age 50+) are permitted above the regular limit (plan-configurable per IRS rules)
- Super Catch-Up (ages 60–63, SECURE 2.0): higher catch-up limit (plan-configurable per IRS rules) [DATE-VERIFY]

### 415 Annual Additions Limit (IRC 415)

- Applies to the combined total of all annual additions per participant: employee deferrals (pre-tax and Roth) + employer contributions (match, non-elective) + employee after-tax + forfeitures allocated
- Does NOT include rollover contributions or loan repayments
- Monitor year-to-date annual additions against the 415 limit (plan-configurable per IRS rules)
- Stop employer contributions or deferrals when approaching the limit

### Catch-Up Contribution Monitoring

Participants eligible for catch-up contributions have a separate limit layer:
- Regular catch-up: age 50 and over (plan-configurable per IRS rules)
- Super Catch-Up: ages 60–63 (SECURE 2.0; plan-configurable per IRS rules) [DATE-VERIFY]
- Super Catch-Up is the higher of the regular catch-up limit or the Super Catch-Up amount
- Age tracking must accurately determine which catch-up tier applies each year
- Mandatory Roth routing: higher earners' catch-up contributions may be required to be Roth [DATE-VERIFY — confirm current rules and compensation threshold]

---

## 4. Employer Match Calculation

The match formula is defined in the plan's adoption agreement and is plan-configurable. Common formula types:
- **Fixed match:** Employer matches X% of employee deferrals up to Y% of compensation (both X and Y are plan-configurable)
- **Tiered match:** Different match rates at different deferral tiers (all rates plan-configurable)
- **Dollar-for-dollar match:** Employer matches 100% of employee deferrals up to a dollar cap (plan-configurable)
- **Discretionary match:** Employer decides the match formula at year end

**Per-payroll vs. annualized match:**
- **Per-payroll match:** Match is calculated and funded each payroll cycle. Participants who stop contributing mid-year may receive less match than the formula implies annually.
- **Annualized match (with true-up):** Match is calculated annually. A year-end true-up contribution corrects for participants who received less match on a per-payroll basis.

**Platform requirements:**
- Calculate match per the plan-configured formula each payroll cycle
- Apply match only to eligible sources (pre-tax and Roth deferrals unless plan document specifies otherwise)
- Post match to employer match source (separate from non-elective)
- Apply match contribution toward 415 annual additions limit monitoring
- If annualized match: calculate year-end true-up and process as a corrective contribution

---

## 5. Auto-Escalation

For plans with auto-escalation enabled, the platform must automatically increase participant deferral rates on a plan-configured schedule.

**Key rules:**
- Escalation increment: plan-configurable (e.g., 1% per year)
- Escalation date: plan-configurable (e.g., each January 1, or plan anniversary)
- Maximum deferral rate cap: plan-configurable (escalation stops when cap is reached)
- Participants must receive notice of auto-escalation and have the opportunity to opt out
- QACA minimum escalation rate: plan-configurable per QACA requirements [DATE-VERIFY]

**Platform requirements:**
- Run escalation engine on the plan-configured escalation date
- Increase participant deferral rate by the configured increment
- Apply the configured maximum cap
- Notify participants of upcoming escalation and opt-out deadline
- Process opt-out elections before escalation takes effect
- Integrate with payroll to activate the new deferral rate on the next payroll cycle

---

## 6. Investment Allocation of Posted Contributions

After contributions are posted to participant accounts by source, they must be invested per the participant's current investment election.

**Allocation rules:**
- If participant has an active investment election: allocate per the elected percentages across funds
- If no investment election exists: route to the plan's QDIA
- New contributions follow the current "future contributions" allocation (separate from existing balance allocation)

**Platform requirements:**
- Aggregate contributions by fund across all participants for net trade calculation
- Generate net trade instructions by fund (net buys and sells across all participant transactions)
- Submit trade instructions to custodian for end-of-day NAV execution

---

## 7. Validation Rules Before Posting

All contributions must pass validation before posting. Failures route to the exception queue:

| Validation Rule | Failure Action |
|---|---|
| Participant exists in the system | Route to exception queue: unmatched participant |
| Participant is eligible for the source | Route to exception queue: ineligible source |
| Deferral amount does not exceed annual limit | Cap or reject; alert |
| 415 annual additions not exceeded | Cap or reject; alert |
| Source code is valid for the plan | Route to exception queue: invalid source |
| No duplicate payroll file submission | Route to exception queue: duplicate detected |
| Contribution amount is positive and non-zero | Route to exception queue: invalid amount |
| Payroll period is expected and current | Flag for review if unexpected period |

---

## 8. Agent Rules

- **[COMPLIANCE-SENSITIVE]** — Limit monitoring is mandatory. Contributions in excess of annual limits or 415 limits are qualification failures.
- Never hardcode any contribution limit — always reference as plan-configurable per current IRS limit table.
- Match formula parameters must trace to the plan's adoption agreement — do not hardcode match percentages or tiers.
- Auto-escalation must include participant notification and opt-out capability.
- The exception queue must have sufficient detail for the plan sponsor or TPA to investigate and resolve each exception.
- All posted contributions must be reconciled to trust receipts before the next payroll cycle.

---

## Sources

- IRC Sections 402(g), 414(v), 415 | IRS | https://www.irs.gov/retirement-plans | Retrieved 2026-03-06
- SECURE 2.0 Act of 2022 (Super Catch-Up, Mandatory Roth Catch-Up) | https://www.congress.gov | Retrieved 2026-03-06
- DOL Deposit Timing Regulations | https://www.dol.gov/agencies/ebsa | Retrieved 2026-03-06
- SPARK Institute Contribution API Guidelines, June 2025 | https://www.sparkinstitute.org | Retrieved 2026-03-06
