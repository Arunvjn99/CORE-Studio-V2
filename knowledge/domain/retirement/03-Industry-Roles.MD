# Skill: Industry Roles and Interactions
**Skill-ID:** 03-Industry-Roles
**World:** Retirement World v1.0
**Category:** Foundation
**Last-Reviewed:** 2026-03-06

---

## Purpose

This skill defines every role in the retirement plan ecosystem, their responsibilities, their data ownership, and how they interact with the CORE platform. Understanding roles is prerequisite to designing correct workflows, access controls, and approval chains.

---

## 1. Plan Sponsor

**Who they are:** The employer entity that adopts and maintains the retirement plan.

**Core responsibilities:**
- Signs the plan document and adoption agreement
- Makes plan design decisions (eligibility, contributions, vesting, investment menu)
- Selects service providers (recordkeeper, TPA, advisor, custodian)
- Has ultimate responsibility for plan operation and ERISA compliance

**Accountable to:** ERISA (as plan administrator if not delegated), DOL, IRS, participants and beneficiaries.

**Data and workflows owned:** Plan design parameters, employer contribution decisions, eligibility rules, investment menu selection (unless delegated to a 3(38)), amendment decisions, payroll data origination.

**Platform interaction:** Plan sponsor portal — reporting, approval workflows, contribution remittance initiation, compliance test results review, document access. May delegate administrative tasks to a TPA.

**Key distinction:** The plan sponsor is the employer entity, typically a named fiduciary under ERISA. In many plans, the plan sponsor also serves as the ERISA Section 3(16) plan administrator unless that role is delegated.

---

## 2. Participant

**Who they are:** An individual employee or former employee who is eligible for or enrolled in the plan.

**Core responsibilities:**
- Enrolls in the plan; elects deferral rate and investment elections
- Manages account (loans, withdrawals, beneficiary designations)
- Takes distributions at qualifying events

**Accountable to:** Responsible for accuracy of self-reported information; bound by plan terms.

**Data and workflows owned:** Deferral rate elections, investment allocations, beneficiary designations, loan requests, distribution requests, contact information.

**Platform interaction:** Participant portal (web and mobile) — enrollment, deferral changes, investment changes, account balance viewing, transaction history, loan origination, and distribution requests.

**Key distinction:** Participants are the beneficial owners of their individual account balances. Their rights are protected by ERISA — including rights to plan information, fee disclosures, and statements of benefits.

---

## 3. Recordkeeper

**Who they are:** The service provider that maintains individual participant account records.

**Core responsibilities:**
- Maintains individual participant account records
- Processes contributions, distributions, loans, and investment transactions
- Generates participant statements
- Produces compliance data
- Interfaces with all other parties

**Accountable to:** Plan sponsor (contractual); DOL and IRS (regulatory); participants (disclosure obligations).

**Data and workflows owned:** Participant account balances by source/money type, transaction history, investment positions, vesting records, compliance testing data, notice delivery records.

**Platform interaction:** The recordkeeper IS the platform — CORE is the recordkeeping system.

