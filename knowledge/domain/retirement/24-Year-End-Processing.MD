# Skill: Year-End Processing
**Skill-ID:** 24-Year-End-Processing
**World:** Retirement World v1.0
**Category:** Plan Administration Lifecycle
**Last-Reviewed:** 2026-03-06

---

## Purpose

This skill defines the year-end processing cycle — match true-up, forfeiture processing, Form 5500 data preparation, SAR generation, and participant statement generation. Year-end is the highest-volume, highest-stakes administrative period in the plan calendar.

---

## 1. Year-End Processing Sequence

Year-end processing occurs in a defined sequence. Dependencies between steps must be respected:

1. Final payroll contribution processing and reconciliation
2. HCE determination for the completed plan year
3. Compliance testing data finalization (ADP, ACP, 415, 416, 410(b), 401(a)(4))
4. Compliance test execution and results
5. Corrective action processing (if tests failed)
6. Match true-up calculation and posting
7. Forfeiture processing
8. Year-end valuation and asset reconciliation
9. Form 5500 data preparation and delivery to TPA
10. SAR generation and distribution
11. Annual participant statement generation and distribution
12. 1099-R generation for all distributions in the calendar year

---

## 2. Match True-Up

If the plan's employer match is calculated on an annual basis but funded on a per-payroll basis, a year-end true-up is required.

**True-up concept:** Some participants stop contributing mid-year and receive less per-payroll match than the annual formula implies. The true-up calculates the total match each participant should have received based on the full plan year's compensation and deferrals, then subtracts what was already funded.

**True-up calculation:**
1. For each participant, calculate the total annual match due based on the plan's match formula applied to full-year compensation and deferrals
2. Sum the match actually funded throughout the plan year for each participant
3. The true-up amount = annual match due − match already funded (if positive; if negative, an excess contribution exists and must be corrected)
4. Post the true-up as an employer match contribution to each eligible participant

**Platform requirements:**
- Calculate true-up amounts per participant after the final payroll of the plan year
- Verify true-up does not cause 415 limit violations for any participant
- Post true-up contributions to the employer match source
- Generate a true-up contribution report for plan sponsor review and approval before posting
- Apply vesting schedule to true-up amounts (same as regular match contributions)

[COMPLIANCE-SENSITIVE — excess match amounts require corrective action, not just a skip of the true-up]

---

## 3. Forfeiture Processing

Forfeitures arise when terminated participants leave without being fully vested. Year-end is a common time to process and apply accumulated forfeitures.

**Forfeiture timing rules:** Forfeitures must be used within the plan year they arise or the following plan year, per plan document and IRS guidance. [DATE-VERIFY — confirm current forfeiture usage timing rules]

**Permitted forfeiture uses (plan-configurable per plan document):**
- Reduce employer contributions for the current or next plan year
- Pay plan expenses
- Fund QNECs or QMACs
- Reallocate to other participants (if plan document permits)

**Forfeiture processing steps:**
1. Identify all forfeitures arising during the plan year (from terminations where vesting was finalized)
2. Finalize the forfeiture account balance
3. Apply forfeitures per the plan document's permitted uses
4. Post forfeiture application transactions with full audit trail
5. Reduce future employer contributions or post allocations as configured

**Platform requirements:**
- Track forfeiture account balance by source throughout the year
- Apply forfeitures by the deadline per plan document
- Document forfeiture application for 5500 reporting and audit trail
- Alert plan sponsor if forfeitures are approaching the deadline for usage

---

## 4. Compliance Testing — Year-End Execution

See Skill 36 (Compliance Testing) for the full testing methodology. Year-end triggers:
- Final data compilation for ADP, ACP, 415, 416, 410(b), and 401(a)(4) tests
- Test execution (either in-platform or data export to TPA's testing system)
- Results review by TPA and plan sponsor
- Corrective action processing (QNEC, QMAC, excess refunds) if tests fail

**Correction deadlines:**
- ADP/ACP corrective distributions (excess refunds): 2.5 months after plan year end for non-excise-tax correction; 12 months for corrections with 10% excise tax [DATE-VERIFY]
- QNEC/QMAC contributions: must be made before the last day for filing the plan's tax return (including extensions) [DATE-VERIFY]

---

## 5. Form 5500 Data Preparation

Form 5500 is the annual information return filed with the DOL and IRS. The plan sponsor or TPA is responsible for filing; the recordkeeper provides the underlying data.

**Data prepared by the recordkeeper:**
- Total plan assets as of the first and last day of the plan year
- Net plan assets
- Contributions received (by type: employee, employer match, non-elective)
- Distributions paid (by type: benefits, withdrawals, administrative expenses)
- Total number of participants (active, terminated vested, deceased, total)
- Investment holdings by fund (Schedule H for large plans)
- Service provider information (recordkeeper, TPA, trustee, advisor) for 408(b)(2) schedule
- Insurance/contract information (for plans with annuity or insurance contracts)

**Platform requirements:**
- Generate Form 5500 data package at year end
- Reconcile participant counts against the participant database
- Reconcile financial data against trust statements
- Deliver data to TPA in the required format and by the required deadline

**Filing deadlines:** [DATE-VERIFY — confirm current 5500 filing deadline and extension rules]
- Generally due 7 months after the plan year end
- Extensions may be available

---

## 6. Summary Annual Report (SAR)

The SAR summarizes the Form 5500 financial information and must be distributed to all plan participants.

**SAR timing:** Must be provided within 9 months after the plan year end, or 2 months after the 5500 due date if an extension was filed. [DATE-VERIFY]

**Platform requirements:**
- Generate the SAR from year-end financial data after the 5500 is filed
- Distribute to all participants (active and terminated vested) via the plan's delivery method
- Track SAR delivery and log confirmations
- Store the SAR in the document management system

---

## 7. Annual Participant Statements

Annual (or more frequent) participant statements must be provided showing:
- Account balances as of the end of the statement period (by source and by fund)
- Contributions received during the period (by source)
- Investment activity (purchases, sales, transfers)
- Plan fees charged to the participant's account during the period
- Vested balance by source
- Loan balance (if applicable)
- Beneficiary designation summary
- Annual Lifetime Income Statement (SECURE 2.0) [DATE-VERIFY]

**Statement generation timing:**
- Annual statements: within 45 days after the plan year end [DATE-VERIFY — confirm current statement timing requirements]
- Quarterly statements: within 45 days after the quarter end (for participant-directed plans) [DATE-VERIFY]

**Platform requirements:**
- Generate statements per the required frequency and format
- Include all required data elements
- Include the Lifetime Income Statement (IRS prescribed methodology)
- Deliver via the plan's configured delivery method (electronic or paper)
- Track delivery and log confirmations

[COMPLIANCE-SENSITIVE]

---

## 8. 1099-R Generation

All distributions made during the calendar year require a Form 1099-R issued to the distributee and filed with the IRS.

**1099-R generation process:**
1. Compile all distribution records for the calendar year
2. Assign correct distribution codes to each distribution
3. Calculate gross distribution, taxable amount, and withholding for each
4. Generate 1099-R forms
5. Deliver to participants by IRS deadline [DATE-VERIFY — generally January 31 of the following year]
6. File with IRS by IRS deadline [DATE-VERIFY — generally February 28 paper, March 31 electronic]

---

## Agent Rules

- Year-end processing steps are sequential — compliance test results must be finalized before corrective actions are posted; corrective actions must be complete before 5500 data is finalized.
- **[COMPLIANCE-SENSITIVE]** — Forfeiture usage deadlines are regulatory — not using forfeitures within the required period is a plan operational failure. [DATE-VERIFY]
- Match true-up must be calculated before 415 limit finalization — the true-up itself may cause a 415 violation for some participants.
- 1099-R distribution codes must be accurate — the IRS matches 1099-R filings to tax returns; incorrect codes create participant tax disputes.
- 5500 data reconciliation is mandatory — submit data to TPA only after reconciling participant counts and financial figures to the platform's internal records and trust statements.

---

## Sources

- DOL Form 5500 Filing Requirements | https://www.dol.gov/agencies/ebsa/employers-and-advisers/plan-administration-and-compliance/reporting-and-filing | Retrieved 2026-03-06
- ERISA Sections 101, 104 (Disclosure and Reporting) | U.S. Department of Labor | https://www.dol.gov/agencies/ebsa | Retrieved 2026-03-06
- IRC Section 6057 (5500 Reporting) | IRS | https://www.irs.gov | Retrieved 2026-03-06
- IRS 1099-R Instructions | https://www.irs.gov/forms-pubs/about-form-1099-r | Retrieved 2026-03-06
- SECURE 2.0 Act — Lifetime Income Statement | https://www.congress.gov | Retrieved 2026-03-06