**Key distinction:** The recordkeeper maintains the books and records of the plan at the individual account level. The recordkeeper does NOT hold plan assets (that is the custodian/trustee's role). In bundled models, recordkeeper and custodian may be affiliated.

---

## 4. Third Party Administrator (TPA)

**Who they are:** A service provider performing plan administration tasks on behalf of the plan sponsor.

**Core responsibilities:**
- Conducts compliance testing (ADP, ACP, 415, 416, 410(b))
- Prepares Form 5500
- Manages plan document and adoption agreement
- Handles distribution and loan processing
- Advises on plan design

**Accountable to:** Plan sponsor (contractual); may serve as ERISA Section 3(16) plan administrator if explicitly appointed.

**Data and workflows owned:** Compliance test data, census data, plan document versions, government reporting files, correction workflows.

**Platform interaction:** TPA portal — participant data, plan configuration, compliance testing outputs, document generation. May initiate certain plan-level transactions.

**Key distinction:** The TPA is a service provider, not automatically a fiduciary. If appointed as Section 3(16) administrator, they assume fiduciary responsibility for plan administration functions. Most prominent in unbundled service models.

---

## 5. Financial Advisor / Broker

**Who they are:** Advises the plan sponsor on plan design, investment menu, and service providers; may advise participants on investment elections.

**Core responsibilities:**
- Advises plan sponsor on investment menu, plan design, and provider selection
- Earns compensation disclosed under ERISA Section 408(b)(2)
- May provide investment recommendations (3(21)) or exercise full discretion (3(38))

**Accountable to:** Plan sponsor (fiduciary or non-fiduciary depending on appointment); DOL; SEC or FINRA depending on registration.

**Platform interaction:** Advisor portal — plan-level data, investment performance reporting, fee analytics. May not have direct access to individual participant PII without plan sponsor authorization.

### 3(21) vs. 3(38) Investment Fiduciary Distinction

| Dimension | ERISA Section 3(21) Co-Fiduciary | ERISA Section 3(38) Investment Manager |
|---|---|---|
| Role | Investment Advisor | Investment Manager |
| Authority | Provides recommendations; plan sponsor retains final decision | Full discretionary authority to select, manage, replace investments |
| Fiduciary responsibility | Shared with plan sponsor | Shifts to the 3(38) for investment decisions |
| Platform implication | Platform must present recommendations for plan sponsor approval; cannot auto-implement | Platform may implement investment changes directed by the 3(38) without additional plan sponsor approval |

**[COMPLIANCE-SENSITIVE]** — Any feature that auto-implements investment changes must verify whether a 3(38) is appointed. If only a 3(21) is in place, an approval workflow is required.

---

## 6. Custodian / Trustee

**Who they are:** The entity that holds legal title to plan assets.

**Core responsibilities:**
- Holds legal title to plan assets
- Executes investment transactions
- Maintains asset-level records
- Ensures assets are used for exclusive benefit of participants

**Data and workflows owned:** Asset positions, trade confirmations, NAV data, cash management records.

**Platform interaction:** Trust accounting system receives trade instructions from recordkeeper; sends NAV/pricing feeds and confirmed trade data back; reconciliation occurs between recordkeeping system and trust system.

### Directed vs. Discretionary Trustee

| Type | Description | Platform Implication |
|---|---|---|
| **Directed Trustee** | Acts only on instructions from a named fiduciary; no investment discretion | Platform sends explicit trade instructions; trustee confirms execution |
| **Discretionary Trustee** | Has independent authority over investment decisions; rare in DC plans | Platform may receive investment direction from trustee rather than plan sponsor |

In most DC plans, the trustee is a directed trustee. The recordkeeper instructs trades based on participant or plan-level direction.

---

## 7. Payroll Provider

**Who they are:** Calculates and processes employee payroll; produces contribution data for retirement plan remittance.

**Core responsibilities:**
- Calculates and processes employee payroll
- Produces contribution data for retirement plan remittance
- Provides census data for eligibility and compliance testing

**Data and workflows owned:** Compensation data, hours data, employee demographics, payroll cycle outputs, contribution amounts by source.

**Platform interaction:** Sends contribution files and census data to recordkeeper via file-based or API-based integration.

### Integration Patterns

| Pattern | Description | Common Formats | Timing |
|---|---|---|---|
| **File-based** | Structured file delivered via SFTP | Fixed-width, delimited (CSV/tab), SPARK-format | Batch; per payroll cycle |
| **API-based** | Real-time or near-real-time data exchange | JSON; SPARK Institute API Integration Guidelines (June 2025) | Event-driven or scheduled |

**360° integration:** Bidirectional payroll integration — payroll sends contribution and census data to the recordkeeper; the recordkeeper sends loan repayment schedules and distribution data back to payroll.

---

## 8. Investment Managers / DCIOs

**Who they are:** Manage investment funds offered on the plan's investment menu.

**Core responsibilities:**
- Manage investment funds; provide fund data (NAV, performance, fees)
- Comply with SEC regulatory obligations
- Provide Rule 22c-2 shareholder data upon request

**Platform interaction:** Investment data feeds (NAV, fund characteristics) flow into the recordkeeping system; trade orders flow out; revenue sharing and fee data flows to fee disclosure systems.

---

## 9. Regulators: IRS and DOL

| Regulator | Primary Jurisdiction | Key Tools |
|---|---|---|
| **IRS** | Tax qualification; contribution limits; distribution taxation; EPCRS correction | Revenue rulings, notices, private letter rulings, audits, EPCRS |
| **DOL / EBSA** | ERISA fiduciary standards; participant rights; fee disclosure; cybersecurity | Prohibited transaction exemptions, advisory opinions, DOL audits, civil enforcement |

---

## 10. Role Interaction Summary

A typical plan administration workflow:

1. **Plan Sponsor** adopts the plan and selects service providers.
2. **Payroll Provider** transmits contribution and census data to the **Recordkeeper** each payroll cycle.
3. **Recordkeeper** allocates contributions to participant accounts, executes investment trades via the **Custodian/Trustee**, and maintains the books of record.
4. **TPA** uses recordkeeping data to perform compliance testing, prepare government filings, and manage the plan document.
5. **Financial Advisor** advises the plan sponsor on investment menu and plan design; if appointed as a 3(38), directs investment changes.
6. **Participants** interact with the recordkeeper's participant portal to manage their accounts.
7. **Investment Managers** provide fund data and execute trades.
8. **IRS and DOL** set the regulatory framework and have audit/enforcement authority.

---

## Agent Rules

- When designing approval workflows, always identify which role holds decision authority for each action.
- Any feature that automates a decision previously made by a human must be evaluated for unintended fiduciary assumption.
- TPA portal access must be role-scoped — TPAs must not have access to participant PII beyond what is necessary for their administrative function.
- 3(21) vs. 3(38) status must be verified before designing any auto-implementation of investment changes. **[COMPLIANCE-SENSITIVE]**

---

## Sources

- ERISA Sections 3(16), 3(21), 3(38) | U.S. Department of Labor | https://www.dol.gov/agencies/ebsa | Retrieved 2026-03-06
- SPARK Institute API Integration Guidelines, June 2025 | https://www.sparkinstitute.org | Retrieved 2026-03-06
- FINRA Investor Education | https://www.finra.org/investors/retirement | Retrieved 2026-03-06
